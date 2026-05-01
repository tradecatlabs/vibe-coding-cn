#!/usr/bin/env python3
"""
Build a robust EPUB from Markdown with local image assets.

Features:
- Normalize Markdown image references into build_dir/assets
- Detect real image extensions from file signatures (.png/.jpg/.gif/.webp/.svg)
- Optionally resolve missing files via fallback JSON map
- Convert using Calibre ebook-convert
- Emit conversion report JSON for verification
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
import zipfile
from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path
from typing import Dict, List, Optional, Tuple


IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
REMOTE_PREFIXES = ("http://", "https://", "data:")
VALID_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp"}


@dataclass
class RewriteResult:
    normalized_markdown: Path
    assets_dir: Path
    total_refs: int
    rewritten_refs: int
    copied_assets: int
    missing_images: List[str]


def detect_extension(file_path: Path, data: bytes) -> str:
    lower_name = file_path.name.lower()
    if lower_name.endswith(".svg"):
        return ".svg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return ".gif"
    if data.startswith(b"RIFF") and len(data) >= 12 and data[8:12] == b"WEBP":
        return ".webp"
    if data.startswith(b"BM"):
        return ".bmp"
    current_ext = file_path.suffix.lower()
    if current_ext in VALID_IMAGE_EXTS:
        return current_ext
    return ".bin"


def decode_reference(reference: str) -> str:
    return urllib.parse.unquote(reference.strip())


def resolve_source_file(
    source_root: Path,
    decoded_ref: str,
    fallback_map: Dict[str, str],
) -> Tuple[Optional[Path], str]:
    decoded_ref = decoded_ref.replace("\\", "/")
    basename = Path(decoded_ref).name
    candidates = []

    # Keep relative path when possible.
    rel_path = Path(decoded_ref)
    if not rel_path.is_absolute():
        candidates.append((source_root / rel_path).resolve())

    # Common exported markdown style: "<folder>/<asset>"
    if "/" in decoded_ref:
        candidates.append((source_root / basename).resolve())

    # Direct basename fallback.
    candidates.append((source_root / basename).resolve())

    checked = set()
    for candidate in candidates:
        key = str(candidate).lower()
        if key in checked:
            continue
        checked.add(key)
        if candidate.exists() and candidate.is_file():
            return candidate, basename

    fallback_name = fallback_map.get(basename)
    if fallback_name:
        fallback_candidate = (source_root / fallback_name).resolve()
        if fallback_candidate.exists() and fallback_candidate.is_file():
            return fallback_candidate, basename

    return None, basename


def rewrite_markdown_and_copy_assets(
    input_md: Path,
    source_root: Path,
    build_dir: Path,
    input_encoding: str,
    fallback_map: Dict[str, str],
    strict_missing: bool,
) -> RewriteResult:
    assets_dir = build_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    text = input_md.read_text(encoding=input_encoding)
    copied_name_by_source: Dict[str, str] = {}
    missing_images: List[str] = []
    total_refs = 0
    rewritten_refs = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal total_refs, rewritten_refs
        total_refs += 1
        alt_text = match.group(1)
        original_ref = match.group(2).strip()

        if original_ref.lower().startswith(REMOTE_PREFIXES):
            return match.group(0)

        decoded = decode_reference(original_ref)
        source_file, missing_name = resolve_source_file(source_root, decoded, fallback_map)
        if source_file is None:
            missing_images.append(missing_name)
            return match.group(0)

        source_key = str(source_file.resolve()).lower()
        if source_key in copied_name_by_source:
            target_name = copied_name_by_source[source_key]
        else:
            data = source_file.read_bytes()
            ext = detect_extension(source_file, data)
            target_name = f"{source_file.stem}{ext}"
            target_path = assets_dir / target_name
            if target_path.exists():
                existing_data = target_path.read_bytes()
                if existing_data != data:
                    digest = sha1(data).hexdigest()[:8]
                    target_name = f"{source_file.stem}-{digest}{ext}"
                    target_path = assets_dir / target_name
            target_path.write_bytes(data)
            copied_name_by_source[source_key] = target_name

        rewritten_refs += 1
        return f"![{alt_text}](assets/{target_name})"

    rewritten = IMAGE_PATTERN.sub(replace, text)
    normalized_md = build_dir / "book.normalized.md"
    normalized_md.write_text(rewritten, encoding="utf-8")

    unique_missing = sorted(set(missing_images))
    if strict_missing and unique_missing:
        msg = (
            "Missing local image files detected. "
            f"Count={len(unique_missing)}; examples={unique_missing[:10]}"
        )
        raise FileNotFoundError(msg)

    return RewriteResult(
        normalized_markdown=normalized_md,
        assets_dir=assets_dir,
        total_refs=total_refs,
        rewritten_refs=rewritten_refs,
        copied_assets=len(copied_name_by_source),
        missing_images=unique_missing,
    )


def run_ebook_convert(
    ebook_convert_bin: str,
    normalized_md: Path,
    output_epub: Path,
    title: Optional[str],
    authors: Optional[str],
    language: Optional[str],
    input_encoding: str,
    conversion_log: Path,
) -> None:
    cmd = [
        ebook_convert_bin,
        str(normalized_md),
        str(output_epub),
        "--input-encoding",
        input_encoding,
        "--level1-toc",
        "//h:h1",
        "--level2-toc",
        "//h:h2",
        "--level3-toc",
        "//h:h3",
    ]

    if title:
        cmd.extend(["--title", title])
    if authors:
        cmd.extend(["--authors", authors])
    if language:
        cmd.extend(["--language", language])

    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    conversion_log.write_text(
        "\n".join(
            [
                f"COMMAND: {' '.join(cmd)}",
                "",
                "STDOUT:",
                proc.stdout,
                "",
                "STDERR:",
                proc.stderr,
                "",
                f"EXIT_CODE: {proc.returncode}",
            ]
        ),
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ebook-convert failed with exit code {proc.returncode}")


def inspect_epub(epub_file: Path) -> Dict[str, object]:
    if not epub_file.exists():
        raise FileNotFoundError(f"EPUB not found: {epub_file}")

    with zipfile.ZipFile(epub_file) as zf:
        names = zf.namelist()
        image_files = [
            n for n in names if re.search(r"\.(png|jpg|jpeg|gif|svg|webp|bmp)$", n, flags=re.IGNORECASE)
        ]
        has_opf = any(n.lower().endswith(".opf") for n in names)
        has_ncx_or_nav = any(n.lower().endswith(".ncx") or "nav" in n.lower() for n in names)
        nav_points = 0
        for name in names:
            if name.lower().endswith(".ncx"):
                content = zf.read(name).decode("utf-8", errors="ignore")
                nav_points = len(re.findall(r"<navPoint\b", content))
                break

    return {
        "file_size": epub_file.stat().st_size,
        "total_files": len(names),
        "image_files": len(image_files),
        "has_opf": has_opf,
        "has_ncx_or_nav": has_ncx_or_nav,
        "ncx_nav_points": nav_points,
    }


def load_fallback_map(path: Optional[Path]) -> Dict[str, str]:
    if path is None:
        return {}
    content = path.read_text(encoding="utf-8-sig")
    raw = json.loads(content)
    if not isinstance(raw, dict):
        raise ValueError("--fallback-map must be a JSON object")
    output: Dict[str, str] = {}
    for key, value in raw.items():
        if isinstance(key, str) and isinstance(value, str):
            output[key] = value
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从 Markdown 与本地图片资产构建 EPUB。")
    parser.add_argument("--input-md", required=True, type=Path, help="源 Markdown 路径。")
    parser.add_argument(
        "--output-epub",
        type=Path,
        help="输出 EPUB 路径。默认：当前目录下的 <input-stem>.epub。",
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        help="解析图片引用的根目录。默认：Markdown 所在目录。",
    )
    parser.add_argument(
        "--build-dir",
        type=Path,
        default=Path.cwd() / "build_epub",
        help="构建工作区目录（规范化 Markdown / assets / 日志 / 报告）。",
    )
    parser.add_argument(
        "--fallback-map",
        type=Path,
        help="JSON 映射：缺失图片 basename → 替换 basename。",
    )
    parser.add_argument("--title", help="EPUB 标题元数据。")
    parser.add_argument("--authors", help="EPUB 作者元数据。")
    parser.add_argument("--language", default="zh-CN", help="EPUB 语言元数据。")
    parser.add_argument("--input-encoding", default="utf-8", help="输入 Markdown 编码。")
    parser.add_argument("--ebook-convert-bin", default="ebook-convert", help="ebook-convert 可执行文件名/路径。")
    parser.add_argument(
        "--strict-missing",
        action="store_true",
        default=True,
        help="严格模式：任何本地图片无法解析则失败（默认开启）。",
    )
    parser.add_argument(
        "--no-strict-missing",
        action="store_false",
        dest="strict_missing",
        help="关闭严格模式：即使存在未解析的本地图片引用也继续转换。",
    )
    parser.add_argument(
        "--clean-build-dir",
        action="store_true",
        help="转换前清空 build-dir。",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    input_md = args.input_md.resolve()
    if not input_md.exists():
        raise FileNotFoundError(f"Markdown not found: {input_md}")

    output_epub = (
        args.output_epub.resolve()
        if args.output_epub
        else (Path.cwd() / f"{input_md.stem}.epub").resolve()
    )
    source_root = args.source_root.resolve() if args.source_root else input_md.parent.resolve()
    build_dir = args.build_dir.resolve()

    if args.clean_build_dir and build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)

    fallback_map = load_fallback_map(args.fallback_map.resolve() if args.fallback_map else None)

    rewrite_result = rewrite_markdown_and_copy_assets(
        input_md=input_md,
        source_root=source_root,
        build_dir=build_dir,
        input_encoding=args.input_encoding,
        fallback_map=fallback_map,
        strict_missing=args.strict_missing,
    )

    conversion_log = build_dir / "conversion.log"
    run_ebook_convert(
        ebook_convert_bin=args.ebook_convert_bin,
        normalized_md=rewrite_result.normalized_markdown,
        output_epub=output_epub,
        title=args.title,
        authors=args.authors,
        language=args.language,
        input_encoding="utf-8",
        conversion_log=conversion_log,
    )

    epub_info = inspect_epub(output_epub)
    report = {
        "input_markdown": str(input_md),
        "output_epub": str(output_epub),
        "build_dir": str(build_dir),
        "total_image_refs": rewrite_result.total_refs,
        "rewritten_image_refs": rewrite_result.rewritten_refs,
        "copied_assets": rewrite_result.copied_assets,
        "missing_images": rewrite_result.missing_images,
        "epub": epub_info,
    }
    report_path = build_dir / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(f"错误：{exc}", file=sys.stderr)
        raise
