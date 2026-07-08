#!/usr/bin/env python3
"""Fetch raw GitHub facts for research repository domains."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH_DIR = ROOT / "research"

REPO_VIEW_FIELDS = [
    "nameWithOwner",
    "url",
    "description",
    "homepageUrl",
    "isArchived",
    "isFork",
    "isMirror",
    "defaultBranchRef",
    "licenseInfo",
    "primaryLanguage",
    "repositoryTopics",
    "stargazerCount",
    "forkCount",
    "watchers",
    "createdAt",
    "updatedAt",
    "pushedAt",
    "latestRelease",
]


def run_gh(args: list[str]) -> tuple[bool, str]:
    result = subprocess.run(
        ["gh", *args],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode == 0:
        return True, result.stdout
    return False, result.stderr.strip() or result.stdout.strip()


def run_git(args: list[str], cwd: Path = ROOT) -> tuple[bool, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode == 0:
        return True, result.stdout.strip()
    return False, result.stderr.strip() or result.stdout.strip()


def read_repo_slug(domain_file: Path) -> str | None:
    text = domain_file.read_text(encoding="utf-8")
    match = re.search(r"^\s+url:\s+https://github\.com/([^\s#]+)\s*$", text, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().rstrip("/")


def read_domain_id(domain_file: Path) -> str:
    text = domain_file.read_text(encoding="utf-8")
    match = re.search(r"^\s+domain_id:\s+(.+?)\s*$", text, re.MULTILINE)
    if match:
        return unquote_yaml_value(match.group(1))
    return domain_file.parent.name


def unquote_yaml_value(value: str) -> str:
    value = value.strip()
    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
        return value[1:-1]
    return value


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, content: str) -> bool:
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        write_text(path, content)
        return False
    write_text(path, json.dumps(parsed, ensure_ascii=False, indent=2))
    return True


def raw_readme(repo_slug: str) -> str:
    return f"""# raw 事实层

本目录保存 `{repo_slug}` 的本地原始材料快照。

这里不写分析结论，只保存可复查的一手资料：

- `sources.yml`：来源清单、拉取时间、命令和文件状态。
- `repository/`：Git 仓库工作树；本目录由 `.gitignore` 忽略，只作为本地研究材料。
- `github-repo.raw.json`：GitHub 仓库元数据。
- `github-readme.raw.md.txt`：GitHub README 原文快照。
- `github-license.raw.txt`：GitHub license 原文快照；仓库无 license 时可能不存在。
- `github-root-contents.raw.json`：默认分支根目录内容快照。
- `github-languages.raw.json`：GitHub language 统计快照。
- `github-latest-release.raw.json`：最新 release 快照；无 release 时可能不存在。

`repository/` 是外部源码快照，不参与本仓库 Markdown、链接、README/AGENTS 覆盖检查。原始 README 使用 `.txt` 后缀保存，避免其中的外部相对链接被本仓库 Markdown 链接检查误判。
"""


def raw_agents(repo_slug: str) -> str:
    return f"""# raw/ Agent 指南

本目录是 `{repo_slug}` 的原始事实层。

## 维护规则

