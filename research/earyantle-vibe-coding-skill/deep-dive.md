# earyantLe/vibe-coding-skill 深度研究

## 研究级别

- 当前级别：L2 结构深度研究。
- 研究对象：`earyantLe/vibe-coding-skill`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、README 快照、Skill 包和 references 工作树。
- 观察日期：2026-07-03。

## L2 结论

`earyantLe/vibe-coding-skill` 的核心价值是一个最小 Skill 产品化样本。它把 Vibe Coding 方法压成
`SKILL.md`、`references/`、`PUBLISH.md` 和 `SUBMISSION.md`，展示了“方法论如何变成可安装、
可触发、可交付的 Agent 能力包”。

对本仓最重要的启发是：Skill 不应该只是长 prompt。成熟 Skill 至少要包含触发条件、边界约束、
工作流、参考资料、质量检查和发布契约。

## 本地证据

- `raw/repository/SKILL.md`：Skill 主入口，包含触发条件、约束和工作流。
- `raw/repository/references/index.md`：参考资料索引，说明 Skill 可通过 references 分层读取。
- `raw/repository/references/workflow.md`：工作流资料。
- `raw/repository/references/quality-checklist.md`：质量检查资料。
- `raw/repository/references/glue-coding.md`：胶水式编码理念资料。
- `raw/repository/PUBLISH.md`：发布说明。
- `raw/repository/SUBMISSION.md`：提交说明。
- `domain.yml`：当前优先级为 P3，研究方向为 `workflow-methodology`。

## 关键机制

### Skill 是可分发能力包

该仓库不是只写一篇方法论文章，而是用 `SKILL.md` 承载入口，用 references 承载展开资料，用
发布/提交文档承载交付边界。这让经验从“读过”变成“可被 Agent 调用”。

### 主入口和参考资料分层

`SKILL.md` 负责触发和工作流，`references/` 负责细节。这个结构适合避免 Skill 主入口过长，
同时保留深度材料。

### 质量检查前置

`quality-checklist.md` 把质量要求显式化，说明 Skill 的交付不是生成文本结束，而是要形成检查项。

## 可迁移模式

- 为本仓 Skill 建立最小发布契约：触发条件、输入、输出、边界、验证和引用资料。
- 将长方法论拆成 `SKILL.md` 主入口和 `references/` 细节。
- 为 Skill 增加质量检查清单，防止只生成过程不验证结果。
- 将“是否应该成为 Skill”作为存在性门禁，避免把每条经验都拆成独立 Skill。
- 在 `skills/README.md` 或 Skill 契约中明确发布、归档和替代入口。

## 对本仓的影响

本仓已经有 `skills/`，但经验和 Skill 之间仍需要更硬的迁移规则。该对象提示我们：

- 经验短句不能直接等于 Skill，必须先证明可重复触发、可验证、可边界化。
- Skill 主入口要短，细节放 references，避免上下文污染。
- Skill 需要发布检查和归档策略，否则会变成 prompt 杂物间。
- `auto-skill` 和项目内技能库可以吸收这个结构，但不需要照搬其具体方法论表达。

## 风险和待验证项

- 仓库规模很小，stars、forks 和社区反馈不足，不能单独支撑通用标准。
- 缺少许可证信息，引用或复制内容前必须核验授权。
- Skill 是否有效需要实际任务集验证，不能只看结构。
- 本仓已有更复杂的 skill 体系，迁移时应只吸收发布契约和分层方式。

## 下一步 L3 验证任务

- 为本仓新增一份 Skill 发布检查清单，覆盖触发、输入、输出、边界、验证和归档。
- 抽样 3 个现有 Skill，检查主入口是否过长、references 是否足够分层。
- 为“经验 -> Skill”建立升级条件：高频、可重复、可验证、边界清晰。
- 给每个新增 Skill 增加失败信号：什么情况下不应调用该 Skill。
