#!/usr/bin/env python3
"""Build a versioned CandidateObservation snapshot from immutable candidate raw files.

Candidates remain research-ineligible. This command never writes admitted records or
canonical ProblemContracts.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import stat
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, urlparse

from jsonschema import Draft202012Validator, FormatChecker, SchemaError

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "problem-library"
RAW = LIBRARY / "raw" / "candidates"
DERIVED = LIBRARY / "derived" / "candidate-observations"
INVENTORY = RAW / "inventory.json"
REGISTRY = LIBRARY / "registry" / "candidate-sources.json"
SCHEMA = LIBRARY / "schema" / "candidate-observation.schema.json"
LEGACY_EXTRACTOR = ROOT / "scripts" / "consolidate_candidates.py"
MAX_EXCERPT_CHARS = 16000
TRUNCATION_MARKER = " … [excerpt truncated]"
MAX_PATH_CHARS = 4_096
MAX_FIELD_CHARS = 8_192
MAX_STATEMENT_CHARS = 1_000_000
MAX_CATEGORIES = 1_000
MAX_ARTIFACT_BYTES = 30_000_000
MAX_OBSERVATION_BYTES = 1_000_000
MAX_OBSERVATIONS = 100_000
MAX_SNAPSHOT_BYTES = 128_000_000
MAX_ERROR_CHARS = 4_096


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _safe_repo_path(path: Path) -> Path:
    path = Path(path)
    if (
        len(str(path)) > MAX_PATH_CHARS
        or "\x00" in str(path)
        or "\\" in str(path)
        or any(part in {".", ".."} for part in path.parts)
    ):
        raise ValueError(f"repository path contains an invalid component: {path}")
    path = path if path.is_absolute() else ROOT / path
    try:
        relative = path.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"repository path escapes root: {path}") from exc
    if ".." in relative.parts:
        raise ValueError(f"repository path escapes root: {path}")
    lexical = ROOT
    for part in relative.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise ValueError(f"repository path contains symlink: {path}")
    return path


def _read_bounded(path: Path, *, max_bytes: int = MAX_ARTIFACT_BYTES) -> bytes:
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_SNAPSHOT_BYTES
    ):
        raise ValueError("candidate file read budget is invalid")
    path = _safe_repo_path(path)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ValueError("platform cannot safely read candidate artifact")
    try:
        descriptor = os.open(path, os.O_RDONLY | nofollow)
    except OSError as exc:
        raise ValueError(f"cannot read candidate artifact: {path}") from exc
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise ValueError(f"candidate artifact is not a regular file: {path}")
        if file_stat.st_size > max_bytes:
            raise ValueError(f"candidate artifact exceeds size budget: {path}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, max_bytes - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"candidate artifact exceeds size budget: {path}")
            chunks.append(chunk)
    except OSError as exc:
        raise ValueError(f"cannot read candidate artifact: {path}") from exc
    finally:
        os.close(descriptor)


def sha256_file(path: Path) -> str:
    path = _safe_repo_path(path)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ValueError("platform cannot safely hash candidate artifact")
    try:
        descriptor = os.open(path, os.O_RDONLY | nofollow)
    except OSError as exc:
        raise ValueError(f"cannot hash candidate artifact: {path}") from exc
    digest = hashlib.sha256()
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise ValueError(f"candidate artifact is not a regular file: {path}")
        if file_stat.st_size > MAX_ARTIFACT_BYTES:
            raise ValueError(f"candidate artifact exceeds size budget: {path}")
        total = 0
        while True:
            block = os.read(descriptor, 1024 * 1024)
            if not block:
                break
            total += len(block)
            if total > MAX_ARTIFACT_BYTES:
                raise ValueError(f"candidate artifact exceeds size budget: {path}")
            digest.update(block)
    finally:
        os.close(descriptor)
    return digest.hexdigest()


def load_extractors() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location("candidate_extractors", LEGACY_EXTRACTOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load candidate extractors")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.EXTRACTORS


def _reject_json_constant(value: str) -> Any:
    raise ValueError(f"candidate JSON contains illegal constant: {value}")


def _validate_https_url(value: object, *, label: str, allow_generated: bool = False) -> str:
    if not isinstance(value, str) or len(value) > MAX_FIELD_CHARS:
        raise ValueError(f"{label} URL is invalid or exceeds size budget")
    parsed = urlparse(value)
    if (
        (parsed.scheme != "https" and not (allow_generated and parsed.scheme == "generated"))
        or not parsed.netloc
        or parsed.username
        or parsed.password
    ):
        raise ValueError(f"{label} URL must be HTTPS with a host")
    return value


def source_registry() -> dict[str, dict[str, Any]]:
    value = json.loads(
        _read_bounded(REGISTRY, max_bytes=5_000_000).decode("utf-8"),
        parse_constant=_reject_json_constant,
    )
    if not isinstance(value, dict) or not isinstance(value.get("sources"), list):
        raise ValueError("candidate source registry must be an object with sources")
    schema_path = LIBRARY / "schema" / "candidate-source.schema.json"
    schema = json.loads(
        _read_bounded(schema_path, max_bytes=5_000_000).decode("utf-8"),
        parse_constant=_reject_json_constant,
    )
    if not isinstance(schema, dict):
        raise ValueError("candidate source schema must be an object")
    try:
        errors = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value),
            key=lambda item: list(item.path),
        )
    except (SchemaError, TypeError, ValueError) as exc:
        raise ValueError("candidate source schema is invalid") from exc
    if errors:
        raise ValueError(f"candidate source registry schema invalid: {errors[0].message}")
    entries: dict[str, dict[str, Any]] = {}
    if len(value["sources"]) > MAX_OBSERVATIONS:
        raise ValueError("candidate source registry exceeds size budget")
    for item in value["sources"]:
        if not isinstance(item, dict):
            raise ValueError("candidate source entry must be an object")
        source_id = item.get("source_id")
        if (
            not isinstance(source_id, str)
            or not re.fullmatch(r"[a-z][a-z0-9_]{1,63}", source_id)
            or source_id in entries
        ):
            raise ValueError("candidate source ID is invalid or duplicated")
        parser = item.get("parser")
        if parser is not None and (
            not isinstance(parser, str) or len(parser) > MAX_FIELD_CHARS
        ):
            raise ValueError(f"{source_id}: candidate parser is invalid")
        for key in ("ingestion_role", "record_scope", "admission_policy"):
            if not isinstance(item.get(key), str) or len(item[key]) > MAX_FIELD_CHARS:
                raise ValueError(f"{source_id}: candidate registry field is invalid: {key}")
        license_value = item.get("license")
        if not isinstance(license_value, dict):
            raise ValueError(f"{source_id}: candidate license is invalid")
        attribution = license_value.get("attribution")
        allowed_uses = license_value.get("allowed_uses")
        if (
            not isinstance(attribution, str)
            or not attribution
            or len(attribution) > MAX_FIELD_CHARS
            or not isinstance(allowed_uses, list)
            or len(allowed_uses) > MAX_CATEGORIES
            or any(not isinstance(use, str) or len(use) > MAX_FIELD_CHARS for use in allowed_uses)
        ):
            raise ValueError(f"{source_id}: candidate license fields are invalid")
        license_url = license_value.get("url")
        if license_url is not None and (
            not isinstance(license_url, str) or len(license_url) > MAX_FIELD_CHARS
        ):
            raise ValueError(f"{source_id}: candidate license URL is invalid")
        status_map = item.get("status_map")
        if not isinstance(status_map, dict) or len(status_map) > MAX_CATEGORIES or any(
            not isinstance(key, str)
            or not isinstance(value, str)
            or len(key) > MAX_FIELD_CHARS
            or len(value) > MAX_FIELD_CHARS
            for key, value in status_map.items()
        ):
            raise ValueError(f"{source_id}: candidate status map is invalid")
        entries[source_id] = item
    return entries


def validate_inventory(inventory: object) -> dict[str, Any]:
    if (
        not isinstance(inventory, dict)
        or inventory.get("schema_version") != "candidate-inventory.v1"
        or not isinstance(inventory.get("sources"), dict)
        or not isinstance(inventory.get("failures"), list)
        or len(inventory.get("sources", {})) > MAX_OBSERVATIONS
        or len(inventory.get("failures", [])) > MAX_OBSERVATIONS
    ):
        raise ValueError("candidate inventory shape or size is invalid")
    total_files = 0
    for source_id, entry in inventory["sources"].items():
        if (
            not isinstance(source_id, str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,255}", source_id)
            or not isinstance(entry, dict)
        ):
            raise ValueError("candidate inventory source entry is invalid")
        files = entry.get("files", [])
        if not isinstance(files, list) or len(files) > MAX_OBSERVATIONS:
            raise ValueError(f"{source_id}: candidate inventory files exceed budget")
        total_files += len(files)
        if total_files > MAX_OBSERVATIONS:
            raise ValueError("candidate inventory files exceed budget")
        names: set[str] = set()
        paths: set[str] = set()
        for item in files:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("name"), str)
                or not isinstance(item.get("path"), str)
                or not isinstance(item.get("url"), str)
                or not item.get("url")
                or not isinstance(item.get("sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"])
                or not isinstance(item.get("bytes"), int)
                or isinstance(item.get("bytes"), bool)
                or item["bytes"] < 0
                or item["bytes"] > MAX_ARTIFACT_BYTES
                or len(item["name"]) > MAX_PATH_CHARS
                or len(item["path"]) > MAX_PATH_CHARS
                or len(item["url"]) > MAX_FIELD_CHARS
                or "\x00" in item["name"]
                or "\x00" in item["path"]
                or "\\" in item["name"]
                or "\\" in item["path"]
                or any(part in {".", ".."} for part in Path(item["path"]).parts)
                or item["name"] in names
                or item["path"] in paths
            ):
                raise ValueError(f"{source_id}: candidate inventory file entry is invalid")
            try:
                _validate_https_url(
                    item["url"], label=f"{source_id} artifact", allow_generated=True
                )
            except ValueError:
                raise
            if "/" in item["name"] or "/" in item["path"] and not item["path"].startswith(
                f"problem-library/raw/candidates/{source_id}/"
            ):
                raise ValueError(f"{source_id}: candidate inventory name/path is invalid")
            names.add(item["name"])
            paths.add(item["path"])
            artifact_prefix = f"problem-library/raw/candidates/{source_id}/"
            if not item["path"].startswith(artifact_prefix):
                raise ValueError(f"{source_id}: candidate inventory path is not source-bound")
            artifact = safe_candidate_artifact(item["path"])
            expected = str(artifact.relative_to(ROOT))
            if expected != item["path"]:
                raise ValueError(f"{source_id}: candidate inventory path is not canonical")
        counts = entry.get("counts", {})
        if not isinstance(counts, dict) or len(counts) > MAX_CATEGORIES or any(
            not isinstance(key, str)
            or len(key) > MAX_FIELD_CHARS
            or not isinstance(value, int)
            or isinstance(value, bool)
            or value < 0
            for key, value in counts.items()
        ):
            raise ValueError(f"{source_id}: candidate inventory counts are invalid")
    for failure in inventory["failures"]:
        if (
            not isinstance(failure, dict)
            or not all(isinstance(failure.get(key), str) for key in ("source", "name", "url", "reason"))
            or len(failure["source"]) > MAX_FIELD_CHARS
            or len(failure["name"]) > MAX_PATH_CHARS
            or len(failure["url"]) > MAX_FIELD_CHARS
            or len(failure["reason"]) > MAX_FIELD_CHARS
        ):
            raise ValueError("candidate inventory failure entry is invalid")
    generated_at = inventory.get("generated_at")
    if not isinstance(generated_at, str) or not generated_at or len(generated_at) > MAX_FIELD_CHARS:
        raise ValueError("candidate inventory generated_at is invalid")
    return inventory


def inventory_files(inventory: dict[str, Any], source: str) -> list[dict[str, Any]]:
    sources = inventory.get("sources")
    if not isinstance(sources, dict):
        raise ValueError("candidate inventory sources must be an object")
    entry = sources.get(source, {})
    if not isinstance(entry, dict):
        raise ValueError(f"{source}: candidate inventory entry is invalid")
    files = entry.get("files", [])
    if not isinstance(files, list) or len(files) > MAX_OBSERVATIONS:
        raise ValueError(f"{source}: candidate inventory files exceed budget")
    return list(files)


def safe_candidate_artifact(path_text: object) -> Path:
    """Resolve only an inventory path inside the ignored candidate raw tree."""
    if not isinstance(path_text, str) or len(path_text) > MAX_PATH_CHARS or "\x00" in path_text or "\\" in path_text:
        raise ValueError("candidate raw artifact path must be a bounded POSIX string")
    path = Path(path_text)
    if (
        path.is_absolute()
        or any(part in {".", ".."} for part in path.parts)
        or not path_text.startswith("problem-library/raw/candidates/")
    ):
        raise ValueError(f"unsafe candidate raw artifact path: {path_text}")
    if RAW.is_symlink():
        raise ValueError("candidate raw root cannot be a symlink")
    lexical = ROOT
    for part in path.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise ValueError(f"candidate raw artifact path contains symlink: {path_text}")
    resolved = (ROOT / path).resolve()
    raw_root = RAW.resolve()
    if resolved != raw_root and raw_root not in resolved.parents:
        raise ValueError(f"candidate raw artifact escapes raw root: {path_text}")
    if not resolved.is_file():
        raise ValueError(f"candidate raw artifact is missing: {path_text}")
    return resolved


def _native_id(record: dict[str, Any]) -> str | None:
    extra = record.get("extra") if isinstance(record.get("extra"), dict) else {}
    for key in ("id", "problem_id", "problem_number", "question_id"):
        value = extra.get(key)
        if value in (None, ""):
            continue
        if isinstance(value, bool) or not isinstance(value, (str, int)):
            raise ValueError(f"candidate native ID has invalid type: {key}")
        native = str(value)
        if not native or len(native) > MAX_FIELD_CHARS:
            raise ValueError(f"candidate native ID exceeds size budget: {key}")
        return native
    return None


def _path_matches(item: dict[str, Any], suffixes: tuple[str, ...]) -> bool:
    path = str(item.get("path", ""))
    return any(path.endswith(suffix) for suffix in suffixes)


def _contains(path: Path, needles: list[bytes]) -> bool:
    if not needles:
        return False
    data = _read_bounded(path)
    return any(needle and needle in data for needle in needles)


def choose_artifact(
    source: str,
    record: dict[str, Any],
    files: list[dict[str, Any]],
    *,
    digest_cache: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Choose an inventoried artifact and a stable locator, or fail closed.

    Extractors may read a distribution file rather than expose its path. This
    function uses source-specific locators and bounded content matching. It never
    silently falls back to an unrelated first file when several distributions are
    present.
    """
    if (
        not isinstance(source, str)
        or not source
        or len(source) > MAX_FIELD_CHARS
        or not isinstance(record, dict)
    ):
        raise ValueError("candidate artifact binding inputs are invalid")
    if not files or not isinstance(files, list):
        raise ValueError(f"{source}: no inventoried raw distribution")
    url_value = record.get("url")
    title_value = record.get("title")
    if not isinstance(url_value, str) or not isinstance(title_value, str):
        raise ValueError(f"{source}: record URL/title must be strings")
    url = _validate_https_url(url_value, label=f"{source} record")
    title = title_value
    if len(title) > MAX_FIELD_CHARS:
        raise ValueError(f"{source}: record title exceeds size budget")
    native = _native_id(record)
    extra = record.get("extra") if isinstance(record.get("extra"), dict) else {}
    explicit_path = next(
        (extra[key] for key in ("raw_artifact_path", "artifact_path") if extra.get(key)),
        None,
    )
    selected: dict[str, Any] | None = None
    locator = native or url or title

    if explicit_path is not None and (
        not isinstance(explicit_path, str) or len(explicit_path) > MAX_PATH_CHARS
    ):
        raise ValueError(f"{source}: explicit artifact path is invalid")
    if explicit_path is not None:
        selected = next((item for item in files if item.get("path") == explicit_path), None)
        if selected is None:
            raise ValueError(f"{source}: explicit artifact is not in inventory: {explicit_path}")
        locator = f"inventory-path:{explicit_path}"

    if selected is None:
        selected = next((item for item in files if item.get("url") == url and url), None)

    parsed = urlparse(url)
    if selected is None and source == "theoremdb":
        slug = parse_qs(parsed.query).get("ref", [""])[0]
        if slug:
            suffix = "statement/" + quote(slug, safe="") + ".html"
            selected = next((item for item in files if str(item.get("path", "")).endswith(suffix)), None)
            locator = f"statement-ref:{slug}"
    if selected is None and source in {"mathoverflow", "mo_conjectures", "mse"} and native:
        needle = native.encode("ascii", "ignore")
        matches = []
        for item in files:
            path = safe_candidate_artifact(item.get("path"))
            if "/api/" in str(item.get("path", "")) and _contains(path, [needle]):
                matches.append(item)
        if len(matches) == 1:
            selected = matches[0]
            locator = f"question-id:{native}"
        elif len(matches) > 1:
            raise ValueError(f"{source}: native id matches multiple raw artifacts: {native}")
    if selected is None and source == "clay":
        slug = parsed.path.rstrip("/").split("/")[-1]
        if slug:
            selected = next(
                (item for item in files if _path_matches(item, (f"millennium_{slug}.html", f"{slug}.html"))),
                None,
            )
            locator = f"clay-slug:{slug}"
    if selected is None and source == "openquantum":
        selected = next((item for item in files if _path_matches(item, ("source-tarball.tar.gz",))), None)
        if selected is not None:
            locator = "openquantum-source-tarball"
    if selected is None and source == "fmop":
        selected = next((item for item in files if _path_matches(item, ("open_problems_data.zip",))), None)
        if selected is not None:
            locator = "fmop-open-problems-data"
    if selected is None and source == "vibemathed":
        selected = next((item for item in files if _path_matches(item, ("dataset-latest.json",))), None)
        if selected is not None:
            locator = "vibemathed-dataset-latest"
    if selected is None:
        basename = parsed.path.rstrip("/").rsplit("/", 1)[-1]
        if basename:
            basename_matches = [
                item for item in files if basename in str(item.get("path", ""))
            ]
            if len(basename_matches) == 1:
                selected = basename_matches[0]
            elif len(basename_matches) > 1:
                raise ValueError(f"{source}: URL basename matches multiple raw artifacts")
    if selected is None:
        needles = []
        if native:
            needles.append(native.encode("utf-8", "ignore"))
        if title:
            needles.append(title.encode("utf-8", "ignore"))
        matches = []
        for item in files:
            path = safe_candidate_artifact(item.get("path"))
            if _contains(path, needles):
                matches.append(item)
        if len(matches) == 1:
            selected = matches[0]
        elif len(matches) > 1:
            raise ValueError(f"{source}: record matches multiple raw artifacts")
    if selected is None:
        raise ValueError(f"{source}: cannot bind record to one inventoried raw artifact")

    path = safe_candidate_artifact(selected.get("path"))
    declared_digest = selected.get("sha256")
    if not isinstance(declared_digest, str) or not re.fullmatch(r"[a-f0-9]{64}", declared_digest):
        raise ValueError(f"{source}: inventory artifact has invalid sha256")
    cache_key = str(selected["path"])
    actual_digest = (digest_cache or {}).get(cache_key)
    if actual_digest is None:
        actual_digest = sha256_file(path)
        if digest_cache is not None:
            digest_cache[cache_key] = actual_digest
    if actual_digest != declared_digest:
        raise ValueError(f"{source}: raw artifact digest drift: {selected['path']}")
    declared_bytes = selected.get("bytes")
    if declared_bytes is not None and (
        not isinstance(declared_bytes, int)
        or isinstance(declared_bytes, bool)
        or declared_bytes < 0
    ):
        raise ValueError(f"{source}: inventory artifact byte count is invalid")
    if declared_bytes is not None:
        nofollow = getattr(os, "O_NOFOLLOW", None)
        if nofollow is None:
            raise ValueError("platform cannot safely inspect candidate artifact")
        descriptor = os.open(path, os.O_RDONLY | nofollow)
        try:
            file_stat = os.fstat(descriptor)
            if not stat.S_ISREG(file_stat.st_mode) or declared_bytes != file_stat.st_size:
                raise ValueError(f"{source}: raw artifact byte count drift: {selected['path']}")
        finally:
            os.close(descriptor)
    if not isinstance(locator, str) or not locator or len(locator) > MAX_FIELD_CHARS:
        raise ValueError(f"{source}: artifact locator is invalid or exceeds size budget")
    return {"path": selected["path"], "sha256": declared_digest, "locator": locator}


