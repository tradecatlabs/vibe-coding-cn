#!/usr/bin/env python3
"""candidates 整理器：把可解析来源归一化为统一问题记录（JSONL）+ 去重统计。

用法: python3 scripts/consolidate_candidates.py
输出:
  problem-library/raw/candidates/consolidated/problems.jsonl  统一问题记录
  problem-library/raw/candidates/consolidated/summary.json    每来源统计 + 去重重叠报告
"""
from __future__ import annotations

import csv
import hashlib
import html
import io
import json
import os
import re
import stat
import sys
import tarfile
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CAND = ROOT / "problem-library" / "raw" / "candidates"
OUT = CAND / "consolidated"
MAX_INPUT_BYTES = 30_000_000
MAX_RECORDS = 100_000
MAX_PATHS = 100_000
MAX_ARCHIVE_MEMBERS = 100_000
MAX_FIELD_CHARS = 8_192
MAX_OUTPUT_BYTES = 30_000_000
MAX_RECORD_BYTES = 1_000_000


def _safe_output_path(path: Path) -> Path:
    path = Path(path)
    if (
        len(str(path)) > 4_096
        or "\x00" in str(path)
        or "\\" in str(path)
        or any(part in {".", ".."} for part in path.parts)
    ):
        raise RuntimeError(f"candidate output path is invalid: {path}")
    if CAND.is_symlink() or CAND.resolve() != CAND:
        raise RuntimeError("candidate raw root cannot be a symlink")
    candidate = Path(os.path.abspath(path))
    root = Path(os.path.abspath(CAND))
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(f"candidate output escapes raw root: {candidate}") from exc
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise RuntimeError(f"candidate output path contains symlink: {candidate}")
    return candidate


def _atomic_write_output(path: Path, data: bytes) -> None:
    if not isinstance(data, bytes) or len(data) > MAX_INPUT_BYTES:
        raise RuntimeError("candidate output exceeds size budget")
    candidate = _safe_output_path(path)
    candidate.parent.mkdir(parents=True, exist_ok=True)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if nofollow is None or directory is None:
        raise RuntimeError("candidate output cannot be safely persisted")
    temporary = candidate.with_name(f".{candidate.name}.{os.getpid()}.tmp")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, candidate)
        directory_descriptor = os.open(candidate.parent, os.O_RDONLY | directory | nofollow)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        temporary.unlink(missing_ok=True)


