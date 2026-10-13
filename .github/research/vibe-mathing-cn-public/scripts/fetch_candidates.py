#!/usr/bin/env python3
# 批量下载候选数学问题库（problem-library/RESEARCH_CANDITATES.md 的 A/B 类）。
#
# 范围与边界：
#   - 只保存公开来源响应到 problem-library/raw/candidates/{source}/（gitignored 证据缓存）；
#   - 遵守各来源 robots（theoremdb Allow /；无 robots 的按默认允许并限速）；
#   - 不保存论文全文（arXiv 等除外仅索引页；Kourovka/K3/Green/Kyoto 官方问题清单 PDF 属于
#     清单本身，允许保存，与本项目"不保存论文全文"不冲突）；
#   - MathDB（疑 AI 合成）不在本清单内。
#
# 运行：python3 scripts/fetch_candidates.py [--delay 0.3] [--refresh] [--only theoremdb]
# 复用已存在缓存；output 为 raw/candidates/inventory.json（URL、路径、SHA-256、时间、失败）。

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import stat
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fails closed at CLI entry.
    fcntl = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "problem-library" / "raw" / "candidates"
INVENTORY_PATH = RAW / "inventory.json"
USER_AGENT = "vibe-mathing-problem-library/0.2 (local research archive)"
LOCKFILE = ROOT / "vendor" / "sources.lock.json"
CANDIDATE_REGISTRY = ROOT / "problem-library" / "registry" / "candidate-sources.json"
LOCK_PATH = RAW / ".fetch.lock"
DEFAULT_MAX_RESPONSE_BYTES = 30_000_000
ROBOTS_MAX_RESPONSE_BYTES = 1_000_000
MAX_TIMEOUT_SECONDS = 300.0
MAX_DELAY_SECONDS = 300.0
MAX_RETRIES = 10
MAX_INVENTORY_BYTES = 30_000_000
MAX_INVENTORY_ENTRIES = 100_000
MAX_PAGES = 1_000
MAX_DISCOVERED_ITEMS = 100_000
MAX_PATH_CHARS = 4_096
MAX_FIELD_CHARS = 8_192


def valid_inventory_url(value: object, *, allow_generated: bool = True) -> bool:
    if not isinstance(value, str) or not value or len(value) > MAX_FIELD_CHARS:
        return False
    parsed = urllib.parse.urlparse(value)
    if parsed.username or parsed.password or not parsed.netloc:
        return False
    if parsed.scheme.lower() == "https":
        return True
    return allow_generated and parsed.scheme.lower() == "generated"


def assert_safe_raw_root() -> None:
    """Reject redirected/symlinked raw roots before any read or write."""
    if RAW.is_symlink() or RAW.resolve() != RAW:
        raise RuntimeError(f"candidate raw root cannot be a symlink: {RAW}")
    lexical = ROOT
    for part in RAW.relative_to(ROOT).parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise RuntimeError(f"candidate raw path contains symlink: {RAW}")


def _reject_json_constant(value: str) -> Any:
    raise ValueError(f"JSON 常量非法：{value}")


def loads_json(data: bytes | str) -> Any:
    try:
        text = data.decode("utf-8") if isinstance(data, bytes) else data
        if not isinstance(text, str) or len(text.encode("utf-8")) > MAX_INVENTORY_BYTES:
            raise RuntimeError("JSON 输入超过大小预算")
        return json.loads(text, parse_constant=_reject_json_constant)
    except (UnicodeDecodeError, UnicodeEncodeError, ValueError) as exc:
        raise RuntimeError("JSON 输入无效") from exc


def bounded_items(value: Any, label: str, *, limit: int = MAX_DISCOVERED_ITEMS) -> list[Any]:
    if not isinstance(value, list) or len(value) > limit:
        raise RuntimeError(f"{label} 超过发现预算")
    return value


