# 研究域治理契约

## 目标

研究域不是资料夹，而是一个研究对象的可演化档案。它必须同时回答四件事：

- 这个对象是什么。
- 它为什么值得研究。
- 哪些事实已经核验，哪些只是判断或假设。
- 它最终应该沉淀到 concepts、references、workflow、skills 还是 archive。

`research/` 的长期形态是“研究对象网络”，不是“外部链接清单”。每个持续研究对象都必须有自己的目录、raw 原始事实层、事实摘要层、判断层和维护边界。

## 基本原则

### 一对象一研究域

一个研究域只承载一个稳定研究对象。外部仓库默认按“一仓库一研究域”建目录，目录名使用 `<owner>-<repo>` 的小写短横线形式。

允许的研究对象包括：

- 一个外部仓库。
- 一个工具、框架、模型、协议或工程范式。
- 一个可持续跟踪的技术主题。

不允许的研究域包括：

- 把多个仓库混在一起的“生态域”。
- 只有链接、没有判断的资源堆。
- 无法持续维护、无法验证、无法沉淀的临时兴趣点。

### 事实和判断分层

研究域内必须区分原始事实、事实摘要、判断、假设和决策：

| 类型 | 存放位置 | 要求 |
|:---|:---|:---|
| 原始事实 | `raw/` | 本地保存一手材料快照，不写分析判断 |
| 事实摘要 | `domain.yml` | 从 raw 或可信来源抽取，有来源、日期和可复查入口 |
| 判断 | `README.md` 或 `analysis.md` | 说明判断依据和适用边界 |
| 假设 | `analysis.md`、`experiments/` 或 TODO | 标注待验证条件 |
| 决策 | `decisions.md` 或下游稳定文档 | 说明采用、不采用或继续观察的理由 |

动态事实不能写死成永久结论。stars、forks、release、归档状态、维护活跃度、许可证和默认分支等字段只代表观测日快照。

### 研究必须可迁移

研究域不能停在“这个对象是什么”。进入 L1 以后，研究必须继续回答：

- 它为什么能产生结果。
- 哪些机制是真正有效部分。
- 哪些做法可以迁移到本仓。
- 哪些条件不能迁移，不能照搬。
- 本仓应该如何改良成自己的版本。
- 用什么最小动作验证迁移是否有效。

深度研究必须遵循“对标拆解 -> 改良迭代 -> 杂交创新”的转化链：

| 方法 | 研究问题 | 必备输出 |
|:---|:---|:---|
| 对标拆解 | 成熟对象为什么有效 | 参考对象、核心机制、可迁移做法、不可迁移条件、下一步试用动作 |
| 改良迭代 | 这个机制怎样适配本仓 | 改动点、验证指标、反馈信号和下一轮方向 |
| 杂交创新 | 多个成熟机制如何组合 | 来源机制、组合逻辑、适用条件、风险点和验证指标 |

如果一篇研究读完以后不能指导用户下一步行动，它还只是资料整理，不能算 L2 深度研究。

## 标准目录结构

每个长期研究域的推荐结构如下：

```text
<research-domain>/
├── README.md      # 判断层：定位、当前结论、使用方式和后续观察
├── AGENTS.md      # 维护层：本研究域边界、更新规则和验证命令
├── domain.yml     # 事实层：对象身份、动态快照、来源证据和维护策略
├── raw/           # 原始事实层：本地一手材料快照，不写判断
├── analysis.md    # 可选：结构化分析、采用评估、风险和替代方案
├── deep-dive.md   # 可选：L2 源码/结构深度研究、关键机制和可迁移模式
├── experiments/   # 可选：本地实验、验证记录和可复现命令
├── decisions.md   # 可选：采用、不采用、迁移或下沉决策
└── archive/       # 可选：失效观察、旧实验和被替代结论
```

