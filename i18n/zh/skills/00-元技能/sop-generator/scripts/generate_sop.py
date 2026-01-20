#!/usr/bin/env python3
import argparse
from datetime import datetime
from pathlib import Path


def load_template(template_path: Path) -> str:
    return template_path.read_text(encoding="utf-8")


def render_template(template: str, values: dict) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="生成 SOP 模板（全量/最小版），输出到文件或标准输出"
    )
    parser.add_argument("--title", required=True, help="SOP 标题")
    parser.add_argument("--doc-id", default="SOP-000", help="文档编号")
    parser.add_argument("--version", default="v1.0", help="版本号")
    parser.add_argument("--date", default=None, help="发布日期（默认今天）")
    parser.add_argument("--owner", default="未指定", help="编制人")
    parser.add_argument("--reviewer", default="未指定", help="审核人")
    parser.add_argument("--approver", default="未指定", help="批准人")
    parser.add_argument(
        "--mvp",
        action="store_true",
        help="使用最小可行 SOP 模板（MVP）",
    )
    parser.add_argument(
        "--output",
        default="-",
        help="输出路径，使用 '-' 表示标准输出",
    )
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    script_dir = Path(__file__).resolve().parent
    assets_dir = script_dir.parent / "assets"
    template_file = assets_dir / ("sop-mvp.md" if args.mvp else "sop-template.md")

    if not template_file.exists():
        raise FileNotFoundError(f"找不到模板文件: {template_file}")

    date_value = args.date or datetime.now().strftime("%Y-%m-%d")
    values = {
        "title": args.title,
        "doc_id": args.doc_id,
        "version": args.version,
        "date": date_value,
        "owner": args.owner,
        "reviewer": args.reviewer,
        "approver": args.approver,
    }

    template = load_template(template_file)
    rendered = render_template(template, values)

    if args.output == "-":
        print(rendered)
        return

    output_path = Path(args.output)
    output_path.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
