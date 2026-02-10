# AGENTS.md（i18n/zh/skills/05-生产力）

本目录用于收纳「生产力类」技能：偏向内容生产、格式转换与交付物构建。

## 目录结构

```text
i18n/zh/skills/05-生产力/
├── AGENTS.md
└── markdown-to-epub/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── scripts/
        └── build_epub.py
```

## 模块职责与边界

- `markdown-to-epub/`：将 Markdown 手稿 + 本地图片资产稳定转换为 EPUB，并做最小可用的完整性校验。
  - `markdown-to-epub/SKILL.md`：面向使用者的入口文档（触发条件、边界、快速上手、排错）。
  - `markdown-to-epub/agents/openai.yaml`：Codex Skill 的交互入口元数据（展示名、默认提示语）。
  - `markdown-to-epub/scripts/build_epub.py`：核心实现脚本（重写图片引用、拷贝资产、调用 `ebook-convert`、输出报告）。

## 依赖与上下游

- 上游输入：Markdown 手稿文件、同目录或指定根目录下的本地图片。
- 外部依赖：Calibre `ebook-convert`（用于实际转换）。
- 下游输出：EPUB 文件 + `build_dir/` 工作目录（规范化 Markdown、assets、转换日志、报告 JSON）。

