#!/usr/bin/env python3
# 抓取 Erdős Problems（https://www.erdosproblems.com/）的公开问题目录并重建本地问题库。
#
# 数据边界（与 problem-library/AGENTS.md 一致）：
#   - 全部问题页 /1..N（编号连续、服务端渲染）作为主记录来源；
#   - /bibs/{key} 保存完整书目条目；/lists（Erdős 问题列表）经
#     /search_bib/{key}?sources_only=1 建立问题归属（problem_sets）；
#   - /tags 与 /prizes 提供对账证据；/faq、/definitions 等规范页仅留快照；
#   - 不抓取论坛评论、用户资料、点赞反应或登录后内容。
#
# 授权：robots.txt 声明 User-agent: * 允许全站；Content-Signal
#   search=yes, ai-train=no, use=reference。本抓取器以 reference 用途
#   保存公开问题陈述与归属，不把内容用于 AI 训练。
#
# 运行：python3 scripts/fetch_erdosproblems.py [crawl|build|all]
#   crawl —— 网络抓取（复用已存在缓存，--refresh 强制重取）
#   build —— 仅从本地原始快照重算记录、索引与 manifest（无网络）
#   all   —— crawl + build（默认）
# 依赖：Python 3、beautifulsoup4、lxml 与可访问 erdosproblems.com 的网络。

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import time
import urllib.parse
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    from bs4 import BeautifulSoup
except ImportError as exc:  # pragma: no cover - 由启动环境决定
    raise SystemExit("缺少解析依赖。请安装 requirements-problem-library.txt 后重试。") from exc


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "problem-library"
RAW = LIBRARY / "raw" / "erdosproblems"
RAW_PROBLEMS = RAW / "problems"
RAW_BIBS = RAW / "bibs"
RAW_LISTS = RAW / "lists"
RAW_TAGS = RAW / "tags"
RAW_AUX = RAW / "aux"
DISCOVERY_PATH = RAW / "discovery.json"
STATUS_INVENTORY_PATH = RAW / "status-inventory.json"
GAPS_PATH = RAW / "gaps.json"
LISTS_INDEX_PATH = RAW_LISTS / "lists-index.json"

RECORDS_PATH = LIBRARY / "records" / "problems.jsonl"
MANIFEST_PATH = LIBRARY / "manifest.json"
CATALOG_PATH = LIBRARY / "indexes" / "catalog.json"
BY_SOURCE_PATH = LIBRARY / "indexes" / "by-source.json"
BY_CATEGORY_PATH = LIBRARY / "indexes" / "by-category.json"

ERDOS_URL = "https://www.erdosproblems.com"
# 抓取前实测（2026-08-31）：/1218..5000 全部为无内容页，编号 1..1217 连续。
# 爬取器仍以连续缺失探测尾部，避免把探测值当死事实。
KNOWN_LAST = 1217
TAIL_PROBE_MIN = 30  # 尾部连续缺失达到该值才认为枚举结束
SCHEMA_VERSION = "1.0.0"
MAX_PROBLEM_SCAN = 100_000
MAX_REFERENCE_KEYS = 100_000
MAX_LIST_ENTRIES = 100_000
MAX_TAG_ENTRIES = 100_000
MAX_COMPONENT_CHARS = 256


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"JSON contains non-portable constant: {value}")


