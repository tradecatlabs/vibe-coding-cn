#!/usr/bin/env python3
"""Validate external source-fact mirrors and their provenance manifest."""

from __future__ import annotations

import hashlib
import stat
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FACTS_DIR = ROOT / "research" / "facts"
MANIFEST = FACTS_DIR / "sources.yml"
EXPECTED_IDS = {
    "vibe-cybersecurity-cn",
    "vibe-harness-cn",
    "vibe-mathing-cn-public",
}


def mirror_files(path: Path) -> tuple[list[Path], list[Path]]:
    files: list[Path] = []
    invalid: list[Path] = []
    for item in path.rglob("*"):
        if item.is_symlink() or (item.exists() and not item.is_file() and not item.is_dir()):
            invalid.append(item)
        elif item.is_file():
            files.append(item)
    return files, invalid


def mirror_digest(files: list[Path], root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(files, key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        mode = "100755" if stat.S_IMODE(path.stat().st_mode) & stat.S_IXUSR else "100644"
        digest.update(relative + b"\0" + mode.encode("ascii") + b"\0")
        digest.update(path.read_bytes() + b"\0")
    return digest.hexdigest()


def main() -> int:
    errors: list[str] = []
    if not MANIFEST.is_file():
        print(f"SOURCE_FACT_ERRORS\n{MANIFEST.relative_to(ROOT)}: missing manifest")
        return 1

    try:
        document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        print(f"SOURCE_FACT_ERRORS\n{MANIFEST.relative_to(ROOT)}: invalid YAML: {error}")
        return 1

    if document.get("kind") != "external-source-facts":
        errors.append("research/facts/sources.yml: kind must be external-source-facts")
    privacy_audit = ROOT / str(document.get("privacy_audit", ""))
    if not privacy_audit.is_file():
        errors.append("research/facts/sources.yml: privacy_audit file is missing")
    records = document.get("sources") or []
    actual_ids = {record.get("id") for record in records if isinstance(record, dict)}
    if actual_ids != EXPECTED_IDS:
        errors.append(f"research/facts/sources.yml: source IDs mismatch: {sorted(actual_ids)}")

    for record in records:
        if not isinstance(record, dict):
            errors.append("research/facts/sources.yml: each source record must be a mapping")
            continue
        source_id = record.get("id", "<unknown>")
        mirror_raw = record.get("mirror_path", "")
        mirror = ROOT / str(mirror_raw).rstrip("/")
        if not mirror.is_dir():
            errors.append(f"{source_id}: missing mirror directory {mirror_raw}")
            continue

        for field in (
            "source_commit",
            "source_tree",
            "archive_sha256",
            "tracked_file_count",
            "mirror_content_sha256",
        ):
            if not record.get(field):
                errors.append(f"{source_id}: missing fact field {field}")

        files, invalid = mirror_files(mirror)
        if len(files) != int(record.get("tracked_file_count", -1)):
            errors.append(
                f"{source_id}: mirror file count {len(files)} != manifest {record.get('tracked_file_count')}"
            )
        actual_digest = mirror_digest(files, mirror)
        if actual_digest != record.get("mirror_content_sha256"):
            errors.append(f"{source_id}: mirror content digest {actual_digest} != manifest")
        for item in invalid:
            errors.append(f"{item.relative_to(ROOT)}: symlink or special file is not allowed in source mirror")
        if any(part == ".git" for item in mirror.rglob("*") for part in item.relative_to(mirror).parts):
            errors.append(f"{source_id}: mirror contains nested .git content")
        if record.get("legacy_material_public") is not False:
            errors.append(f"{source_id}: legacy material must remain non-public")

        for raw_entry in record.get("privacy_sanitized_files", []) or []:
            raw_path, _, raw_line = str(raw_entry).partition(":")
            target = mirror / raw_path
            if not target.is_file():
                errors.append(f"{source_id}: privacy-sanitized file missing: {raw_entry}")
                continue
            try:
                line_number = int(raw_line)
                lines = target.read_text(encoding="utf-8").splitlines()
                line = lines[line_number - 1]
            except (ValueError, IndexError, UnicodeDecodeError):
                errors.append(f"{source_id}: invalid privacy-sanitized line: {raw_entry}")
                continue
            if "/home/" in line or "\\Users\\" in line or "C:\\Users\\" in line:
                errors.append(f"{source_id}: private path remains at {raw_entry}")

    if errors:
        print("SOURCE_FACT_ERRORS")
        print("\n".join(errors))
        print(f"TOTAL={len(errors)}")
        return 1

    print(f"OK source facts checked: {len(records)} mirrors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
