# vibemathing/vibe-mathing-cn-public 研究域

## 字多不看

- 这是一个独立的数学研究与验证工作台，不是当前项目的运行依赖。
- 源仓库继续在原位置开发；本目录只保存 `main` 的安全快照和研究判断。
- 快照不包含源仓库 `.git`、未提交内容、缓存、运行产物或私密材料。
- 源仓库当前文件已通过自身质量检查；其旧 Git 历史曾出现本机路径记录，但历史不纳入本快照。
- 当前建议：作为 L2 研究对象观察，不自动启用其中的 Codex skills 或外部命令。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 源仓库身份、动态事实和维护策略。 |
| [analysis.md](analysis.md) | 结构化研究、迁移价值、风险和采用判断。 |
| [deep-dive.md](deep-dive.md) | 源码结构、验证闭环和可迁移机制的深度研究。 |
| [IMPORT_MANIFEST.yml](IMPORT_MANIFEST.yml) | 本次快照的提交号、树哈希、过滤规则和审计结论。 |
| [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) | 快照内第三方材料的来源和许可证边界。 |
| [AGENTS.md](AGENTS.md) | 本研究域的同步和维护规则。 |
| [snapshot/](snapshot/) | 从源仓库 `main` 复制的已提交文件快照。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 源仓库身份、动态事实和维护策略。
- [analysis.md](analysis.md) - 结构化研究、迁移价值、风险和采用判断。
- [deep-dive.md](deep-dive.md) - 源码结构、验证闭环和可迁移机制的深度研究。
- [IMPORT_MANIFEST.yml](IMPORT_MANIFEST.yml) - 快照提交、树哈希、过滤规则和审计结论。
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) - 第三方材料的来源和许可证边界。
- [AGENTS.md](AGENTS.md) - 本研究域的同步和维护规则。
- [snapshot/](snapshot/) - 当前 `main` 的安全文件快照。

</details>

## 使用方式

- 先读本页判断，再读 `analysis.md` 和 `deep-dive.md`。
- 需要核对源仓库动态事实时，读取 `raw/` 的一手材料，并重新访问源仓库。
- 需要更新快照时，只从源仓库已提交的 `main` 生成，不直接修改 `snapshot/`。
- `snapshot/.codex/skills/` 只作为研究资料，不进入当前项目顶层 `skills/`，也不自动执行其中的命令。
- 研究结论稳定后，再决定是否下沉到当前项目的 concepts、references、workflow 或 skills。

## 正文

### 研究定位

`vibemathing/vibe-mathing-cn-public` 是一个把数学问题、研究尝试、结果和验证证据组织成可追溯工作流的公开工程。它重点研究 ProblemContract、CandidateObservation、Result 证据闭环、SymPy/SMT/Lean 工具边界以及公共发布安全。

### 当前审计结论

- 源仓库 `main` 当前提交为 `0a934de9cd445a1bad7218e7def5a2a2879a0465`，工作树干净。
- 源仓库自己的 `bash scripts/check.sh` 已通过。
- 当前 `main` 文件快照未发现本机私人路径、硬编码凭据、私钥或 Token。
- 源仓库旧 Git 历史存在本机路径记录；本研究域不复制 `.git` 和源历史，因此不会把该记录带入当前项目。
- 当前项目只检查和阅读快照，不把它当作可执行的生产依赖。

### 研究价值

最值得研究的不是数学结果本身，而是它把“模型提出候选”与“系统承认证据”分开的工程方式：问题契约、受限运行时、证据回执、失败语义和公开边界共同限制了自动化系统的过度宣称。

### 后续观察

- 证据链能否在更多数学领域保持可复现和可反驳。
- 工具成熟度、资源预算和失败回执能否沉淀为当前项目通用的 Agent 门禁。
- 外部问题目录、文献缓存和第三方 skills 的许可证与数据边界是否持续清楚。
- 研究结论是否能形成当前项目的稳定 workflow 或 quality gate，而不是只增加目录体积。