外部仓库研究域的最低可合并形态是 `README.md`、`AGENTS.md`、`domain.yml` 和 `raw/`。其中 `raw/` 至少包含 `README.md`、`AGENTS.md`、`sources.yml`、`repository/` 和一个可复查的原始材料文件。没有这些文件的目录不能算完整研究域。

## 文件职责

### README.md

`README.md` 是研究域入口，面向人类读者。它只写当前判断，不堆外部项目 README 全文。

必须包含：

- 研究对象和研究角色。
- 当前优先级。
- 当前判断。
- 用户读完能拿走什么。
- 关键观察字段。
- 后续观察点。

不得包含：

- 未标注来源的动态事实。
- 大段复制的外部 README。
- 多个仓库的横向比较正文。
- 维护者规则；维护规则写入 `AGENTS.md`。

### AGENTS.md

`AGENTS.md` 是研究域维护规则，面向 AI Agent 和维护者。

必须说明：

- 本目录只研究哪个对象。
- 哪些内容只能写在 `domain.yml`。
- 哪些内容可以新增到 `analysis.md`、`experiments/` 或 `decisions.md`。
- 修改后需要运行的验证命令。
- 不能把本目录重新变成聚合域。

### domain.yml

`domain.yml` 是事实层和机器可读入口。

必填字段：

```yaml
version: 1
repo:
  name: owner/repo
  source_name: owner/repo
  url: https://github.com/owner/repo
research:
  domain_id: owner-repo
  domain_name: owner/repo 研究域
  primary_direction: coding-agent-tooling
  role: 研究角色
  priority: 1
  why_study: 研究理由
github_observed:
  observed_at: 'YYYY-MM-DD'
  source: gh repo view
  stars: 0
  forks: 0
  archived: false
  language: ''
  license: ''
  default_branch: ''
  pushed_at: ''
  updated_at: ''
  latest_release: ''
  homepage: ''
  topics: []
source_evidence:
  file: 来源文件
  line: 1
maintenance:
  fact_policy: 动态事实只代表 observed_at 当日快照，更新结论前必须重新核验。
  split_policy: 本目录已经是一等研究域；更深分析放入本目录新增文档。
```

非 GitHub 对象可以保留 `domain.yml`，但应把 `repo` 替换为对应对象身份，并用 `observed` 记录来源、日期和核验方式。

### raw/

`raw/` 是原始事实层，只保存拉取到本地的一手材料，不写分析判断。

GitHub 仓库研究域推荐包含：

```text
raw/
├── README.md                  # raw 层说明
├── AGENTS.md                  # raw 层维护规则
├── sources.yml                # 来源、拉取时间、命令和文件状态
├── repository/                # Git 仓库工作树，本地忽略，不提交进主仓
├── github-repo.raw.json       # GitHub 仓库元数据
├── github-readme.raw.md.txt   # GitHub README 原文快照
├── github-license.raw.txt     # license 原文快照；仓库无 license 时可不存在
├── github-root-contents.raw.json
├── github-languages.raw.json
└── github-latest-release.raw.json
```

`repository/` 是真实 Git 工作树，用来本地阅读源码、目录和历史入口；它由 `.gitignore` 忽略，不提交进主仓。原始 README 必须保存为 `.txt`，不要保存成 `.md`。原因是外部 README 常包含相对链接、图片和徽章路径，保存成 Markdown 会被本仓库链接检查误判为本地坏链。

刷新 GitHub 仓库 raw 层时运行：

```bash
python3 scripts/fetch-research-raw.py
```

只刷新单个研究域时传入目录名或 `owner/repo`：

```bash
python3 scripts/fetch-research-raw.py openai-codex
python3 scripts/fetch-research-raw.py openai/codex
```

raw 层拉取成功后，再把稳定事实摘要同步到 `domain.yml`；不要直接从记忆或二手总结更新 `domain.yml`。

### analysis.md

`analysis.md` 是迁移层，不是普通摘要。它必须把事实和判断转成可执行研究结论。

