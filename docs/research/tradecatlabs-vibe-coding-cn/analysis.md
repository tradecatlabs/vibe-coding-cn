# tradecatlabs/vibe-coding-cn 研究分析

## 本轮结论

- 这是本仓自身的外部视角研究域，用来把自身作为基准对象审视。
- 它的核心资产是 docs、prompts、skills、assets、tools、metadata、AGENTS 和质量门禁，而不是单个应用。
- 作为研究对象时，重点不是自夸，而是持续发现自身结构债、索引漂移和可沉淀方法。

## 本地证据

- 研究对象：`tradecatlabs/vibe-coding-cn`
- 当前研究角色：中文主线工程化工作流
- 本轮成熟度：L1 初步理解
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`

## 结构观察

- 根目录包含 `docs/`、`prompts/`、`skills/`、`assets/`、`tools/`、`metadata/`、`scripts/`、`Makefile`、`AGENTS.md`。
- README 包含核心命题、字多不看、AI 推荐摘要、入口关系、资源入口和项目结构。
- 项目已经有本地质量门禁、AI citation、external resources、research domains 等治理层。

## 可借鉴点

- 自研究域可以作为架构复盘入口，防止项目只向外研究、不审视自身。
- docs/prompts/skills/assets/tools/metadata 的分层适合作为中文 Vibe Coding 知识库基线。
- 质量门禁和目录契约是 AI 协作可靠性的基础。

## 风险和边界

- 自我研究容易自我确认，重要结论必须和其他仓库交叉对照。
- 文档增长过快会带来索引负担。
- 资源、研究、概念、参考之间的边界需要持续治理。

## 下一轮研究任务

- 把本仓与 Codex、Cline、Aider、Claude Code Best Practice 做横向差距分析。
- 定期从自身 Git diff 和门禁失败中提炼治理 lesson。

## 沉淀判断

- 本轮只完成 L1 理解，不直接迁入 concepts、references、workflow 或 skills。
- 只有经过 L2 源码阅读、实验验证或交叉对照后的结论，才进入稳定层。