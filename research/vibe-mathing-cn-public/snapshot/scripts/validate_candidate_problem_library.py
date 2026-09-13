#!/usr/bin/env python3
"""Fail-closed validation for versioned candidate problem observations."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    from jsonschema import Draft202012Validator, SchemaError
except ImportError as exc:  # pragma: no cover
    raise SystemExit("missing jsonschema Draft 2020-12 support") from exc

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "problem-library"
RAW = LIBRARY / "raw" / "candidates"
DERIVED = LIBRARY / "derived" / "candidate-observations"
INVENTORY = RAW / "inventory.json"
REGISTRY = LIBRARY / "registry" / "candidate-sources.json"
OBS_SCHEMA = LIBRARY / "schema" / "candidate-observation.schema.json"
SOURCE_SCHEMA = LIBRARY / "schema" / "candidate-source.schema.json"
PARSER = ROOT / "scripts" / "consolidate_candidates.py"
MAX_FILE_BYTES = 128_000_000
MAX_RECORDS = 100_000
MAX_LINE_BYTES = 30_000_000
MAX_PATH_CHARS = 4_096
MAX_SOURCE_ENTRIES = 1_000
MAX_FIELD_CHARS = 8_192
MAX_ARTIFACT_BYTES = 30_000_000


def validated_root(root: Path) -> Path:
    root_input = Path(root)
    canonical = root_input.resolve()
    if (
        not root_input.is_absolute()
        or len(str(root_input)) > MAX_PATH_CHARS
        or "\x00" in str(root_input)
        or "\\" in str(root_input)
        or root_input.is_symlink()
        or root_input.absolute() != canonical
        or not canonical.is_dir()
    ):
        raise ValueError(f"project root is not a canonical directory: {root_input}")
    return canonical


def safe_repo_path(root: Path, path: Path) -> Path:
    root_input = Path(root)
    root = root_input.resolve()
    if root_input.is_symlink() or root_input.absolute() != root:
        raise ValueError(f"project root contains symlink: {root_input}")
    candidate = path if path.is_absolute() else root / path
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes project root: {candidate}") from exc
    if (
        len(str(candidate)) > MAX_PATH_CHARS
        or any(part in {".", ".."} for part in relative.parts)
        or "\x00" in str(candidate)
        or "\\" in str(candidate)
    ):
        raise ValueError(f"path escapes project root: {candidate}")
    lexical = root
    for part in relative.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise ValueError(f"path contains symlink: {candidate}")
    return candidate


def regular_file_size(path: Path, *, root: Path | None = None) -> int:
    path = safe_repo_path(ROOT if root is None else root, path)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ValueError("platform cannot safely stat candidate files")
    descriptor = os.open(path, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > MAX_FILE_BYTES:
            raise ValueError(f"candidate file exceeds size budget: {path}")
        return file_stat.st_size
    finally:
        os.close(descriptor)


def sha256_file(
    path: Path, *, max_bytes: int = MAX_FILE_BYTES, root: Path | None = None
) -> str:
    path = safe_repo_path(ROOT if root is None else root, path)
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_FILE_BYTES
    ):
        raise ValueError("candidate file hash budget is invalid")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ValueError("platform cannot safely hash candidate files")
    try:
        descriptor = os.open(path, os.O_RDONLY | nofollow)
    except OSError as exc:
        raise ValueError(f"cannot open candidate file: {path}") from exc
    digest = hashlib.sha256()
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise ValueError(f"candidate file is not regular: {path}")
        if file_stat.st_size > max_bytes:
            raise ValueError(f"candidate file exceeds size budget: {path}")
        total = 0
        while True:
            block = os.read(descriptor, 1024 * 1024)
            if not block:
                break
            total += len(block)
            if total > max_bytes:
                raise ValueError(f"candidate file exceeds size budget: {path}")
            digest.update(block)
    finally:
        os.close(descriptor)
    return digest.hexdigest()


def _reject_json_constant(value: str) -> Any:
    raise ValueError(f"illegal JSON constant: {value}")


def read_json(
    path: Path, *, max_bytes: int = MAX_FILE_BYTES, root: Path | None = None
) -> Any:
    path = safe_repo_path(ROOT if root is None else root, path)
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_FILE_BYTES
    ):
        raise ValueError("candidate file read budget is invalid")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ValueError("platform cannot safely read candidate files")
    try:
        descriptor = os.open(path, os.O_RDONLY | nofollow)
    except OSError as exc:
        raise ValueError(f"cannot read candidate file: {path}") from exc
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise ValueError(f"candidate file is not regular: {path}")
        if file_stat.st_size > max_bytes:
            raise ValueError(f"candidate file exceeds size budget: {path}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, max_bytes - total + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"candidate file exceeds size budget: {path}")
            chunks.append(chunk)
    finally:
        os.close(descriptor)
    return json.loads(b"".join(chunks).decode("utf-8"), parse_constant=_reject_json_constant)


def safe_relative_path(root: Path, value: object, *, prefix: str, label: str) -> Path:
    root_input = Path(root)
    root = root_input.resolve()
    if (
        root_input.is_symlink()
        or root_input.absolute() != root
        or not isinstance(prefix, str)
        or not prefix
        or len(prefix) > MAX_PATH_CHARS
        or "\x00" in prefix
        or "\\" in prefix
    ):
        raise ValueError(f"unsafe project or {label} prefix")
    if (
        not isinstance(value, str)
        or not value
        or len(value) > MAX_PATH_CHARS
        or "\x00" in value
        or "\\" in value
    ):
        raise ValueError(f"{label} must be a bounded relative path")
    path = Path(value)
    if (
        path.is_absolute()
        or any(part in {".", ".."} for part in path.parts)
        or not value.startswith(prefix)
    ):
        raise ValueError(f"unsafe {label}: {value}")
    allowed = (root / prefix.rstrip("/")).resolve()
    if (root / prefix.rstrip("/")).is_symlink() or allowed != root / prefix.rstrip("/"):
        raise ValueError(f"unsafe {label} root: {value}")
    lexical = root
    for part in path.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise ValueError(f"unsafe {label} symlink: {value}")
    resolved = (root / path).resolve()
    if resolved != allowed and allowed not in resolved.parents:
        raise ValueError(f"{label} escapes allowed root: {value}")
    return resolved


def _valid_inventory_url(value: object) -> bool:
    if not isinstance(value, str) or not value or len(value) > MAX_FIELD_CHARS:
        return False
    parsed = urlparse(value)
    return (
        parsed.scheme in {"https", "generated"}
        and bool(parsed.netloc)
        and not parsed.username
        and not parsed.password
    )


def validate_inventory_shape(inventory: object, *, root: Path) -> dict[str, Any]:
    if (
        not isinstance(inventory, dict)
        or inventory.get("schema_version") != "candidate-inventory.v1"
        or not isinstance(inventory.get("sources"), dict)
        or not isinstance(inventory.get("failures"), list)
        or len(inventory["sources"]) > MAX_SOURCE_ENTRIES
        or len(inventory["failures"]) > MAX_RECORDS
    ):
        raise ValueError("candidate inventory shape or size is invalid")
    generated_at = inventory.get("generated_at")
    if not isinstance(generated_at, str) or not generated_at or len(generated_at) > MAX_FIELD_CHARS:
        raise ValueError("candidate inventory generated_at is invalid")
    total_files = 0
    seen_paths: set[str] = set()
    for source, entry in inventory["sources"].items():
        if (
            not isinstance(source, str)
            or not re.fullmatch(r"[a-z][a-z0-9_]{1,63}", source)
            or not isinstance(entry, dict)
            or not isinstance(entry.get("files", []), list)
            or len(entry.get("files", [])) > MAX_RECORDS
            or not isinstance(entry.get("counts", {}), dict)
        ):
            raise ValueError(f"{source}: inventory source entry is invalid")
        files = entry.get("files", [])
        counts = entry.get("counts", {})
        if len(counts) > MAX_SOURCE_ENTRIES or any(
            not isinstance(key, str)
            or len(key) > MAX_FIELD_CHARS
            or not isinstance(value, int)
            or isinstance(value, bool)
            or value < 0
            for key, value in counts.items()
        ):
            raise ValueError(f"{source}: inventory counts are invalid")
        total_files += len(files)
        if total_files > MAX_RECORDS:
            raise ValueError("candidate inventory files exceed budget")
        for item in files:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("name"), str)
                or not item["name"]
                or len(item["name"]) > MAX_PATH_CHARS
                or "/" in item["name"]
                or "\\" in item["name"]
                or not isinstance(item.get("path"), str)
                or not isinstance(item.get("sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"])
                or not isinstance(item.get("bytes"), int)
                or isinstance(item["bytes"], bool)
                or item["bytes"] < 0
                or item["bytes"] > MAX_ARTIFACT_BYTES
                or not _valid_inventory_url(item.get("url"))
            ):
                raise ValueError(f"{source}: inventory file entry is invalid")
            path = item["path"]
            if path in seen_paths:
                raise ValueError(f"duplicate inventory path: {path}")
            seen_paths.add(path)
            safe_relative_path(
                root,
                path,
                prefix=f"problem-library/raw/candidates/{source}/",
                label="inventory path",
            )
    for item in inventory["failures"]:
        if (
            not isinstance(item, dict)
            or not all(isinstance(item.get(key), str) for key in ("source", "name", "url", "reason"))
            or any(len(item[key]) > MAX_FIELD_CHARS for key in ("source", "url", "reason"))
            or len(item["name"]) > MAX_PATH_CHARS
        ):
            raise ValueError("candidate inventory failure entry is invalid")
    return inventory


def iter_text_lines_nofollow(path: Path):
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ValueError("platform cannot safely read candidate observations")
    descriptor = os.open(path, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > MAX_FILE_BYTES:
            raise ValueError(f"candidate observations exceed size budget: {path}")
        total = 0
        with os.fdopen(descriptor, "r", encoding="utf-8") as handle:
            for number, line in enumerate(handle, 1):
                encoded_length = len(line.encode("utf-8"))
                if encoded_length > MAX_LINE_BYTES:
                    raise ValueError(f"candidate observation line exceeds size budget: {path}")
                total += encoded_length
                if total > MAX_FILE_BYTES:
                    raise ValueError(f"candidate observations exceed size budget: {path}")
                yield number, line
    finally:
        try:
            os.close(descriptor)
        except OSError:
            pass


def validate_registry_only(*, root: Path = ROOT) -> list[str]:
    root = validated_root(root)
    errors: list[str] = []
    registry_path = root / REGISTRY.relative_to(ROOT)
    source_schema_path = root / SOURCE_SCHEMA.relative_to(ROOT)
    for path in (registry_path, source_schema_path):
        try:
            safe_repo_path(root, path)
        except ValueError as exc:
            errors.append(str(exc))
    if errors:
        return errors
    if not registry_path.is_file() or not source_schema_path.is_file():
        return ["candidate source registry/schema is missing"]
    try:
        registry = read_json(registry_path, root=root)
        source_schema = read_json(source_schema_path, root=root)
        if not isinstance(source_schema, dict) or not isinstance(registry, dict):
            raise ValueError("candidate source registry/schema must be objects")
        Draft202012Validator.check_schema(source_schema)
        errors.extend(
            f"source registry schema: {error.message}"
            for error in Draft202012Validator(source_schema).iter_errors(registry)
        )
        sources = registry.get("sources")
        if not isinstance(sources, list) or len(sources) > MAX_SOURCE_ENTRIES:
            errors.append("candidate source registry exceeds entry budget")
        else:
            ids = [item.get("source_id") for item in sources if isinstance(item, dict)]
            if len(ids) != len(sources) or any(not isinstance(item, str) for item in ids):
                errors.append("candidate source registry contains invalid source_id")
            elif len(ids) != len(set(ids)):
                errors.append("duplicate source_id in candidate source registry")
    except (OSError, KeyError, TypeError, ValueError, AttributeError, SchemaError, json.JSONDecodeError) as exc:
        errors.append(f"candidate source registry invalid: {exc}")
    return errors


def validate_paths(*, root: Path = ROOT, verify_raw: bool = False) -> list[str]:
    root = validated_root(root)
    errors: list[str] = []
    latest_path = root / DERIVED.relative_to(ROOT) / "latest.json"
    inventory_path = root / INVENTORY.relative_to(ROOT)
    registry_path = root / REGISTRY.relative_to(ROOT)
    observation_schema_path = root / OBS_SCHEMA.relative_to(ROOT)
    source_schema_path = root / SOURCE_SCHEMA.relative_to(ROOT)
    parser_path = root / PARSER.relative_to(ROOT)
    required = [latest_path, inventory_path, registry_path, observation_schema_path, source_schema_path, parser_path]
    for path in required:
        try:
            safe_repo_path(root, path)
        except ValueError as exc:
            errors.append(str(exc))
    missing = [str(path.relative_to(root)) for path in required if not path.is_file()]
    if missing:
        return [f"missing required file: {path}" for path in missing]
    registry = read_json(registry_path, root=root)
    source_schema = read_json(source_schema_path, root=root)
    Draft202012Validator.check_schema(source_schema)
    for error in Draft202012Validator(source_schema).iter_errors(registry):
        errors.append(f"source registry schema: {error.message}")
    if not isinstance(registry, dict):
        errors.append("candidate source registry must be an object")
        return errors
    registry_sources = registry.get("sources")
    if not isinstance(registry_sources, list) or len(registry_sources) > MAX_SOURCE_ENTRIES:
        errors.append("candidate source registry exceeds entry budget")
        registry_sources = []
    source_ids = [item.get("source_id") for item in registry_sources if isinstance(item, dict)]
    if len(source_ids) != len(registry_sources) or any(not isinstance(item, str) for item in source_ids):
        errors.append("candidate source registry contains invalid source_id")
    if len(source_ids) != len(set(source_ids)):
        errors.append("duplicate source_id in candidate source registry")
    source_map = {
        item["source_id"]: item
        for item in registry_sources
        if isinstance(item, dict) and isinstance(item.get("source_id"), str)
    }
    try:
        inventory = validate_inventory_shape(read_json(inventory_path, root=root), root=root)
    except (OSError, KeyError, TypeError, ValueError, AttributeError, json.JSONDecodeError) as exc:
        errors.append(f"candidate inventory invalid: {exc}")
        return errors
    inventory_sources = set(inventory["sources"])
    if inventory_sources != set(source_map):
        errors.append(
            f"registry/inventory source set drift: registry_only={sorted(set(source_map)-inventory_sources)} "
            f"inventory_only={sorted(inventory_sources-set(source_map))}"
        )
    inventory_files: dict[str, dict[str, Any]] = {}
    for source, value in inventory["sources"].items():
        if not isinstance(source, str) or not isinstance(value, dict) or not isinstance(value.get("files", []), list):
            errors.append(f"{source}: inventory source entry is invalid")
            continue
        for item in value.get("files", []):
            if not isinstance(item, dict):
                errors.append(f"{source}: inventory file entry is invalid")
                continue
            path = item.get("path")
            if (
                not isinstance(item.get("sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"])
                or not isinstance(item.get("bytes"), int)
                or isinstance(item.get("bytes"), bool)
                or item["bytes"] < 0
            ):
                errors.append(f"{source}: inventory file metadata is invalid")
            if not isinstance(path, str):
                errors.append(f"{source}: inventory file missing path")
                continue
            try:
                safe_relative_path(
                    root,
                    path,
                    prefix=f"problem-library/raw/candidates/{source}/",
                    label="inventory path",
                )
            except ValueError as exc:
                errors.append(str(exc))
                continue
            old = inventory_files.get(path)
            if old is not None:
                errors.append(f"inventory path is duplicated: {path}")
            inventory_files[path] = item
            if verify_raw:
                raw_path = safe_relative_path(
                    root,
                    path,
                    prefix=f"problem-library/raw/candidates/{source}/",
                    label="inventory path",
                )
                if not raw_path.is_file():
                    errors.append(f"missing raw distribution: {path}")
                elif regular_file_size(raw_path, root=root) != item.get("bytes") or sha256_file(raw_path, root=root) != item.get("sha256"):
                    errors.append(f"raw distribution drift: {path}")
    latest = read_json(latest_path, root=root)
    if not isinstance(latest, dict):
        errors.append("latest pointer must be an object")
        return errors
    if latest.get("schema_version") != "candidate-latest.v1":
        errors.append("latest pointer schema_version is invalid")
    try:
        snapshot_path = safe_relative_path(
            root, latest.get("snapshot_path"),
            prefix="problem-library/derived/candidate-observations/", label="latest snapshot path"
        )
        observations_path = safe_relative_path(
            root, latest.get("observations_path"),
            prefix="problem-library/derived/candidate-observations/", label="latest observations path"
        )
    except ValueError as exc:
        errors.append(str(exc))
        return errors
    for path, label in ((snapshot_path, "snapshot"), (observations_path, "observations")):
        if not path.is_file():
            errors.append(f"missing latest {label}: {path}")
    if errors:
        return errors
    snapshot = read_json(snapshot_path, root=root)
    if not isinstance(snapshot, dict):
        errors.append("candidate snapshot manifest must be an object")
        return errors
    if latest.get("snapshot_id") != snapshot.get("snapshot_id"):
        errors.append("latest snapshot_id does not match snapshot manifest")
    if latest.get("inputs") != snapshot.get("inputs"):
        errors.append("latest input digests do not match snapshot manifest")
    if latest.get("output") != snapshot.get("output"):
        errors.append("latest output summary does not match snapshot manifest")
    if snapshot.get("decision") != "PASS":
        errors.append(f"latest candidate snapshot is not PASS: {snapshot.get('decision')}")
    if not isinstance(snapshot.get("inputs"), dict) or not isinstance(snapshot.get("output"), dict):
        errors.append("candidate snapshot inputs/output must be objects")
        return errors
    expected_inputs = {
        "inventory_sha256": sha256_file(inventory_path, root=root),
        "parser_sha256": sha256_file(parser_path, root=root),
        "candidate_schema_sha256": sha256_file(observation_schema_path, root=root),
        "source_registry_sha256": sha256_file(registry_path, root=root),
    }
    if snapshot.get("inputs") != expected_inputs:
        errors.append("candidate snapshot input digests are stale")
    expected_output_path = str(observations_path.relative_to(root))
    if snapshot.get("output", {}).get("path") != expected_output_path:
        errors.append("candidate snapshot output path is not latest-bound")
    if sha256_file(observations_path, root=root) != snapshot.get("output", {}).get("sha256"):
        errors.append("candidate observations digest does not match snapshot")
    if regular_file_size(observations_path, root=root) != snapshot.get("output", {}).get("bytes"):
        errors.append("candidate observations byte count does not match snapshot")
    observation_schema = read_json(observation_schema_path, root=root)
    Draft202012Validator.check_schema(observation_schema)
    validator = Draft202012Validator(observation_schema)
    ids: set[str] = set()
    counts: Counter[str] = Counter()
    records = 0
    for number, line in iter_text_lines_nofollow(observations_path):
        if not line.strip():
            continue
        records += 1
        if records > MAX_RECORDS:
            errors.append("candidate observations exceed record budget")
            break
        try:
            value = json.loads(line, parse_constant=_reject_json_constant)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"observation line {number}: invalid JSON: {exc}")
            continue
        schema_errors = list(validator.iter_errors(value))
        if schema_errors:
            errors.append(f"observation line {number}: {schema_errors[0].message}")
            continue
        observation_id = value["observation_id"]
        if observation_id in ids:
            errors.append(f"duplicate observation_id: {observation_id}")
        ids.add(observation_id)
        source = value["source"]
        counts[source] += 1
        policy = source_map.get(source)
        if policy is None or policy.get("ingestion_role") != "parsed-candidate":
            errors.append(f"observation uses non-parsed source: {source}")
        else:
            if value["record_scope"] != policy["record_scope"]:
                errors.append(f"observation scope disagrees with registry: {observation_id}")
            if value.get("parser", {}).get("name") != policy.get("parser"):
                errors.append(f"observation parser disagrees with registry: {observation_id}")
            if value["license"] != policy.get("license"):
                errors.append(f"observation license disagrees with registry: {observation_id}")
            if value["source_status_class"] != policy.get("status_map", {}).get(
                value["source_status_raw"] or "", "unknown"
            ):
                errors.append(f"observation status mapping disagrees with registry: {observation_id}")
        artifact = value["raw_artifact"]
        try:
            safe_relative_path(
                root,
                artifact.get("path"),
                prefix=f"problem-library/raw/candidates/{source}/",
                label="observation artifact path",
            )
        except ValueError as exc:
            errors.append(f"{observation_id}: {exc}")
        declared = inventory_files.get(artifact.get("path"))
        if declared is None or declared.get("sha256") != artifact["sha256"]:
            errors.append(f"observation raw artifact is not inventory-bound: {observation_id}")
        if value["admission"] != {"state": "candidate", "research_eligible": False}:
            errors.append(f"candidate gained research eligibility: {observation_id}")
    if records != snapshot.get("candidate_count"):
        errors.append("candidate_count does not match observations")
    if dict(sorted(counts.items())) != snapshot.get("source_counts"):
        errors.append("source_counts do not match observations")
    if snapshot.get("duplicate_observation_ids") != 0:
        errors.append("snapshot reports duplicate observation ids")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate candidate problem observations without admitting them.")
    parser.add_argument("--verify-raw", action="store_true", help="rehash every raw distribution")
    parser.add_argument("--registry-only", action="store_true", help="只校验候选来源注册表与 schema，不要求 raw/snapshot")
    args = parser.parse_args()
    try:
        errors = (
            validate_registry_only()
            if args.registry_only
            else validate_paths(verify_raw=args.verify_raw)
        )
    except (OSError, KeyError, TypeError, ValueError, AttributeError, SchemaError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors[:100]:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"candidate problem library validation failed: {len(errors)} issue(s)", file=sys.stderr)
        return 1
    if args.registry_only:
        print("candidate source registry: PASS")
        return 0
    snapshot = read_json(ROOT / read_json(DERIVED / "latest.json")["snapshot_path"])
    print(
        f"candidate problem library: PASS records={snapshot['candidate_count']} "
        f"sources={len(snapshot['source_counts'])} upstream_failures={len(snapshot['upstream_failures'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