def _safe_read_bytes(path: Path, *, max_bytes: int = MAX_INPUT_BYTES) -> bytes:
    if not isinstance(max_bytes, int) or isinstance(max_bytes, bool) or max_bytes <= 0 or max_bytes > MAX_INPUT_BYTES:
        raise RuntimeError("candidate parser read budget is invalid")
    path = Path(path)
    if (
        len(str(path)) > 4_096
        or "\x00" in str(path)
        or "\\" in str(path)
        or any(part in {".", ".."} for part in path.parts)
    ):
        raise RuntimeError(f"candidate parser path is invalid: {path}")
    if CAND.is_symlink() or CAND.resolve() != CAND:
        raise RuntimeError("candidate raw root cannot be a symlink")
    root = CAND
    candidate = path if path.is_absolute() else CAND / path
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(f"candidate parser path escapes raw root: {candidate}") from exc
    if any(part in {".", ".."} for part in relative.parts) or "\x00" in str(candidate):
        raise RuntimeError(f"candidate parser path escapes raw root: {candidate}")
    lexical = root
    for part in relative.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise RuntimeError(f"candidate parser path contains symlink: {candidate}")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeError("candidate parser cannot safely read raw files")
    descriptor = os.open(candidate, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > max_bytes:
            raise RuntimeError(f"candidate parser input exceeds budget: {candidate}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, max_bytes - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > max_bytes:
                raise RuntimeError(f"candidate parser input exceeds budget: {candidate}")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def _reject_json_constant(value: str) -> Any:
    raise ValueError(f"candidate JSON contains illegal constant: {value}")


def _bounded_paths(base: Path, pattern: str) -> list[Path]:
    if (
        len(str(base)) > 4_096
        or "\x00" in str(base)
        or "\\" in str(base)
        or not isinstance(pattern, str)
        or not pattern
        or len(pattern) > 4_096
        or "\x00" in pattern
        or "\\" in pattern
    ):
        raise RuntimeError("candidate input path pattern is invalid")
    paths = sorted(base.glob(pattern))
    if len(paths) > MAX_PATHS:
        raise RuntimeError(f"candidate input path count exceeds budget: {base}/{pattern}")
    return paths


def _safe_read_text(path: Path, encoding: str = "utf-8") -> str:
    return _safe_read_bytes(path).decode(encoding, errors="replace")


def _safe_read_json(path: Path) -> Any:
    return json.loads(_safe_read_text(path), parse_constant=_reject_json_constant)


def _bounded_archive_member(archive: Any, member: Any) -> bytes:
    if getattr(member, "file_size", 0) > MAX_INPUT_BYTES:
        raise RuntimeError("candidate archive member exceeds size budget")
    handle = archive.extractfile(member)
    if handle is None:
        raise RuntimeError("candidate archive member is not readable")
    chunks: list[bytes] = []
    total = 0
    try:
        while True:
            chunk = handle.read(min(64 * 1024, MAX_INPUT_BYTES - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > MAX_INPUT_BYTES:
                raise RuntimeError("candidate archive member exceeds size budget")
            chunks.append(chunk)
    finally:
        handle.close()


def _bounded_zip_member(archive: zipfile.ZipFile, name: str) -> bytes:
    info = archive.getinfo(name)
    if info.file_size > MAX_INPUT_BYTES:
        raise RuntimeError("candidate ZIP member exceeds size budget")
    chunks: list[bytes] = []
    total = 0
    with archive.open(info) as handle:
        while True:
            chunk = handle.read(min(64 * 1024, MAX_INPUT_BYTES - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > MAX_INPUT_BYTES:
                raise RuntimeError("candidate ZIP member exceeds size budget")
            chunks.append(chunk)


def norm_statement(s: str) -> str:
    """题面归一化（去空白/小写），用于跨源去重近似。"""
    if not isinstance(s, str):
        raise RuntimeError("candidate statement must be a string")
    return re.sub(r"\s+", " ", html.unescape(s)).strip().lower()


def strip_html(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", s or ""))


def strip_document_html(s: str) -> str:
    value = re.sub(r"<!--.*?-->", " ", s or "", flags=re.S)
    value = re.sub(r"<(script|style|svg|noscript|head)\b[^>]*>.*?</\1\s*>", " ", value, flags=re.I | re.S)
    return re.sub(r"\s+", " ", strip_html(value)).strip()


def rec(source: str, title: str, statement: str, status: str | None, url: str, extra: dict | None = None) -> dict:
    values = (("source", source), ("title", title), ("statement", statement), ("url", url))
    if any(not isinstance(value, str) or len(value) > MAX_FIELD_CHARS for _, value in values):
        raise RuntimeError("candidate record string field is invalid or too long")
    if status is not None and (not isinstance(status, str) or len(status) > MAX_FIELD_CHARS):
        raise RuntimeError("candidate record status is invalid or too long")
    if extra is not None and not isinstance(extra, dict):
        raise RuntimeError("candidate record extra must be an object")
    record = {
        "source": source,
        "title": title,
        "statement": statement,
        "status": status,
        "url": url,
        "extra": extra or {},
    }
    try:
        encoded = json.dumps(record, ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise RuntimeError("candidate record is not portable JSON") from exc
    if len(encoded) > MAX_RECORD_BYTES:
        raise RuntimeError("candidate record exceeds size budget")
    return record


def parse_theoremdb() -> list[dict]:
    out = []
    idx = _safe_read_json(CAND / "theoremdb" / "search-index.json")["items"]
    if not isinstance(idx, list) or len(idx) > MAX_RECORDS:
        raise RuntimeError("TheoremDB records exceed budget")
    for it in idx:
        slug = it.get("slug")
        ps = it.get("public_status") or {}
        resolution = ps.get("resolution") if isinstance(ps, dict) else None
        state = resolution.get("state") if isinstance(resolution, dict) else str(ps or "")
        out.append(rec(
            "theoremdb", it.get("title") or "", it.get("statement") or "",
            state or "",
            f"https://theoremdb.org/statement/?ref={slug}" if slug else "",
            {"domain": it.get("domain"), "lean_verified": it.get("lean_verified"),
             "active_bounty": it.get("active_bounty"), "formal_statement": it.get("formal_statement"),
             "problem_number": it.get("problem_number")},
        ))
    return out


def parse_se_api(source: str, base: Path) -> list[dict]:
    out = []
    for p in _bounded_paths(base / "api", "*.json"):
        items = _safe_read_json(p).get("items", [])
        if not isinstance(items, list) or len(items) > MAX_RECORDS:
            raise RuntimeError("Stack Exchange records exceed budget")
        for it in items:
            if not isinstance(it, dict):
                raise RuntimeError("Stack Exchange record is not an object")
            out.append(rec(
                source, it.get("title") or "", strip_html(it.get("body") or ""),
                "answered" if it.get("is_answered") else "open",
                it.get("link") or f"https://{source}.stackexchange.com/questions/{it.get('question_id')}",
                {"tags": it.get("tags"), "score": it.get("score"), "creation_date": it.get("creation_date")},
            ))
    return out


def parse_oqp() -> list[dict]:
    out = []
    with tarfile.open(
        fileobj=io.BytesIO(_safe_read_bytes(CAND / "openquantum" / "source-tarball.tar.gz"))
    ) as tar:
        for member_number, member in enumerate(tar, 1):
            if member_number > MAX_ARCHIVE_MEMBERS:
                raise RuntimeError("candidate TAR member count exceeds budget")
            if (
                not member.isreg()
                or
                "app/data/cat-" not in member.name
                or not member.name.endswith(".js")
                or member.name.endswith("index.js")
            ):
                continue
            text = _bounded_archive_member(tar, member).decode("utf-8", "replace")
            match_count = 0
            for match in re.finditer(r'\{\s*id:\s*"([A-Za-z0-9-]+)"', text):
                match_count += 1
                if len(out) >= MAX_RECORDS:
                    raise RuntimeError("OpenQuantum records exceed budget")
                obj = text[match.start():]
                endm = re.search(r'\n\s*\}\s*,', obj)
                obj = obj[:endm.start()] if endm else obj[:4000]
                title_match = re.search(r'title:\s*"((?:[^"\\]|\\.)*)"', obj)
                statement_match = re.search(r'statement:\s*r`((?:[^`]|``)*)`', obj)
                category_match = re.search(r'cat:\s*"([^"]+)"', obj)
                horizon_match = re.search(r'horizon:\s*"([^"]*)"', obj)
                if not title_match:
                    continue
                out.append(rec(
                    "openquantum", title_match.group(1), statement_match.group(1) if statement_match else "",
                    "open", "https://openquantumproblems.com/",
                    {"id": match.group(1), "cat": category_match.group(1) if category_match else "",
                     "horizon": horizon_match.group(1) if horizon_match else ""},
                ))
    return out


def parse_topp() -> list[dict]:
    out = []
    for p in _bounded_paths(CAND / "topp" / "pages", "*.html"):
        t = _safe_read_text(p, "latin-1")
        m = re.search(r"<title>([^<]*)</title>", t)
        body = strip_html(t)
        body = re.sub(r"^\s*TOPP[:\s]*Problem\s*\d+.*?:\s*", "", body, flags=re.I)
        out.append(rec("topp", (m.group(1) if m else p.stem).split(": ", 1)[-1],
                       body[:4000], "open", "https://topp.openproblem.net/" + p.name))
    return out


def parse_ucsd() -> list[dict]:
    out = []
    for p in _bounded_paths(CAND / "ucsd" / "erdos" / "newproblems", "*.html"):
        t = _safe_read_text(p, "latin-1")
        body = strip_html(t)
        out.append(rec("ucsd_erdos", p.stem.replace("_", " "), body[:4000], "open",
                       "https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/" + p.name))
    return out


def parse_openlogic() -> list[dict]:
    out = []
    for p in _bounded_paths(CAND / "openlogicproblems" / "pages", "*.html"):
        t = _safe_read_text(p)
        m = re.search(r"<title>([^<]*)</title>", t)
        body = strip_html(t)
        out.append(rec("openlogicproblems", m.group(1) if m else p.stem, body[:4000], "open",
                       "https://openlogicproject.org/" + p.name))
    return out


def parse_clay() -> list[dict]:
    out = []
    for p in _bounded_paths(CAND / "clay" / "pages", "millennium_*.html"):
        t = _safe_read_text(p)
        slug = p.stem.removeprefix("millennium_")
        title_match = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)', t, re.I)
        description_match = re.search(r'<meta\s+property=["\']og:description["\']\s+content=["\']([^"\']+)', t, re.I)
        fallback = re.search(r"<title>([^<]*)</title>", t, re.I)
        title = html.unescape((title_match or fallback).group(1) if (title_match or fallback) else slug)
        statement = strip_document_html(description_match.group(1) if description_match else t)[:5000]
        status = "solved" if slug == "poincare-conjecture" else "open"
        out.append(rec(
            "clay",
            title.replace(" - Clay Mathematics Institute", "").replace(" - CMI", ""),
            statement,
            status,
            f"https://www.claymath.org/millennium/{slug}/",
            {"id": slug},
        ))
    return out


def parse_unsolvedproblems() -> list[dict]:
    out = []
    for p in _bounded_paths(CAND / "unsolvedproblems", "index_files_*.htm"):
        t = _safe_read_text(p, "latin-1")
        body = strip_html(t)
        out.append(rec("unsolvedproblems", p.stem, body[:3000], "open",
                       "https://unsolvedproblems.org/index_files/" + p.name))
    return out


def parse_oeis_articles() -> list[dict]:
    out = []
    for p in _bounded_paths(CAND / "oeis_articles" / "pages", "*.html"):
        t = _safe_read_text(p)
        m = re.search(r"<title>([^<]*)</title>", t)
        out.append(rec("oeis_articles", html.unescape(m.group(1)) if m else p.stem,
                       strip_html(t)[:4000], "open", "https://oeis.org/wiki/" + p.stem))
    return out


def parse_wiki_extracts(source: str, base: Path, pattern: str) -> list[dict]:
    out = []
    for p in _bounded_paths(base, pattern):
        d = _safe_read_json(p)
        pages = d.get("query", {}).get("pages", [])
        if not isinstance(pages, list) or len(pages) > MAX_RECORDS:
            raise RuntimeError("Wikipedia extract records exceed budget")
        for pg in pages:
            if not isinstance(pg, dict):
                raise RuntimeError("Wikipedia extract record is not an object")
            if pg.get("extract"):
                out.append(rec(source, pg.get("title", ""), pg["extract"][:3000], "open",
                               "https://en.wikipedia.org/wiki/" + pg.get("title", "").replace(" ", "_")))
    return out


def parse_wiki_lists(source: str, base: Path, glob_pat: str, host: str) -> list[dict]:
    out = []
    for p in _bounded_paths(base, glob_pat):
        d = _safe_read_json(p)
        text = d.get("parse", {}).get("text", "")
        list_items = re.findall(r"<li>(.*?)</li>", text, re.S)
        if len(list_items) > MAX_RECORDS:
            raise RuntimeError("Wikipedia list records exceed budget")
        for li in list_items:
            item = strip_html(li).strip()
            if len(item) < 10:
                continue
            out.append(rec(source, item[:200], item, "open", f"https://{host}/wiki/" + p.stem))
    return out


def parse_fmop() -> list[dict]:
    out = []
    with zipfile.ZipFile(
        io.BytesIO(_safe_read_bytes(CAND / "fmop" / "open_problems_data.zip"))
    ) as zf:
        infos = zf.infolist()
        if len(infos) > MAX_ARCHIVE_MEMBERS:
            raise RuntimeError("candidate ZIP member count exceeds budget")
        for info in infos:
            name = info.filename
            if name.endswith("metadata.csv"):
                rows = []
                for row_number, row in enumerate(
                    csv.DictReader(io.StringIO(_bounded_zip_member(zf, name).decode())), 1
                ):
                    if row_number > MAX_RECORDS:
                        raise RuntimeError("candidate CSV record count exceeds budget")
                    rows.append(row)
                for r in rows:
                    out.append(rec("fmop", r.get("title", ""), r.get("short_description") or r.get("title", ""),
                                   "solved" if str(r.get("solved")).lower() == "true" else "open",
                                   "https://epoch.ai/frontiermath/open-problems",
                                   {"problem_id": r.get("problem_id"), "field": r.get("field"),
                                    "notability": r.get("notability"), "tags": r.get("tags"),
                                    "solved_by_human": r.get("solved_by_human")}))
    return out


def parse_vibemathed() -> list[dict]:
    """VibeMathed：AI 已解决/部分解决目录（API source-of-truth 最新版，CC BY 4.0）。"""
    out = []
    d = _safe_read_json(CAND / "vibemathed" / "dataset-latest.json")
    problems = d.get("problems", [])
    if not isinstance(problems, list) or len(problems) > MAX_RECORDS:
        raise RuntimeError("VibeMathed records exceed budget")
    for it in problems:
        if not isinstance(it, dict):
            raise RuntimeError("VibeMathed record is not an object")
        title_v = it.get("name") or it.get("slug", "")
        out.append(rec(
            "vibemathed", title_v,
            it.get("statement") or title_v,
            it.get("resolution") or "",
            it.get("sourceUrl") or f"https://vibemathed.com/problem/{it.get('slug')}",
            {"model": it.get("model"), "modelMaker": it.get("modelMaker"),
             "verification": it.get("verification"), "significance": it.get("significance"),
             "solveType": it.get("solveType"), "problemNumber": it.get("problemNumber"),
             "field": it.get("field"), "fieldGroup": it.get("fieldGroup"),
             "solveDate": it.get("solveDate"), "publication": it.get("publication"),
             "aiRole": it.get("aiRole"), "sourceName": it.get("sourceName"),
             "solveCostUsd": it.get("solveCostUsd")},
        ))
    return out


EXTRACTORS = {
    "theoremdb": parse_theoremdb,
    "mathoverflow": lambda: parse_se_api("mathoverflow", CAND / "mathoverflow"),
    "mo_conjectures": lambda: parse_se_api("mo_conjectures", CAND / "mo_conjectures"),
    "mse": lambda: parse_se_api("mse", CAND / "mse"),
    "openquantum": parse_oqp,
    "topp": parse_topp,
    "ucsd": parse_ucsd,
    "openlogicproblems": parse_openlogic,
    "clay": parse_clay,
    "unsolvedproblems": parse_unsolvedproblems,
    "oeis_articles": parse_oeis_articles,
    "wikipedia_categories": lambda: parse_wiki_extracts("wikipedia_categories", CAND / "wikipedia_categories" / "extracts", "*-*.json"),
    "zh_conjectures": lambda: parse_wiki_extracts("zh_conjectures", CAND / "zh_conjectures" / "extracts", "zh-*.json"),
    "multilingual_conjectures": lambda: parse_wiki_extracts("multilingual_conjectures", CAND / "multilingual_conjectures" / "extracts", "*-*.json"),
    "wiki_subsets": lambda: parse_wiki_extracts("wiki_subsets", CAND / "wiki_subsets" / "extracts", "*-*.json"),
    "wiki_more_lists": lambda: parse_wiki_lists("wiki_more_lists", CAND / "wiki_more_lists" / "pages", "*.json", "en.wikipedia.org"),
    "multilingual_lists": lambda: parse_wiki_lists("multilingual_lists", CAND / "multilingual_lists", "*-unsolved-math.json", "wikipedia.org"),
    "wikipedia_conjectures": lambda: parse_wiki_lists("wikipedia_conjectures", CAND / "wikipedia_conjectures", "list-of-conjectures.json", "en.wikipedia.org"),
    "fmop": parse_fmop,
    "vibemathed": parse_vibemathed,
}


def main() -> int:
    if CAND.is_symlink() or CAND.resolve() != CAND:
        raise RuntimeError("candidate raw root cannot be a symlink")
    CAND.mkdir(parents=True, exist_ok=True)
    if CAND.is_symlink() or CAND.resolve() != CAND:
        raise RuntimeError("candidate raw root cannot be a symlink")
    OUT.mkdir(parents=True, exist_ok=True)
    all_recs: list[dict] = []
    per_source: dict[str, int] = {}
    for source, fn in EXTRACTORS.items():
        try:
            recs = fn()
            if not isinstance(recs, list) or len(recs) > MAX_RECORDS:
                raise RuntimeError("extractor record count exceeds budget")
            if len(all_recs) + len(recs) > MAX_RECORDS:
                raise RuntimeError("combined candidate record count exceeds budget")
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] {source}: {exc}")
            recs = []
        for r in recs:
            r["id"] = hashlib.sha1(f"{r['source']}\x1f{r['title']}\x1f{norm_statement(r['statement'])[:200]}".encode()).hexdigest()[:16]
        per_source[source] = len(recs)
        all_recs.extend(recs)
        print(f"  {source:<26} {len(recs):>6}")

    # 跨源重叠（归一化题面 top 配对）
    by_norm: dict[str, list[str]] = defaultdict(list)
    for r in all_recs:
        k = norm_statement(r["statement"])
        if len(k) >= 40:
            by_norm[k].append(r["source"])
    dup_pairs = Counter(tuple(sorted(set(v))) for v in by_norm.values() if len(set(v)) > 1)

    # 状态分布
    status_dist = Counter((r["status"] or "unknown").split()[0] for r in all_recs)

    summary = {
        "total_records": len(all_recs),
        "per_source": per_source,
        "status_distribution": dict(status_dist),
        "cross_source_overlap_sets": [{"pair": list(k), "count": v}
                                       for k, v in dup_pairs.most_common(15)],
        "overlap_record_count": sum(len(v) for v in by_norm.values() if len(set(v)) > 1),
    }
    record_chunks: list[bytes] = []
    record_total = 0
    for record in all_recs:
        try:
            chunk = (
                json.dumps(
                    record, ensure_ascii=False, allow_nan=False, separators=(",", ":")
                )
                + "\n"
            ).encode("utf-8")
        except (TypeError, ValueError, UnicodeEncodeError) as exc:
            raise RuntimeError("candidate records are not portable JSON") from exc
        record_total += len(chunk)
        if record_total > MAX_OUTPUT_BYTES:
            raise RuntimeError("candidate records exceed output size budget")
        record_chunks.append(chunk)
    records_bytes = b"".join(record_chunks)
    summary_bytes = json.dumps(
        summary, ensure_ascii=False, indent=1, allow_nan=False
    ).encode("utf-8")
    _atomic_write_output(OUT / "problems.jsonl", records_bytes)
    _atomic_write_output(OUT / "summary.json", summary_bytes)
    print("-" * 60)
    print(f"总记录 {summary['total_records']} | 状态分布 {status_dist}")
    print(f"跨源重叠（归一化题面>40字符）: {summary['overlap_record_count']} 条参与, 前几组:")
    for k in dup_pairs.most_common(8):
        print("  ", k[0], "x", k[1])
    print("输出:", OUT / "problems.jsonl")
    return 0


if __name__ == "__main__":
    # The legacy seven-field output is not an admission-safe contract. Keep the
    # extractors importable, but route CLI use to the versioned observation builder.
    from build_candidate_observations import main as build_main

    sys.exit(build_main())