def safe_component(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or len(value) > MAX_COMPONENT_CHARS:
        raise ValueError(f"{label} 无效或过长")
    path = Path(value)
    if len(path.parts) != 1 or value in {".", ".."} or "/" in value or "\\" in value or "\x00" in value:
        raise ValueError(f"{label} 不能包含路径分隔符")
    return value


def load_fetcher_module() -> Any:
    """复用 scripts/fetch_problem_library.py 的 Fetcher 与公共工具，不改动共享文件。"""
    path = ROOT / "scripts" / "fetch_problem_library.py"
    spec = importlib.util.spec_from_file_location("fetch_problem_library", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载基础抓取器：{path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_fetcher_module()
Fetcher = BASE.Fetcher
cached_fetch = BASE.cached_fetch
write_atomic = BASE.write_atomic
write_json = BASE.write_json
utc_now = BASE.utc_now
file_timestamp = BASE.file_timestamp
sha256_bytes = BASE.sha256_bytes
read_bounded_bytes = BASE.read_bounded_bytes
normalize_space = BASE.normalize_space
MAX_RAW_BYTES = BASE.DEFAULT_MAX_RESPONSE_BYTES
MAX_RECORDS = BASE.MAX_RECORDS
MAX_RECORDS_BYTES = BASE.MAX_RECORDS_BYTES


def cached_fetch_with_429_backoff(fetcher: Fetcher, url: str, path: Path, *, refresh: bool, attempts: int = 5) -> tuple[bytes, dict[str, str], bool]:
    if not isinstance(attempts, int) or isinstance(attempts, bool) or attempts < 1 or attempts > 10:
        raise ValueError("429 retry attempts exceed budget")
    for attempt in range(attempts):
        try:
            return cached_fetch(fetcher, url, path, refresh=refresh)
        except RuntimeError as exc:
            if "429" in str(exc) and attempt < attempts - 1:
                wait = 45 * (attempt + 1)
                print(f"429 限流：等待 {wait}s 后重试 {url}", flush=True)
                time.sleep(wait)
                continue
            raise
    raise RuntimeError(f"429 重试耗尽：{url}")


# --------------------------------------------------------------------------
# 发现证据
# --------------------------------------------------------------------------

def probe_discovery(fetcher: Fetcher, *, refresh: bool) -> dict[str, Any]:
    if DISCOVERY_PATH.is_file() and not refresh:
        return json.loads(
            read_bounded_bytes(DISCOVERY_PATH, MAX_RAW_BYTES).decode("utf-8"),
            parse_constant=_reject_json_constant,
        )
    probe_urls = {
        "robots": f"{ERDOS_URL}/robots.txt",
        "sitemap": f"{ERDOS_URL}/sitemap.xml",
        "sitemap_txt": f"{ERDOS_URL}/sitemap.txt",
        "sitemap_index": f"{ERDOS_URL}/sitemap_index.xml",
        "sitemaps_alt": f"{ERDOS_URL}/sitemaps.xml",
    }
    probes = {name: fetcher.probe(url) for name, url in probe_urls.items()}
    robots = probes["robots"]
    signals: list[str] = []
    if robots.get("status") == 200:
        body = fetch_probe_body(fetcher, probe_urls["robots"])
        content_signal = re.search(r"^Content-Signal:\s*(.+)$", body, re.M)
        signals = [content_signal.group(1).strip()] if content_signal else []
    aux = {
        "homepage": {name: f"{ERDOS_URL}/{name}" for name in ("", "faq", "tags", "prizes", "lists", "definitions", "latex/1", "history/1")},
    }
    discovery = {
        "observed_at": utc_now(),
        "site": ERDOS_URL,
        "probes": probes,
        "robots_content_signals": signals,
        "enumeration_note": (
            "问题编号由 /1 连续递增；页面是否真实问题按是否存在 .problem-box 判定"
            "（不存在的编号返回 HTTP 200 的 'No results' 页）。"
        ),
        "aux_snapshots": aux,
    }
    write_json(DISCOVERY_PATH, discovery)
    return discovery


def fetch_probe_body(fetcher: Fetcher, url: str) -> str:
    body, _headers = fetcher.fetch(url)
    return body.decode("utf-8", errors="replace")


def crawl_aux_pages(fetcher: Fetcher, *, refresh: bool) -> None:
    for name, path_part in (
        ("homepage", ""),
        ("faq", "faq"),
        ("tags", "tags"),
        ("prizes", "prizes"),
        ("lists", "lists"),
        ("definitions", "definitions"),
        ("latex-sample", "latex/1"),
        ("history-sample", "history/1"),
    ):
        raw_path = RAW_AUX / f"{name}.html"
        cached_fetch(
            fetcher,
            f"{ERDOS_URL}/{path_part}".rstrip("/") or ERDOS_URL,
            raw_path,
            refresh=refresh,
        )


# --------------------------------------------------------------------------
# 问题页
# --------------------------------------------------------------------------

def is_real_problem(soup: BeautifulSoup) -> bool:
    return soup.select_one(".problem-box") is not None


def parse_problem_page(raw_path: Path) -> dict[str, Any]:
    """从原始 HTML 快照解析一条 erdosproblems 问题记录。"""
    soup = BeautifulSoup(read_bounded_bytes(raw_path, MAX_RAW_BYTES), "lxml")
    if not is_real_problem(soup):
        raise ValueError(f"不是真实问题页：{raw_path}")
    raw_path = Path(raw_path).resolve()
    number_text = raw_path.stem
    number = int(number_text.lstrip("0") or "0")
    box = soup.select_one(".problem-box")
    problem_text = box.select_one(".problem-text")
    status = (problem_text.get("id") or "").strip()
    if not status:
        raise ValueError(f"缺少状态 id：{raw_path}")
    prize_node = problem_text.select_one("#prize")
    prize_text = prize_node.get_text(" ", strip=True) if prize_node else ""
    prize = None
    prize_match = re.search(r"-\s*\$([\d,]+)", prize_text)
    if prize_match:
        prize = int(prize_match.group(1).replace(",", ""))
    tooltip = ""
    if prize_node:
        tip = prize_node.select_one(".tooltiptext")
        tooltip = normalize_space(tip.get_text(" ", strip=True)) if tip else ""
    content_node = problem_text.select_one("#content")
    if content_node is None:
        raise ValueError(f"缺少陈述内容：#content 不存在：{raw_path}")
    statement = normalize_space(content_node.get_text(" ", strip=True))
    if not statement:
        raise ValueError(f"空陈述：{raw_path}")
    problem_id_node = problem_text.select_one("#problem_id")
    ref_keys: list[str] = []
    problem_refs: list[int] = []
    if problem_id_node is not None:
        for link in problem_id_node.select("a[href]"):
            label = normalize_space(link.get_text(" ", strip=True))
            href = link.get("href", "")
            if href.startswith("#bib-container"):
                key = label.strip("[]").split(",")[0].strip()
                if key:
                    ref_keys.append(key)
            elif re.fullmatch(r"\[\d+\]", label):
                try:
                    problem_refs.append(int(label.strip("[]")))
                except ValueError:
                    pass
    tags_node = problem_text.select_one("#tags")
    tags: list[str] = []
    if tags_node is not None:
        tags = [
            normalize_space(link.get_text(" ", strip=True))
            for link in tags_node.select("a[href^='/tags/']")
            if normalize_space(link.get_text(" ", strip=True))
        ]
        if not tags:
            tags = [t for t in (normalize_space(tags_node.get_text(" ", strip=True)).split(" | ")) if t]
    remarks_parts: list[str] = []
    for node in box.select("div.problem-additional-text"):
        text = normalize_space(node.get_text(" ", strip=True))
        if text and not re.match(r"^(Previous|Next|Random)\b", text):
            remarks_parts.append(text)
    remarks = "\n".join(remarks_parts)
    additional_bib_keys: list[str] = []
    for link in box.select('a[href^="#bib-container"]'):
        label = normalize_space(link.get_text(" ", strip=True))
        key = label.strip("[]").split(",")[0].strip()
        if key:
            additional_bib_keys.append(key)
    all_ref_keys: list[str] = []
    for key in ref_keys + additional_bib_keys:
        if key not in all_ref_keys:
            all_ref_keys.append(key)
    last_edited = None
    formalised_status = None
    lean_url = None
    oeis_links: list[str] = []
    for row in box.select(".problem-info-data-row"):
        text = normalize_space(row.get_text(" ", strip=True))
        if text.startswith("Formalised statement?"):
            formalised_status = text.split("?", 1)[1].strip()
            lean = row.select_one("a[href]")
            if lean is not None:
                lean_url = lean.get("href")
        if text.startswith("OEIS"):
            href = row.select_one("a[href]")
            if href is not None:
                oeis_links.append(href.get("href"))
    for small in box.select(".problem-info-small"):
        text = normalize_space(small.get_text(" ", strip=True))
        match = re.search(r"This page was last edited ([^.]+)\.", text)
        if match:
            last_edited = match.group(0)
    related_urls: list[str] = []
    for link in box.select("a[href]"):
        href = link.get("href", "")
        if re.match(r"^https?://", href):
            if href not in related_urls:
                related_urls.append(href)
    related_urls = [url for url in related_urls if url and url != "https://github.com/teorth/erdosproblems"]
    if lean_url and lean_url not in related_urls:
        related_urls.append(lean_url)
    for url in oeis_links:
        if url and url not in related_urls:
            related_urls.append(url)
    title = erdos_title(number, statement)
    identity = f"{number}\x1f{status}\x1f{statement}".encode("utf-8")
    record_id = f"erdosproblems-{hashlib.sha1(identity).hexdigest()[:16]}"
    return {
        "id": record_id,
        "source": "erdosproblems",
        "source_native_id": str(number),
        "source_order": number,
        "source_page": f"{ERDOS_URL}/{number}",
        "detail_url": f"{ERDOS_URL}/{number}",
        "record_scope": "problem_page",
        "title": title,
        "statement_excerpt": statement,
        "status": status,
        "difficulty": None,
        "prize": prize,
        "categories": tags,
        "problem_sets": [],
        "related_urls": related_urls,
        "source_revision": None,
        "retrieved_at": file_timestamp(raw_path),
        "license": {
            "name": "site robots.txt Content-Signal; no explicit license",
            "url": f"{ERDOS_URL}/robots.txt",
            "attribution": "Erdős Problems, Thomas Bloom and contributors (https://www.erdosproblems.com/)",
        },
        "_internal": {
            "status_tooltip": tooltip,
            "prize_text": prize_text,
            "remarks": remarks,
            "ref_keys": all_ref_keys,
            "problem_refs": problem_refs,
            "last_edited": last_edited,
            "formalised_status": formalised_status,
            "raw_file": str(raw_path.relative_to(ROOT)),
        },
    }


def erdos_title(number: int, statement: str) -> str:
    plain = statement.replace("$", " ").replace("\\[", " ").replace("\\]", " ")
    plain = re.sub(r"\s+", " ", plain).strip()
    if not plain:
        return f"Erdős problem #{number}"
    end = len(plain)
    for match in re.finditer(r"(?<=[a-zA-Z0-9\)\]])\.(?:\s+|$)", plain):
        if match.start() >= 40:
            end = match.end()
            break
    else:
        end = min(220, len(plain))
    title = plain[:end].strip().rstrip(".,;:")
    if len(title) < 20 and len(plain) > 20:
        title = plain[:220].strip().rstrip(".,;:")
    return title[:240] or f"Erdős problem #{number}"


def crawl_problems(fetcher: Fetcher, *, refresh: bool) -> dict[str, Any]:
    problems: list[dict[str, Any]] = []
    status_counter: Counter[str] = Counter()
    gaps: list[int] = []
    cache_hits = 0
    requests = 0
    consecutive_misses = 0
    last_problem = 0
    n = 1
    while True:
        raw_path = RAW_PROBLEMS / f"{n:04d}.html"
        body, _, from_cache = cached_fetch(fetcher, f"{ERDOS_URL}/{n}", raw_path, refresh=refresh)
        cache_hits += int(from_cache)
        requests += 1
        soup = BeautifulSoup(body, "lxml")
        if is_real_problem(soup):
            record = parse_problem_page(raw_path)
            problems.append(record)
            status_counter[record["status"]] += 1
            last_problem = n
            consecutive_misses = 0
        else:
            gaps.append(n)
            consecutive_misses += 1
            if n > KNOWN_LAST and consecutive_misses >= TAIL_PROBE_MIN:
                break
        n += 1
        if n % 100 == 1 and last_problem:
            print(f"Erdős 问题：已扫描到 /{n - 1}，最近真实问题 /{last_problem}，累计 {len(problems)} 条", flush=True)
        if n > MAX_PROBLEM_SCAN:
            raise RuntimeError(f"问题枚举超过上限 {MAX_PROBLEM_SCAN}，拒绝继续抓取。")
        if len(problems) > MAX_RECORDS:
            raise RuntimeError(f"问题记录超过上限 {MAX_RECORDS}，拒绝继续抓取。")
        if n > KNOWN_LAST + TAIL_PROBE_MIN and consecutive_misses >= TAIL_PROBE_MIN:
            break
    if not problems:
        raise RuntimeError("Erdős 问题枚举结果为空；站点结构可能已变化。")
    summary = {
        "problem_range": {"first": 1, "last": last_problem, "record_count": len(problems)},
        "gaps_within_range": [g for g in gaps if g <= last_problem],
        "tail_probe": {
            "start": last_problem + 1,
            "end": gaps[-1] if gaps else last_problem,
            "checked_after_last": (gaps[-1] - last_problem) if gaps else 0,
            "threshold": TAIL_PROBE_MIN,
        },
        "cache_hits": cache_hits,
        "requests": requests,
    }
    if len(problems) > MAX_RECORDS:
        raise RuntimeError(f"问题记录超过上限 {MAX_RECORDS}，拒绝写入。")
    write_json(STATUS_INVENTORY_PATH, {"status_counts": dict(sorted(status_counter.items()))})
    write_json(GAPS_PATH, {"gaps": gaps, "summary": summary})
    return {"problems": problems, "summary": summary, "status_counts": dict(sorted(status_counter.items()))}


# --------------------------------------------------------------------------
# 书目键与问题列表
# --------------------------------------------------------------------------

def crawl_bibs(fetcher: Fetcher, keys: list[str], *, refresh: bool) -> dict[str, Any]:
    if len(keys) > MAX_REFERENCE_KEYS:
        raise RuntimeError(f"书目键超过上限 {MAX_REFERENCE_KEYS}。")
    fetched: list[str] = []
    cache_hits = 0
    missing: list[str] = []
    for index, key in enumerate(keys, 1):
        key = safe_component(key, "书目键")
        raw_path = RAW_BIBS / f"{key}.html"
        if raw_path.is_file() and not refresh:
            body = read_bounded_bytes(raw_path, MAX_RAW_BYTES)
            from_cache = True
            cache_hits += int(from_cache)
        else:
            try:
                body, _, _ = cached_fetch(fetcher, f"{ERDOS_URL}/bibs/{key}", raw_path, refresh=refresh)
            except RuntimeError as exc:
                if "404" in str(exc):
                    missing.append(key)
                    if index % 200 == 0:
                        print(f"书目：已抓取 {index}/{len(keys)}（缺失 {len(missing)}）", flush=True)
                    continue
                raise
        soup = BeautifulSoup(body, "lxml")
        if soup.select_one(".bib") is None:
            missing.append(key)
            raw_path.unlink(missing_ok=True)
        else:
            fetched.append(key)
        if index % 200 == 0:
            print(f"书目：已抓取 {index}/{len(keys)}（缺失 {len(missing)}）", flush=True)
    return {"unique_keys": len(keys), "fetched": len(fetched), "missing": missing, "cache_hits": cache_hits}


def parse_lists_page() -> list[dict[str, Any]]:
    raw_path = RAW_AUX / "lists.html"
    soup = BeautifulSoup(read_bounded_bytes(raw_path, MAX_RAW_BYTES), "lxml")
    rows: list[dict[str, Any]] = []
    for row in soup.select("tr"):
        link = row.select_one('a[href^="/search_bib/"]')
        if link is None:
            continue
        href = link.get("href", "")
        match = re.search(r"/search_bib/([^?]+)", href)
        if not match:
            continue
        key = safe_component(match.group(1), "问题列表键")
        count_match = re.search(r"(\d+)\s+problems", normalize_space(link.get_text(" ", strip=True)))
        solved_match = re.search(r"(\d+)\s+solved", normalize_space(link.get_text(" ", strip=True)))
        title_node = row.select_one("th i")
        title = normalize_space(title_node.get_text(" ", strip=True)) if title_node else key
        meta = normalize_space(row.select_one("th").get_text(" | ", strip=True)) if row.select_one("th") else ""
        mr_match = re.search(r"MR\s*([\d]+)", normalize_space(row.get_text(" ", strip=True)))
        rows.append(
            {
                "key": key,
                "title": title,
                "declared_problem_count": int(count_match.group(1)) if count_match else None,
                "declared_solved_count": int(solved_match.group(1)) if solved_match else None,
                "meta": meta[:400],
                "mathscinet_mr": mr_match.group(1) if mr_match else None,
            }
        )
    return rows


def crawl_lists(fetcher: Fetcher, *, refresh: bool, last_problem: int = 99999) -> dict[str, Any]:
    index_path = RAW_LISTS / "lists-index.json"
    if index_path.is_file() and not refresh:
        index = json.loads(
            read_bounded_bytes(index_path, MAX_RAW_BYTES).decode("utf-8"),
            parse_constant=_reject_json_constant,
        )
    else:
        rows = parse_lists_page()
        if not rows:
            raise RuntimeError("无法从 /lists 页面解析问题列表行。")
        if len(rows) > MAX_LIST_ENTRIES:
            raise RuntimeError(f"问题列表条目超过上限 {MAX_LIST_ENTRIES}。")
        index = {"observed_at": utc_now(), "list_count": len(rows), "lists": rows}
        write_json(index_path, index)
    if not isinstance(index, dict) or not isinstance(index.get("lists"), list):
        raise RuntimeError("问题列表索引结构无效。")
    if len(index["lists"]) > MAX_LIST_ENTRIES:
        raise RuntimeError(f"问题列表条目超过上限 {MAX_LIST_ENTRIES}。")
    membership: dict[int, list[int]] = defaultdict(list)  # key -> [problem numbers]
    problem_lists: dict[int, list[str]] = defaultdict(list)  # n -> [list titles]
    cache_hits = 0
    for entry in index["lists"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("key"), str) or not entry["key"]:
            raise RuntimeError("问题列表索引条目无效。")
        key = safe_component(entry["key"], "问题列表键")
        raw_path = RAW_LISTS / f"{key}.html"
        body, _, from_cache = cached_fetch_with_429_backoff(
            fetcher,
            f"{ERDOS_URL}/search_bib/{key}?sources_only=1",
            raw_path,
            refresh=refresh,
        )
        cache_hits += int(from_cache)
        soup = BeautifulSoup(body, "lxml")
        numbers = sorted(
            int(m)
            for link in soup.select("a[href]")
            if re.fullmatch(r"#\d+", normalize_space(link.get_text(" ", strip=True)))
            for m in re.findall(r"/(\d+)", link.get("href", ""))
        )
        numbers = [m for m in numbers if 1 <= m <= last_problem]
        if len(numbers) > MAX_RECORDS:
            raise RuntimeError(f"问题列表 {key!r} 的成员超过上限 {MAX_RECORDS}。")
        membership[key] = sorted(set(numbers))
        for number in numbers:
            problem_lists[number].append(key)
        entry["observed_problem_count"] = len(set(numbers))
        if sum(len(values) for values in membership.values()) > MAX_RECORDS:
            raise RuntimeError(f"问题列表归属总数超过上限 {MAX_RECORDS}。")
    index["cache_hits"] = cache_hits
    index["membership"] = {key: sorted(values) for key, values in membership.items()}
    write_json(index_path, index)
    return {"lists": index, "problem_lists": problem_lists}


def crawl_tags(fetcher: Fetcher, *, refresh: bool) -> list[dict[str, Any]]:
    tags_path = RAW_TAGS / "tags-index.json"
    if tags_path.is_file() and not refresh:
        index = json.loads(
            read_bounded_bytes(tags_path, MAX_RAW_BYTES).decode("utf-8"),
            parse_constant=_reject_json_constant,
        )
    else:
        soup = BeautifulSoup(read_bounded_bytes(RAW_AUX / "tags.html", MAX_RAW_BYTES), "lxml")
        entries: list[dict[str, Any]] = []
        for row in soup.select("li"):
            link = row.select_one('a[href^="/tags/"]')
            if link is None:
                continue
            slug = link.get("href").rstrip("/").split("/")[-1]
            text = normalize_space(row.get_text(" ", strip=True))
            solved_match = re.search(r"(\d+)\s+solved\s+out\s+of\s+(\d+)", text)
            entries.append(
                {
                    "slug": slug,
                    "label": normalize_space(link.get_text(" ", strip=True)),
                    "declared_solved": int(solved_match.group(1)) if solved_match else None,
                    "declared_total": int(solved_match.group(2)) if solved_match else None,
                }
            )
        if not entries:
            raise RuntimeError("无法从 /tags 页面解析标签列表。")
        if len(entries) > MAX_TAG_ENTRIES:
            raise RuntimeError(f"标签条目超过上限 {MAX_TAG_ENTRIES}。")
        index = {"observed_at": utc_now(), "tag_count": len(entries), "tags": entries}
        write_json(tags_path, index)
    if not isinstance(index, dict) or not isinstance(index.get("tags"), list):
        raise RuntimeError("标签索引结构无效。")
    if len(index["tags"]) > MAX_TAG_ENTRIES:
        raise RuntimeError(f"标签条目超过上限 {MAX_TAG_ENTRIES}。")
    cache_hits = 0
    for entry in index["tags"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("slug"), str) or not entry["slug"]:
            raise RuntimeError("标签索引条目无效。")
        tag_slug = safe_component(entry["slug"], "标签 slug")
        slug = urllib.parse.quote(tag_slug)
        raw_path = RAW_TAGS / f"{tag_slug}.html"
        _, _, from_cache = cached_fetch_with_429_backoff(
            fetcher, f"{ERDOS_URL}/tags/{slug}", raw_path, refresh=refresh
        )
        cache_hits += int(from_cache)
    index["cache_hits"] = cache_hits
    write_json(tags_path, index)
    return index["tags"]


# --------------------------------------------------------------------------
# 构建记录与对账
# --------------------------------------------------------------------------

STATUS_SEMANTICS: dict[str, str] = {
    # 站点原始状态 id -> 统一问题状态词汇（与 problem.schema.json 枚举一致）
    "open": "open",
    "solved": "solved",
    "partial": "partially_solved",
}


def reconcile_tags(records: list[dict[str, Any]], tags_index: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    computed: Counter[str] = Counter()
    for record in records:
        for tag in record["categories"]:
            computed[tag] += 1
    declared = {entry["slug"]: entry["declared_total"] for entry in tags_index["tags"] if entry["declared_total"]}
    missing_declared = [slug for slug in computed if slug not in declared]
    missing_computed = [slug for slug in declared if slug not in computed]
    deviations = {
        slug: {"declared": declared[slug], "computed": computed[slug]}
        for slug in set(declared) & set(computed)
        if declared[slug] != computed[slug]
    }
    anomaly: list[str] = []
    if missing_declared:
        anomaly.append(f"记录中存在但 /tags 页面未声明的标签：{sorted(missing_declared)}")
    if deviations:
        anomaly.append(f"标签计数与 /tags 页面有差别的共 {len(deviations)} 个：{deviations}")
    return anomaly, {
        "declared_total": sum(declared.values()),
        "computed_total": sum(computed.values()),
        "missing_declared": sorted(missing_declared),
        "missing_computed": sorted(missing_computed),
        "deviations": deviations,
    }


def reconcile_prizes(records: list[dict[str, Any]], prizes_path: Path) -> tuple[list[str], dict[str, Any]]:
    soup = BeautifulSoup(read_bounded_bytes(prizes_path, MAX_RAW_BYTES), "lxml")
    body = re.sub(r"<script.*?</script>", " ", str(soup), flags=re.S)
    text = normalize_space(BeautifulSoup(body, "lxml").get_text(" ", strip=True))
    declared: dict[int, tuple[int, int]] = {}
    for amount, solved, total in re.findall(r"\$([\d,]+)\s*:\s*(\d+)\s+solved\s+out\s+of\s+(\d+)", text):
        declared[int(amount.replace(",", ""))] = (int(solved), int(total))
    computed_by_prize: Counter[int] = Counter(record.get("prize") or 0 for record in records)
    mismatch = {
        str(amount): {"declared_total": declared[amount][1], "computed": computed_by_prize[amount]}
        for amount in declared
        if declared[amount][1] != computed_by_prize[amount]
    }
    declared_total = sum(total for _, total in declared.values())
    anomaly: list[str] = []
    if declared_total and declared_total != len(records):
        anomaly.append(f"/prizes 页面声明的奖金组总数 {declared_total} 与记录数 {len(records)} 不一致。")
    return anomaly, {
        "page_text_excerpt": text[:800],
        "declared_groups": {str(k): v for k, v in sorted(declared.items())},
        "mismatches": mismatch,
        "declared_total": declared_total,
    }


def build_records(*, problems: list[dict[str, Any]], problem_lists: dict[int, list[str]]) -> tuple[dict[str, Any], dict[str, Any]]:
    generated_at = utc_now()
    status_anomalies: list[str] = []
    for record in problems:
        raw_status = record["status"]
        if raw_status in STATUS_SEMANTICS:
            record["status"] = STATUS_SEMANTICS[raw_status]
        else:
            status_anomalies.append(f"未映射状态 {raw_status!r}：{record['source_native_id']}")
    if status_anomalies:
        raise RuntimeError("存在未映射状态：\n" + "\n".join(status_anomalies))
    lists_rows: list[dict[str, Any]] = []
    if LISTS_INDEX_PATH.is_file():
        lists_payload = json.loads(
            read_bounded_bytes(LISTS_INDEX_PATH, MAX_RAW_BYTES).decode("utf-8"),
            parse_constant=_reject_json_constant,
        )
        if not isinstance(lists_payload, dict):
            raise RuntimeError("问题列表索引结构无效。")
        lists_rows = lists_payload.get("lists", [])
    titles_by_key = {entry["key"]: entry["title"] for entry in lists_rows}
    problems_without_list = 0
    for record in problems:
        number = int(record["source_native_id"])
        keys = problem_lists.get(number, [])
        record["problem_sets"] = [titles_by_key[key] for key in keys if key in titles_by_key]
        if not keys:
            problems_without_list += 1
    for record in problems:
        record.pop("_internal", None)
    # 从缓存重算 Wikipedia 与 UnsolvedMath 记录（不访问网络）
    base = load_fetcher_module()
    wikipedia_records, wikipedia_metadata = base.fetch_wikipedia(
        base.Fetcher(timeout=30, delay=0, retries=1), refresh=False, retrieved_at=generated_at
    )
    unsolvedmath_records, unsolvedmath_metadata = base.fetch_unsolvedmath(
        base.Fetcher(timeout=30, delay=0, retries=1), refresh=False, retrieved_at=generated_at
    )
    all_records = wikipedia_records + unsolvedmath_records + problems
    if len(all_records) > MAX_RECORDS:
        raise RuntimeError(f"问题记录超过上限 {MAX_RECORDS}，拒绝生成快照。")
    payload = "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n"
        for record in all_records
    )
    encoded_payload = payload.encode("utf-8")
    if len(encoded_payload) > MAX_RECORDS_BYTES:
        raise RuntimeError(f"问题记录输出超过上限 {MAX_RECORDS_BYTES} bytes。")
    write_atomic(RECORDS_PATH, encoded_payload)
    catalog = base.build_indexes(all_records, generated_at=generated_at)
    erdos_metadata = {
        "source_url": ERDOS_URL,
        "record_scope": "all problem pages /1..N rendered by the site; satellite pages (bibs, lists, tags) kept as raw evidence",
        "license": {
            "name": "site robots.txt Content-Signal; no explicit license",
            "url": f"{ERDOS_URL}/robots.txt",
            "policy": "Content-Signal search=yes, ai-train=no, use=reference；按 reference 用途保存问题事实与归属。",
        },
        "discovery_file": str(DISCOVERY_PATH.relative_to(ROOT)),
        "discovery_sha256": sha256_bytes(read_bounded_bytes(DISCOVERY_PATH, MAX_RAW_BYTES)),
        "record_count": len(problems),
        "status_counts": dict(sorted(Counter(record["status"] for record in problems).items())),
        "problems_without_list": problems_without_list,
        "status_inventory_file": str(STATUS_INVENTORY_PATH.relative_to(ROOT)),
        "status_inventory_sha256": sha256_bytes(read_bounded_bytes(STATUS_INVENTORY_PATH, MAX_RAW_BYTES)),
        "gaps_file": str(GAPS_PATH.relative_to(ROOT)),
        "gaps_sha256": sha256_bytes(read_bounded_bytes(GAPS_PATH, MAX_RAW_BYTES)),
    }
    return erdos_metadata, {
        "records": all_records,
        "catalog": catalog,
        "wikipedia": wikipedia_metadata,
        "unsolvedmath": unsolvedmath_metadata,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="抓取与重建 Erdős Problems 问题库。")
    parser.add_argument("mode", nargs="?", default="all", choices=("crawl", "build", "all"))
    parser.add_argument("--refresh", action="store_true", help="忽略现有原始缓存并重新访问来源。")
    parser.add_argument("--delay", type=float, default=0.3, help="同一进程两次 HTTP 请求的最小间隔秒数。")
    parser.add_argument("--timeout", type=float, default=30.0, help="单次 HTTP 请求超时秒数。")
    parser.add_argument("--retries", type=int, default=3, help="瞬时网络失败的最大尝试次数。")
    args = parser.parse_args()
    fetcher = Fetcher(timeout=args.timeout, delay=args.delay, retries=args.retries)
    problems: list[dict[str, Any]] = []
    problem_lists: dict[int, list[str]] = defaultdict(list)
    tags_index: dict[str, Any] = {"tags": []}
    if args.mode in ("crawl", "all"):
        print("阶段 1/4：来源发现与规范页快照", flush=True)
        probe_discovery(fetcher, refresh=args.refresh)
        crawl_aux_pages(fetcher, refresh=args.refresh)
        print("阶段 2/4：枚举并抓取全部问题页", flush=True)
        crawled = crawl_problems(fetcher, refresh=args.refresh)
        problems = crawled["problems"]
        summary = crawled["summary"]
        if summary["gaps_within_range"]:
            raise RuntimeError(f"问题编号区间内出现缺口：{summary['gaps_within_range']}")
        ref_keys: list[str] = []
        for record in problems:
            for key in record["_internal"]["ref_keys"]:
                if key not in ref_keys:
                    ref_keys.append(key)
                    if len(ref_keys) > MAX_REFERENCE_KEYS:
                        raise RuntimeError(f"书目键超过上限 {MAX_REFERENCE_KEYS}，拒绝继续抓取。")
        print(f"阶段 3/4：抓取 {len(ref_keys)} 个唯一书目键", flush=True)
        bibs_result = crawl_bibs(fetcher, ref_keys, refresh=args.refresh)
        print(
            f"书目完成：{bibs_result['fetched']}/{bibs_result['unique_keys']}，"
            f"缺失 {bibs_result['missing']}",
            flush=True,
        )
        print("阶段 4/4：问题列表归属与标签对账证据", flush=True)
        lists_result = crawl_lists(fetcher, refresh=args.refresh, last_problem=crawled["summary"]["problem_range"]["last"])
        problem_lists = lists_result["problem_lists"]
        tags_index_data = crawl_tags(fetcher, refresh=args.refresh)
        tags_index = {"tags": tags_index_data}
        print(
            f"完成网络阶段：{len(problems)} 条问题；列表归属键 {len(lists_result['lists']['membership'])} 个；"
            f"标签页 {len(tags_index_data)} 个",
            flush=True,
        )
        if args.mode == "crawl":
            print(
                "提示：请运行 build 生成记录；若出现未映射状态，先按 status-inventory.json "
                "扩展 STATUS_SEMANTICS 与 schema。",
                flush=True,
            )
            return 0
    else:  # build：从本地原始快照重算
        gaps_data = (
            json.loads(
                read_bounded_bytes(GAPS_PATH, MAX_RAW_BYTES).decode("utf-8"),
                parse_constant=_reject_json_constant,
            )
            if GAPS_PATH.is_file()
            else {}
        )
        last_problem = gaps_data.get("summary", {}).get("problem_range", {}).get("last") or 0
        for raw_path in sorted(RAW_PROBLEMS.glob("*.html")):
            if last_problem and int(Path(raw_path).stem) > last_problem:
                break
            problems.append(parse_problem_page(raw_path))
        problems.sort(key=lambda record: record["source_order"])
        if LISTS_INDEX_PATH.is_file():
            lists_index = json.loads(
                read_bounded_bytes(LISTS_INDEX_PATH, MAX_RAW_BYTES).decode("utf-8"),
                parse_constant=_reject_json_constant,
            )
            for key, numbers in lists_index.get("membership", {}).items():
                for number in numbers:
                    problem_lists[number].append(key)
        if (RAW_TAGS / "tags-index.json").is_file():
            tags_index = json.loads(
                read_bounded_bytes(RAW_TAGS / "tags-index.json", MAX_RAW_BYTES).decode("utf-8"),
                parse_constant=_reject_json_constant,
            )
    if len(problems) != len({record["id"] for record in problems}):
        raise RuntimeError("erdosproblems 本地记录 id 重复，拒绝生成不确定快照。")
    generated_at = utc_now()
    print(f"构建记录：{len(problems)} 条 erdosproblems", flush=True)
    erdos_metadata, built = build_records(
        problems=problems,
        problem_lists=dict(problem_lists),
    )
    tag_anomalies, tag_reconciliation = reconcile_tags(
        [record for record in built["records"] if record["source"] == "erdosproblems"],
        tags_index,
    )
    prize_anomalies, prize_reconciliation = reconcile_prizes(
        [record for record in built["records"] if record["source"] == "erdosproblems"],
        RAW_AUX / "prizes.html",
    )
    gaps_data = (
        json.loads(
            read_bounded_bytes(GAPS_PATH, MAX_RAW_BYTES).decode("utf-8"),
            parse_constant=_reject_json_constant,
        )
        if GAPS_PATH.is_file()
        else {}
    )
    erdos_metadata.update(
        {
            "generated_at": generated_at,
            "snapshot_evidence": {
                "gaps": gaps_data.get("gaps", []),
                "gaps_summary": gaps_data.get("summary", {}),
                "status_counts": json.loads(
                    read_bounded_bytes(STATUS_INVENTORY_PATH, MAX_RAW_BYTES).decode("utf-8"),
                    parse_constant=_reject_json_constant,
                )["status_counts"]
                if STATUS_INVENTORY_PATH.is_file()
                else {},
            },
            "reconciliation": {
                "tags": tag_reconciliation,
                "tags_anomalies": tag_anomalies,
                "prizes": prize_reconciliation,
                "prizes_anomalies": prize_anomalies,
            },
        }
    )
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "generator": "scripts/fetch_erdosproblems.py (coordinator) + scripts/fetch_problem_library.py",
        "records_file": str(RECORDS_PATH.relative_to(ROOT)),
        "records_sha256": sha256_bytes(read_bounded_bytes(RECORDS_PATH, MAX_RECORDS_BYTES)),
        "record_count": len(built["records"]),
        "catalog": built["catalog"],
        "sources": {
            "wikipedia": built["wikipedia"],
            "unsolvedmath": built["unsolvedmath"],
            "erdosproblems": erdos_metadata,
        },
    }
    write_json(MANIFEST_PATH, manifest)
    print(
        f"完成：{manifest['record_count']} 条（Wikipedia {built['wikipedia']['record_count']}；"
        f"UnsolvedMath {built['unsolvedmath']['record_count']}；"
        f"ErdősProblems {len(problems)}），清单与索引已重建。",
        flush=True,
    )
    return 0



if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        OSError,
        RuntimeError,
        ValueError,
        KeyError,
        TypeError,
        AttributeError,
        IndexError,
        json.JSONDecodeError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc