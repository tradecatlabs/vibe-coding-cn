#!/usr/bin/env python3
"""Validate the local external resources registry."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

import yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_DIR = ROOT / "assets" / "external-resources"
MANIFEST = REGISTRY_DIR / "resources.yml"
SCHEMA = REGISTRY_DIR / "schema.yml"
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_yaml(path: Path) -> object:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def as_dict(value: object, label: str, errors: list[str]) -> dict:
    if isinstance(value, dict):
        return value
    errors.append(f"{label}: expected mapping")
    return {}


def as_list(value: object, label: str, errors: list[str]) -> list:
    if isinstance(value, list):
        return value
    errors.append(f"{label}: expected list")
    return []


def main() -> int:
    errors: list[str] = []

    if not MANIFEST.is_file():
        print(f"EXTERNAL_RESOURCE_ERRORS\n{MANIFEST.relative_to(ROOT)}: missing manifest")
        return 1
    if not SCHEMA.is_file():
        print(f"EXTERNAL_RESOURCE_ERRORS\n{SCHEMA.relative_to(ROOT)}: missing schema")
        return 1

    manifest = as_dict(load_yaml(MANIFEST), str(MANIFEST.relative_to(ROOT)), errors)
    schema = as_dict(load_yaml(SCHEMA), str(SCHEMA.relative_to(ROOT)), errors)

    resource_schema = as_dict(schema.get("resource"), "schema.yml resource", errors)
    required_resource_fields = set(as_list(resource_schema.get("required_fields"), "schema.yml required_fields", errors))
    enums = as_dict(schema.get("enums"), "schema.yml enums", errors)
    allowed_status = set(as_list(enums.get("status"), "schema.yml enums.status", errors))
    allowed_verification = set(as_list(enums.get("verification_status"), "schema.yml enums.verification_status", errors))
    allowed_risk_flags = set(as_list(enums.get("risk_flags"), "schema.yml enums.risk_flags", errors))
    allowed_resource_types = set(as_list(enums.get("resource_type"), "schema.yml enums.resource_type", errors))
    allowed_link_kinds = set(as_dict(as_dict(schema.get("link"), "schema.yml link", errors).get("kinds"), "schema.yml link.kinds", errors))

    ids: list[str] = []
    total_resources = 0
    risk_counter: Counter[str] = Counter()

    categories = as_list(manifest.get("categories"), "resources.yml categories", errors)
    for index, category_ref in enumerate(categories, start=1):
        category_ref = as_dict(category_ref, f"resources.yml categories[{index}]", errors)
        category_id = category_ref.get("id")
        category_file = category_ref.get("file")
        expected_count = category_ref.get("count")
        if not category_id or not isinstance(category_id, str):
            errors.append(f"resources.yml categories[{index}].id: missing string")
            continue
        if not category_file or not isinstance(category_file, str):
            errors.append(f"resources.yml categories[{index}].file: missing string")
            continue

        path = REGISTRY_DIR / category_file
        if not path.is_file():
            errors.append(f"{path.relative_to(ROOT)}: missing category file")
            continue

        payload = as_dict(load_yaml(path), str(path.relative_to(ROOT)), errors)
        category = as_dict(payload.get("category"), f"{path.relative_to(ROOT)} category", errors)
        if category.get("id") != category_id:
            errors.append(f"{path.relative_to(ROOT)}: category.id does not match resources.yml")

        resources = as_list(payload.get("resources"), f"{path.relative_to(ROOT)} resources", errors)
        if expected_count != len(resources):
            errors.append(
                f"{path.relative_to(ROOT)}: expected {expected_count} resources from manifest, found {len(resources)}"
            )

        for row_index, resource in enumerate(resources, start=1):
            label = f"{path.relative_to(ROOT)} resources[{row_index}]"
            resource = as_dict(resource, label, errors)
            missing_fields = sorted(field for field in required_resource_fields if field not in resource)
            for field in missing_fields:
                errors.append(f"{label}.{field}: missing required field")

            resource_id = resource.get("id")
            if not isinstance(resource_id, str) or not ID_PATTERN.match(resource_id):
                errors.append(f"{label}.id: must be lowercase kebab-case")
            elif not resource_id.startswith(f"{category_id}-"):
                errors.append(f"{label}.id: must start with category prefix {category_id}-")
            else:
                ids.append(resource_id)

            resource_type = resource.get("resource_type")
            if resource_type not in allowed_resource_types:
                errors.append(f"{label}.resource_type: unknown value {resource_type!r}")

            status = resource.get("status")
            if status not in allowed_status:
                errors.append(f"{label}.status: unknown value {status!r}")

            verification_status = resource.get("verification_status")
            if verification_status not in allowed_verification:
                errors.append(f"{label}.verification_status: unknown value {verification_status!r}")

            link = as_dict(resource.get("link"), f"{label}.link", errors)
            link_kind = link.get("kind")
            if link_kind not in allowed_link_kinds:
                errors.append(f"{label}.link.kind: unknown value {link_kind!r}")
            elif link_kind == "external_url":
                url = link.get("url")
                domain = link.get("domain")
                parsed = urlparse(str(url))
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    errors.append(f"{label}.link.url: must be http(s) URL")
                if not isinstance(domain, str) or not domain:
                    errors.append(f"{label}.link.domain: missing domain")
                elif parsed.netloc and domain != parsed.netloc.lower():
                    errors.append(f"{label}.link.domain: does not match URL netloc")
            elif link_kind in {"internal_reference", "search_instruction"}:
                if not link.get("locator"):
                    errors.append(f"{label}.link.locator: required for {link_kind}")
                if status != "needs-review":
                    errors.append(f"{label}.status: non-URL locator must remain needs-review")
            elif link_kind == "missing":
                if status != "needs-review":
                    errors.append(f"{label}.status: missing link must remain needs-review")

            risk_flags = as_list(resource.get("risk_flags"), f"{label}.risk_flags", errors)
            unknown_flags = sorted(flag for flag in risk_flags if flag not in allowed_risk_flags)
            for flag in unknown_flags:
                errors.append(f"{label}.risk_flags: unknown value {flag!r}")
            risk_counter.update(risk_flags)
            total_resources += 1

    duplicate_ids = sorted(resource_id for resource_id, count in Counter(ids).items() if count > 1)
    for resource_id in duplicate_ids:
        errors.append(f"duplicate resource id: {resource_id}")

    stats = as_dict(manifest.get("stats"), "resources.yml stats", errors)
    if stats.get("total_resources") != total_resources:
        errors.append(f"resources.yml stats.total_resources: expected {total_resources}")
    manifest_risks = as_dict(stats.get("risk_flags"), "resources.yml stats.risk_flags", errors)
    if dict(sorted(risk_counter.items())) != manifest_risks:
        errors.append("resources.yml stats.risk_flags: does not match category files")

    if errors:
        print("EXTERNAL_RESOURCE_ERRORS")
        for error in errors:
            print(error)
        print(f"TOTAL={len(errors)}")
        return 1

    print(f"OK external resources checked: {total_resources} resources, {len(categories)} categories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
