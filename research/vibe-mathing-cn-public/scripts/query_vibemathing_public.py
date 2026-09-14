#!/usr/bin/env python3
"""Read-only index for the public vibemathing problem namespace.

The command reads public GitHub metadata or the public catalog index. It never
clones repositories, executes remote code, or writes local problem records.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PUBLIC_NAMESPACE = "vibemathing"
REPOSITORIES_URL = "https://api.github.com/users/vibemathing/repos?per_page=100&sort=updated"
CATALOG_URL = (
    "https://raw.githubusercontent.com/vibemathing/"
    "vibe-mathing-problem-library-public/main/catalog/canonical-index.json"
)
PUBLIC_REPOSITORY_PREFIX = "https://github.com/vibemathing/"
USER_AGENT = "vibe-mathing-cn-public-index/1.0"
DEFAULT_TIMEOUT_SECONDS = 10
MAX_TIMEOUT_SECONDS = 30
MAX_RESPONSE_BYTES = 2_000_000
MAX_REPOSITORIES = 100
MAX_LIMIT = 100
REPOSITORY_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
PROBLEM_ID_RE = re.compile(r"^problem:[a-z0-9][a-z0-9.-]*$")
ALLOWED_URLS = {REPOSITORIES_URL, CATALOG_URL}


class PublicIndexError(RuntimeError):
    """Raised when remote metadata cannot be safely interpreted."""


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant: {value}")


def fetch_json(url: str, *, timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> Any:
    if url not in ALLOWED_URLS:
        raise PublicIndexError("refusing an unregistered public index URL")
    if (
        not isinstance(timeout_seconds, int)
        or isinstance(timeout_seconds, bool)
        or timeout_seconds < 1
        or timeout_seconds > MAX_TIMEOUT_SECONDS
    ):
        raise PublicIndexError("timeout must be between 1 and 30 seconds")
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="GET",
    )
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            content_length = response.headers.get("Content-Length")
            if content_length is not None:
                try:
                    if int(content_length) > MAX_RESPONSE_BYTES:
                        raise PublicIndexError("public index response exceeds the size budget")
                except ValueError as exc:
                    raise PublicIndexError("public index Content-Length is invalid") from exc
            body = response.read(MAX_RESPONSE_BYTES + 1)
    except PublicIndexError:
        raise
    except HTTPError as exc:
        raise PublicIndexError(f"public index HTTP failure: {exc.code}") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise PublicIndexError(f"public index request failed: {exc}") from exc
    if len(body) > MAX_RESPONSE_BYTES:
        raise PublicIndexError("public index response exceeds the size budget")
    try:
        return json.loads(body.decode("utf-8"), parse_constant=_reject_json_constant)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise PublicIndexError(f"public index returned invalid JSON: {exc}") from exc


def validate_repository(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise PublicIndexError("repository metadata item must be an object")
    name = item.get("name")
    full_name = item.get("full_name")
    html_url = item.get("html_url")
    if (
        not isinstance(name, str)
        or not REPOSITORY_NAME_RE.fullmatch(name)
        or not isinstance(full_name, str)
        or full_name != f"{PUBLIC_NAMESPACE}/{name}"
        or not isinstance(html_url, str)
        or html_url != f"{PUBLIC_REPOSITORY_PREFIX}{name}"
    ):
        raise PublicIndexError("repository identity is not bound to the vibemathing namespace")
    if item.get("private") is not False:
        raise PublicIndexError(f"repository {full_name} is not explicitly public")
    if item.get("fork") is not False:
        raise PublicIndexError(f"repository {full_name} is a fork; refusing ambiguous source data")
    if item.get("archived") is not False:
        raise PublicIndexError(f"repository {full_name} is archived; refusing stale source data")
    description = item.get("description")
    if description is not None and not isinstance(description, str):
        raise PublicIndexError(f"repository {full_name} has an invalid description")
    default_branch = item.get("default_branch")
    updated_at = item.get("updated_at")
    if not isinstance(default_branch, str) or not default_branch:
        raise PublicIndexError(f"repository {full_name} has no default branch")
    if not isinstance(updated_at, str) or not updated_at:
        raise PublicIndexError(f"repository {full_name} has no update timestamp")
    topics = item.get("topics", [])
    if not isinstance(topics, list) or any(not isinstance(topic, str) for topic in topics):
        raise PublicIndexError(f"repository {full_name} has invalid topics")
    return {
        "name": name,
        "full_name": full_name,
        "html_url": html_url,
        "description": description,
        "default_branch": default_branch,
        "updated_at": updated_at,
        "topics": sorted(set(topics)),
    }


def load_repositories(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, list) or not payload:
        raise PublicIndexError("public repository index must be a non-empty array")
    if len(payload) > MAX_REPOSITORIES:
        raise PublicIndexError("public repository index exceeds the 100-repository budget")
    repositories = [validate_repository(item) for item in payload]
    return sorted(repositories, key=lambda item: (item["name"].casefold(), item["name"]))


def repository_kind(repository: dict[str, Any]) -> str:
    name = repository["name"]
    if name == "vibe-mathing-problem-library-public":
        return "library"
    if name == "vibe-mathing-problem-public-template":
        return "template"
    if name.startswith("problem-um-"):
        return "candidate"
    if name.startswith("problem-"):
        # A repository name is only a locator. Canonical status comes from
        # the separately fetched catalog index, never from this prefix.
        return "concrete"
    return "other"


def select_repositories(repositories: list[dict[str, Any]], kind: str) -> list[dict[str, Any]]:
    allowed = {"all", "library", "template", "candidate", "concrete", "other"}
    if kind not in allowed:
        raise PublicIndexError(f"unknown repository kind: {kind}")
    if kind == "all":
        return repositories
    if kind == "concrete":
        return [
            repository
            for repository in repositories
            if repository_kind(repository) in {"concrete", "candidate"}
        ]
    return [repository for repository in repositories if repository_kind(repository) == kind]


def validate_catalog(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or payload.get("schema_version") != "1.0.0":
        raise PublicIndexError("canonical catalog schema_version is invalid")
    count = payload.get("count")
    records = payload.get("records")
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        raise PublicIndexError("canonical catalog count is invalid")
    if not isinstance(records, list) or count != len(records):
        raise PublicIndexError("canonical catalog count does not match records")
    if count > MAX_REPOSITORIES:
        raise PublicIndexError("canonical catalog exceeds the record budget")
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            raise PublicIndexError("canonical catalog record must be an object")
        problem_id = record.get("problem_id")
        path = record.get("path")
        lifecycle = record.get("lifecycle")
        digest = record.get("contract_sha256")
        if (
            not isinstance(problem_id, str)
            or not PROBLEM_ID_RE.fullmatch(problem_id)
            or problem_id in seen
            or not isinstance(path, str)
            or not path.startswith("catalog/problems/")
            or not path.endswith(".json")
            or lifecycle not in {"draft", "active", "withdrawn"}
            or not isinstance(digest, str)
            or not re.fullmatch(r"[a-f0-9]{64}", digest)
        ):
            raise PublicIndexError("canonical catalog record is malformed")
        seen.add(problem_id)
        normalized.append(
            {
                "problem_id": problem_id,
                "lifecycle": lifecycle,
                "path": path,
                "contract_sha256": digest,
                "contract_url": (
                    "https://github.com/vibemathing/"
                    f"vibe-mathing-problem-library-public/blob/main/{path}"
                ),
            }
        )
    return {
        "schema_version": "1.0.0",
        "count": count,
        "records": sorted(normalized, key=lambda item: item["problem_id"]),
    }


def output_payload(source: str, value: Any, *, kind: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "source": source,
        "retrieved_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
    }
    if kind is not None:
        payload["kind"] = kind
    if isinstance(value, list):
        payload["count"] = len(value)
        payload["repositories"] = value
    else:
        payload.update(value)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="只读查询 vibemathing 公共问题仓库元数据和 canonical catalog。"
    )
    parser.add_argument(
        "--kind",
        choices=("all", "library", "template", "candidate", "concrete", "other"),
        default="all",
        help="仓库类别；candidate/concrete 只是 locator 分类，不是 canonical 或数学 Result 状态。",
    )
    parser.add_argument("--catalog", action="store_true", help="读取 canonical catalog index，而非仓库列表。")
    parser.add_argument("--json", action="store_true", help="输出 JSON；默认输出简短表格。")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, dest="timeout_seconds")
    args = parser.parse_args()
    if args.limit < 1 or args.limit > MAX_LIMIT:
        parser.error(f"limit 必须在 [1, {MAX_LIMIT}] 内。")
    if args.timeout_seconds < 1 or args.timeout_seconds > MAX_TIMEOUT_SECONDS:
        parser.error(f"timeout 必须在 [1, {MAX_TIMEOUT_SECONDS}] 内。")
    return args


def main() -> int:
    args = parse_args()
    try:
        if args.catalog:
            catalog = validate_catalog(fetch_json(CATALOG_URL, timeout_seconds=args.timeout_seconds))
            records = catalog["records"][: args.limit]
            if args.json:
                catalog_output = {
                    **catalog,
                    "source_count": catalog["count"],
                    "count": len(records),
                    "records": records,
                }
                print(json.dumps(output_payload(CATALOG_URL, catalog_output), ensure_ascii=False, indent=2))
            else:
                for record in records:
                    print(
                        f"{record['problem_id']}\t{record['lifecycle']}\t"
                        f"{record['path']}\t{record['contract_url']}"
                    )
            return 0

        repositories = select_repositories(
            load_repositories(fetch_json(REPOSITORIES_URL, timeout_seconds=args.timeout_seconds)),
            args.kind,
        )[: args.limit]
        if args.json:
            print(json.dumps(output_payload(REPOSITORIES_URL, repositories, kind=args.kind), ensure_ascii=False, indent=2))
        else:
            for repository in repositories:
                print(
                    f"{repository['name']}\t{repository['description'] or ''}\t"
                    f"{repository['html_url']}"
                )
        return 0
    except PublicIndexError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