P1/P2 研究域的 `analysis.md` 必须包含：

- 本轮结论。
- 本地证据。
- 对标拆解。
- 改良迭代。
- 可迁移清单。
- 不可迁移清单。
- 验证动作。
- 沉淀判断。

其中“验证动作”必须同时写成功信号和失败信号，避免研究结论不可证伪。

## 成熟度分级

研究域按成熟度推进，不要求一次写满。

| 级别 | 名称 | 必备产物 | 判断标准 |
|:---|:---|:---|:---|
| L0 | 登记 | `README.md`、`AGENTS.md`、`domain.yml`、`raw/` | 对象身份清楚，原始材料已拉取到本地且来源可复查 |
| L1 | 理解 | `analysis.md` | 能解释架构、工作流、适用场景、风险和初步迁移方向 |
| L2 | 验证 | `deep-dive.md`、`experiments/` 或可复现验证记录 | 关键判断经过源码阅读、本地实验或一手资料核验，并能产出对标拆解、迁移边界和验证动作 |
| L3 | 沉淀 | 下游 concepts / references / workflow / skills 文档 | 研究结论已经变成稳定方法、模板、流程或技能 |
| L4 | 归档 | `archive/` 或归档说明 | 对象失效、被替代、已归档或不再值得跟踪 |

优先级决定维护频率：

- P1：关键研究对象；重要结论更新前必须重新核验动态事实。
- P2：重要参考对象；有新采用决策或明显生态变化时更新。
- P3：低频观察对象；只在引用、迁移或归档时更新。

## 新增研究域流程

1. 判断对象是否应该存在：能否持续研究、验证和沉淀。
2. 如果是外部仓库，使用 `<owner>-<repo>` 目录名。
3. 创建 `README.md`、`AGENTS.md`、`domain.yml` 三件套。
4. 运行 `python3 scripts/fetch-research-raw.py <domain>` 拉取 raw 原始材料。
5. 把稳定事实摘要放入 `domain.yml`，并写明 `observed_at` 和来源。
6. 更新 `research/README.md`、`docs/README.md`、`metadata/taxonomy.yml` 和 AI 引用索引。
7. 运行 `make sync-doc-toc` 和 `make test`。

## 横向比较规则

单个研究域只写单个对象。横向比较应放在：

- `research/README.md` 的索引判断中。
- 新增的独立对比文档中。
- `research-transfer-synthesis.md` 这样的迁移综合文档中。
- 成熟后迁入 `docs/references/` 或 `docs/concepts/`。

禁止为了比较方便把多个研究对象塞回同一个目录。

## 沉淀和归档规则

研究结论稳定后必须下沉，而不是长期停在 research：

- 概念和方法论进入 `docs/concepts/`。
- 工程模板、清单和技术栈判断进入 `docs/references/`。
- 开发流程和门禁进入 `docs/workflow/`。
- 可复用 Agent 能力进入 `skills/`。
- 只剩历史价值的观察进入本研究域 `archive/`，或在 `domain.yml.maintenance` 中说明归档原因。

研究域的最终目标不是越写越厚，而是把可复用结论迁移到稳定层，把失效内容及时归档。

## 最小验收清单

新增或重构研究域时，至少检查：

- 是否一个目录只研究一个对象。
- 是否存在 `README.md`、`AGENTS.md`、`domain.yml` 和 `raw/`。
- `raw/` 是否存在 `README.md`、`AGENTS.md`、`sources.yml`、`repository/` 和至少一个原始材料文件。
- 是否区分原始事实、事实摘要、判断、假设和决策。
- `analysis.md` 是否包含对标拆解、改良迭代、可迁移清单、不可迁移清单和验证动作。
- 动态事实是否有 `observed_at`、来源、核验方式和本地 raw 依据。
- 是否避免复制外部项目全文。
- 是否更新所有索引和机器可读入口。
- 是否通过 `make sync-doc-toc` 和 `make test`。
