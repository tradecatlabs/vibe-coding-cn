---
name: markdown-to-epub
description: "将 Markdown 手稿与本地图片资产转换为可校验的 EPUB：修复/归一化图片引用与扩展名，保持标题层级 TOC，并做基础包结构检查。"
---

# markdown-to-epub Skill

把 Markdown 手稿（含本地图片）稳定构建为 EPUB：规范化图片引用、拷贝资产到可重复的构建目录、调用 Calibre `ebook-convert` 转换，并输出可核查报告。

## When to Use This Skill

触发条件（满足其一即可）：
- 需要把一份（或多份）Markdown 手稿打包交付为 EPUB。
- 图片引用混乱（URL 编码、路径飘忽、扩展名不可信如 `.bin/.idunno`），需要自动归一化。
- 需要在转换后做最基本的 EPUB 包结构检查（OPF/NCX/NAV、图片数量等）。

## Not For / Boundaries

- 不负责生成/改写正文内容（不会修改源手稿，只在构建目录里产出规范化版本）。
- 不下载远程图片（`http(s)`/`data:` 引用会保持原样）。
- 不替代真正的排版/校对流程（这里只做可交付构建与结构验证）。

## Quick Start

从仓库根目录执行（推荐 `python3`）：

```bash
python3 assets/skills/markdown-to-epub/scripts/build_epub.py \
  --input-md "./book.md" \
  --output-epub "./book.epub" \
  --title "Book Title" \
  --authors "Author Name" \
  --language "zh-CN"
```

脚本会创建构建工作区（默认 `build_epub/`），包含：
- `book.normalized.md`
- `assets/`：拷贝后的图片（会按真实文件签名推断扩展名）
- `conversion.log`
- `report.json`

## 依赖

- 需要安装 Calibre，并确保 `ebook-convert` 在 `PATH` 中（或用 `--ebook-convert-bin` 指定路径）。

## Missing Asset Recovery

如果 Markdown 里引用了图片但文件找不到，可以提供一个 JSON 映射表（按「basename」匹配）：

```json
{
  "missing-file.idunno": "replacement-file.idunno"
}
```

然后重跑（示例）：

```bash
python3 assets/skills/markdown-to-epub/scripts/build_epub.py \
  --input-md "./book.md" \
  --output-epub "./book.epub" \
  --fallback-map "./fallback-map.json"
```

## Operational Rules

- 优先使用 `ebook-convert`；缺失时明确报错并快速失败。
- 源手稿只读；所有输出写入 `build_dir/`。
- TOC 以标题层级（`h1/h2/h3`）为准。
- 缺失资产必须显式报告；严格模式下不允许静默跳过。
- 命令保持非交互式。

## Script Interface

`scripts/build_epub.py` 参数：
- `--input-md`（必选）：源 Markdown 路径
- `--output-epub`（可选）：输出 EPUB 路径，默认 `<input-stem>.epub`
- `--source-root`（可选）：解析图片引用的根目录，默认使用 Markdown 所在目录
- `--build-dir`（可选）：构建工作区目录，默认 `<cwd>/build_epub`
- `--fallback-map`（可选）：JSON 映射（缺失图片 basename → 替换 basename）
- `--title` / `--authors` / `--language`：传给 `ebook-convert` 的元数据
- `--input-encoding`：输入 Markdown 编码，默认 `utf-8`
- `--strict-missing`：严格模式（有任何本地图片无法解析则失败，默认开启）
- `--no-strict-missing`：关闭严格模式（保留未解析链接，继续转换）
- `--ebook-convert-bin`：`ebook-convert` 可执行文件名/路径，默认 `ebook-convert`

## Validation Checklist

- 确认 EPUB 文件生成且大小不是「几 KB 的空壳」。
- 确认 EPUB（zip）内包含 OPF 与 NCX/NAV。
- 确认 EPUB 内图片数量不低于对手稿的预期。
- 严格模式下确认 `report.json` 的 `missing_images` 为空。