def categories_for(record: dict[str, Any]) -> list[str]:
    extra = record.get("extra") if isinstance(record.get("extra"), dict) else {}
    values: list[str] = []
    for key in ("domain", "field", "cat"):
        value = extra.get(key)
        if value is not None and not isinstance(value, str):
            raise ValueError(f"candidate category field is invalid: {key}")
        if value:
            if len(value) > MAX_FIELD_CHARS:
                raise ValueError(f"candidate category field is invalid: {key}")
            values.append(value)
    tags = extra.get("tags")
    if isinstance(tags, list):
        if len(tags) > MAX_OBSERVATIONS or any(
            not isinstance(tag, str) or len(tag) > MAX_FIELD_CHARS for tag in tags
        ):
            raise ValueError("candidate tags exceed type or size budget")
        values.extend(tag for tag in tags if tag.strip())
    elif isinstance(tags, str):
        if len(tags) > MAX_FIELD_CHARS:
            raise ValueError("candidate tags exceed size budget")
        values.extend(part.strip() for part in re.split(r"[,;|]", tags) if part.strip())
    elif tags is not None:
        raise ValueError("candidate tags have invalid type")
    values = list(dict.fromkeys(values))
    if len(values) > MAX_CATEGORIES:
        raise ValueError("candidate categories exceed count budget")
    return values