- 只保存从研究对象拉取的一手材料，不写分析判断。
- `repository/` 是本地 Git 工作树，刷新时由脚本 clone 或 fast-forward pull。
- 不手工改写 `*.raw.*` 文件内容；需要刷新时运行 `python3 scripts/fetch-research-raw.py`。
- `sources.yml` 必须记录拉取时间、来源命令和每个文件的状态。
- 外部 README 原文必须保存为 `.txt`，避免本仓库 Markdown 链接检查误判。
- 分析、判断、采用建议和沉淀路径写回上一级 `README.md`、`analysis.md` 或 `decisions.md`。
"""


def fetch_domain(domain_file: Path, pulled_at: str, force: bool) -> tuple[str, bool, list[str]]:
    repo_slug = read_repo_slug(domain_file)
    domain_id = read_domain_id(domain_file)
    if not repo_slug:
        return domain_id, False, [f"{domain_file}: missing github repo url"]

    raw_dir = domain_file.parent / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    write_text(raw_dir / "README.md", raw_readme(repo_slug))
    write_text(raw_dir / "AGENTS.md", raw_agents(repo_slug))

    records: list[dict[str, str]] = []
    errors: list[str] = []

    def record(path: str, kind: str, status: str, source: str, message: str | None = None) -> None:
        item = {
            "path": path,
            "kind": kind,
            "status": status,
            "source": source,
        }
        if message:
            item["message"] = message.replace("\n", " ")[:240]
        records.append(item)

    def fetch_file(path: str, command: list[str], *, kind: str, json_file: bool = False) -> None:
        target = raw_dir / path
        ok, output = run_gh(command)
        command_text = "gh " + " ".join(command)
        if ok:
            if json_file:
                write_json(target, output)
            else:
                write_text(target, output)
            record(path, kind, "ok", command_text)
            return

        if force and target.exists():
            target.unlink()
        record(path, kind, "missing_or_error", command_text, output)
        if kind not in {"latest-release", "license"}:
            errors.append(f"{domain_id}: {path}: {output}")

    def fetch_repository() -> None:
        repository_dir = raw_dir / "repository"
        clone_url = f"https://github.com/{repo_slug}.git"
        if (repository_dir / ".git").exists():
            ok, output = run_git(["-C", str(repository_dir), "pull", "--ff-only"])
            command_text = f"git -C {repository_dir.relative_to(ROOT)} pull --ff-only"
            if ok:
                record("repository/", "git-working-tree", "ok", command_text, output)
            else:
                record("repository/", "git-working-tree", "missing_or_error", command_text, output)
                errors.append(f"{domain_id}: repository pull failed: {output}")
            return

        if repository_dir.exists():
            message = "repository path exists but is not a Git working tree"
            record("repository/", "git-working-tree", "missing_or_error", f"git clone {clone_url}", message)
            errors.append(f"{domain_id}: {message}")
            return

        ok, output = run_git(
            [
                "clone",
                "--depth=1",
                "--single-branch",
                "--no-tags",
                clone_url,
                str(repository_dir),
            ]
        )
        command_text = (
            f"git clone --depth=1 --single-branch --no-tags {clone_url} "
            f"{repository_dir.relative_to(ROOT)}"
        )
        if ok:
            record("repository/", "git-working-tree", "ok", command_text, output)
        else:
            record("repository/", "git-working-tree", "missing_or_error", command_text, output)
            errors.append(f"{domain_id}: repository clone failed: {output}")

    fetch_repository()
    fetch_file(
        "github-repo.raw.json",
        [
            "repo",
            "view",
            repo_slug,
            "--json",
            ",".join(REPO_VIEW_FIELDS),
            "--jq",
            ".",
        ],
        kind="repository-metadata",
        json_file=True,
    )
    fetch_file(
        "github-readme.raw.md.txt",
        [
            "api",
            f"repos/{repo_slug}/readme",
            "-H",
            "Accept: application/vnd.github.raw",
        ],
        kind="readme",
    )
    fetch_file(
        "github-license.raw.txt",
        [
            "api",
            f"repos/{repo_slug}/license",
            "-H",
            "Accept: application/vnd.github.raw",
        ],
        kind="license",
    )
    fetch_file(
        "github-root-contents.raw.json",
        [
            "api",
            f"repos/{repo_slug}/contents",
        ],
        kind="root-contents",
        json_file=True,
    )
    fetch_file(
        "github-languages.raw.json",
        [
            "api",
            f"repos/{repo_slug}/languages",
        ],
        kind="languages",
        json_file=True,
    )
    fetch_file(
        "github-latest-release.raw.json",
        [
            "api",
            f"repos/{repo_slug}/releases/latest",
        ],
        kind="latest-release",
        json_file=True,
    )

    write_text(raw_dir / "sources.yml", sources_yml(domain_id, repo_slug, pulled_at, records))
    return domain_id, not errors, errors


def yaml_quote(value: str) -> str:
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def sources_yml(domain_id: str, repo_slug: str, pulled_at: str, records: list[dict[str, str]]) -> str:
    lines = [
        "version: 1",
        f"domain_id: {domain_id}",
        "object:",
        "  type: github_repository",
        f"  name: {repo_slug}",
        f"  url: https://github.com/{repo_slug}",
        f"pulled_at: {yaml_quote(pulled_at)}",
        "puller: scripts/fetch-research-raw.py",
        "files:",
    ]
    for record in records:
        lines.extend(
            [
                f"  - path: {record['path']}",
                f"    kind: {record['kind']}",
                f"    status: {record['status']}",
                f"    source: {yaml_quote(record['source'])}",
            ]
        )
        if "message" in record:
            lines.append(f"    message: {yaml_quote(record['message'])}")
    return "\n".join(lines) + "\n"


def domain_files(selected: set[str] | None) -> list[Path]:
    files = sorted(RESEARCH_DIR.glob("*/domain.yml"))
    if not selected:
        return files
    return [path for path in files if path.parent.name in selected or read_repo_slug(path) in selected]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("domains", nargs="*", help="Optional domain id or owner/repo slug to fetch.")
    parser.add_argument("--force", action="store_true", help="Remove stale optional files when fetch fails.")
    args = parser.parse_args()

    selected = set(args.domains) if args.domains else None
    files = domain_files(selected)
    if not files:
        print("No research domain.yml files found.", file=sys.stderr)
        return 1

    pulled_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    all_errors: list[str] = []
    ok_count = 0
    for path in files:
        domain_id, ok, errors = fetch_domain(path, pulled_at, args.force)
        if ok:
            ok_count += 1
        all_errors.extend(errors)
        print(f"{domain_id}: {'OK' if ok else 'WARN'}")

    if all_errors:
        print("FETCH_RESEARCH_RAW_WARNINGS")
        for error in all_errors:
            print(error)
        print(f"OK={ok_count} TOTAL={len(files)}")
        return 1

    print(f"OK fetched raw research materials: {ok_count} domains")
    return 0


if __name__ == "__main__":
    sys.exit(main())