def bounded_values(values: list[Any], label: str, *, limit: int = MAX_DISCOVERED_ITEMS) -> list[Any]:
    if len(values) > limit:
        raise RuntimeError(f"{label} 超过发现预算")
    return values


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_bounded_file(path: Path, max_bytes: int) -> bytes:
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_INVENTORY_BYTES
    ):
        raise RuntimeError("candidate file read budget is invalid")
    path = Path(path)
    if (
        len(str(path)) > MAX_PATH_CHARS
        or "\x00" in str(path)
        or "\\" in str(path)
        or any(part == ".." for part in path.parts)
    ):
        raise RuntimeError(f"candidate file path contains an invalid component: {path}")
    root = ROOT.resolve()
    candidate = path if path.is_absolute() else ROOT / path
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(f"candidate file path escapes project root: {candidate}") from exc
    lexical = root
    for part in relative.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise RuntimeError(f"candidate file path contains symlink: {candidate}")
    if candidate.resolve() != candidate:
        raise RuntimeError(f"candidate file path contains symlink: {candidate}")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeError("current platform cannot safely read candidate files")
    descriptor = os.open(candidate, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > max_bytes:
            raise RuntimeError(f"candidate file exceeds budget or is not regular: {candidate}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, max_bytes - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > max_bytes:
                raise RuntimeError(f"candidate file exceeds budget: {candidate}")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def validate_inventory(inventory: object) -> dict[str, Any]:
    if not isinstance(inventory, dict):
        raise RuntimeError("candidate inventory must be an object")
    if inventory.get("schema_version") not in (None, "candidate-inventory.v1"):
        raise RuntimeError("candidate inventory schema_version is invalid")
    sources = inventory.get("sources")
    failures = inventory.get("failures")
    if not isinstance(sources, dict) or not isinstance(failures, list):
        raise RuntimeError("candidate inventory shape is invalid")
    if len(sources) > MAX_INVENTORY_ENTRIES or len(failures) > MAX_INVENTORY_ENTRIES:
        raise RuntimeError("candidate inventory entry count exceeds budget")
    total_files = 0
    for source_id, entry in sources.items():
        if (
            not isinstance(source_id, str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,255}", source_id)
            or not isinstance(entry, dict)
        ):
            raise RuntimeError("candidate inventory source entry is invalid")
        files = entry.get("files", [])
        counts = entry.get("counts", {})
        if not isinstance(files, list) or len(files) > MAX_INVENTORY_ENTRIES or not isinstance(counts, dict):
            raise RuntimeError("candidate inventory source files/counts are invalid")
        if any(
            not isinstance(key, str)
            or len(key) > MAX_FIELD_CHARS
            or not isinstance(value, int)
            or isinstance(value, bool)
            or value < 0
            for key, value in counts.items()
        ):
            raise RuntimeError("candidate inventory counts are invalid")
        total_files += len(files)
        if total_files > MAX_INVENTORY_ENTRIES:
            raise RuntimeError("candidate inventory files exceed budget")
        names: set[str] = set()
        paths: set[str] = set()
        for file_entry in files:
            if (
                not isinstance(file_entry, dict)
                or not isinstance(file_entry.get("name"), str)
                or not isinstance(file_entry.get("path"), str)
                or not isinstance(file_entry.get("url"), str)
                or not valid_inventory_url(file_entry.get("url"))
                or not isinstance(file_entry.get("sha256"), str)
                or not isinstance(file_entry.get("bytes"), int)
                or isinstance(file_entry.get("bytes"), bool)
                or file_entry["bytes"] < 0
                or file_entry["bytes"] > DEFAULT_MAX_RESPONSE_BYTES
                or len(file_entry["name"]) > MAX_PATH_CHARS
                or len(file_entry["path"]) > MAX_PATH_CHARS
                or len(file_entry["url"]) > MAX_FIELD_CHARS
                or "\x00" in file_entry["name"]
                or "\x00" in file_entry["path"]
                or "\\" in file_entry["name"]
                or "\\" in file_entry["path"]
                or any(part in {".", ".."} for part in Path(file_entry["path"]).parts)
                or not re.fullmatch(r"[0-9a-f]{64}", file_entry["sha256"])
                or file_entry["name"] in names
                or file_entry["path"] in paths
            ):
                raise RuntimeError("candidate inventory file entry is invalid")
            names.add(file_entry["name"])
            paths.add(file_entry["path"])
            expected_path = str(safe_raw_artifact_path(source_id, file_entry["name"]).relative_to(ROOT))
            if file_entry["path"] != expected_path:
                raise RuntimeError("candidate inventory artifact path is not source-bound")
    for item in failures:
        if (
            not isinstance(item, dict)
            or not all(isinstance(item.get(key), str) for key in ("source", "name", "url", "reason"))
            or any(len(item[key]) > MAX_FIELD_CHARS for key in ("source", "url", "reason"))
            or len(item["name"]) > MAX_PATH_CHARS
        ):
            raise RuntimeError("candidate inventory failures are invalid")
    return inventory


def read_inventory() -> dict[str, Any]:
    assert_safe_raw_root()
    if INVENTORY_PATH.is_symlink() or INVENTORY_PATH.resolve() != INVENTORY_PATH:
        raise RuntimeError(f"candidate inventory cannot be a symlink: {INVENTORY_PATH}")
    if INVENTORY_PATH.is_file():
        return validate_inventory(
            loads_json(read_bounded_file(INVENTORY_PATH, MAX_INVENTORY_BYTES))
        )
    return validate_inventory(
        {"schema_version": "candidate-inventory.v1", "sources": {}, "failures": [], "generated_at": None}
    )


def write_inventory(inventory: dict[str, Any]) -> None:
    assert_safe_raw_root()
    INVENTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    validate_inventory(inventory)
    try:
        data = (
            json.dumps(inventory, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise RuntimeError("candidate inventory is not portable JSON") from exc
    if len(data) > MAX_INVENTORY_BYTES:
        raise RuntimeError("candidate inventory exceeds size budget")
    if INVENTORY_PATH.is_symlink():
        raise RuntimeError(f"candidate inventory cannot be a symlink: {INVENTORY_PATH}")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if nofollow is None or directory is None:
        raise RuntimeError("current platform cannot safely publish candidate inventory")
    tmp = INVENTORY_PATH.with_name(f".inventory.{os.getpid()}.tmp")
    try:
        descriptor = os.open(
            tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow, 0o600
        )
    except OSError as exc:
        raise RuntimeError("cannot create candidate inventory temporary file") from exc
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, INVENTORY_PATH)
        directory_descriptor = os.open(
            INVENTORY_PATH.parent,
            os.O_RDONLY | directory | nofollow,
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        tmp.unlink(missing_ok=True)


def safe_raw_artifact_path(source: str, name: str) -> Path:
    """Resolve a candidate artifact without crossing or following a symlink."""
    if (
        not isinstance(source, str)
        or not isinstance(name, str)
        or not source
        or not name
        or len(source) > MAX_PATH_CHARS
        or len(name) > MAX_PATH_CHARS
        or len(source) + len(name) + len(str(RAW)) + 2 > MAX_PATH_CHARS
    ):
        raise ValueError("candidate artifact path is invalid or too long")
    source_path = Path(source)
    relative_name = Path(name)
    if (
        source_path.parts != (source,)
        or "\x00" in source
        or "\\" in source
        or source_path.is_absolute()
        or ".." in source_path.parts
        or not relative_name.parts
        or any(part in {".", ".."} for part in relative_name.parts)
        or "\x00" in name
        or "\\" in name
        or relative_name.is_absolute()
        or RAW.is_symlink()
    ):
        raise ValueError(f"unsafe candidate artifact path: {source}/{name}")
    lexical = RAW
    for part in (*source_path.parts, *relative_name.parts):
        lexical = lexical / part
        if lexical.is_symlink():
            raise ValueError(f"candidate artifact path contains symlink: {source}/{name}")
    path = lexical.resolve()
    raw_root = RAW.resolve()
    if path != raw_root and raw_root not in path.parents:
        raise ValueError(f"candidate artifact escapes raw root: {source}/{name}")
    return path


class FetchError(RuntimeError):
    """A bounded or transport-level fetch failure that belongs in the source ledger."""


def _set_response_timeout(response: Any, timeout: float) -> None:
    candidates: list[Any] = [response]
    current = response
    for attribute in ("fp", "raw", "_sock"):
        current = getattr(current, attribute, None)
        if current is None:
            break
        candidates.append(current)
    for candidate in candidates:
        setter = getattr(candidate, "settimeout", None)
        if callable(setter):
            try:
                setter(max(0.001, timeout))
            except OSError as exc:
                raise FetchError("无法设置候选响应读取超时") from exc
            return


class ResponseTooLarge(FetchError):
    pass


class HTTPSRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Reject redirects that downgrade a candidate fetch from HTTPS to HTTP."""

    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Any:
        target = urllib.parse.urljoin(req.full_url, newurl)
        parsed_target = urllib.parse.urlparse(target)
        if parsed_target.scheme.lower() != "https" or not parsed_target.netloc:
            raise FetchError(f"拒绝非 HTTPS 重定向：{target}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


HTTPS_OPENER = urllib.request.build_opener(HTTPSRedirectHandler())


class Fetcher:
    def __init__(self, *, timeout: float, delay: float, retries: int) -> None:
        if not math.isfinite(timeout) or timeout <= 0 or timeout > MAX_TIMEOUT_SECONDS:
            raise ValueError(f"timeout 必须在 (0, {MAX_TIMEOUT_SECONDS}] 内")
        if not math.isfinite(delay) or delay < 0 or delay > MAX_DELAY_SECONDS:
            raise ValueError(f"delay 必须在 [0, {MAX_DELAY_SECONDS}] 内")
        if isinstance(retries, bool) or not isinstance(retries, int) or retries <= 0 or retries > MAX_RETRIES:
            raise ValueError(f"retries 必须在 [1, {MAX_RETRIES}] 内")
        self.timeout = timeout
        self.delay = delay
        self.retries = retries
        self._last_request_at = 0.0

    def _wait(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

    @staticmethod
    def _read_limited(
        response: Any, max_bytes: int, *, timeout: float = MAX_TIMEOUT_SECONDS
    ) -> bytes:
        if (
            isinstance(max_bytes, bool)
            or not isinstance(max_bytes, int)
            or max_bytes <= 0
            or max_bytes > DEFAULT_MAX_RESPONSE_BYTES
        ):
            raise ValueError("响应大小上限无效")
        if not math.isfinite(timeout) or timeout <= 0 or timeout > MAX_TIMEOUT_SECONDS:
            raise ValueError("响应读取 timeout 无效")
        content_length = response.headers.get("Content-Length")
        if content_length:
            try:
                declared = int(content_length)
            except (TypeError, ValueError) as exc:
                raise FetchError("响应 Content-Length 无效") from exc
            if declared < 0:
                raise FetchError("响应 Content-Length 无效")
            if declared > max_bytes:
                raise ResponseTooLarge(f"响应声明大小超过上限 {max_bytes} bytes")
        chunks: list[bytes] = []
        total = 0
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise FetchError(f"响应读取超时：{timeout}s")
            _set_response_timeout(response, min(timeout, remaining))
            chunk = response.read(min(64 * 1024, max_bytes - total + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise ResponseTooLarge(f"响应超过上限 {max_bytes} bytes")
            chunks.append(chunk)
        return b"".join(chunks)

    def fetch(
        self, url: str, *, max_bytes: int = DEFAULT_MAX_RESPONSE_BYTES
    ) -> tuple[bytes, int, dict[str, str]]:
        parsed_url = urllib.parse.urlparse(url)
        if (
            parsed_url.scheme.lower() != "https"
            or not parsed_url.netloc
            or parsed_url.username
            or parsed_url.password
        ):
            raise FetchError(f"候选来源只允许带主机的 HTTPS URL：{url}")
        if (
            isinstance(max_bytes, bool)
            or not isinstance(max_bytes, int)
            or max_bytes <= 0
            or max_bytes > DEFAULT_MAX_RESPONSE_BYTES
        ):
            raise ValueError("响应大小上限无效")
        headers = {
            "Accept": "text/html,application/json;q=0.9,*/*;q=0.1",
            "Accept-Encoding": "identity",
            "User-Agent": USER_AGENT,
        }
        error: Exception | None = None
        for attempt in range(1, self.retries + 1):
            self._wait()
            request = urllib.request.Request(url, headers=headers)
            try:
                with HTTPS_OPENER.open(request, timeout=self.timeout) as response:
                    final_url = response.geturl()
                    final_parsed = urllib.parse.urlparse(final_url)
                    if (
                        final_parsed.scheme.lower() != "https"
                        or not final_parsed.netloc
                        or final_parsed.username
                        or final_parsed.password
                    ):
                        raise FetchError(f"候选响应不是带主机的 HTTPS URL：{final_url}")
                    response_headers = {k.lower(): v for k, v in response.headers.items()}
                    body = self._read_limited(
                        response, max_bytes, timeout=self.timeout
                    )
                    self._last_request_at = time.monotonic()
                    return body, response.status, response_headers
            except urllib.error.HTTPError as exc:
                self._last_request_at = time.monotonic()
                if exc.code == 429 and attempt < self.retries:
                    wait = 30 * attempt
                    print(f"  429 限流：等待 {wait}s 重试 {url}", flush=True)
                    time.sleep(wait)
                    continue
                return b"", exc.code, {}
            except ResponseTooLarge:
                self._last_request_at = time.monotonic()
                raise
            except FetchError:
                self._last_request_at = time.monotonic()
                raise
            except (urllib.error.URLError, TimeoutError) as exc:
                self._last_request_at = time.monotonic()
                error = exc
                if attempt < self.retries:
                    time.sleep(min(2 ** (attempt - 1), 10))
        raise FetchError(f"抓取失败（重试 {self.retries} 次）：{url}: {error}") from error


class Sink:
    """记录每个 URL 的下载结果并追加到 inventory。"""

    def __init__(self, inventory: dict[str, Any], source: str) -> None:
        self.inventory = inventory
        self.source = source
        self.entries = inventory["sources"].setdefault(source, {"files": [], "counts": Counter()})
        self.failures: list[dict[str, Any]] = []

    def save(self, name: str, url: str, body: bytes) -> Path:
        if (
            not isinstance(name, str)
            or not isinstance(url, str)
            or not name
            or not url
            or len(name) > MAX_PATH_CHARS
            or len(url) > MAX_FIELD_CHARS
        ):
            raise ValueError("candidate artifact name or URL is invalid or too long")
        if not valid_inventory_url(url):
            raise ValueError("candidate artifact URL must be HTTPS or generated with a host")
        if not isinstance(body, bytes):
            raise TypeError("candidate artifact body must be bytes")
        if len(body) > DEFAULT_MAX_RESPONSE_BYTES:
            raise ResponseTooLarge("candidate artifact exceeds size budget")
        if len(self.entries["files"]) >= MAX_INVENTORY_ENTRIES:
            raise RuntimeError("candidate inventory file count exceeds budget")
        path = safe_raw_artifact_path(self.source, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
        nofollow = getattr(os, "O_NOFOLLOW", None)
        directory = getattr(os, "O_DIRECTORY", None)
        if nofollow is None or directory is None:
            raise RuntimeError("current platform cannot safely publish candidate artifact")
        try:
            descriptor = os.open(
                temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow, 0o600
            )
        except OSError as exc:
            raise RuntimeError("cannot create candidate artifact temporary file") from exc
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(body)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
            directory_descriptor = os.open(
                path.parent, os.O_RDONLY | directory | nofollow
            )
            try:
                os.fsync(directory_descriptor)
            finally:
                os.close(directory_descriptor)
        finally:
            temporary.unlink(missing_ok=True)
        self.entries["files"].append(
            {
                "name": name,
                "url": url,
                "path": str(path.relative_to(ROOT)),
                "sha256": sha256_bytes(body),
                "bytes": len(body),
            }
        )
        self.entries["counts"]["files"] = self.entries["counts"].get("files", 0) + 1
        return path

    def fail(self, name: str, url: str, reason: str) -> None:
        if not all(isinstance(value, str) for value in (name, url, reason)):
            raise RuntimeError("candidate inventory failure fields must be strings")
        item = {
            "source": self.source,
            "name": name[:MAX_PATH_CHARS],
            "url": url[:MAX_FIELD_CHARS],
            "reason": reason[:MAX_FIELD_CHARS],
        }
        self.failures.append(item)
        failures = self.inventory.setdefault("failures", [])
        if len(failures) >= MAX_INVENTORY_ENTRIES:
            raise RuntimeError("candidate inventory failure count exceeds budget")
        failures.append(item)


def download(
    sink: Sink,
    fetcher: Fetcher,
    name: str,
    url: str,
    *,
    refresh: bool = False,
    ok_status: tuple[int, ...] = (200,),
    max_bytes: int | None = None,
) -> bytes | None:
    limit = DEFAULT_MAX_RESPONSE_BYTES if max_bytes is None else max_bytes
    if (
        isinstance(limit, bool)
        or not isinstance(limit, int)
        or limit <= 0
        or limit > DEFAULT_MAX_RESPONSE_BYTES
    ):
        raise ValueError("响应大小上限无效")
    path = safe_raw_artifact_path(sink.source, name)
    if path.is_file() and not refresh:
        try:
            return read_bounded_file(path, limit)
        except (OSError, RuntimeError) as exc:
            sink.fail(name, url, f"缓存读取失败：{type(exc).__name__}")
            return None
    try:
        body, status, _headers = fetcher.fetch(url, max_bytes=limit)
    except FetchError as exc:
        sink.fail(name, url, str(exc))
        return None
    if status not in ok_status:
        sink.fail(name, url, f"HTTP {status}")
        return None
    if not body:
        sink.fail(name, url, "空响应")
        return None
    sink.save(name, url, body)
    return body


def probe_robots(fetcher: Fetcher, sink: Sink, source: str, url: str) -> dict[str, Any]:
    body, status, _ = fetcher.fetch(url, max_bytes=ROBOTS_MAX_RESPONSE_BYTES)
    result = {"status": status, "url": url}
    if status == 200 and body:
        result["summary"] = "\n".join(
            line for line in body.decode("utf-8", errors="replace").splitlines() if line and not line.startswith("#")
        )[:600]
    return result


# ---------------------------------------------------------------------------
# 各来源
# ---------------------------------------------------------------------------

def fetch_theoremdb(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    for name, url in (
        ("statement-slugs.json", "https://theoremdb.org/statement-slugs.json"),
        ("search-index.json", "https://theoremdb.org/search-index.json"),
        ("problems-index.html", "https://theoremdb.org/problems"),
    ):
        download(sink, fetcher, name, url, refresh=refresh)
    if not (RAW / "theoremdb" / "statement-slugs.json").is_file():
        return
    slugs_path = safe_raw_artifact_path("theoremdb", "statement-slugs.json")
    slugs = bounded_items(loads_json(read_bounded_file(slugs_path, DEFAULT_MAX_RESPONSE_BYTES))["slugs"], "TheoremDB slugs")
    if any(not isinstance(slug, str) or not slug or len(slug) > MAX_PATH_CHARS for slug in slugs):
        raise RuntimeError("TheoremDB slug is invalid")
    index_path = RAW / "theoremdb" / "search-index.json"
    if index_path.is_file():
        index_slugs = [
            item["slug"]
            for item in bounded_items(
                loads_json(read_bounded_file(index_path, DEFAULT_MAX_RESPONSE_BYTES))["items"],
                "TheoremDB index items",
            )
            if isinstance(item, dict) and item.get("slug")
        ]
        if any(not isinstance(slug, str) or len(slug) > MAX_PATH_CHARS for slug in index_slugs):
            raise RuntimeError("TheoremDB index slug is invalid")
        slugs = list(dict.fromkeys(slugs + index_slugs))
    for index, slug in enumerate(slugs, 1):
        name = f"statement/{urllib.parse.quote(slug, safe='')}.html"
        path = RAW / "theoremdb" / "statement" / f"{urllib.parse.quote(slug, safe='')}.html"
        if path.is_file() and not refresh:
            continue
        body = download(sink, fetcher, name, f"https://theoremdb.org/statement/?ref={urllib.parse.quote(slug)}", refresh=refresh)
        if index % 400 == 0:
            print(f"  TheoremDB 陈述页 {index}/{len(slugs)}", flush=True)


def fetch_openlogicproblems(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    body = download(sink, fetcher, "problems.html", "https://www.openlogicproblems.com/problems", refresh=refresh)
    if body is None:
        return
    links = re.findall(r'href="(/problems/[^"]+)"', body.decode("utf-8", errors="replace"))
    links = bounded_values(list(dict.fromkeys(links)), "OpenLogic problem links")
    for link in links:
        name = f"pages/{link.strip('/').replace('/', '_')}.html"
        download(sink, fetcher, name, f"https://www.openlogicproblems.com{link}", refresh=refresh)


def fetch_topp(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    body = download(
        sink, fetcher, "problems_by_number.html", "https://topp.openproblem.net/problems_by_number", refresh=refresh
    )
    if body is None:
        return
    text = body.decode("utf-8", errors="replace")
    numbers = bounded_values(sorted({int(m[1:]) for m in re.findall(r"/(p\d+)", text)}), "TOPP problem links")
    print(f"  TOPP 检出 {len(numbers)} 个问题编号", flush=True)
    for number in numbers:
        download(sink, fetcher, f"pages/p{number}.html", f"https://topp.openproblem.net/p{number}", refresh=refresh)


def fetch_openquantum(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    download(sink, fetcher, "home.html", "https://openquantumproblems.com/", refresh=refresh)
    # The linked Git archive is branch-addressed and has no public lock entry yet.
    # Refuse to turn a moving branch into an apparently reproducible snapshot.
    sink.fail(
        "source-tarball.tar.gz",
        "https://github.com/jpbruneton/open_quantum_problems",
        "Git archive is not pinned in vendor/sources.lock.json; source remains discovery-only",
    )


def fetch_ucsd(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    base = "https://mathweb.ucsd.edu/~erdosproblems/"
    pages = ["index.htm", "All.html", "Search.html", "SiteDetails.html", "disclaimer.html", "About.html",
             "RamseyTheory.html", "ExtremalGraphTheory.html", "ColoringPackingandCovering.html",
             "RandomGraphsandGraphEnumeration.html", "Hypergraphs.html", "InfiniteGraphs.html"]
    for page in pages:
        name = page.replace(".htm", ".html") if page == "index.htm" else page
        body = download(sink, fetcher, name, base + page, refresh=refresh)
        if body is None:
            print(f"  UCSD 页面失败：{page}", flush=True)
    all_path = safe_raw_artifact_path("ucsd", "All.html")
    all_body = read_bounded_file(all_path, DEFAULT_MAX_RESPONSE_BYTES) if all_path.is_file() else b""
    if not all_body:
        return
    problems = re.findall(r'HREF="(erdos/newproblems/[^"]+)"', all_body.decode("latin-1", errors="replace"))
    problems = bounded_values(list(dict.fromkeys(problems)), "UCSD problem links")
    for link in problems:
        name = f"erdos/newproblems/{link.rsplit('/', 1)[-1]}"
        download(sink, fetcher, name, base + link, refresh=refresh)

def fetch_aim(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    body = download(sink, fetcher, "problemlists.html", "https://aimath.org/problemlists/", refresh=refresh)
    if body is None:
        return
    text = body.decode("utf-8", errors="replace")
    pdfs = bounded_values(sorted(
        set(re.findall(r'href="(/pastworkshops/[^"]+\.pdf|/WWN/[^"]+\.pdf|/WWN/[^"]*/[^"]+\.pdf)"', text))
    ), "AIM PDF links")
    for pdf in pdfs:
        name = f"pdfs/{pdf.strip('/').replace('/', '_')}"
        if name.endswith(".pdf"):
            download(sink, fetcher, name, f"https://aimath.org{pdf}", refresh=refresh)
    aimpl = bounded_values(sorted(set(re.findall(r'href="(https?://aimpl\.org/[^"]+)"', text))), "AIM problem links")
    for url in aimpl:
        path = urllib.parse.urlparse(url).path.strip("/")
        name = f"aimpl/{path}.html"
        download(sink, fetcher, name, url, refresh=refresh)


def fetch_pdfs(fetcher: Fetcher, sink: Sink, *, refresh: bool, items: dict[str, str]) -> None:
    for name, url in items.items():
        download(sink, fetcher, name, url, refresh=refresh)


def fetch_kirby(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    body = download(
        sink, fetcher, "kirby-faculty.html",
        "https://pantheon.math.berkeley.edu/people/faculty/robion-kirby", refresh=refresh
    )
    if body is None:
        return
    text = body.decode("utf-8", errors="replace")
    cands = re.findall(r'href="([^"]+\.pdf)"', text)
    pdfs: list[str] = []
    for cand in cands:
        if cand.startswith("http"):
            pdfs.append(cand)
        else:
            pdfs.append(urllib.parse.urljoin("https://pantheon.math.berkeley.edu/", cand))
    for pdf in dict.fromkeys(pdfs):
        name = f"pdfs/{urllib.parse.urlparse(pdf).path.rsplit('/', 1)[-1]}"
        if name.endswith(".pdf"):
            download(sink, fetcher, name, pdf, refresh=refresh)
    if not pdfs:
        sink.fail("k3.pdf", "https://pantheon.math.berkeley.edu/people/faculty/robion-kirby", "页面未发现 PDF 链接")


def fetch_mathoverflow(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    page = 1
    while True:
        url = (
            "https://api.stackexchange.com/2.3/questions"
            f"?tagged=open-problems&site=mathoverflow&pagesize=100&page={page}&filter=withbody"
        )
        name = f"api/questions-page-{page:02d}.json"
        body = download(sink, fetcher, name, url, refresh=refresh, max_bytes=25_000_000)
        if body is None:
            return
        data = loads_json(body)
        if not data.get("has_more"):
            break
        page += 1
        if page > 10:
            sink.fail("api", url, "超过 10 页上限")
            break
    download(sink, fetcher, "biglist-100265.html", "https://mathoverflow.net/questions/100265", refresh=refresh)


def fetch_polymath(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    # 原 wiki（michaelnielsen.org/polymath）2026-09-01 已 404；抓取存活的官方 blog 入口页。
    for name, url in (
        ("blog-index.html", "https://polymathprojects.org/"),
        ("about.html", "https://polymathprojects.org/about/"),
        ("rules.html", "https://polymathprojects.org/general-polymath-rules/"),
    ):
        download(sink, fetcher, name, url, refresh=refresh)


def fetch_oeis_wiki(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    pages = {
        "Category_Problems.html": "Category:Problems",
        "List_of_prime_conjectures.html": "List of prime conjectures",
        "Index_to_OEIS_Section_Se.html": "Index to OEIS: Section Se",
        "Suggestions_for_OEIS_from_OEIS_50_Workshop.html": "Suggestions for OEIS from OEIS 50 Workshop",
    }
    for name, title in pages.items():
        download(sink, fetcher, name, "https://oeis.org/wiki/" + urllib.parse.quote(title), refresh=refresh)


def fetch_amr(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    download(sink, fetcher, "problems.html", "https://amathr.org/problems/", refresh=refresh)


def fetch_wikipedia_more(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """Wikipedia「未解问题」清单家族（数学之外的相关领域 + 中文版数学清单）。"""
    pages = (
        "List_of_unsolved_problems_in_computer_science",
        "List_of_unsolved_problems_in_statistics",
        "List_of_unsolved_problems_in_physics",
        "List_of_unsolved_problems_in_economics",
        "List_of_unsolved_problems_in_neuroscience",
        "未解决的数学问题",
    )
    for page in pages:
        if page.startswith("未"):
            name = "zh-unsolved-math.json"
            url = ("https://zh.wikipedia.org/w/api.php?action=parse&page="
                   + urllib.parse.quote(page) + "&prop=text%7Csections&format=json&formatversion=2&redirects=1")
        else:
            name = page.replace("_", "-") + ".json"
            url = ("https://en.wikipedia.org/w/api.php?action=parse&page=" + page
                   + "&prop=text%7Csections&format=json&formatversion=2&redirects=1")
        download(sink, fetcher, name, url, refresh=refresh)

def fetch_oeis_unsolved(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    download(sink, fetcher, "Category_Unsolved_problems.html", "https://oeis.org/wiki/Category:Unsolved_problems", refresh=refresh)


def fetch_planetmath(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    download(sink, fetcher, "unsolvedproblems.html", "https://planetmath.org/unsolvedproblems", refresh=refresh)


def fetch_zh_conjectures(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """中文维基「猜想」分类：成员列表 + 每条目摘要。"""
    cat = "Category:猜想"
    url = ("https://zh.wikipedia.org/w/api.php?action=query&list=categorymembers"
           f"&cmtitle={urllib.parse.quote(cat)}&cmlimit=500&format=json&formatversion=2")
    body = download(sink, fetcher, "members/zh-conjectures.json", url, refresh=refresh)
    if body is None:
        return
    data = loads_json(body)
    members = bounded_items(
        [m["title"] for m in data.get("query", {}).get("categorymembers", [])],
        "中文维基猜想成员",
    )
    if any(not isinstance(title, str) or len(title) > MAX_PATH_CHARS for title in members):
        raise RuntimeError("中文维基猜想成员无效")
    for start in range(0, len(members), 20):
        batch = members[start:start + 20]
        titles = "|".join(urllib.parse.quote(t, safe="") for t in batch)
        url = ("https://zh.wikipedia.org/w/api.php?action=query&prop=extracts"
               f"&exintro&explaintext&redirects=1&titles={titles}&format=json&formatversion=2&exlimit=20")
        download(sink, fetcher, f"extracts/zh-{start // 20:02d}.json", url, refresh=refresh)


def record_locked_reference(sink: Sink, lock_id: str, *, refresh: bool) -> None:
    """Record a lockfile-pinned reference without cloning or materializing a worktree."""
    try:
        lock = loads_json(read_bounded_file(LOCKFILE, 5_000_000))
        if not isinstance(lock, dict) or not isinstance(lock.get("sources"), list):
            raise ValueError("lockfile source list is invalid")
        if len(lock["sources"]) > MAX_INVENTORY_ENTRIES:
            raise ValueError("lockfile source count exceeds budget")
        lock_ids: set[str] = set()
        for item in lock["sources"]:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("id"), str)
                or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,255}", item["id"])
                or item["id"] in lock_ids
            ):
                raise ValueError("lockfile source ID list is invalid")
            lock_ids.add(item["id"])
        source = next(item for item in lock["sources"] if item["id"] == lock_id)
    except (OSError, KeyError, StopIteration, TypeError, ValueError, json.JSONDecodeError) as exc:
        sink.fail(lock_id, "vendor/sources.lock.json", f"无法读取固定 reference：{type(exc).__name__}")
        return
    commit = source.get("commit")
    url = source.get("url")
    parsed_url = urllib.parse.urlparse(url) if isinstance(url, str) else None
    if (
        source.get("kind") != "git-reference"
        or not isinstance(commit, str)
        or not re.fullmatch(r"[0-9a-f]{40}", commit)
        or not isinstance(url, str)
        or not url
        or parsed_url is None
        or parsed_url.scheme.lower() != "https"
        or not parsed_url.netloc
        or parsed_url.username
        or parsed_url.password
    ):
        sink.fail(lock_id, url if isinstance(url, str) and url else "vendor/sources.lock.json", "lockfile 不是有效的 git-reference/40 位 commit")
        return
    if refresh:
        sink.fail(
            lock_id,
            url,
            "reference-only snapshot 不能由候选抓取器刷新；请先审查并更新 vendor/sources.lock.json",
        )
        return
    reference_path = source.get("path")
    if (
        not isinstance(reference_path, str)
        or not reference_path
        or len(reference_path) > MAX_PATH_CHARS
        or "\x00" in reference_path
        or "\\" in reference_path
        or not reference_path.startswith("vendor/upstream/reference/")
        or any(part in {".", ".."} for part in Path(reference_path).parts)
    ):
        sink.fail(lock_id, url, "lockfile reference path is invalid")
        return
    sink.entries["reference_only"] = {
        "lock_id": lock_id,
        "url": url,
        "commit": commit,
        "license": source.get("license"),
        "license_sha256": source.get("license_sha256"),
        "path": reference_path,
    }
    sink.entries["counts"]["files"] = 0


def fetch_teorth(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """teorth/erdosproblems：只记录固定 reference，不克隆未固定 HEAD。"""
    record_locked_reference(sink, "teorth-erdosproblems", refresh=refresh)


def fetch_mse(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """math.stackexchange 的 open-problem 标签全量（SE API）。"""
    page = 1
    while True:
        url = ("https://api.stackexchange.com/2.3/questions"
               f"?tagged=open-problem&site=math&pagesize=100&page={page}&filter=withbody")
        name = f"api/questions-page-{page:02d}.json"
        body = download(sink, fetcher, name, url, refresh=refresh, max_bytes=25_000_000)
        if body is None:
            return
        data = loads_json(body)
        if not data.get("has_more"):
            break
        page += 1
        if page > 10:
            sink.fail("api", url, "超过 10 页上限")
            break


def fetch_multilingual_conjectures(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """西/法/意/俄维基「猜想」分类：成员列表 + 摘要。"""
    sites = {
        "es": ("es.wikipedia.org", "Categoría:Conjeturas matemáticas"),
        "fr": ("fr.wikipedia.org", "Catégorie:Conjecture"),
        "it": ("it.wikipedia.org", "Categoria:Congetture matematiche"),
        "ru": ("ru.wikipedia.org", "Категория:Математические гипотезы"),
    }
    for slug, (host, cat) in sites.items():
        url = (f"https://{host}/w/api.php?action=query&list=categorymembers"
               f"&cmtitle={urllib.parse.quote(cat)}&cmlimit=500&format=json&formatversion=2")
        body = download(sink, fetcher, f"members/{slug}.json", url, refresh=refresh)
        if body is None:
            continue
        data = loads_json(body)
        members = bounded_items(
            [m["title"] for m in data.get("query", {}).get("categorymembers", [])],
            "多语言维基猜想成员",
        )
        if any(not isinstance(title, str) or len(title) > MAX_PATH_CHARS for title in members):
            raise RuntimeError("多语言维基猜想成员无效")
        for start in range(0, len(members), 20):
            batch = members[start:start + 20]
            titles = "|".join(urllib.parse.quote(t, safe="") for t in batch)
            url = (f"https://{host}/w/api.php?action=query&prop=extracts"
                   f"&exintro&explaintext&redirects=1&titles={titles}&format=json&formatversion=2&exlimit=20")
            download(sink, fetcher, f"extracts/{slug}-{start // 20:02d}.json", url, refresh=refresh)


def fetch_multilingual_lists(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """多语言维基「未解决的数学问题」主清单页（MediaWiki API 原始 JSON）。"""
    pages = {
        "de": ("de.wikipedia.org", "Ungelöste Probleme der Mathematik"),
        "fr": ("fr.wikipedia.org", "Problèmes non résolus en mathématiques"),
        "es": ("es.wikipedia.org", "Problemas no resueltos de la matemática"),
        "ru": ("ru.wikipedia.org", "Нерешённые проблемы математики"),
        "ja": ("ja.wikipedia.org", "数学上の未解決問題"),
    }
    for slug, (host, page) in pages.items():
        url = (f"https://{host}/w/api.php?action=parse&page={urllib.parse.quote(page)}"
               "&prop=text%7Csections&format=json&formatversion=2&redirects=1")
        download(sink, fetcher, f"{slug}-unsolved-math.json", url, refresh=refresh)


def fetch_oeis_extra(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """OEIS wiki 更多问题相关分类页 + Open_problems 分类下的问题条目页。"""
    for cat in ("Conjectures", "Open_problems"):
        download(sink, fetcher, f"Category_{cat}.html", f"https://oeis.org/wiki/Category:{cat}", refresh=refresh)
    body = RAW / "oeis_extra" / "Category_Open_problems.html"
    if not body.is_file():
        return
    text = read_bounded_file(body, DEFAULT_MAX_RESPONSE_BYTES).decode("utf-8", errors="replace")
    for href, title in bounded_values(
        re.findall(r'<a href="/wiki/([^"]+)"[^>]*title="([^"]+)"', text),
        "OEIS open-problems links",
    ):
        if href.startswith(("Help:", "Special:", "OeisWiki:", "The_OEIS")):
            continue
        if href.startswith("Category:"):
            if href in ("Category:Open_problems", "Category:Conjectures", "Category:Unsolved_problems", "Category:Articles_containing_conjectures", "Category:Conjectured_sequences"):
                continue
            name = "categories/" + href.removeprefix("Category:").replace("/", "_")
        else:
            name = "pages/" + href.replace("/", "_")
        if not (RAW / "oeis_extra" / name).is_file() or refresh:
            download(sink, fetcher, name, "https://oeis.org/wiki/" + href, refresh=refresh)


def fetch_primepages(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """PrimePages 术语表：Open Problems 条目页。"""
    download(sink, fetcher, "glossary-open-problems.html",
             "https://t5k.org/glossary/page.php?sort=OpenProblems", refresh=refresh)


def fetch_wiki_subsets(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """en 维基「部分解决」「ABC 猜想」子分类：成员 + 摘要（部分解决仍是开放问题）。"""
    cats = {
        "partially-resolved": "Category:Partially resolved conjectures",
        "abc": "Category:Abc conjecture",
    }
    for slug, cat in cats.items():
        url = ("https://en.wikipedia.org/w/api.php?action=query&list=categorymembers"
               f"&cmtitle={urllib.parse.quote(cat)}&cmlimit=500&format=json&formatversion=2")
        body = download(sink, fetcher, f"members/{slug}.json", url, refresh=refresh)
        if body is None:
            continue
        data = loads_json(body)
        members = bounded_items(
            [m["title"] for m in data.get("query", {}).get("categorymembers", [])],
            "维基子分类成员",
        )
        if any(not isinstance(title, str) or len(title) > MAX_PATH_CHARS for title in members):
            raise RuntimeError("维基子分类成员无效")
        for start in range(0, len(members), 20):
            batch = members[start:start + 20]
            titles = "|".join(urllib.parse.quote(t, safe="") for t in batch)
            url = ("https://en.wikipedia.org/w/api.php?action=query&prop=extracts"
                   f"&exintro&explaintext&redirects=1&titles={titles}&format=json&formatversion=2&exlimit=20")
            download(sink, fetcher, f"extracts/{slug}-{start // 20:02d}.json", url, refresh=refresh)


def fetch_wiki_more_lists(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """领域未解清单（en Lists of unsolved problems 分类成员中未拉过的）+ it 主清单。"""
    # en 分类成员（先拿列表）
    url = ("https://en.wikipedia.org/w/api.php?action=query&list=categorymembers"
           "&cmtitle=Category:Lists_of_unsolved_problems&cmlimit=200&format=json&formatversion=2")
    body = download(sink, fetcher, "members/lists-of-unsolved.json", url, refresh=refresh)
    if body is not None:
        data = loads_json(body)
        have = {"computer science", "economics", "neuroscience", "physics", "statistics", "mathematics"}
        category_members = bounded_items(
            data.get("query", {}).get("categorymembers", []),
            "未解问题列表成员",
        )
        for m in category_members:
            if not isinstance(m, dict) or not isinstance(m.get("title"), str):
                raise RuntimeError("未解问题列表成员无效")
            title = m["title"]
            if any(h in title for h in have):
                continue
            name = "pages/" + title.replace(" ", "_") + ".json"
            url2 = ("https://en.wikipedia.org/w/api.php?action=parse&page="
                    + urllib.parse.quote(title) + "&prop=text%7Csections&format=json&formatversion=2&redirects=1")
            download(sink, fetcher, name, url2, refresh=refresh)
    # it 主清单
    download(sink, fetcher, "it-unsolved-math.json",
             "https://it.wikipedia.org/w/api.php?action=parse&page="
             + urllib.parse.quote("Problemi irrisolti in matematica")
             + "&prop=text%7Csections&format=json&formatversion=2&redirects=1", refresh=refresh)


def fetch_arxiv_index(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """arXiv 元数据发现索引：标题含 open problems 的论文清单（只存元数据，不存全文）。"""
    query = 'ti:"open problems"'
    for start in range(0, 600, 100):
        url = ("https://export.arxiv.org/api/query?search_query="
               + urllib.parse.quote(query) + f"&start={start}&max_results=100&sortBy=submittedDate&sortOrder=descending")
        body = download(sink, fetcher, f"title-{start // 100:02d}.xml", url, refresh=refresh, max_bytes=5_000_000)
        if body is None:
            break
        if b"<entry>" not in body:
            break


def fetch_oeis_articles(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """OEIS wiki「含猜想文章」分类页及其成员（问题条目）。"""
    body = download(sink, fetcher, "Category_Articles_containing_conjectures.html",
                    "https://oeis.org/wiki/Category:Articles_containing_conjectures", refresh=refresh)
    if body is None:
        return
    text = body.decode("utf-8", errors="replace")
    for href, title in bounded_values(
        re.findall(r'<a href="/wiki/([^"]+)"[^>]*title="([^"]+)"', text),
        "OEIS article links",
    ):
        if href.startswith(("Category:", "Help:", "Special:", "OeisWiki:", "The_OEIS", "Template:", "Main_Page")):
            continue
        name = "pages/" + href.replace("/", "_")
        if not (RAW / "oeis_articles" / name).is_file() or refresh:
            download(sink, fetcher, name, "https://oeis.org/wiki/" + href, refresh=refresh)


def fetch_arxiv_unsolved(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """arXiv 元数据：标题含 unsolved problems（45 条）。"""
    query = 'ti:"unsolved problems"'
    url = ("https://export.arxiv.org/api/query?search_query="
           + urllib.parse.quote(query) + "&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending")
    download(sink, fetcher, "title-unsolved-00.xml", url, refresh=refresh, max_bytes=5_000_000)


def fetch_unsolvedproblems(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """UnsolvedProblems.org（业余站，C 类下限但归档补齐）：首页 + index_files/* 全量。"""
    body = download(sink, fetcher, "index.html", "https://unsolvedproblems.org/index.htm", refresh=refresh, max_bytes=3_000_000)
    if body is None:
        return
    text = body.decode("latin-1", errors="replace")
    links = bounded_values(sorted(set(re.findall(r'href="(index_files/[^"]+)"', text))), "UnsolvedProblems links")
    for link in links:
        name = link.replace("/", "_")
        if not (RAW / "unsolvedproblems" / name).is_file() or refresh:
            download(sink, fetcher, name, "https://unsolvedproblems.org/" + link, refresh=refresh, max_bytes=3_000_000)


def fetch_vibemathed(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """VibeMathed：只读取带明确许可声明的网站 dataset API。"""
    download(
        sink,
        fetcher,
        "dataset-latest.json",
        "https://vibemathed.com/api/dataset",
        refresh=refresh,
        max_bytes=30_000_000,
    )


def fetch_wikipedia_categories(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """Wikipedia 问题/猜想分类深度：全部成员列表 + 每条目摘要（exintro）。"""
    categories = {
        "unsolved-in-math": "Category:Unsolved problems in mathematics",
        "conjectures": "Category:Conjectures",
        "unsolved-in-cs": "Category:Unsolved problems in computer science",
        "unsolved-in-physics": "Category:Unsolved problems in physics",
        "prime-conjectures": "Category:Conjectures about prime numbers",
    }
    all_members: list[str] = []
    for slug, cat in categories.items():
        cmcontinue = ""
        members: list[str] = []
        page_count = 0
        while True:
            page_count += 1
            if page_count > MAX_PAGES:
                raise RuntimeError("维基问题分类分页超过上限")
            url = ("https://en.wikipedia.org/w/api.php?action=query&list=categorymembers"
                   f"&cmtitle={urllib.parse.quote(cat)}&cmlimit=500&format=json&formatversion=2"
                   + (f"&cmcontinue={urllib.parse.quote(cmcontinue)}" if cmcontinue else ""))
            body = download(sink, fetcher, f"members/{slug}.json", url, refresh=refresh)
            if body is None:
                break
            data = loads_json(body)
            members += [m["title"] for m in bounded_items(
                data.get("query", {}).get("categorymembers", []),
                "维基问题分类成员页",
            ) if isinstance(m, dict) and isinstance(m.get("title"), str)]
            if any(len(title) > MAX_PATH_CHARS for title in members) or len(members) > MAX_DISCOVERED_ITEMS:
                raise RuntimeError("维基问题分类成员超过发现预算")
            cmcontinue = data.get("continue", {}).get("cmcontinue", "")
            if not cmcontinue:
                break
        # 去重追加（同名成员已拉过就跳过）
        seen = set(all_members)
        fresh = [t for t in members if t not in seen]
        all_members += fresh
        if len(all_members) > MAX_DISCOVERED_ITEMS:
            raise RuntimeError("维基问题分类总成员超过发现预算")
        if fresh:
            for start in range(0, len(fresh), 20):
                batch = fresh[start:start + 20]
                titles = "|".join(urllib.parse.quote(t, safe="") for t in batch)
                url = ("https://en.wikipedia.org/w/api.php?action=query&prop=extracts"
                       f"&exintro&explaintext&redirects=1&titles={titles}&format=json&formatversion=2&exlimit=20")
                sink.entries["counts"]["batch"] = sink.entries["counts"].get("batch", 0) + 1
                download(sink, fetcher, f"extracts/{slug}-{start // 20:02d}.json", url, refresh=refresh)
    summary = (json.dumps(
        {"categories": categories, "member_count": len(all_members)},
        ensure_ascii=False,
        sort_keys=True,
    ) + "\n").encode("utf-8")
    summary_path = safe_raw_artifact_path("wikipedia_categories", "summary.json")
    if summary_path.is_file() and not refresh:
        if read_bounded_file(summary_path, DEFAULT_MAX_RESPONSE_BYTES) != summary:
            sink.fail("summary.json", "generated://wikipedia_categories", "缓存摘要漂移")
    else:
        sink.save("summary.json", "generated://wikipedia_categories", summary)


def fetch_wikipedia_conjectures(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    """Wikipedia「List of conjectures」：MediaWiki API 原始 JSON（与问题库 wikipedia 管道同源）。"""
    for name, url in (
        ("list-of-conjectures.json",
         "https://en.wikipedia.org/w/api.php?action=parse&page=List+of+conjectures&prop=text%7Csections&format=json&formatversion=2&redirects=1"),
        ("revision.json",
         "https://en.wikipedia.org/w/api.php?action=query&titles=List+of+conjectures&prop=revisions&rvprop=ids%7Ctimestamp%7Csha1&format=json&formatversion=2&redirects=1"),
    ):
        download(sink, fetcher, name, url, refresh=refresh)


def fetch_mo_conjectures(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    page = 1
    while True:
        url = (
            "https://api.stackexchange.com/2.3/questions"
            f"?tagged=conjectures&site=mathoverflow&pagesize=100&page={page}&filter=withbody"
        )
        name = f"api/questions-page-{page:02d}.json"
        body = download(sink, fetcher, name, url, refresh=refresh, max_bytes=25_000_000)
        if body is None:
            return
        data = loads_json(body)
        if not data.get("has_more"):
            break
        page += 1
        if page > 10:
            sink.fail("api", url, "超过 10 页上限")
            break


def fetch_fmop(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    download(sink, fetcher, "open_problems_data.zip", "https://epoch.ai/data/open_problems_data.zip", refresh=refresh, max_bytes=5_000_000)
    for name, url in (
        ("overview.html", "https://epoch.ai/frontiermath/open-problems/about/overview"),
        ("faq.html", "https://epoch.ai/frontiermath/open-problems/about/faq"),
        ("index.html", "https://epoch.ai/frontiermath/open-problems"),
    ):
        download(sink, fetcher, name, url, refresh=refresh)


def fetch_polymath_archive(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    import urllib.parse as _up

    pages = ("Main_Page", "Unsolved_problems", "Other_proposed_projects")
    for page in pages:
        target = "https://michaelnielsen.org/polymath/index.php?" + _up.urlencode({"title": page})
        avail_url = "https://archive.org/wayback/available?" + _up.urlencode({"url": target})
        body = download(sink, fetcher, f"wayback-{page}.html", avail_url, refresh=refresh)
        if body is None:
            continue
        data = loads_json(body)
        snap = data.get("archived_snapshots", {}).get("closest", {})
        snap_url = snap.get("url")
        if not snap_url or snap.get("status") != "200":
            sink.fail(f"wayback-{page}", target, "无可用 200 快照")
            continue
        if not (RAW / "polymath_archive" / f"{page}.html").is_file() or refresh:
            body2 = download(sink, fetcher, f"{page}.html", snap_url, refresh=refresh, max_bytes=15_000_000)


def fetch_scottish(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    base = "https://old.wmi.uni.wroc.pl/sites/default/files/"
    for name, path in (
        ("nks-1.pdf", "nks/NKS.1.pdf"),
        ("nks-2.pdf", "nks/NKS.2.pdf"),
        ("nks-3.pdf", "nks/NKS.3.pdf"),
        ("scottish-book-1.pdf", "upload_attach/ksiega_szkocka_1.pdf"),
        ("scottish-book-2.pdf", "upload_attach/ksiega_szkocka_2.pdf"),
        ("scottish-book-3.pdf", "upload_attach/ksiega_szkocka_3.pdf"),
    ):
        download(sink, fetcher, name, base + path, refresh=refresh)


def fetch_oeis_categories(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    body = download(sink, fetcher, "Category_Problems.html", "https://oeis.org/wiki/Category:Problems", refresh=refresh)
    if body is None:
        return
    text = body.decode("utf-8", errors="replace")
    subcats = bounded_values(sorted(
        set(re.findall(r'href="/wiki/Category:([^"]+)"', text))
    ), "OEIS category links")
    for cat in subcats:
        if cat in ("Problems", "Number_theory", "Mathematical_term"):
            continue
        # href 内已是编码形式；URL 直接使用原值避免二次编码，仅文件名做一次 quote
        name = "categories/Category_" + urllib.parse.quote(cat.replace(" ", "_")) + ".html"
        download(sink, fetcher, name, "https://oeis.org/wiki/Category:" + cat, refresh=refresh)


def fetch_clay(fetcher: Fetcher, sink: Sink, *, refresh: bool) -> None:
    body = download(sink, fetcher, "unsolved.html", "https://www.claymath.org/problem/unsolved/", refresh=refresh)
    if body is None:
        return
    text = body.decode("utf-8", errors="replace")
    links = bounded_values(sorted(set(re.findall(r'href="(https://www\.claymath\.org/[^"]+)"', text))), "Clay problem links")
    for url in links:
        path = urllib.parse.urlparse(url).path.strip("/").replace("/", "_")
        name = f"pages/{path or 'index'}.html"
        if not (RAW / "clay" / name).is_file() or refresh:
            download(sink, fetcher, name, url, refresh=refresh)


def fetch_formal_conjectures(sink: Sink, *, refresh: bool) -> None:
    """formal-conjectures：只记录固定 reference，不克隆未固定 HEAD。"""
    record_locked_reference(sink, "formal-conjectures", refresh=refresh)


# ---------------------------------------------------------------------------

# This source is intentionally registry-only: it is a discovery pointer, not
# a fetcher, parser, or admitted candidate source.
REGISTRY_ONLY_SOURCES = {"awesome_solved_index"}

SOURCES: dict[str, Any] = {
    "theoremdb": fetch_theoremdb,
    "openlogicproblems": fetch_openlogicproblems,
    "topp": fetch_topp,
    "openquantum": fetch_openquantum,
    "ucsd": fetch_ucsd,
    "aim": fetch_aim,
    "pdfs": lambda f, s, refresh=False: fetch_pdfs(
        f, s,
        refresh=refresh,
        items={
            "kourovka-21tkt.pdf": "https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/07/21tkt.pdf",
            "kourovka-21upd.pdf": "https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/07/21upd.pdf",
            "green-100-open-problems.pdf": "https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf",
            "kyoto-lowdim-topology-2024.pdf": "https://www.kurims.kyoto-u.ac.jp/~ildt/prob24.pdf",
        },
    ),
    "kirby": fetch_kirby,
    "mathoverflow": fetch_mathoverflow,
    "polymath": fetch_polymath,
    "oeis_wiki": fetch_oeis_wiki,
    "amr": fetch_amr,
    "formal_conjectures": lambda f, s, refresh=False: fetch_formal_conjectures(s, refresh=refresh),
    "wikipedia_conjectures": fetch_wikipedia_conjectures,
    "mo_conjectures": fetch_mo_conjectures,
    "fmop": fetch_fmop,
    "polymath_archive": fetch_polymath_archive,
    "scottish": fetch_scottish,
    "oeis_categories": fetch_oeis_categories,
    "clay": fetch_clay,
    "wikipedia_more": fetch_wikipedia_more,
    "oeis_unsolved": fetch_oeis_unsolved,
    "planetmath": fetch_planetmath,
    "wikipedia_categories": fetch_wikipedia_categories,
    "zh_conjectures": fetch_zh_conjectures,
    "teorth": fetch_teorth,
    "mse": fetch_mse,
    "multilingual_conjectures": fetch_multilingual_conjectures,
    "multilingual_lists": fetch_multilingual_lists,
    "oeis_extra": fetch_oeis_extra,
    "primepages": fetch_primepages,
    "wiki_subsets": fetch_wiki_subsets,
    "wiki_more_lists": fetch_wiki_more_lists,
    "arxiv_index": fetch_arxiv_index,
    "oeis_articles": fetch_oeis_articles,
    "arxiv_unsolved": fetch_arxiv_unsolved,
    "unsolvedproblems": fetch_unsolvedproblems,
    "vibemathed": fetch_vibemathed,
}


def source_coverage_errors() -> list[str]:
    try:
        registry = loads_json(read_bounded_file(CANDIDATE_REGISTRY, 5_000_000))
        if not isinstance(registry, dict) or not isinstance(registry.get("sources"), list):
            raise ValueError("候选来源注册表结构无效")
        if len(registry["sources"]) > MAX_INVENTORY_ENTRIES:
            raise ValueError("候选来源注册表条目超过预算")
        registry_ids_list = [
            item["source_id"]
            for item in registry["sources"]
            if isinstance(item, dict) and isinstance(item.get("source_id"), str)
        ]
        if len(registry_ids_list) != len(registry["sources"]):
            raise ValueError("候选来源注册表包含非法条目")
        registry_ids = set(registry_ids_list)
        if len(registry_ids) != len(registry_ids_list):
            raise ValueError("候选来源注册表包含重复 source_id")
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return [f"无法读取候选来源注册表：{exc}"]
    missing = registry_ids - set(SOURCES)
    unexpected = set(SOURCES) - registry_ids
    if missing != REGISTRY_ONLY_SOURCES or unexpected:
        return [
            "候选来源抓取器/注册表不一致："
            f"missing={sorted(missing)} unexpected={sorted(unexpected)} "
            f"registry_only_allowlist={sorted(REGISTRY_ONLY_SOURCES)}"
        ]
    return []


def run_locked(args: argparse.Namespace) -> int:
    inventory = read_inventory()
    inventory["schema_version"] = "candidate-inventory.v1"
    fetcher = Fetcher(timeout=args.timeout, delay=args.delay, retries=args.retries)
    failures: list[dict[str, Any]] = []
    selected = [args.only] if args.only else list(SOURCES)
    for source in selected:
        if source not in SOURCES:
            print(f"未知来源：{source}（可用：{', '.join(SOURCES)}）", file=sys.stderr)
            return 1
        print(f"== 来源：{source} ==", flush=True)
        sink = Sink(inventory, source)
        try:
            SOURCES[source](fetcher, sink, refresh=args.refresh)
        except Exception as exc:  # noqa: BLE001 - record failure, continue auditing other selected sources
            sink.fail("__source__", source, f"{type(exc).__name__}: {exc}")
        failures.extend(sink.failures)
        done = sink.entries["counts"].get("files", 0)
        print(f"  完成：{done} 个文件；失败 {len(sink.failures)}", flush=True)
    prior = {json.dumps(item, sort_keys=True) for item in inventory.get("failures", [])}
    merged = list(inventory.get("failures", []))
    for item in failures:
        key = json.dumps(item, sort_keys=True)
        if key not in prior:
            merged.append(item)
            prior.add(key)
    if len(merged) > MAX_INVENTORY_ENTRIES:
        raise RuntimeError("candidate inventory failure count exceeds budget")
    inventory["failures"] = merged
    inventory["generated_at"] = utc_now()
    write_inventory(inventory)
    try:
        inventory_display = INVENTORY_PATH.relative_to(ROOT)
    except ValueError:
        inventory_display = INVENTORY_PATH
    print(f"\n全部完成：inventory -> {inventory_display}；失败 {len(failures)} 项")
    for item in failures:
        print("  失败：", item["source"], item["name"], item["reason"], item["url"])
    return 0 if not failures or args.allow_partial else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="批量下载候选数学问题库。")
    parser.add_argument("--delay", type=float, default=0.3)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--retries", type=int, default=4)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--only", default=None, help="只跑指定来源")
    parser.add_argument("--allow-partial", action="store_true", help="允许来源失败但仍返回成功；默认 fail-closed")
    args = parser.parse_args()
    if not math.isfinite(args.delay) or args.delay < 0 or args.delay > MAX_DELAY_SECONDS:
        parser.error(f"--delay 必须在 [0, {MAX_DELAY_SECONDS}] 内")
    if not math.isfinite(args.timeout) or args.timeout <= 0 or args.timeout > MAX_TIMEOUT_SECONDS:
        parser.error(f"--timeout 必须在 (0, {MAX_TIMEOUT_SECONDS}] 内")
    if args.retries <= 0 or args.retries > MAX_RETRIES:
        parser.error(f"--retries 必须在 [1, {MAX_RETRIES}] 内")
    if fcntl is None:
        parser.error("当前平台不支持 fail-closed 文件锁")
    if args.only is None:
        coverage_errors = source_coverage_errors()
        if coverage_errors:
            for error in coverage_errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
    try:
        assert_safe_raw_root()
        RAW.mkdir(parents=True, exist_ok=True)
        assert_safe_raw_root()
    except OSError as exc:
        parser.error(f"候选 raw 根目录不可用：{exc}")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        parser.error("当前平台不支持安全候选抓取锁")
    try:
        lock_descriptor = os.open(
            LOCK_PATH,
            os.O_WRONLY | os.O_CREAT | nofollow,
            0o600,
        )
    except OSError as exc:
        parser.error(f"候选抓取锁不可用：{exc}")
    try:
        fcntl.flock(lock_descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        os.close(lock_descriptor)
        print("候选问题抓取器已有实例运行；拒绝并发写 inventory。", file=sys.stderr)
        return 1
    except OSError:
        os.close(lock_descriptor)
        raise
    try:
        return run_locked(args)
    finally:
        os.close(lock_descriptor)


if __name__ == "__main__":
    raise SystemExit(main())