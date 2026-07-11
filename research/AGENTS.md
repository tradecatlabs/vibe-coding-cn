# Research 目录 Agent 指南

## 目录职责

`research/` 存放新技术、新技术栈、优秀 repo、工程范式和工具趋势的研究对象与短篇研究。

这里的文档回答：

- 它是什么。
- 它解决什么问题。
- 为什么值得关注。
- 适合什么场景。
- 有什么风险和替代方案。

## 文件地图

```text
research/
├── README.md  # 索引入口：研究对象与研究笔记导航
├── research-domain-contract.md  # 研究域治理契约：结构、分层、成熟度、证据和归档规则
├── research-value-application-map.md  # 研究价值与应用地图：用户价值、核心启示和下沉路线
├── research-transfer-synthesis.md  # 研究迁移综合：对标拆解、改良迭代、杂交创新和验证动作
├── harness/
│   ├── README.md
│   ├── harness-engineering.md
│   └── AGENTS.md
├── ai-for-developers-awesome-vibe-coding/
│   ├── README.md
│   ├── domain.yml
│   ├── analysis.md
│   ├── raw/
│   └── AGENTS.md
├── aider-ai-aider/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── cline-cline/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── daotin-ai-coding/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── datawhalechina-easy-vibe/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── datawhalechina-vibe-vibe/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── earyantle-vibe-coding-skill/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── filipecalegario-awesome-vibe-coding/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── hesreallyhim-awesome-claude-code/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── liyupi-ai-guide/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── luzhenqian-ai-coding-lab/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── openai-codex/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── roocodeinc-roo-code/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── shanraisshan-claude-code-best-practice/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── shouzhengai-cs146s-cn/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── tradecatlabs-vibe-coding-cn/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── wendy7756-vibe-coding-guide/
│   ├── README.md
│   ├── domain.yml
│   └── AGENTS.md
├── tmux-ai-swarm.md
└── AGENTS.md  # 本目录操作规则
```

上方只展开了第一个外部仓库研究域的基础形态；所有外部仓库研究域都必须包含同样的原始事实层、
`analysis.md` 和 `deep-dive.md`。
`deep-dive.md` 是 L2 产物；当前 17 个外部仓库研究域已经全部补齐，P3 只表示采用优先级低，
不再表示研究深度缺口。

## 修改规则

- 继承 `docs/AGENTS.md` 的 README 结构契约：H1 后直接进入 `## 字多不看`，再按 `快速导航 -> 完整细粒度目录 -> 使用方式 -> 正文` 排列。
- 长期研究域必须遵循 `research-domain-contract.md`；外部仓库研究域至少包含 `README.md`、`AGENTS.md`、`domain.yml` 和 `raw/`。
- 长期研究对象优先使用独立目录；目录内必须包含 `README.md` 和 `AGENTS.md`。
- 外部仓库研究对象采用“一仓库一研究域”，目录名使用 `<owner>-<repo>` 的小写短横线形式。
- `raw/` 是原始事实层，只保存拉取到本地的一手材料；分析判断写入上一级 `README.md`、`analysis.md` 或 `decisions.md`。
- `raw/repository/` 是外部仓库快照，只作为本地事实缓存；不提交到主仓、不按本仓 Markdown 风格重写，并从 lint、链接和目录文档门禁中排除。
- `research-value-application-map.md` 是研究体系的转化入口，用于说明研究给用户带来的价值、启示、应用位置和下沉路线。
- `research-transfer-synthesis.md` 是横向迁移入口，用于把研究对象拆成机制、迁移边界、改良动作和验证指标。
- GitHub 仓库 raw 层通过 `python3 scripts/fetch-research-raw.py` 刷新；不要手工改写 `*.raw.*` 文件。
- 单次短篇观察可以先写成独立 `.md` 文档；如果对象会持续演化，应迁入对象目录。
- 新增研究对象目录或研究 `.md` 文件时，必须同步更新 `README.md`、`metadata/taxonomy.yml` 和必要的 `redirects.yml`。
- 研究内容稳定后，放入 `docs/concepts/`、`docs/references/` 或 `docs/philosophy/` 的对应章节。
- 外部项目、模型、工具、版本和事实状态可能变化，涉及最新信息时必须核验来源。
- 不在 README 正文中写 `和其他目录的边界` 或 `维护规则`；维护者规则只写本文件。

## 质量要求

- 不写新闻转述，要给出判断、边界、采用建议和后续观察点。
- L2 研究不能只写“可借鉴点”，必须写清对标拆解、可迁移做法、不可迁移条件、下一步试用动作和验证指标。
- 对不确定信息标注“待验证”或 TODO。
- 引入外部事实时优先引用官方文档、原始仓库、论文或可信一手来源。
- 修改后必须运行 `make sync-doc-toc` 和 `make test`。