def build_observation(
    record: dict[str, Any],
    *,
    ordinal: int,
    source: dict[str, Any],
    files: list[dict[str, Any]],
    retrieved_at: str,
    parser_digest: str,
    digest_cache: dict[str, str] | None = None,
) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError(f"{source['source_id']} record {ordinal}: record must be an object")
    if "extra" in record and not isinstance(record.get("extra"), dict):
        raise ValueError(f"{source['source_id']} record {ordinal}: extra must be an object")
    title_value = record.get("title")
    statement_value = record.get("statement")
    url_value = record.get("url")
    if not all(isinstance(value, str) for value in (title_value, statement_value, url_value)):
        raise ValueError(f"{source['source_id']} record {ordinal}: string fields are invalid")
    title = title_value.strip()
    statement = statement_value.strip()
    url = url_value.strip()
    if len(title) > MAX_FIELD_CHARS or len(url) > MAX_FIELD_CHARS:
        raise ValueError(f"{source['source_id']} record {ordinal}: title or URL exceeds budget")
    if len(statement) > MAX_STATEMENT_CHARS:
        raise ValueError(f"{source['source_id']} record {ordinal}: statement exceeds budget")
    if not title or not statement or not url:
        raise ValueError(f"{source['source_id']} record {ordinal}: blank title, statement, or URL")
    artifact = choose_artifact(
        source["source_id"], record, files, digest_cache=digest_cache
    )
    extra = record.get("extra") if isinstance(record.get("extra"), dict) else {}
    try:
        extra_bytes = json.dumps(extra, ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise ValueError(f"{source['source_id']} record {ordinal}: extra is not portable JSON") from exc
    if len(extra_bytes) > MAX_OBSERVATION_BYTES:
        raise ValueError(f"{source['source_id']} record {ordinal}: extra exceeds size budget")
    native = _native_id(record)
    raw_status = record.get("status")
    if raw_status is not None and (
        not isinstance(raw_status, str) or len(raw_status) > MAX_FIELD_CHARS
    ):
        raise ValueError(f"{source['source_id']} record {ordinal}: status must be a bounded string")
    status_key = "" if raw_status is None else raw_status
    status_class = source["status_map"].get(status_key, "unknown")
    cap_hit = len(statement) in {3000, 4000, 5000}
    truncated = cap_hit or len(statement) > MAX_EXCERPT_CHARS
    if truncated:
        excerpt = statement[: MAX_EXCERPT_CHARS - len(TRUNCATION_MARKER)] + TRUNCATION_MARKER
    else:
        excerpt = statement
    record_key = native or sha256_bytes(
        "\x1f".join([title, url, statement]).encode("utf-8")
    )
    identity = "\x1f".join(
        [
            source["source_id"],
            record_key,
            artifact["path"],
            artifact["sha256"],
            artifact["locator"],
            parser_digest,
        ]
    )
    return {
        "observation_id": "candidate:" + sha256_bytes(identity.encode("utf-8")),
        "collection": "candidate",
        "source": source["source_id"],
        "source_native_id": native,
        "source_url": url,
        "record_scope": source["record_scope"],
        "title": title,
        "statement_excerpt": excerpt,
        "excerpt_truncated": truncated,
        "excerpt_original_chars": None if cap_hit else len(statement),
        "source_status_raw": raw_status,
        "source_status_class": status_class,
        "raw_artifact": artifact,
        "parser": {"name": source["parser"], "version": "sha256:" + parser_digest},
        "retrieved_at": retrieved_at,
        "license": source["license"],
        "categories": categories_for(record),
        "extra": extra,
        "admission": {"state": "candidate", "research_eligible": False},
    }


def atomic_write(path: Path, data: bytes, mode: int = 0o600) -> None:
    if not isinstance(data, bytes) or len(data) > MAX_SNAPSHOT_BYTES:
        raise ValueError("candidate snapshot write exceeds size budget")
    path = _safe_repo_path(path)
    if path.is_symlink() or path.parent.is_symlink():
        raise ValueError(f"candidate snapshot path cannot be a symlink: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ValueError("platform cannot safely publish candidate snapshot")
    try:
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow,
            mode,
        )
    except OSError as exc:
        raise ValueError("cannot create candidate snapshot temporary file") from exc
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        fsync_directory(path.parent)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def fsync_directory(path: Path) -> None:
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if nofollow is None or directory is None:
        raise ValueError("platform cannot safely persist candidate snapshot directory")
    descriptor = os.open(path, os.O_RDONLY | directory | nofollow)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def publish_snapshot(
    output_dir: Path,
    snapshot: dict[str, Any],
    observations: bytes,
    *,
    update_latest: bool,
) -> None:
    """Publish a complete immutable snapshot before advancing the latest pointer."""
    _safe_repo_path(DERIVED)
    if DERIVED.is_symlink() or DERIVED.resolve() != DERIVED:
        raise RuntimeError("candidate snapshot root cannot be a symlink")
    DERIVED.mkdir(parents=True, exist_ok=True)
    _safe_repo_path(DERIVED)
    output_dir = _safe_repo_path(output_dir)
    if (
        output_dir.is_symlink()
        or output_dir.parent != DERIVED
        or not output_dir.name
        or output_dir.name in {".", ".."}
    ):
        raise RuntimeError(f"unsafe snapshot output path: {output_dir}")
    temporary = DERIVED / f".{output_dir.name}.{os.getpid()}.tmp"
    if temporary.exists() or temporary.is_symlink():
        raise RuntimeError(f"snapshot temporary directory already exists: {temporary.name}")
    temporary.mkdir(mode=0o700)
    try:
        snapshot_bytes = (
            json.dumps(
                snapshot, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False
            )
            + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise RuntimeError("candidate snapshot metadata is not portable JSON") from exc
    if len(snapshot_bytes) > MAX_SNAPSHOT_BYTES:
        raise RuntimeError("candidate snapshot metadata exceeds size budget")
    try:
        atomic_write(temporary / "observations.jsonl", observations)
        atomic_write(temporary / "snapshot.json", snapshot_bytes)
        fsync_directory(temporary)
        if output_dir.exists():
            if not output_dir.is_dir() or output_dir.resolve() != output_dir:
                raise RuntimeError(f"unsafe existing snapshot directory: {output_dir.name}")
            existing_observations = output_dir / "observations.jsonl"
            existing_snapshot = output_dir / "snapshot.json"
            if existing_observations.is_symlink() or existing_snapshot.is_symlink():
                raise RuntimeError(f"snapshot files cannot be symlinks: {output_dir.name}")
            try:
                existing_observations_bytes = _read_bounded(
                    existing_observations, max_bytes=MAX_SNAPSHOT_BYTES
                )
                existing_snapshot_bytes = _read_bounded(
                    existing_snapshot, max_bytes=MAX_SNAPSHOT_BYTES
                )
            except ValueError as exc:
                raise RuntimeError(f"existing snapshot cannot be safely read: {output_dir.name}") from exc
            if (
                existing_observations_bytes != observations
                or existing_snapshot_bytes != snapshot_bytes
            ):
                raise RuntimeError(f"immutable snapshot already differs: {output_dir.name}")
            existing_children = list(output_dir.iterdir())
            if len(existing_children) > 16 or {
                child.name for child in existing_children
            } != {"observations.jsonl", "snapshot.json"}:
                raise RuntimeError(
                    f"existing snapshot directory contains unexpected files: {output_dir.name}"
                )
            for child in temporary.iterdir():
                child.unlink()
            temporary.rmdir()
        else:
            os.replace(temporary, output_dir)
            fsync_directory(DERIVED)
    except Exception:
        if temporary.is_dir():
            shutil.rmtree(temporary)
        raise

    if update_latest:
        latest = {
            "schema_version": "candidate-latest.v1",
            "snapshot_id": snapshot["snapshot_id"],
            "snapshot_path": snapshot["output"]["path"].replace("observations.jsonl", "snapshot.json"),
            "observations_path": snapshot["output"]["path"],
            "inputs": snapshot["inputs"],
            "output": snapshot["output"],
        }
        latest_bytes = (
            json.dumps(latest, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")
        atomic_write(DERIVED / "latest.json", latest_bytes)
        fsync_directory(DERIVED)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a research-ineligible candidate observation snapshot.")
    parser.add_argument("--allow-partial", action="store_true", help="write an explicitly partial snapshot")
    args = parser.parse_args()
    inventory = validate_inventory(
        json.loads(
            _read_bounded(INVENTORY, max_bytes=MAX_ARTIFACT_BYTES).decode("utf-8"),
            parse_constant=_reject_json_constant,
        )
    )
    registry = source_registry()
    extractors = load_extractors()
    parser_digest = sha256_file(LEGACY_EXTRACTOR)
    inventory_digest = sha256_file(INVENTORY)
    schema_digest = sha256_file(SCHEMA)
    try:
        observation_schema = json.loads(
            _read_bounded(SCHEMA, max_bytes=5_000_000).decode("utf-8"),
            parse_constant=_reject_json_constant,
        )
        observation_validator = Draft202012Validator(
            observation_schema, format_checker=FormatChecker()
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, SchemaError, ValueError) as exc:
        raise ValueError("candidate observation schema is invalid") from exc
    registry_digest = sha256_file(REGISTRY)
    snapshot_material = "\n".join([inventory_digest, parser_digest, schema_digest, registry_digest])
    snapshot_id = "candidate-snapshot:" + sha256_bytes(snapshot_material.encode("ascii"))
    output_dir = DERIVED / snapshot_id.split(":", 1)[1]
    observations: list[dict[str, Any]] = []
    source_counts: Counter[str] = Counter()
    artifact_digests: dict[str, str] = {}
    errors: list[dict[str, str]] = []
    for source_id, extractor in extractors.items():
        source = registry.get(source_id)
        if source is None:
            errors.append({"source": source_id, "error": "missing candidate registry entry"})
            continue
        if source.get("ingestion_role") != "parsed-candidate":
            # A legacy extractor may remain available for local discovery, but
            # registry policy is authoritative: discovery-only sources never
            # enter the public observation snapshot.
            continue
        try:
            records = extractor()
            if not isinstance(records, list) or len(records) > MAX_OBSERVATIONS:
                raise ValueError("candidate extractor records exceed budget")
            files = inventory_files(inventory, source_id)
            for ordinal, record in enumerate(records, 1):
                if len(observations) >= MAX_OBSERVATIONS:
                    raise ValueError("candidate observation count exceeds budget")
                observation = build_observation(
                    record,
                    ordinal=ordinal,
                    source=source,
                    files=files,
                    retrieved_at=inventory["generated_at"],
                    parser_digest=parser_digest,
                    digest_cache=artifact_digests,
                )
                validation_errors = sorted(
                    observation_validator.iter_errors(observation),
                    key=lambda item: list(item.path),
                )
                if validation_errors:
                    raise ValueError(
                        f"candidate observation schema invalid: {validation_errors[0].message}"
                    )
                try:
                    encoded_observation = json.dumps(
                        observation, ensure_ascii=False, allow_nan=False
                    ).encode("utf-8")
                except (TypeError, ValueError, UnicodeEncodeError) as exc:
                    raise ValueError("candidate observation is not portable JSON") from exc
                if len(encoded_observation) > MAX_OBSERVATION_BYTES:
                    raise ValueError("candidate observation exceeds size budget")
                observations.append(observation)
                source_counts[source_id] += 1
        except Exception as exc:  # an explicit snapshot error, never a silent warning
            errors.append(
                {
                    "source": source_id,
                    "error": f"{type(exc).__name__}: {exc}"[:MAX_ERROR_CHARS],
                }
            )
    if errors and not args.allow_partial:
        for error in errors:
            print(f"ERROR: {error['source']}: {error['error']}", file=sys.stderr)
        print("candidate snapshot blocked; use --allow-partial only for quarantined diagnostics", file=sys.stderr)
        return 1
    line_chunks: list[bytes] = []
    line_total = 0
    for value in observations:
        try:
            line = (
                json.dumps(
                    value,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                    allow_nan=False,
                )
                + "\n"
            ).encode("utf-8")
        except (TypeError, ValueError, UnicodeEncodeError) as exc:
            raise ValueError("candidate snapshot observation is not portable JSON") from exc
        line_total += len(line)
        if line_total > MAX_SNAPSHOT_BYTES:
            print("candidate snapshot blocked: output exceeds size budget", file=sys.stderr)
            return 1
        line_chunks.append(line)
    lines = b"".join(line_chunks)
    if len(lines) > MAX_SNAPSHOT_BYTES:
        print("candidate snapshot blocked: output exceeds size budget", file=sys.stderr)
        return 1
    output_sha = sha256_bytes(lines)
    duplicate_count = len(observations) - len({value["observation_id"] for value in observations})
    snapshot = {
        "schema_version": "candidate-snapshot.v1",
        "snapshot_id": snapshot_id,
        "decision": "PARTIAL" if errors else "PASS",
        "candidate_count": len(observations),
        "duplicate_observation_ids": duplicate_count,
        "source_counts": dict(sorted(source_counts.items())),
        "source_errors": errors,
        "upstream_failures": inventory.get("failures", []),
        "inputs": {
            "inventory_sha256": inventory_digest,
            "parser_sha256": parser_digest,
            "candidate_schema_sha256": schema_digest,
            "source_registry_sha256": registry_digest,
        },
        "output": {
            "path": str((output_dir / "observations.jsonl").relative_to(ROOT)),
            "sha256": output_sha,
            "bytes": len(lines),
        },
    }
    if duplicate_count:
        print(
            f"candidate snapshot blocked: duplicate observation ids={duplicate_count}",
            file=sys.stderr,
        )
        return 1
    publish_snapshot(
        output_dir,
        snapshot,
        lines,
        update_latest=not errors,
    )
    if errors:
        print("partial snapshot quarantined; latest pointer was not advanced", file=sys.stderr)
    print(
        f"candidate snapshot {snapshot['decision']}: records={len(observations)} "
        f"sources={len(source_counts)} duplicate_ids={duplicate_count}"
    )
    return 0 if not errors and duplicate_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
