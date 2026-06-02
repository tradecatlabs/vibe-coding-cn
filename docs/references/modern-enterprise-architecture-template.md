# 现代企业数字化平台架构说明文档

**文档版本**：V2.43
**适用对象**：企业管理层、产品负责人、架构师、研发负责人、数据负责人、平台团队、安全合规团队
**适用范围**：中大型企业数字化平台建设、业务系统重构、平台工程建设、数据产品化、组织协同机制设计
**文档定位**：本文件用于说明现代企业数字化平台的总体架构、核心组成、团队职责、治理机制、技术原则和落地路径。
**专项修订**：V2.43 在 V2.42 基础上新增基线生命周期状态机，把 `draft`、`candidate`、`baseline`、`frozen`、`emergency-patch`、`superseded` 和 `eol` 的允许迁移、禁止迁移、门禁证据、审批责任和状态回写统一为可执行版本控制协议。

---

## 0. 文档版本控制与发布治理

本文件从 V1.6 起按企业架构基线文档管理。版本号不是装饰字段，而是用于控制“哪些内容已经形成基线、哪些仍在评审、哪些变更会影响团队执行”的治理入口。

版本治理目标：

1. 让管理层、架构组、平台团队、领域团队、数据团队、安全团队和 AI 团队引用同一份基线。
2. 让每次架构升级都有变更范围、影响面、审批责任和验证证据。
3. 避免文档持续堆内容但没有稳定版本，导致执行团队不知道该按哪一版落地。
4. 为后续把蓝图升级为可执行企业标准、模板、契约和自动化门禁保留演进路径。

### 0.1 版本语义

| 版本形态 | 含义 | 使用条件 |
| -------- | ---- | -------- |
| `V0.x` | 研究草案版 | 用于概念探索、资料整理和内部讨论，不作为企业执行基线 |
| `V1.x` | 正式蓝图迭代版 | 架构原则、分层、职责边界和治理方向已经稳定，可用于方案评审和试点规划 |
| `V1.x.y` | 勘误和补丁版 | 只修正文案、链接、格式、局部示例或不改变执行含义的小问题 |
| `V2.x` | 可执行企业标准版 | 必须具备模板、契约、门禁、RACI、自动化校验和落地 starter kit |
| `V3.0` | 组织级规模化运营版 | 已与平台门户、catalog、GitOps、成本、审计和运行指标形成闭环 |

版本升级规则：

1. 只改错别字、格式、链接和引用，不提升主版本，可使用补丁记录。
2. 新增章节、职责边界、治理要求、技术基线或路线图，提升当前主版本的小版本。
3. 改变目录真相源、团队职责、发布准入、风险等级或运行边界，必须提升小版本并记录影响面。
4. 改变执行模型、组织模型、平台边界或兼容策略，必须进入架构评审并形成 ADR。
5. 升级到 `V2.0` 前，必须证明本文档不只是说明文，而是能被仓库模板、机器契约和 CI 门禁执行。

### 0.2 发布状态

| 状态 | 含义 | 允许动作 |
| ---- | ---- | -------- |
| `Draft` | 草案，内容仍在探索 | 可频繁修改，但不得作为执行口径 |
| `Review` | 评审中，内容需要架构组和相关 owner 确认 | 允许修改，但必须保留评审意见和待决问题 |
| `Baseline Candidate` | 基线候选，已具备执行口径但仍待正式会审确认 | 可用于试点和评审，不应用作冻结审计口径 |
| `Baseline` | 已形成基线，可作为试点或项目规划依据 | 只能通过受控变更更新 |
| `Frozen` | 冻结基线，通常用于招标、审计、监管或大规模推广 | 除勘误和安全修复外不得直接修改 |
| `Superseded` | 已被新版本替代 | 只保留引用和迁移说明，不再作为新项目依据 |

当前版本状态：

| 版本 | 状态 | 说明 |
| ---- | ---- | ---- |
| `V2.43` | `Baseline Candidate` | 用作可执行企业标准起点；包含机器可读版本清单、控制项覆盖清单、76 组 starter kit schema/example、基线生命周期状态机、基线就绪评分卡、基线例外总账、基线回滚验证记录、基线通知确认总账、基线验证环境锁定、基线制品清单、基线符合性声明、基线发布列车、基线支持矩阵、基线采纳总账、基线兼容性总账、基线发布证据包、版本控制面、外部标准版本锁定、企业执行控制面、合规等级、门禁决策、证据新鲜度、例外放行、break-glass、季度复核、仓库变更控制、远端保护漂移整改、控制证据映射、审计导出清单、审计导出自动化、控制评估报告、架构基线变更记录、架构决策记录、AI 证据账本、微调运行证据、AI 事件响应 playbook、OSCAL 交换映射、POA&M 整改计划、企业架构风险登记、审计导出门禁、审计导出完整性清单、审计导出 provenance statement、审计导出签名策略、审计导出签名验签回执、严格 schema 模式、访问复核、密钥轮换、漏洞修复、事故复盘、可靠性、数据治理、AI 运行、GitOps 安全、供应链证据链一致性和自动化校验入口 |

### 0.3 变更分级

| 变更级别 | 典型内容 | 审批要求 | 版本影响 |
| -------- | -------- | -------- | -------- |
| `Editorial` | 错别字、排版、链接、术语统一 | 文档 owner 自审 | 不提升主版本，可记录补丁 |
| `Minor` | 新增示例、补充说明、局部增强，不改变团队职责 | 文档 owner 和相关章节 owner 确认 | 提升 `V1.x` 或记录补丁 |
| `Major` | 新增架构层、治理门禁、组织职责、发布流程或运行边界 | 架构组、平台、数据、安全、AI 或受影响领域 owner 评审 | 提升 `V1.x` |
| `Breaking` | 改变真相源、团队职责、契约兼容、发布准入或迁移路径 | 企业架构评审；必须有 ADR、迁移计划和弃用策略 | 进入下一主版本或明确迁移版本 |

### 0.4 版本发布证据

每次提升版本前，至少保留以下证据：

1. 变更摘要：说明新增、修改、删除和废弃内容。
2. 影响范围：列出受影响的架构层、目录、团队、契约、门禁和落地流程。
3. 决策记录：重大变更必须链接 ADR 或评审记录。
4. 版本清单：同步更新 `内部版本清单`，并让 CI 校验版本、状态、pair 数量、控制项数量和索引提及。
5. 控制覆盖：同步更新 `内部控制项覆盖清单`，并让 CI 校验控制项到 schema、example 和 checker 证据链。
6. 索引同步：同步更新 `docs/README.md`、`docs/references/README.md`、`metadata/taxonomy.yml` 和 AI 引用语料入口。
7. 链接校验：仓库内 Markdown 链接和锚点必须通过检查。
8. 格式校验：Markdown lint 和文档结构检查必须通过。
9. 回滚入口：保留上一版本引用、Git commit 或变更记录，保证可以回退到上一基线。

V2.31 起，生产基线发布还必须形成 `baseline-release-evidence.yaml`。它不是普通 release note，而是晋级、冻结和复核的证据包，用于证明当前基线与版本控制面、控制覆盖、标准基线、审计导出和远端保护状态一致。

V2.32 起，任何 `Major`、`Breaking` 或带迁移窗口的 `Minor` 基线还必须形成 `baseline-compatibility-ledger.yaml`。它用于证明消费者影响已经识别，迁移状态可以跟踪，未迁移对象已经进入例外、POA&M 或风险接受。

V2.33 起，企业级基线还必须形成 `baseline-adoption-ledger.yaml`。它用于证明哪些领域、平台、数据产品、AI 产品、GitOps 环境和生产资产已经采用当前基线，哪些仍在迁移、逾期、例外或整改。

V2.34 起，企业级基线还必须形成 `baseline-support-matrix.yaml`。它用于证明每条历史基线处于 active、maintenance、security-only、frozen、superseded 还是 eol，哪些门禁等级仍允许使用，安全补丁窗口何时结束，以及旧基线是否必须迁移或退役。

V2.35 起，企业级基线还必须形成 `baseline-release-train.yaml`。它用于证明基线发布不再是临时动作，而是具备候选窗口、冻结窗口、晋级日期、通知节奏、黑窗、紧急补丁入口和发布节奏的受控列车。

V2.36 起，纳入企业基线治理的资产还必须形成 `baseline-conformance-claim.yaml`。它用于证明单个领域、服务、数据产品、AI 产品、平台能力或 GitOps 环境声明采用哪条基线、由谁签署、证据在哪里、例外何时到期，以及这条声明如何汇总到组织级采纳总账。

V2.37 起，企业级基线还必须形成 `baseline-artifact-inventory.yaml`。它用于证明当前基线到底包含哪些源文档、schema、示例、控制项、证据模板、脚本、生成物和外部引用，并为每个制品记录路径、类型、摘要、owner、必需性、签名状态和导出关系。

V2.38 起，企业级基线还必须形成 `baseline-verification-lock.yaml`。它用于证明当前基线由哪些命令、工具版本、runner 镜像、策略包、schema validator、签名验签工具和审计导出生成环境验证，避免同一源制品因为工具链漂移产生不同门禁结果。

V2.39 起，企业级基线还必须形成 `baseline-notification-ledger.yaml`。它用于证明哪些领域 owner、平台 owner、数据产品 owner、AI 产品 owner、GitOps 环境 owner 和审计/安全相关方在冻结前收到通知，是否确认影响，是否提出异议，以及未确认对象是否已有例外、POA&M 或风险接受。

V2.40 起，企业级基线还必须形成 `baseline-rollback-verification.yaml`。它用于证明上一基线、回滚目标 tag/commit、GitOps revision、审计导出恢复、关键烟测和验证时效已经被实际检查，避免“有回滚说明但无法恢复”的空心化基线。

V2.41 起，企业级基线还必须形成 `baseline-exception-ledger.yaml`。它不是替代单项 `policy-exception.yaml`，而是把兼容性、采纳、支持矩阵、通知确认、回滚验证、门禁决策、执行控制面和风险登记中的例外聚合为基线级总账，用于证明哪些例外仍有效、哪些已经过期、哪些会阻断冻结、哪些已经有风险接受和 POA&M。

V2.42 起，企业级基线还必须形成 `baseline-readiness-scorecard.yaml`。它不是替代发布证据包，而是把发布证据包中分散的硬门禁和评分维度汇总成最终就绪判定，用于回答“这条基线现在是否可以进入 baseline 或 frozen，而不是只看每个局部证据是否存在”。

V2.43 起，企业级基线还必须形成 `baseline-lifecycle-state-machine.yaml`。它不是替代版本控制面或发布证据包，而是把每次状态迁移的允许路径、禁止路径、前置证据、审批责任、回写对象和回滚入口固化为状态机，用于避免基线状态被人工口头解释或跨系统漂移。

推荐发布检查：

```bash
make sync-doc-toc
make test
git diff --check
```

### 0.5 冻结规则

当某个版本被标记为 `Frozen` 后：

1. 不得直接修改核心架构原则、目录真相源、团队职责、治理门禁和落地路线图。
2. 任何实质性变更必须先创建变更提案，并说明业务动机、影响范围、风险和迁移计划。
3. 安全、合规、生产事故或关键错误可走紧急补丁，但必须在事后补齐 ADR 或复盘。
4. 被替代版本必须标记为 `Superseded`，并说明新版本位置和迁移注意事项。
5. 冻结版本不得与未冻结草案混用；项目启动、审计和平台模板必须引用明确版本。

### 0.6 版本控制面不变量

版本控制面用于回答“这次基线到底是哪一版、谁批准、从哪个 commit 发布、覆盖哪些契约、能不能兼容、如何回滚”。它不替代 Git、release note 或审计导出包，而是把这些证据绑定成同一个发布事实。

基线发布必须满足以下不变量：

| 不变量 | 最低要求 | 阻断条件 |
| ------ | -------- | -------- |
| 基线身份 | `baselineId`、`documentVersion`、`status` 唯一且不可复用 | 同一版本号对应多个基线或状态不一致 |
| 生命周期状态 | `baseline-lifecycle-state-machine.yaml` 必须绑定当前状态、允许迁移、禁止迁移、转换证据、审批人、状态回写和回滚入口 | 人工改状态、跨过候选或冻结门禁、直接从冻结退回草案、状态机和版本控制面不一致 |
| 源码绑定 | 每个基线绑定 `sourceCommit`、`releaseTag` 和签署人 | 无 tag、tag 不指向源 commit、签名缺失 |
| 制品清单 | `baseline-artifact-inventory.yaml` 必须列出基线纳入的源文档、schema、示例、控制项、证据模板、脚本、生成物和外部引用 | 基线签署但无法证明包含哪些文件、导出包缺源制品、出现未登记制品或摘要漂移 |
| 验证环境锁 | `baseline-verification-lock.yaml` 必须锁定命令、工具版本、runner 镜像、策略包、validator 和验签工具 | 校验工具版本漂移、runner 环境不可复现、策略包或 validator 变化未入基线 |
| 证据绑定 | 版本清单、控制项覆盖、审计导出、控制评估和门禁决策必须引用同一基线 | 证据包版本和文档版本不一致 |
| 发布证据包 | `baseline-release-evidence.yaml` 必须绑定晋级决策、不可变引用、漂移复核、签名验签和回滚验证 | 基线晋级无证据、证据引用不同 commit、漂移复核缺失 |
| 兼容性总账 | `baseline-compatibility-ledger.yaml` 必须绑定消费者、受影响契约、迁移状态、到期日和例外闭环 | breaking change 无消费者清单、迁移窗口过期、未迁移对象无风险处理 |
| 采纳总账 | `baseline-adoption-ledger.yaml` 必须绑定采纳目标、当前基线、目标基线、采纳状态、截止日期和整改闭环 | 企业基线发布后无人采用、采纳状态未知、关键资产逾期未整改 |
| 支持矩阵 | `baseline-support-matrix.yaml` 必须绑定支持状态、维护窗口、安全补丁、EOL、最低可接受基线和例外闭环 | 旧基线长期无 EOL、低于最低基线仍被 L3/L4 使用、安全补丁窗口结束后继续放行 |
| 发布列车 | `baseline-release-train.yaml` 必须绑定候选窗口、冻结窗口、晋级日期、通知节奏、黑窗、紧急补丁和依赖证据 | 临时发版、绕过冻结窗口、无通知升级、黑窗期间发布非紧急变更 |
| 通知确认 | `baseline-notification-ledger.yaml` 必须绑定通知对象、渠道、送达、确认、异议、例外和冻结前完成状态 | 冻结前关键消费者未确认、通知失败无补发、异议未关闭或无风险接受 |
| 回滚验证 | `baseline-rollback-verification.yaml` 必须绑定上一基线、回滚目标、Git/tag/GitOps revision、审计导出恢复、烟测结果和验证时效 | 只写回滚计划、上一基线不可检出、GitOps revision 不存在、审计导出无法恢复或验证过期 |
| 例外总账 | `baseline-exception-ledger.yaml` 必须聚合兼容、采纳、支持、通知、回滚、门禁和控制面的例外、到期日、风险接受、POA&M 和阻断状态 | 例外散落各处、例外过期仍放行、阻断例外无 owner、风险接受缺失或冻结前未关闭 |
| 就绪评分 | `baseline-readiness-scorecard.yaml` 必须绑定评分维度、权重、硬门禁、证据路径、阻断项、baseline/frozen 最低分和最终判定 | 局部证据都存在但无人能判断是否可晋级、评分覆盖缺失、硬门禁失败仍被平均分掩盖 |
| 符合性声明 | `baseline-conformance-claim.yaml` 必须绑定资产、声明基线、证据路径、签署人、例外、到期复核和采纳总账回写 | 中央台账手填、资产实际未声明基线、声明过期仍被采纳总账计为已采用 |
| 兼容窗口 | `Minor` / `Major` / `Breaking` 必须声明兼容窗口、迁移截止和消费者影响 | breaking change 无迁移窗口或消费者确认 |
| 冻结策略 | `Frozen` 基线只能通过补丁、紧急修复或下一基线替代 | 直接修改冻结基线核心内容 |
| 回滚入口 | 每个基线必须能回滚到上一基线、上一 tag 或上一 GitOps revision | 无回滚 commit、无回滚说明或回滚证据过期 |
| 外部标准 | 外部标准必须绑定版本、稳定性和采纳等级 | 引用 `latest` 或实验标准直接阻断生产 |

发布通道分为五类：

| 通道 | 用途 | 可进入生产 | 典型证据 |
| ---- | ---- | ---------- | -------- |
| `draft` | 设计草案和方案探索 | 否 | 草案记录、待决问题 |
| `candidate` | 评审候选和试点准备 | 仅低风险试点 | 评审意见、控制差距、试点范围 |
| `baseline` | 已批准的执行基线 | 是 | tag、版本清单、门禁结果、签署记录 |
| `frozen` | 审计、招标、监管或大规模推广口径 | 是 | 冻结声明、审计导出、例外清单 |
| `emergency-patch` | 安全、合规或生产事故紧急修复 | 受控允许 | 事故编号、补丁范围、事后复盘 |

版本提升门禁：

1. `Editorial` 只能修正文案、链接和格式，不能改变任何执行含义。
2. `Minor` 必须证明向后兼容，且不得改变目录真相源、owner、风险等级或发布准入。
3. `Major` 必须有 ADR、影响分析、迁移窗口、示例更新和控制项覆盖更新。
4. `Breaking` 必须有消费者清单、弃用策略、并行运行窗口、回滚路径和风险接受记录。
5. 任意版本提升都必须能通过 `make sync-doc-toc`、`make test` 和 `git diff --check`。
6. 任意生产基线都必须能从 `version-governance.yaml` 追溯到版本清单、控制项覆盖、标准基线、审计导出和门禁决策。

禁止事项：

1. 禁止同一版本号复用到不同内容。
2. 禁止发布未打 tag、tag 漂移或 tag 与文档版本不一致的基线。
3. 禁止只改主文档版本号，不同步索引、版本清单、控制覆盖和审计导出范围。
4. 禁止以“兼容”名义偷偷改变契约语义、owner、证据字段或生产准入规则。
5. 禁止把 emergency patch 当作常规发布通道长期使用。

### 0.7 版本记录

| 版本 | 日期 | 变更级别 | 关键变化 |
| ---- | ---- | -------- | -------- |
| `V1.0` | 2026-06-01 | Major | 建立现代企业数字化平台基础蓝图，替代传统“大中台、小前台”叙事 |
| `V1.1` | 2026-06-01 | Major | 补齐 AI 原生能力层、供应链安全、数据产品到 AI 的联动、Lakehouse 过渡和认知负载治理 |
| `V1.2` | 2026-06-01 | Minor | 增加行业对标矩阵、Agent 协议边界和深度调研结论 |
| `V1.3` | 2026-06-01 | Major | 增加 AI 风险分级、AI 资产证据链、SSDF 安全开发、数据契约和 FinOps 成本治理 |
| `V1.4` | 2026-06-01 | Major | 增加微调治理、AI 事件响应和 Policy as Code 策略语言统一 |
| `V1.5` | 2026-06-01 | Major | 增加微服务容器、镜像、Kubernetes、GitOps、catalog 和平台能力的分层真相源 |
| `V1.6` | 2026-06-01 | Major | 增加文档版本治理、发布状态、变更分级、冻结规则、发布证据和 V2.0 路线图 |
| `V1.7` | 2026-06-01 | Major | 增加真相源字段矩阵、starter kit 模板骨架、自动化门禁映射和漂移检测规则 |
| `V1.8` | 2026-06-01 | Major | 增加 RACI 决策权矩阵、可靠性分级、RTO/RPO、错误预算、灾备演练和升级路径 |
| `V1.9` | 2026-06-01 | Major | 增加仓库拓扑剖面、迁移与弃用策略、验证包和审计证据清单 |
| `V2.0` | 2026-06-01 | Major | 新增可执行 starter kit、JSON Schema、YAML 示例和自动化校验入口 |
| `V2.1` | 2026-06-01 | Minor | 增强 starter kit schema 嵌套约束、格式校验、跨文件一致性检查和 CI 门禁口径 |
| `V2.2` | 2026-06-01 | Minor | 补齐 API、事件、AI 工具、RAG、微调、GitOps、catalog 和 scorecard 契约模板 |
| `V2.3` | 2026-06-01 | Minor | 补齐发布证据、供应链证明、治理例外、API/Event 兼容性报告和 GitOps 漂移报告契约模板 |
| `V2.4` | 2026-06-01 | Minor | 增加机器可读版本清单、starter kit pair 清单和版本同步校验规则 |
| `V2.5` | 2026-06-02 | Minor | 加固可靠性、数据治理、AI 运行、GitOps 安全和供应链门禁字段 |
| `V2.6` | 2026-06-02 | Minor | 新增机器可读控制项覆盖清单，校验控制项到 schema、example 和 checker 的证据链 |
| `V2.7` | 2026-06-02 | Minor | 启用 starter kit 严格 schema 模式，要求 `additionalProperties=false` 并阻断未知字段通过门禁 |
| `V2.8` | 2026-06-02 | Minor | 补齐扩展字段策略、Feature Flag / Kill Switch、AI 威胁模型、运行血缘和平台产品指标控制项 |
| `V2.9` | 2026-06-02 | Minor | 补齐隐私影响评估、租户隔离、恢复演练、策略测试、GenAI 观测和成本分摊证据 |
| `V2.10` | 2026-06-02 | Minor | 补齐访问复核、密钥轮换、漏洞修复、事故复盘和证据新鲜度控制项 |
| `V2.11` | 2026-06-02 | Minor | 补齐控制证据映射和审计导出清单 |
| `V2.12` | 2026-06-02 | Minor | 补齐审计导出自动化命令 |
| `V2.13` | 2026-06-02 | Minor | 补齐控制评估报告和审计签署闭环 |
| `V2.14` | 2026-06-02 | Minor | 补齐架构基线变更记录和回滚证明 |
| `V2.15` | 2026-06-02 | Minor | 补齐 OSCAL 交换映射和导出摘要 |
| `V2.16` | 2026-06-02 | Minor | 补齐审计导出门禁和输出不变量校验 |
| `V2.17` | 2026-06-02 | Minor | 补齐审计导出完整性清单和生成物哈希校验 |
| `V2.18` | 2026-06-02 | Minor | 补齐审计导出 provenance statement 和生成上下文追溯 |
| `V2.19` | 2026-06-02 | Minor | 补齐审计导出签名策略和 provenance payload 签名交接 |
| `V2.20` | 2026-06-02 | Minor | 补齐审计导出签名验签回执和外部签名证据闭环 |
| `V2.21` | 2026-06-02 | Minor | 补齐 POA&M 整改计划和 OSCAL 整改视图证据闭环 |
| `V2.22` | 2026-06-02 | Minor | 补齐企业架构风险登记和风险到控制、POA&M、审计导出的证据闭环 |
| `V2.23` | 2026-06-02 | Minor | 补齐机器可读架构决策记录和基线变更 ADR 绑定 |
| `V2.24` | 2026-06-02 | Minor | 补齐机器可读 AI 事件响应 playbook 和 AI 运行证据闭环 |
| `V2.25` | 2026-06-02 | Minor | 补齐机器可读 AI 证据账本和 AI 产品级证据闭环 |
| `V2.26` | 2026-06-02 | Minor | 补齐机器可读微调运行证据和 AI 微调审计闭环 |
| `V2.27` | 2026-06-02 | Minor | 补齐机器可读仓库变更控制、远端保护验证和版本基线保护 |
| `V2.28` | 2026-06-02 | Minor | 补齐企业执行控制面、合规等级、门禁决策、例外放行和季度复核闭环 |
| `V2.29` | 2026-06-02 | Minor | 补齐外部标准版本锁定、稳定性分级、采纳等级和升级门禁 |
| `V2.30` | 2026-06-02 | Minor | 补齐版本控制面、发布通道、版本不变量、兼容窗口、冻结升级和回滚门禁 |
| `V2.31` | 2026-06-02 | Minor | 补齐基线发布证据包、版本晋级、冻结复核、漂移检查和回滚验证闭环 |
| `V2.32` | 2026-06-02 | Minor | 补齐基线兼容性总账、消费者影响、迁移窗口、弃用截止和未迁移风险闭环 |
| `V2.33` | 2026-06-02 | Minor | 补齐基线采纳总账、组织采纳状态、逾期治理、例外和整改闭环 |
| `V2.34` | 2026-06-02 | Minor | 补齐基线支持矩阵、维护窗口、安全补丁、EOL、冻结口径和最低可接受基线 |
| `V2.35` | 2026-06-02 | Minor | 补齐基线发布列车、候选窗口、冻结窗口、晋级日期、通知节奏、黑窗和紧急补丁入口 |
| `V2.36` | 2026-06-02 | Minor | 补齐资产级基线符合性声明、资产自声明、证据绑定、例外、复核和采纳总账回写 |
| `V2.37` | 2026-06-02 | Minor | 补齐基线制品清单、源制品摘要、必需性、签名状态、导出关系和未登记制品阻断 |
| `V2.38` | 2026-06-02 | Minor | 补齐基线验证环境锁定、命令版本、runner 镜像、策略包、validator、验签工具和可复现门禁 |
| `V2.39` | 2026-06-02 | Minor | 补齐基线通知确认总账、通知对象、送达回执、影响确认、异议、例外和冻结前完成状态 |
| `V2.40` | 2026-06-02 | Minor | 补齐基线回滚验证记录、上一基线检出、GitOps revision 恢复、审计导出恢复和烟测证据 |
| `V2.41` | 2026-06-02 | Minor | 补齐基线例外总账、例外来源聚合、风险接受、POA&M、过期阻断和冻结准入 |
| `V2.42` | 2026-06-02 | Minor | 补齐基线就绪评分卡、硬门禁、评分维度、证据绑定和 baseline/frozen 最终判定 |
| `V2.43` | 2026-06-02 | Minor | 补齐基线生命周期状态机、允许迁移、禁止迁移、状态回写和迁移审计证据 |

### 0.8 V2.43 可执行企业标准路线图

V2.0 已将 V1.9 的文档化基线转化为第一批可执行资产。V2.1 继续把字段约束、示例一致性和远程 CI 门禁补强为可执行口径。V2.2 把主文档最小验证包中的 API、事件、AI 工具、RAG、微调、GitOps、catalog 和 scorecard 纳入 schema/example 校验。V2.3 继续把发布证据、供应链证明、治理例外、兼容性报告和 GitOps 漂移报告纳入机器可校验基线。V2.4 把当前版本、发布状态、starter kit pair 清单、pair 数量和索引同步要求固化到机器可读版本清单中。V2.5 把可靠性等级、RTO/RPO、数据保留与访问审计、AI 预算与降级、GitOps 运行安全和供应链 source/vulnerability/scorecard 证据提升为 starter kit 强制字段。V2.6 增加控制项覆盖清单，把关键企业控制要求映射到 schema 字段、示例字段和 checker 规则，避免“文档说有控制、机器无法证明控制存在”。V2.7 启用严格 schema 模式，要求 starter kit 所有对象节点声明 `additionalProperties=false`，并由 checker 阻断未知字段。V2.8 补齐扩展字段策略、Feature Flag / Kill Switch、AI 威胁模型、运行血缘和平台产品指标。V2.9 继续把隐私工程、租户边界、恢复演练、Policy as Code 测试、GenAI 可观测性和 FinOps 成本分摊补成可执行证据。V2.10 把访问复核、密钥轮换、漏洞修复、事故复盘和证据新鲜度纳入控制目录，避免生产安全运营只停留在“有制度、有人看、事后补”的弱证据状态。V2.11 把每个控制项到证据路径、状态、新鲜度和审计导出包的关系纳入总账，避免审计时只能逐段翻文档、不能一键证明控制覆盖。V2.12 增加审计导出自动化命令，把版本、控制目录、证据映射、导出清单、脚本和关键制品哈希生成可交付审计包。V2.13 增加控制评估报告，把证据包进一步闭环到控制结果、发现项、整改、剩余风险和签署状态。V2.14 增加架构基线变更记录，把基线升级的影响分析、审批、验证命令和回滚路径纳入可执行证据。V2.15 增加 OSCAL 交换映射和导出摘要，把内部控制证据映射到 catalog、component-definition、system-security-plan、assessment-results 和 POA&M 视图。V2.16 增加审计导出门禁，把导出包生成、JSON/Markdown/OSCAL 输出和关键不变量校验纳入 `make test`。V2.17 增加审计导出完整性清单，把生成物 SHA-256、源制品哈希和防篡改校验纳入审计包。V2.18 增加审计导出 provenance statement，把生成物 subject、构建定义、源码提交和源证据依赖纳入可追溯证明。V2.19 增加审计导出签名策略，把 provenance payload 摘要、签名方式、验签命令和外部签名交接纳入门禁。V2.20 增加审计导出签名验签回执，把外部签名完成后的 bundle 摘要、证书身份、OIDC issuer、透明日志和验签结果纳入证据链。V2.21 增加 POA&M 整改计划，把控制发现项、责任人、整改行动、里程碑、证据、签署和 OSCAL POA&M 输出纳入闭环。V2.22 增加企业架构风险登记，把风险、控制项、POA&M、缓解行动、残余风险、复审和审计导出风险视图纳入闭环。V2.23 增加架构决策记录，把 ADR 上下文、备选方案、取舍、决策、关联控制项、风险、POA&M、复审和基线变更绑定纳入闭环。V2.24 增加 AI 事件响应 playbook，把幻觉爆发、工具循环、RAG 索引污染、供应商中断、成本异常、检测、遏制、降级、回滚和复盘纳入闭环。V2.25 增加 AI 证据账本，把模型、Prompt、RAG、工具、评估、威胁模型、观测、事件响应、数据使用、审批、留存和复审纳入 AI 产品级证据闭环。V2.26 增加微调运行证据，把训练数据授权、数据准备、实验追踪、评估、模型登记、审批、灰度发布、监控和退役纳入 AI 微调审计闭环。V2.27 增加仓库变更控制，把 CODEOWNERS、受保护分支、PR 审查、必需检查、签名提交、禁止直推、发布 tag 保护、远端保护状态验证、漂移整改、POA&M 和风险登记纳入版本基线保护。V2.28 增加企业执行控制面，把合规等级、门禁决策、证据新鲜度、例外放行、break-glass、季度复核和退出标准变成统一执行协议。V2.29 增加外部标准版本锁定与升级策略，避免把未稳定标准、实验性语义约定或外部规范变更直接带入生产基线。V2.30 增加版本控制面，把基线 ID、发布通道、tag、源 commit、兼容窗口、冻结策略和回滚入口固化为发布不变量。V2.31 增加基线发布证据包，把晋级决策、冻结复核、漂移检查、不可变引用、审计摘要和回滚验证固化为发布证据。V2.32 增加基线兼容性总账，把消费者影响、迁移窗口、弃用截止、例外状态和未迁移风险固化为版本门禁证据。V2.33 增加基线采纳总账，把领域、平台、数据、AI 和生产资产对基线的采用状态、逾期治理和例外整改固化为组织级版本证据。V2.34 增加基线支持矩阵，把旧基线支持状态、维护窗口、安全补丁窗口、EOL 和最低可接受基线固化为版本生命周期门禁。V2.35 增加基线发布列车，把候选窗口、冻结窗口、晋级日期、通知节奏、黑窗和紧急补丁入口固化为版本发布节奏门禁。V2.36 增加资产级基线符合性声明，把资产自声明、证据绑定、例外、复核和采纳总账回写固化为资产级版本证据。V2.37 增加基线制品清单，把源文档、schema、示例、控制项、证据模板、脚本、生成物和外部引用固化为可摘要、可签名、可复现的版本物料清单。V2.38 增加基线验证环境锁定，把校验命令、工具版本、runner 镜像、策略包、schema validator 和验签工具固化为可复现门禁。V2.39 增加基线通知确认总账，把发布列车中的通知计划升级为可审计的送达、确认、异议和例外证据。V2.40 增加基线回滚验证记录，把上一基线检出、GitOps revision 恢复、审计导出恢复和烟测结果升级为独立证据。V2.41 增加基线例外总账，把分散例外、到期、风险接受、POA&M 和冻结阻断收敛为统一审计证据。V2.42 增加基线就绪评分卡，把硬门禁、评分维度、证据摘要和 baseline/frozen 判定统一到最终准入证据。V2.43 增加基线生命周期状态机，把允许迁移、禁止迁移、状态回写、迁移审批和回滚入口统一到状态转换证据。后续 `V2.x` 迭代应继续补充示例仓库，并把平台、catalog、GitOps 和审计系统连接起来。

V2.43 起点包括：

1. 真相源字段矩阵：明确 `domain.yaml`、`service.yaml`、`ai-product.yaml`、`data-product.yaml`、catalog、GitOps 和 runtime 的字段权威。
2. 契约模板：提供服务、领域、数据产品、AI 产品、Agent 工具、RAG、微调、GitOps 和生产就绪模板。
3. 自动化门禁：把 API、事件、数据契约、AI 门禁、SBOM、签名、SLO、成本标签和 catalog entry 纳入 CI。
4. RACI：明确架构组、领域团队、平台团队、数据团队、安全团队、AI 产品团队、SRE 和业务 owner 的决策权。
5. 仓库拓扑剖面：覆盖 monorepo、多仓、独立 GitOps 仓、平台仓和数据仓的适配模式。
6. 可靠性分级：补齐 Tier-1 / Tier-2 / Tier-3、RTO、RPO、灾备演练、错误预算和 on-call 升级路径。
7. 迁移与弃用：定义旧系统绞杀迁移、API 版本弃用、数据产品兼容、AI 模型退役和平台能力下线流程。
8. 验证包：提供 `make test`、schema 校验、示例仓库和审计证据清单，证明标准可以落地执行。
9. Starter Kit：提供 `内部 starter kit` 下的 76 组 schema/example、嵌套字段校验、格式校验、可靠性、数据治理、AI 运行、基线生命周期状态机、基线就绪评分卡、基线例外总账、基线回滚验证记录、基线通知确认总账、基线验证环境锁定、基线制品清单、基线符合性声明、基线发布列车、基线支持矩阵、基线采纳总账、基线兼容性总账、基线发布证据包、版本控制面、外部标准版本锁定、企业执行控制面、合规等级、门禁决策、仓库变更控制、远端保护漂移整改、AI 证据账本、微调运行证据、AI 事件响应 playbook、GitOps 安全、架构决策记录、风险登记、证据链验真字段和示例跨文件一致性检查。
10. 版本清单：提供 `内部版本清单`，让当前版本、发布状态、pair 清单和索引同步进入 CI 校验。
11. 控制项覆盖清单：提供 `内部控制项覆盖清单`，让关键控制项到 schema、example 和 checker 的证据链进入 CI 校验。
12. 严格 schema 模式：starter kit 的对象 schema 必须声明 `additionalProperties=false`，新增字段必须先进入契约、示例和 checker 证据链。
13. 扩展字段策略：新增 `extension-policy.yaml`，让企业自定义字段只能通过受控前缀、审批和默认拒绝策略进入标准。
14. 渐进式发布控制：新增 `feature-flag-control.yaml`，把 Feature Flag、Kill Switch、灰度指标、SLO 燃尽回滚和曝光事件纳入门禁。
15. AI 威胁模型：新增 `ai-threat-model.yaml`，把 OWASP LLM / Agentic AI、MCP 工具同意、红队、出站限制和残余风险接受纳入证据链。
16. 运行血缘：新增 `lineage-event.yaml`，把数据产品的 producer job、run、input/output dataset、schema、质量证据和血缘后端纳入审计。
17. 平台产品指标：新增 `platform-product-metrics.yaml`，把 Platform PM、Golden Path 采用率、开发者满意度、认知负载和平台 SLO 纳入可执行标准。
18. 隐私影响评估：新增 `privacy-impact-assessment.yaml`，把 DPIA、处理目的、合法基础、主体权利、删除传播和 AI 使用限制纳入门禁。
19. 租户隔离：新增 `tenant-boundary.yaml`，把 namespace、ServiceAccount、Secret 范围、ResourceQuota、NetworkPolicy 和准入策略纳入证据链。
20. 恢复演练：新增 `recovery-drill-evidence.yaml`，把 RTO/RPO 从声明升级为演练结果、备份、恢复日志和复盘证据。
21. 策略测试：新增 `policy-test-report.yaml`，把 OPA / Cedar / Kyverno 等策略测试结果、失败数和阻断决策纳入门禁。
22. GenAI 观测：新增 `genai-observability-contract.yaml`，把 OpenTelemetry GenAI、Token、成本、工具调用、RAG span 和日志脱敏纳入运行契约。
23. 成本分摊证据：新增 `cost-allocation-evidence.yaml`，把标签覆盖率、未分摊成本、云/AI/数据成本和优化行动纳入 FinOps 证据。
24. 访问复核：新增 `identity-access-review.yaml`，把身份源、角色、特权访问、break-glass、MFA 和复核结论纳入门禁。
25. 密钥轮换：新增 `secrets-rotation-evidence.yaml`，把 Secret provider、KMS、静态加密、轮换周期、泄露扫描和轮换结果纳入证据链。
26. 漏洞修复：新增 `vulnerability-remediation-evidence.yaml`，把漏洞严重度、KEV 状态、SLA、修复日期、残余风险和发布准入纳入控制项。
27. 事故复盘：新增 `incident-postmortem.yaml`，把检测/恢复时间、影响、根因、纠正行动、runbook 更新和门禁反哺纳入闭环。
28. 证据新鲜度：新增 `evidence-freshness-policy.yaml`，把证据最大年龄、按类型过期策略、CI 执行和过期阻断纳入审计生命周期。
29. 控制证据映射：新增 `control-evidence-map.yaml`，把控制项 ID、证据路径、状态、新鲜度、必需性和阻断属性纳入审计总账。
30. 审计导出清单：新增 `audit-export-manifest.yaml`，把导出包范围、内容、验证结果、签名要求和留存策略纳入可交付证据。
31. 审计导出自动化：新增 `审计导出命令`，生成 `build/modern-enterprise-architecture-audit/audit-export.json`、`audit-export.md`、`oscal-summary.json`、`audit-export-integrity.json`、`audit-export-provenance.json` 和 `audit-export-signing-policy.json`。
32. 控制评估报告：新增 `control-assessment-report.yaml`，把评估范围、评估人、控制结果、发现项、整改、剩余风险和签署状态纳入审计闭环。
33. 架构基线变更记录：新增 `baseline-change-record.yaml`，把基线版本、前序版本、影响分析、审批、验证命令和回滚计划纳入变更控制。
34. OSCAL 交换映射：新增 `oscal-export-profile.yaml`，把内部控制、证据、评估和整改映射到 OSCAL 交换视图，并生成 `oscal-summary.json`。
35. 审计导出门禁：新增 `audit-export-gate.yaml` 和 `审计导出门禁命令`，把导出输出不变量纳入 `make test`。
36. 审计导出完整性清单：新增 `audit-export-integrity.yaml` 和 `audit-export-integrity.json`，把生成物 SHA-256、源制品哈希和防篡改校验纳入审计包。
37. 审计导出 provenance statement：新增 `audit-export-provenance.yaml` 和 `audit-export-provenance.json`，把生成物 subject、构建定义、源码提交和源证据依赖纳入可追溯证明。
38. 审计导出签名策略：新增 `audit-export-signing-policy.yaml` 和 `audit-export-signing-policy.json`，把 provenance payload 摘要、签名方式、验签命令和外部签名交接纳入审计包。
39. 审计导出签名验签回执：新增 `audit-export-signature-receipt.yaml`，把外部签名后的 bundle 摘要、证书身份、透明日志和验签结果纳入证据闭环。
40. POA&M 整改计划：新增 `poam-record.yaml`，把控制发现项、责任人、整改行动、里程碑、证据、签署和复审纳入 OSCAL POA&M 证据闭环。
41. 企业架构风险登记：新增 `risk-register.yaml`，把风险、控制项、POA&M、缓解行动、残余风险、复审和审计导出风险视图纳入证据闭环。
42. 架构决策记录：新增 `architecture-decision-record.yaml`，把 ADR 上下文、备选方案、取舍、决策、关联控制项、风险、POA&M、复审和基线变更绑定纳入证据闭环。
43. AI 事件响应 playbook：新增 `ai-incident-playbook.yaml`，把幻觉爆发、工具循环、RAG 索引污染、供应商中断、成本异常、检测信号、遏制、降级、回滚、RAG 恢复、工具 Kill Switch、沟通和复盘纳入 AI 运行证据闭环。
44. AI 证据账本：新增 `ai-evidence.yaml`，把模型、Prompt、RAG、工具、评估、威胁模型、观测、事件响应、数据使用、审批、留存和复审汇总为 AI 产品级证据总账。
45. 微调运行证据：新增 `fine-tuning-run.yaml`，把训练数据授权、数据准备、实验追踪、评估、模型登记、审批、灰度发布、监控和退役纳入 AI 微调审计闭环。
46. 仓库变更控制：新增 `repository-change-control.yaml`，把 CODEOWNERS、受保护分支、PR 审查、必需检查、签名提交、禁止直推、发布 tag 保护、远端保护状态验证、漂移整改、POA&M 和风险登记纳入版本基线保护。
47. 合规等级画像：新增 `conformance-profile.yaml`，把资产风险、监管强度、数据敏感度、AI 风险等级和必须执行的门禁等级绑定。
48. 执行控制面：新增 `control-plane.yaml`，把控制项、证据、owner、阻断级别、自动化状态、复核周期和退出标准汇总到统一执行账本。
49. 门禁决策记录：新增 `release-gate-decision.yaml`，把每次放行、阻断、条件放行、例外、break-glass 和回滚要求纳入可审计证据。
50. 标准基线锁定：新增 `standards-baseline.yaml`，把外部标准名称、版本、稳定性、采纳等级、owner、复核周期、升级条件和回滚策略纳入可执行基线。
51. 版本控制面：新增 `version-governance.yaml`，把基线 ID、发布通道、tag、源 commit、兼容窗口、冻结策略、升级规则和回滚入口纳入可执行发布协议。
52. 基线发布证据包：新增 `baseline-release-evidence.yaml`，把晋级决策、冻结复核、漂移检查、不可变引用、审计导出摘要和回滚验证纳入可执行证据。
53. 基线兼容性总账：新增 `baseline-compatibility-ledger.yaml`，把消费者影响、迁移状态、弃用截止、例外、POA&M 和风险接受纳入版本门禁。
54. 基线采纳总账：新增 `baseline-adoption-ledger.yaml`，把组织内领域、平台、数据、AI 和生产资产的基线采用状态、逾期、例外和整改纳入版本治理。
55. 基线支持矩阵：新增 `baseline-support-matrix.yaml`，把历史基线支持状态、维护窗口、安全补丁窗口、EOL、最低可接受基线和例外纳入版本生命周期治理。
56. 基线发布列车：新增 `baseline-release-train.yaml`，把候选窗口、冻结窗口、晋级日期、通知节奏、黑窗、紧急补丁和发布日历纳入版本治理。
57. 基线符合性声明：新增 `baseline-conformance-claim.yaml`，把资产自声明基线、证据路径、例外、签署、复核和采纳总账回写纳入资产级版本治理。
58. 基线制品清单：新增 `baseline-artifact-inventory.yaml`，把基线源文档、schema、示例、控制项、证据模板、脚本、生成物、外部引用、摘要和签名状态纳入版本物料清单。
59. 基线验证环境锁定：新增 `baseline-verification-lock.yaml`，把校验命令、runner 镜像、工具版本、策略包、schema validator、签名验签工具和审计导出生成环境纳入可复现门禁。
60. 基线通知确认总账：新增 `baseline-notification-ledger.yaml`，把受影响对象、通知渠道、送达回执、影响确认、异议、例外、补发和冻结前完成状态纳入版本发布门禁。
61. 基线回滚验证记录：新增 `baseline-rollback-verification.yaml`，把上一基线、回滚目标 tag/commit、GitOps revision、审计导出恢复、烟测结果和验证时效纳入版本发布门禁。
62. 基线例外总账：新增 `baseline-exception-ledger.yaml`，把兼容、采纳、支持、通知、回滚、门禁和控制面的例外、风险接受、POA&M、到期状态、关闭证据和冻结阻断纳入版本发布门禁。
63. 基线就绪评分卡：新增 `baseline-readiness-scorecard.yaml`，把版本身份、控制覆盖、制品完整性、验证环境、例外健康、通知确认、回滚验证、审计导出和禁推资产检查汇总为最终准入判定。
64. 基线生命周期状态机：新增 `baseline-lifecycle-state-machine.yaml`，把版本状态、允许迁移、禁止迁移、迁移证据、审批责任、状态回写和回滚入口纳入版本发布门禁。

---

## 1. 背景与建设目标

随着企业业务线上化、服务生态化、数据资产化和 AI 应用普及，传统以项目交付、烟囱系统、集中审批和人工运维为主的 IT 建设模式，已经难以支撑快速变化的业务需求。

传统模式常见问题包括：

1. 业务系统重复建设，能力难复用。
2. 前台团队依赖集中平台或 IT 团队排期，交付周期长。
3. 数据分散在各业务系统中，口径不统一、质量不可控。
4. 平台能力依赖工单和人工配置，研发效率低。
5. 治理主要依赖架构委员会、审批流程和人工检查，难以规模化。
6. 系统运行责任不清晰，业务指标、技术指标和数据指标割裂。

因此，本架构的建设目标是建立一套面向现代企业的数字化平台体系：

> 前台团队端到端负责业务结果，领域团队沉淀可复用业务能力和数据产品，平台团队提供自助式工程底座，治理团队将规则自动化为平台护栏，而不是依赖集中审批。

本架构不是建设一个中央共享服务池，而是建设一个由多个领域产品、数据产品、内部平台和联邦治理机制组成的企业级数字化能力网络。

---

## 2. 架构总览

现代企业数字化平台由七个纵向层级和一个横向治理平面组成。

```text
用户 / 客户 / 合作方 / 员工 / 运营人员
        │
        ▼
一、前台体验层
Web / App / 小程序 / Open API / 运营后台 / Partner Portal
        │
        ▼
二、体验编排层
BFF / API Gateway / GraphQL / Workflow / Event Subscription
        │
        ▼
三、AI 原生能力层
AI 应用 / Agent Runtime / LLM Gateway / RAG / Vector Store / PromptOps / Evals
        │
        ▼
四、领域能力产品层
用户域 / 商品域 / 订单域 / 支付域 / 履约域 / 风控域 / 营销域 / 内容域
        │
        ▼
五、数据产品网络层
Source-aligned Data Product / Aggregate Data Product / Consumer-aligned Data Product
指标层 / 语义层 / 特征层 / 向量索引 / 报表 / AI 数据服务
        │
        ▼
六、自助式平台工程层
Developer Portal / Golden Path / CI/CD / IaC / GitOps / Kubernetes / 可观测性 / AI Platform
        │
        ▼
七、基础设施与云原生层
Cloud / Kubernetes / Network / Storage / Database / Queue / Cache / Search / GPU / Vector DB

横向贯穿：
联邦治理平面
身份权限 / API 标准 / 数据契约 / AI 治理 / 安全策略 / 供应链安全 / 合规审计 / 架构决策
SLO / 成本规则 / 质量门禁 / Policy as Code / 自动化检测 / SBOM / Provenance
```

架构核心可以概括为：

> 现代企业数字化平台 = 前台体验 + 体验编排 + AI 原生能力 + 领域能力产品 + 数据产品网络 + 自助式平台工程 + 云原生基础设施 + 联邦治理。

## 2.1 推荐项目目录结构

落到工程仓库时，应把不同类型的“真相源”分开，避免把架构、契约、运行、治理和文档混成一个目录。

下面结构是企业级数字化平台的推荐参考形态，不是唯一强制目录。若团队采用 `services/*`、`apps/*`、独立 GitOps 仓库或多仓模式，也可以沿用同样职责边界。真正必须保持的是：服务源码、镜像制品、环境部署期望状态、实际运行状态、目录发现、平台能力和治理规则不能混成一个真相源。

```text
repo/
├── apps/                                # 前台体验真相源：Web、App、后台、门户、AI 体验入口
│   ├── web/                             # Web 前台应用；只做体验交付，不沉淀领域核心规则
│   ├── mobile/                          # 移动端应用；通过 BFF/API 消费领域能力
│   ├── admin/                           # 运营后台；承载管理体验，不直接访问领域数据库
│   ├── partner-portal/                  # 合作方门户；通过受控 API 和权限策略接入
│   ├── open-api-portal/                 # 开放 API 门户；展示契约、文档、申请和审计入口
│   └── ai-experiences/                  # AI 体验入口；具体 Agent/RAG/Prompt 资产放 ai/
│
├── ai/                                  # AI 原生能力：Agent、RAG、LLMOps 和 AI 产品运行单元
│   ├── applications/                    # 面向业务场景的 AI 应用
│   ├── agents/                          # Agent 定义、角色、工具权限和运行策略
│   ├── workflows/                       # Agent 工作流、人工确认点和补偿流程
│   ├── prompts/                         # Prompt 模板、版本、评测样例和变更记录
│   ├── evals/                           # 模型、Prompt、RAG 和 Agent 评估集
│   ├── rag/                             # 摄取、切分、嵌入、索引和检索流水线
│   ├── tools/                           # AI 可调用工具和 MCP/A2A 适配器
│   ├── model-gateway/                   # 模型路由、限流、成本、审计和降级；不保存供应商密钥明文
│   ├── guardrails/                      # 安全护栏、输出校验、PII 防泄露和策略
│   ├── observability/                   # Token、延迟、质量、幻觉、工具调用和成本观测
│   ├── model-registry/                  # 模型、Embedding、重排模型和批准状态
│   ├── fine-tuning/                      # 微调数据授权、实验追踪、评估和发布证据
│   └── docs/
│
├── domains/                             # 领域能力产品真相源：领域模型、业务服务、API、事件和数据产品
│   ├── customer/
│   │   ├── domain.yaml                  # 领域边界、owner、SLO、上下游依赖
│   │   ├── apis/                        # 领域 API 契约
│   │   ├── events/                      # 领域事件契约
│   │   ├── services/                    # 领域服务运行单元；默认推荐放领域内，非强制唯一位置
│   │   │   └── customer-profile-service/
│   │   │       ├── src/                 # 服务源码；也可按技术栈拆成 cmd/src/internal 等
│   │   │       ├── Dockerfile           # 镜像构建定义；镜像本体进入 registry，不进入 Git
│   │   │       ├── service.yaml         # 服务运行契约：owner、端口、依赖、资源诉求、SLO、镜像仓库
│   │   │       ├── README.md            # 服务说明、运行方式、runbook 入口
│   │   │       └── tests/               # 服务内测试；跨域测试放仓库 tests/
│   │   ├── workflows/                   # 领域流程和长事务编排
│   │   ├── data-products/               # 领域发布的数据产品
│   │   ├── policies/                    # 领域权限、数据和访问策略
│   │   ├── scorecards/                  # 领域成熟度和运行质量评分
│   │   └── docs/
│   ├── order/
│   ├── payment/
│   ├── fulfillment/
│   ├── risk/
│   └── marketing/
│
├── platform/                            # 内部开发平台真相源：标准能力、模板、自动化和开发者体验
│   ├── portal/                          # Developer Portal；聚合服务、API、数据产品、AI 产品和 scorecard
│   ├── golden-paths/                    # 推荐路径；创建服务、数据产品、AI 产品和容器交付模板
│   ├── scaffolds/                       # 脚手架；生成服务骨架、Dockerfile、service.yaml、catalog descriptor
│   ├── orchestration/                   # 平台编排；自助申请资源、环境、权限和发布流程
│   ├── ci-cd/                           # 流水线模板；不保存某个服务的业务逻辑
│   ├── environments/                    # 环境抽象和平台入口；具体 prod 期望状态放 infra/gitops/
│   ├── observability/                   # 日志、指标、链路追踪和默认仪表盘模板
│   ├── security/                        # 安全扫描、准入、密钥接入和策略模板
│   ├── data-platform/                   # 数据平台自助能力：目录、血缘、质量、权限、计算
│   ├── ai-platform/                     # AI 平台自助能力：LLM Gateway、RAG、Evals、Agent Runtime
│   ├── supply-chain/                    # SBOM、provenance、签名、验签和制品准入能力
│   ├── cost/                            # FinOps、预算、成本归集和异常检测
│   ├── developer-tools/                 # CLI、SDK、代码生成和本地开发工具
│   ├── scorecards/                      # 平台、服务、数据产品和 AI 产品成熟度评分模板
│   └── docs/                            # 平台用户文档和 onboarding 文档
│
├── contracts/                           # 跨团队机器可读契约真相源；进入 CI 校验
│   ├── apis/                            # OpenAPI / GraphQL 等接口契约
│   ├── events/                          # AsyncAPI、事件 topic、Schema 和兼容策略
│   ├── schemas/                         # JSON Schema、Proto、Avro 等共享 Schema
│   ├── datasets/                        # 数据产品契约、质量规则、语义层和数据访问策略
│   ├── ai/                              # AI 工具、Prompt、RAG、评估、微调和护栏契约
│   ├── resources/                       # 云资源、Terraform module、Kubernetes CRD 等资源契约
│   └── policies/                        # OPA/Rego、Cedar、IAM 等策略契约
│
├── catalog/                             # 发现目录真相源：系统、组件、资源、owner、生命周期和关系
│   ├── systems/                         # 系统级聚合；用于表达一组组件共同支撑的业务系统
│   ├── components/                      # 服务、任务、前端、库等组件条目；指向源码和 GitOps 路径
│   ├── resources/                       # 数据库、队列、缓存、对象存储、向量库等资源条目
│   ├── apis/                            # API 目录；指向 contracts/apis 或领域 apis
│   ├── data-products/                   # 数据产品目录；指向领域 data-products 和数据契约
│   ├── ai-products/                     # AI 产品目录；指向 ai/applications 和治理证据
│   ├── models/                          # 模型目录；基础模型、微调模型、Embedding 和重排模型
│   ├── agents/                          # Agent 目录；角色、工具权限、风险等级和 owner
│   ├── domains/                         # 领域目录；领域 owner、上下游、能力地图
│   └── scorecards/                      # 各资产成熟度、生产就绪、安全和可靠性评分
│
├── governance/                          # 联邦治理资产真相源：规则、决策、门禁、风险和复盘
│   ├── standards/                       # API、事件、数据、工程、安全、可靠性、成本等标准
│   ├── decisions/                       # ADR；记录重大架构决策、取舍和后续行动
│   ├── ownership/                       # 团队、RACI、升级路径和服务 owner
│   ├── slo/                             # SLO 分级、错误预算和事件响应策略
│   ├── security/                        # 威胁建模、数据分级、安全开发和隐私规则
│   ├── supply-chain/                    # SLSA、SBOM、签名验签和制品准入规则
│   ├── ai-governance/                   # AI 产品、模型风险、Prompt、微调和 Agent 工具治理
│   ├── data-governance/                 # 数据产品评审、PII、保留期限和权限规则
│   ├── architecture-gates/              # 生产就绪、领域就绪、数据产品就绪和 AI 发布门禁
│   ├── migration/                       # 迁移、兼容、弃用、退役和绞杀者模式治理
│   ├── evidence/                        # 发布、审计、验证、演练和合规证据清单
│   ├── risk-register/                   # 风险登记；必须有 owner、缓解措施和到期时间
│   ├── postmortems/                     # 事故复盘；反哺标准、门禁、平台能力和 playbook
│   └── playbooks/                       # 运行手册；只放通用流程，不放某个服务的部署细节
│       └── ai-incident-playbook.md      # AI 专属事件响应：幻觉、工具失控、RAG 污染、模型降级
│
├── infra/                               # 运行底座真相源：云资源、Kubernetes、GitOps、网络和灾备
│   ├── cloud/                           # 云账号、区域、VPC、IAM、基础资源和 IaC
│   ├── kubernetes/                      # Kubernetes base manifest、集群策略和可复用运行对象
│   │   ├── base/                        # 环境无关 base；Deployment、Service、HPA、PDB、NetworkPolicy
│   │   │   └── services/
│   │   └── policies/                    # 集群准入、Pod 安全、网络、镜像验签等策略
│   ├── gitops/                          # 环境级期望状态；声明 dev/staging/prod 部署什么版本
│   │   └── environments/
│   │       ├── dev/                     # 开发环境 overlay；低副本、宽松配额、实验性配置
│   │       ├── staging/                 # 预发环境 overlay；接近生产，验证发布和数据迁移
│   │       └── prod/                    # 生产环境 overlay；镜像 digest、replicas、资源、灰度策略
│   ├── networking/                      # DNS、Ingress/Gateway、Service Mesh、网络策略
│   ├── databases/                       # 数据库实例、备份、参数、迁移和访问入口
│   ├── vector-databases/                # 向量数据库和索引服务运行配置
│   ├── feature-stores/                  # 在线/离线特征存储运行配置
│   ├── model-serving/                   # 模型服务、GPU、推理网关和扩缩容配置
│   ├── messaging/                       # Kafka、Pulsar、队列、topic 和消费组基础配置
│   ├── storage/                         # 对象存储、文件存储、生命周期和加密配置
│   ├── secrets/                         # Secret 引用和外部密钥系统绑定；不保存明文密钥
│   ├── disaster-recovery/               # 备份、恢复、跨区容灾和演练脚本
│   └── environments/                    # 环境公共变量、命名空间、配额和环境级规则
│
├── shared/                              # 极薄共享层：无业务语义的库、SDK、测试夹具
├── tools/                               # 开发工具、代码生成、迁移工具
├── scripts/                             # 自动化入口和门禁脚本
├── tests/                               # 跨域集成测试、契约测试和仓库门禁
├── docs/                                # 人类可读文档，不替代 contracts/catalog/governance
└── .github/ or ci/                      # CI 工作流入口
```

目录边界判断：

| 目录 | 真相类型 | 不应承载 |
| ---- | -------- | -------- |
| `apps/` | 用户体验和渠道交付真相 | 领域核心规则、领域数据库访问 |
| `ai/` | AI 应用、Agent、RAG、Prompt、评估和模型接入真相 | 领域核心规则、未经治理的直接数据访问 |
| `domains/` | 业务能力、领域模型、领域服务和数据产品真相 | 平台通用工具、跨域集中审批 |
| `platform/` | 内部开发者体验和自助工程能力真相 | 业务规则和领域模型 |
| `contracts/` | API、事件、Schema、数据集、AI 工具和策略契约真相 | 普通说明文档 |
| `catalog/` | 系统、组件、资源、AI 产品、owner 和生命周期真相 | 运行逻辑 |
| `governance/` | 标准、决策、门禁、风险和复盘真相 | 业务代码 |
| `infra/` | 云资源、运行环境、安全、网络和灾备真相 | 业务逻辑 |
| `shared/` | 无业务语义的薄复用真相 | 领域模型和业务流程 |

这套目录结构的核心不是“所有企业都必须照抄这些文件夹”，而是把不同生命周期、不同 owner、不同风险等级的资产分开。目录名可以变，职责边界不能变。

### 2.1.1 目录设计的四个判断问题

新增任何目录或文件前，先回答四个问题：

1. 这个资产的 owner 是谁：业务流团队、领域团队、平台团队、SRE、安全、数据治理还是架构治理委员会。
2. 这个资产的变更频率是什么：随业务每天变、随发布变、随环境变、随治理周期变，还是只在架构决策时变。
3. 这个资产的消费方是谁：人类开发者、CI/CD、Developer Portal、Kubernetes、审计系统、数据平台还是 AI Runtime。
4. 这个资产是不是可执行真相源：能否被校验、生成、部署、路由、授权、审计或阻断发布。

如果一个文件同时被多个团队频繁修改、同时服务人类阅读和机器执行、同时表达业务规则和部署细节，通常说明它放错了位置，或者需要拆成契约、实现、部署、目录和治理五类资产。

### 2.1.2 核心目录的深度职责

| 目录 | 主要 owner | 典型变更触发 | 机器消费方 | 深度说明 |
| ---- | ---------- | ------------ | ---------- | -------- |
| `apps/` | 体验团队 / 业务流团队 | 新渠道、新页面、新用户流程、A/B 实验 | CI、前端发布平台、观测系统 | 只承载体验交付和体验编排。它可以调用 BFF、API、工作流和 AI 体验入口，但不拥有领域事实，不直接读写领域数据库。 |
| `ai/` | AI 产品团队 / AI 平台团队 | Prompt 发布、Agent 工具变更、RAG 索引更新、模型路由调整、评估门禁变化 | LLM Gateway、Agent Runtime、Evals、观测系统 | 管 AI 产品的运行资产。这里可以声明 Agent、Prompt、RAG、工具、评估、护栏和微调运行证据，但 AI 层不是新的业务真相源，不能绕过领域 API、数据产品和权限边界。 |
| `domains/` | 领域团队 / Stream-aligned Team | 领域模型变化、业务服务发布、API/事件契约变化、数据产品发布 | CI、契约测试、catalog、数据平台 | 管领域能力产品。领域内可以放服务源码，但不是唯一合法形态；如果服务在独立仓或顶层 `services/`，必须通过 `service.yaml` 和 `catalog/components` 指回领域 owner、API、事件、数据产品和 GitOps 路径。 |
| `platform/` | 平台团队 / Platform Team | Golden Path 迭代、脚手架升级、流水线模板升级、平台 API 变化 | Developer Portal、脚手架、CI/CD、准入系统 | 管“如何更容易、更安全地创建和交付”。平台不接管业务服务，也不直接成为每个服务的部署目录；它提供模板、能力、默认路径和自助入口。 |
| `contracts/` | 契约 owner + 治理 owner | API、事件、数据、AI 工具、资源和策略契约变更 | CI、兼容性检查、代码生成、网关、策略引擎 | 管跨团队协作的机器契约。凡是会影响消费者、权限、兼容性、数据质量或发布准入的接口，都应能在这里或领域内等价位置找到机器可读契约。 |
| `catalog/` | 平台团队 + 各资产 owner | 新服务、新 API、新数据产品、新 AI 产品、新资源登记 | Developer Portal、Scorecard、审计导出、依赖图 | 管“这是什么、谁负责、在哪里、依赖谁、成熟度如何”。catalog 是发现入口，不是源码仓、不是真实部署状态，也不是运行配置中心。 |
| `governance/` | 架构治理 / 安全 / 数据治理 / 合规 | 标准变化、ADR、风险登记、例外审批、门禁升级、复盘反哺 | CI、审计系统、Policy as Code、评审流程 | 管规则、决策和证据。治理资产必须尽量机器可读：门禁、风险、例外、控制项、POA&M、ADR、证据账本都应能被自动校验或导出。 |
| `infra/` | 平台工程 / SRE / 环境 owner | 环境变更、容量调整、镜像版本发布、集群策略、灾备演练 | GitOps、Kubernetes、云平台、观测系统 | 管运行底座和环境期望状态。它不拥有业务逻辑；它回答“跑在哪里、跑几个、用哪个 digest、什么资源、什么策略、什么发布方式”。 |
| `shared/` | 平台团队或共享库 owner | 通用 SDK、测试夹具、无业务语义工具升级 | 编译、测试、代码生成 | 只能放薄复用能力。若共享代码开始表达订单、客户、支付、履约等业务概念，应回到对应领域，不应把 `shared/` 演化成隐形中台。 |

### 2.1.3 单仓、多仓和混合仓的落地方式

推荐目录结构可以映射到三种仓库拓扑：

| 拓扑 | 适用场景 | 推荐做法 | 风险控制 |
| ---- | -------- | -------- | -------- |
| 单仓 Monorepo | 团队协作强、统一门禁成熟、需要跨域重构和统一发布证据 | 保留上述目录，所有资产在一个仓库内通过 CODEOWNERS、路径门禁和 CI 分层校验 | 必须避免所有团队都能随意改所有目录；按 `domains/`、`platform/`、`infra/`、`governance/` 切 owner 和审批规则 |
| 多仓 Polyrepo | 服务高度自治、权限隔离强、团队发布节奏差异大 | 服务源码在各服务仓；中心仓保留 `contracts/`、`catalog/`、`governance/`、`platform/`、`infra/gitops/` 或用自动同步生成 | 必须用 catalog 记录 `sourceRoot`、`gitopsPath`、owner、API、事件、SLO、证据路径，避免服务失联 |
| 混合仓 Hybrid | 企业最常见；平台、治理、GitOps 集中，领域服务部分集中、部分独立 | 领域核心契约、catalog、治理和 GitOps 集中；服务源码按团队成熟度放 `domains/*/services/*` 或独立服务仓 | 必须明确哪一份是契约真相源，避免中心仓和服务仓同时维护同一契约导致漂移 |

是否把源码放在 `domains/*/services/*`，取决于仓库拓扑，而不是架构原则本身。架构原则只要求每个服务都能被追溯到：

```text
领域 owner -> 服务源码 -> API / Event 契约 -> 镜像构建定义 -> 制品 digest -> GitOps 期望状态 -> 运行观测 -> 审计证据
```

如果服务源码不在 `domains/*/services/*`，至少要在以下位置声明反向索引：

```yaml
service: customer-profile-service
domain: customer
owner: team-customer
sourceRoot: https://git.example.com/customer/customer-profile-service
catalogComponent: catalog/components/customer-profile-service.yaml
gitopsPath: infra/gitops/environments/prod/customer/customer-profile-service
apis:
  - contracts/apis/customer-profile.openapi.yaml
events:
  publishes:
    - contracts/events/customer.profile.updated.asyncapi.yaml
```

### 2.1.4 文件放置决策表

| 要放的东西 | 推荐位置 | 不推荐位置 | 原因 |
| ---------- | -------- | ---------- | ---- |
| 服务源码 | `domains/{domain}/services/{service}/` 或独立服务仓并在 catalog 声明 | `platform/`、`infra/` | 服务属于领域能力，不属于平台模板或环境配置 |
| Dockerfile / Containerfile | 服务源码目录 | `infra/gitops/` | Dockerfile 描述如何构建运行单元，不描述某环境部署哪个版本 |
| 生产镜像版本 | `infra/gitops/environments/prod/...` 使用 digest | `domains/*/services/*` | 生产运行期望状态由环境 owner 管，不应由源码目录暗含 |
| OpenAPI / AsyncAPI | `contracts/` 或 `domains/*/apis`、`domains/*/events` | `docs/` | 契约要能被 CI、网关、代码生成和兼容性检查消费 |
| 数据产品契约 | `domains/*/data-products/` 和 `contracts/datasets/` | BI 报表目录 | 数据产品是可治理资产，不只是报表输入 |
| RAG 索引契约 | `contracts/ai/`、`ai/rag/` | 应用代码常量 | RAG 来源、权限、刷新和删除策略需要审计和回滚 |
| Prompt 版本 | `ai/prompts/` 或 `contracts/ai/prompts/` | 工程代码硬编码 | Prompt 是可评估、可回滚、可审批资产 |
| 微调运行证据 | `ai/fine-tuning/`、`governance/evidence/ai/` 或 starter kit 的 `fine-tuning-run.yaml` | 模型平台截图、聊天记录 | 微调必须证明数据授权、实验追踪、评估、登记、审批和回滚 |
| Kubernetes Deployment | `infra/kubernetes/` 或 `infra/gitops/` | 服务源码目录作为唯一真相 | Deployment 是环境期望状态，和服务构建定义生命周期不同 |
| 服务 owner 和依赖关系 | `catalog/components/` + `domains/*/domain.yaml` | README 手写说明 | owner、依赖和生命周期要能被 Developer Portal、审计和 scorecard 消费 |
| 架构决策 | `governance/decisions/` | 即时聊天记录 | ADR 需要可追溯、可复审、能关联风险和控制项 |
| 安全例外 | `governance/architecture-gates/` 或 `governance/evidence/` | CI 注释、临时豁免变量 | 例外必须有 owner、到期时间、补偿控制和自动阻断 |

### 2.1.5 最小可执行落地包

如果企业不能一次性建立完整目录，最低也要先落下以下资产：

```text
domains/{domain}/domain.yaml             # 领域边界、owner、SLO 和上下游
domains/{domain}/services/{service}/     # 服务源码或 sourceRoot 指针
contracts/apis/                          # 对外 API 契约
contracts/events/                        # 跨域事件契约
contracts/ai/                            # AI 工具、RAG、Prompt、微调和评估契约
catalog/components/                      # 服务发现、owner、生命周期和 GitOps 路径
catalog/data-products/                   # 数据产品发现和 owner
catalog/ai-products/                     # AI 产品发现、风险等级和证据路径
infra/gitops/environments/               # 环境期望状态
platform/golden-paths/                   # 标准创建和交付路径
governance/standards/                    # 标准
governance/decisions/                    # ADR
governance/architecture-gates/           # 发布门禁
governance/evidence/                     # 审计和验证证据
```

这个最小包能先回答企业落地最关键的问题：

1. 谁拥有这个能力。
2. 能力的源码在哪里。
3. 它对外承诺什么契约。
4. 它部署到哪里、用哪个版本。
5. 它是否满足发布门禁。
6. 它的风险、例外、决策和证据在哪里。

### 2.1.6 字段级真相源矩阵

目录结构真正落地时，最容易出问题的不是目录名，而是同一个字段被多处维护。以下字段必须有明确主责位置：

| 字段或信息 | 权威真相源 | 允许的派生位置 | 冲突时以谁为准 |
| ---------- | ---------- | -------------- | -------------- |
| 领域 owner、领域边界、领域 SLO | `domains/{domain}/domain.yaml` | `catalog/domains/`、治理评审报告 | `domain.yaml` |
| 服务 owner、生命周期、runbook | `domains/*/services/*/service.yaml` 或服务仓同名契约 | `catalog/components/`、Developer Portal | `service.yaml` |
| 服务源码位置 | 服务仓路径或 `domains/*/services/*` | `catalog/components/*.yaml` 的 `sourceRoot` | 实际 Git 源码仓 |
| 镜像构建方式 | 服务目录 `Dockerfile` / `Containerfile` | 平台脚手架、CI 模板 | 服务目录构建定义 |
| 镜像制品 digest | Container Registry / provenance | `infra/gitops/`、发布证据 | registry digest + provenance |
| prod 部署版本、replicas、资源限制 | `infra/gitops/environments/prod/...` | catalog 运行摘要、观测面板 | GitOps 期望状态 |
| API 契约 | `contracts/apis/` 或 `domains/*/apis/` | API portal、catalog/apis | 机器可读 OpenAPI / GraphQL 契约 |
| 事件契约 | `contracts/events/` 或 `domains/*/events/` | 事件目录、消息平台 UI | 机器可读 AsyncAPI / Schema 契约 |
| 数据产品口径、质量、访问策略 | `domains/*/data-products/` + `contracts/datasets/` | catalog/data-products、数据目录 | 数据产品契约 |
| Prompt、RAG、工具和评估契约 | `ai/` + `contracts/ai/` | catalog/ai-products、AI 观测面板 | 版本化 AI 契约 |
| 微调数据授权和运行证据 | `ai/fine-tuning/` 或 `governance/evidence/ai/` | starter kit、模型登记系统 | `fine-tuning-run` 证据 |
| 发布门禁、例外和风险接受 | `governance/architecture-gates/`、`risk-register/`、`evidence/` | PR 评论、审计导出 | 治理证据 |

冲突处理原则：

1. 机器可读契约优先于自然语言说明。
2. 环境级 GitOps 配置优先于服务默认值。
3. catalog 负责发现和索引，不能覆盖源码、契约和部署真相。
4. governance 可以阻断发布、记录例外和要求补偿控制，但不应成为业务字段的日常编辑入口。
5. README 只能解释，不应成为唯一事实来源；凡是影响发布、权限、兼容性、审计和运行状态的字段，都应进入可校验文件。

### 2.1.7 典型变更链路

目录结构要服务真实工作流。以下三条链路是企业落地时最需要固定的路径。

新建生产微服务：

```text
领域建模
-> domains/{domain}/domain.yaml 声明边界和 owner
-> domains/{domain}/services/{service}/ 或独立服务仓创建源码
-> service.yaml 声明端口、依赖、SLO、资源诉求和镜像仓库
-> contracts/apis 与 contracts/events 声明外部协作契约
-> catalog/components 注册服务和 sourceRoot/gitopsPath
-> CI 构建镜像、生成 SBOM、provenance、签名和漏洞扫描证据
-> infra/gitops/environments/{env}/... 声明部署版本和运行策略
-> governance/evidence 记录生产就绪、发布证据和例外
```

发布数据产品：

```text
领域确认数据语义
-> domains/{domain}/data-products/{data-product}.yaml 声明 owner、指标、SLO 和消费者
-> contracts/datasets/ 声明 Schema、质量规则、访问策略和保留期限
-> data-platform 接入血缘、质量检查、权限审批和数据目录
-> catalog/data-products 注册可发现入口
-> governance/data-governance 记录 PII、授权、例外和复审周期
```

发布 AI 产品或 Agent：

```text
AI 产品定义
-> ai/applications 或 ai/agents 声明场景、风险等级、工具权限和人工确认点
-> ai/prompts、ai/rag、ai/tools、ai/evals 版本化 Prompt、检索、工具和评估
-> contracts/ai/ 固化工具、RAG、Prompt、评估、微调和护栏契约
-> model-gateway 配置模型路由、限流、成本预算和降级链路
-> governance/ai-governance 与 governance/evidence/ai 记录审批、证据账本和微调运行证据
-> catalog/ai-products 注册 owner、风险等级、运行入口、依赖和 scorecard
```

这三条链路的共同点是：源码、契约、目录、部署、治理和证据必须串起来。只建目录、不建链路，目录会退化成静态分类；只建链路、不分真相源，系统会在规模扩大后失控。

### 2.1.8 目录拆分和合并规则

目录是否需要独立出来，按以下规则判断：

1. owner 不同就倾向拆分：领域团队、平台团队、SRE、安全、数据治理和 AI 治理不应频繁编辑同一类文件。
2. 生命周期不同就倾向拆分：源码随业务发布变，GitOps 随环境变，治理标准随审查周期变，审计证据随发布和复审变。
3. 机器消费方不同就倾向拆分：Kubernetes、CI、Developer Portal、策略引擎、审计导出和人类文档不应依赖同一份非结构化文本。
4. 风险等级不同就倾向拆分：生产部署、权限策略、模型工具调用、PII 数据、密钥和供应链证据必须有更严格 owner 和门禁。
5. 没有稳定 owner、没有机器消费方、没有门禁价值的目录不要新增；先放入既有目录，等变更频率和职责边界稳定后再拆。
6. 一个目录如果开始同时承载业务规则、平台模板、环境部署和治理审批，应立即拆成 `domains/`、`platform/`、`infra/` 和 `governance/`。
7. 一个共享目录如果出现领域名词，应回到领域；共享层只能放无业务语义的 SDK、工具、测试夹具和生成代码。

### 2.1.9 常见错误

1. 把 `platform/` 做成新的大中台，把业务规则、服务部署和审批流程全部塞进去。
2. 把 `shared/` 做成跨域业务模型垃圾桶，让多个领域通过共享对象强耦合。
3. 把 `catalog/` 当部署系统，在目录条目里维护 replicas、资源限制和灰度策略。
4. 把 `docs/` 当契约真相源，只写自然语言说明，没有 OpenAPI、AsyncAPI、JSON Schema 或策略文件。
5. 把 `infra/` 当业务仓，在 Helm values 或 Kustomize patch 里隐藏业务开关和业务规则。
6. 把 AI Prompt、RAG 来源、工具权限和微调审批写在应用代码里，导致无法评估、回滚和审计。
7. 只有服务仓，没有中心 catalog、契约和治理索引，导致企业无法回答“谁依赖谁、谁负责、风险在哪”。

### 2.1.10 目录级 owner、审批和门禁

目录结构只有和 owner、审批规则、自动门禁绑定，才会从“文件夹分类”变成“工程治理系统”。推荐按目录设置
CODEOWNERS、必需检查和变更证据：

| 路径 | 推荐 owner | 最低审批 | 必需门禁 | 变更证据 |
| ---- | ---------- | -------- | -------- | -------- |
| `apps/**` | 体验团队 / 业务流团队 | 应用 owner 1 人 | 单元测试、构建、前端质量、可访问性、契约消费检查 | 发布记录、回滚计划、体验指标 |
| `ai/**` | AI 产品 owner + AI 平台 owner | AI owner 1 人；高风险工具另需治理审批 | Prompt/RAG/Evals、工具权限、成本预算、护栏、AI 事件响应检查 | AI 证据账本、评估报告、模型/Prompt 版本记录 |
| `domains/{domain}/**` | 对应领域团队 | 领域 owner 1 人；跨域契约需消费者确认 | 领域测试、契约兼容、SLO、数据产品质量、scorecard | domain 变更记录、契约变更记录 |
| `platform/**` | 平台团队 | 平台 owner 1 人；破坏性 Golden Path 变更需架构复审 | 脚手架测试、模板回归、平台 API 兼容、开发者体验指标 | 平台发布说明、迁移指南 |
| `contracts/**` | 契约 owner + 消费者代表 | producer 和至少一个 consumer | OpenAPI/AsyncAPI/Schema 兼容、策略测试、breaking change 检查 | 契约版本、兼容性报告 |
| `catalog/**` | 平台团队 + 资产 owner | 资产 owner 1 人 | catalog schema、owner 存在性、sourceRoot/gitopsPath 可达性 | 目录同步报告、scorecard |
| `governance/**` | 架构治理 / 安全 / 数据治理 | 治理 owner 1 人；控制项变更需双人审批 | 控制项覆盖、证据新鲜度、风险/POA&M/ADR 链接完整性 | ADR、风险登记、审计导出 |
| `infra/**` | SRE / 平台工程 / 环境 owner | 环境 owner 1 人；生产变更需 SRE 审批 | GitOps diff、策略准入、镜像验签、资源限制、灾备影响检查 | 变更单、GitOps 同步记录、回滚证据 |
| `shared/**` | 共享库 owner | owner 1 人；破坏性变更需所有消费者确认 | API 兼容、依赖影响、反向依赖测试 | 版本说明、消费者迁移记录 |

最重要的规则是：目录 owner 不是“通知人”，而是对资产正确性、演进节奏和事故后果负责的人。审批不能只看
Markdown 是否写得好，而要验证契约、门禁、证据和运行路径是否闭合。

目录级门禁建议分三层：

1. 路径门禁：用 CODEOWNERS、受保护分支、禁止直推和必需检查保护关键目录。
2. 语义门禁：用 schema、契约兼容、策略测试、scorecard 和风险规则判断内容是否合理。
3. 证据门禁：要求每次关键变更绑定 ADR、发布证据、审计证据、风险接受或 POA&M 整改记录。

### 2.1.11 目录和企业工具链的映射

企业落地时，不应要求人手工维护所有索引。目录结构应被成熟工具链消费、校验和回写摘要：

| 工具链能力 | 读取的目录 | 写入或生成的资产 | 关键门禁 |
| ---------- | ---------- | ---------------- | -------- |
| Developer Portal | `catalog/`、`domains/`、`contracts/`、`governance/scorecards` | 服务地图、API 门户、数据产品目录、AI 产品目录、scorecard | owner、生命周期、依赖、runbook 必填 |
| CI/CD | `apps/`、`domains/`、`ai/`、`contracts/`、`shared/` | 构建产物、测试报告、SBOM、provenance、发布证据 | 测试、契约兼容、漏洞、签名、质量阈值 |
| Container Registry | 服务目录构建定义、CI provenance | 镜像 tag、digest、签名、漏洞报告 | 禁止使用未签名镜像进入生产 GitOps |
| GitOps / CD | `infra/gitops/`、`infra/kubernetes/` | 环境同步状态、漂移报告、发布历史 | production 使用 digest、策略准入、回滚路径 |
| API Gateway | `contracts/apis/`、`catalog/apis/` | 路由、鉴权、限流、审计日志 | OpenAPI 合法、权限策略存在、breaking change 受控 |
| Event Platform | `contracts/events/`、`catalog/` | topic、schema registry、消费者拓扑 | 事件兼容、owner、保留期限、PII 标记 |
| Data Platform | `domains/*/data-products/`、`contracts/datasets/` | 数据目录、血缘、质量报告、访问审批 | 质量 SLO、PII、保留期限、授权边界 |
| AI Platform | `ai/`、`contracts/ai/`、`catalog/ai-products/` | Prompt 版本、RAG 索引、评估结果、模型路由 | Evals、Guardrails、预算、人工确认点 |
| Observability | `catalog/`、`service.yaml`、`domain.yaml`、`infra/` | SLO、仪表盘、告警、错误预算 | owner、SLO、日志/指标/链路追踪接入 |
| GRC / Audit | `governance/`、控制目录、`evidence/`、starter kit | 控制评估、审计导出、POA&M、风险视图 | 证据新鲜度、控制覆盖、签署状态 |

这张映射的意义是把目录从“人看的结构”升级为“工具能执行的接口”。如果某个目录没有稳定 owner、没有工具消费、
没有门禁和证据输出，就不应被列为企业级标准目录。

### 2.1.12 从现有项目迁移到目标结构

迁移不要从重命名目录开始，而要先找真相源、定 owner、补契约，再逐步移动文件。推荐路径如下：

| 阶段 | 目标 | 动作 | 禁止误区 |
| ---- | ---- | ---- | -------- |
| L0 盘点 | 看清现状 | 列出服务、API、事件、数据库、数据产品、AI 资产、部署路径、owner 和证据位置 | 直接批量移动目录，导致 CI、部署和文档同时失效 |
| L1 索引 | 先能发现 | 建 `catalog/`，为每个服务、数据产品、AI 产品和资源建立 owner、sourceRoot、gitopsPath | 把 catalog 当新的手工台账，不接 CI 和 portal |
| L2 契约 | 先稳边界 | 把 OpenAPI、AsyncAPI、数据产品、AI 工具和策略契约迁入 `contracts/` 或领域内等价位置 | 只迁 README，不迁机器可读契约 |
| L3 部署 | 分离运行状态 | 把环境级部署期望状态收敛到 `infra/gitops/`，生产使用镜像 digest 和策略准入 | 让服务源码目录同时决定 prod 版本和资源配额 |
| L4 治理 | 补齐控制 | 增加 `governance/`、ADR、门禁、风险、POA&M、证据和目录级 owner | 只增加审批流程，不增加自动校验和证据 |
| L5 平台化 | 降低认知负载 | 用 `platform/golden-paths`、脚手架、portal 和 scorecard 把标准路径产品化 | 让每个团队手写一套不同模板和检查脚本 |

迁移期间可以长期保持混合形态：新服务走目标结构，旧服务通过 catalog 指针接入。真正要避免的是同一事实在旧目录和新目录
双写。任何双写字段都必须有主真相源、派生方向和漂移检查。

### 2.1.13 目录结构验收清单

一套目录结构是否合格，不看目录名是否“先进”，看它能否稳定回答以下问题：

1. 每个服务是否能找到领域 owner、源码位置、契约、GitOps 路径、SLO、runbook 和最近一次发布证据。
2. 每个 API 和事件是否有机器可读契约、兼容规则、消费者影响面和 breaking change 流程。
3. 每个数据产品是否有 owner、语义口径、质量规则、访问策略、PII 标记、血缘和复审周期。
4. 每个 AI 产品是否有 Prompt/RAG/工具/模型/评估/护栏/预算/人工确认点/事件响应证据。
5. 每个生产部署是否由 GitOps 管理，并明确镜像 digest、资源限制、HPA、策略准入和回滚路径。
6. 每个共享库是否能证明没有承载领域业务语义，并有反向依赖测试和破坏性变更流程。
7. 每个治理控制项是否能映射到 schema、示例、checker、证据路径和审计导出结果。
8. 每个目录是否有 CODEOWNERS、必需检查、变更证据和定期 owner 复核。
9. 每个关键字段是否只有一个权威真相源，catalog 和文档是否只是派生视图或说明。
10. 新人能否通过 Developer Portal 或 catalog 在 10 分钟内找到某个能力的 owner、契约、运行状态和风险。

如果以上问题无法回答，说明目录只是“看起来现代”，还没有形成可运营、可审计、可演进的企业架构骨架。

### 2.1.14 服务源码组织的合法形态

`domains/{domain}/services/{service}/` 是推荐默认值，不是唯一正确答案。它的优点是领域边界、服务源码、API、
事件、数据产品和 owner 放在同一上下文里，新人容易理解“这个服务为什么存在”。但企业真实落地时，源码位置往往受
团队历史、权限隔离、构建系统、语言生态和发布节奏影响。判断一个服务放得对不对，不看目录名字，而看服务能否稳定
接入领域、契约、catalog、GitOps、治理和审计链路。

常见形态如下：

| 形态 | 示例路径 | 适用场景 | 必须补齐的索引 |
| ---- | -------- | -------- | -------------- |
| 领域内服务 | `domains/customer/services/customer-profile-service/` | 单仓或领域仓；领域团队对模型、服务和契约端到端负责 | `service.yaml`、`domain.yaml`、catalog component、GitOps 路径 |
| 顶层服务目录 | `services/customer-profile-service/` 或 `services/customer/customer-profile-service/` | 历史仓库已有 `services/` 约定；平台工具默认扫描顶层服务 | `service.yaml.domain`、`service.yaml.owner`、catalog component、领域映射 |
| 语言工作区 | `packages/customer-profile-service/`、`apps/customer-api/` | Node、Go、Java、.NET 等 monorepo workspace 已有生态约定 | workspace package metadata、`service.yaml`、catalog sourceRoot |
| 独立服务仓 | `git@example.com/customer/customer-profile-service.git` | 多仓自治、权限隔离强、服务发布节奏差异大 | 中心 catalog 的 `sourceRoot`、契约路径、GitOps 路径、证据路径 |
| 遗留系统适配仓 | `legacy-adapters/customer-mainframe-adapter/` | 旧系统绞杀迁移、主机/ERP/SaaS 集成、反腐层建设 | 领域归属、接口契约、迁移状态、弃用计划、风险登记 |

无论源码放在哪里，都必须满足以下不变量：

```yaml
service: customer-profile-service
domain: customer
owner: team-customer
sourceRoot: domains/customer/services/customer-profile-service
runtimeUnit: container
buildDefinition: Dockerfile
catalogComponent: catalog/components/customer-profile-service.yaml
gitopsPath: infra/gitops/environments/prod/customer/customer-profile-service
apiContracts:
  - contracts/apis/customer-profile.openapi.yaml
eventContracts:
  publishes:
    - contracts/events/customer.profile.updated.asyncapi.yaml
sloRef: governance/slo/tier-2.yaml
runbook: governance/playbooks/customer-profile-service.md
```

目录名只是线索，不是治理事实。最终权威必须落在机器可读契约里：`service.yaml` 说明服务是谁、怎么构建、依赖什么；
`domain.yaml` 说明领域边界和 owner；`catalog/components` 提供发现入口；`infra/gitops` 说明生产跑哪个版本；治理证据说明
能否发布、谁批准、风险是否接受。

### 2.1.15 单个服务目录的最小内部结构

一个服务目录不应只是源码文件夹，而应是“可构建、可测试、可观测、可审计”的运行单元源头。推荐最小结构如下：

```text
customer-profile-service/
├── README.md                    # 给人看的服务说明、启动方式、依赖和排障入口
├── service.yaml                 # 给机器看的服务契约：owner、domain、端口、依赖、SLO、镜像仓库
├── Dockerfile                   # 镜像构建定义；生产使用 digest，不把镜像本体提交进 Git
├── src/                         # 服务源码；具体结构服从语言生态和框架最佳实践
├── tests/                       # 单元测试、组件测试和契约消费测试
├── apis/                        # 服务拥有的本地 API 契约；可同步或引用到 contracts/apis/
├── events/                      # 服务发布/订阅的本地事件契约；可同步或引用到 contracts/events/
├── migrations/                  # 该服务独占数据库的 schema 迁移；跨域共享库禁止放这里
├── config/                      # 非敏感默认配置和本地开发配置；不保存生产密钥
├── runbooks/                    # 服务级操作手册；企业级通用 playbook 仍放 governance/
└── docs/                        # 设计说明、领域补充和局部 ADR 链接
```

服务目录内允许放“构建和运行这个服务所需的默认事实”，不允许放“某个环境的最终部署事实”。例如端口、健康检查路径、
依赖声明、最低资源诉求、镜像仓库名称可以放在 `service.yaml`；生产副本数、生产镜像 digest、生产命名空间、生产
ServiceAccount、生产 HPA 阈值应放在 `infra/gitops/environments/prod/...`。

| 内容 | 放服务目录 | 放 GitOps / Infra | 原因 |
| ---- | ---------- | ----------------- | ---- |
| 服务源码、测试、Dockerfile | 是 | 否 | 它们描述如何构建服务 |
| 默认端口、健康检查、依赖声明 | 是 | 可派生 | 它们属于服务运行契约 |
| 生产镜像 digest | 否 | 是 | 它属于环境期望状态和发布证据 |
| 生产 replicas、HPA、PDB | 否 | 是 | 它们随环境和容量策略变化 |
| 明文 Secret | 否 | 否 | 只能保存 Secret 引用和外部密钥绑定 |
| 跨域数据库访问脚本 | 否 | 否 | 违反领域边界，应改为 API、事件或数据产品协作 |

如果一个服务目录开始承载多个领域的业务规则，说明服务边界过大；如果一个服务目录开始维护生产环境策略，说明源码和
运行期望状态混在了一起；如果一个服务目录没有 `service.yaml` 或等价契约，说明它还不能被平台和审计系统稳定识别。

### 2.1.16 GitOps 目录的最小内部结构

GitOps 目录回答的是“某个环境期望运行什么”，不是“服务代码是什么”。推荐把环境无关 base、环境 overlay 和环境级
发布状态分开：

```text
infra/
├── kubernetes/
│   ├── base/
│   │   └── services/
│   │       └── customer-profile-service/
│   │           ├── deployment.yaml     # 环境无关工作负载骨架
│   │           ├── service.yaml        # Kubernetes Service，不等同于业务 service.yaml
│   │           ├── hpa.yaml            # 默认自动扩缩容策略
│   │           ├── pdb.yaml            # 可用性保护
│   │           ├── network-policy.yaml # 默认网络边界
│   │           └── kustomization.yaml
│   └── policies/
│       ├── image-verification/         # 镜像签名、SBOM、provenance 准入
│       ├── pod-security/               # Pod 安全基线
│       └── network/                    # 集群网络策略
└── gitops/
    └── environments/
        ├── dev/customer/customer-profile-service/
        │   └── kustomization.yaml      # 开发环境 overlay，可使用短生命周期 tag
        ├── staging/customer/customer-profile-service/
        │   └── kustomization.yaml      # 预发环境 overlay，接近生产
        └── prod/customer/customer-profile-service/
            ├── kustomization.yaml      # 生产 overlay，必须引用不可变 digest
            ├── rollout.yaml            # 金丝雀、蓝绿或渐进式发布策略
            └── release-evidence.yaml   # 发布证据索引或指针
```

GitOps 目录的关键规则：

1. `base/` 只放环境无关模板，不写生产专属镜像版本、命名空间和容量。
2. `dev/` 可以更灵活，但仍不应绕过镜像扫描和基础策略。
3. `staging/` 应尽量接近生产，用来验证迁移、发布策略、回滚和观测。
4. `prod/` 必须使用不可变镜像 digest，禁止只用可变 tag 作为生产准入依据。
5. GitOps 记录期望状态，实际运行状态由 Kubernetes、Argo CD、Flux 和观测系统提供。
6. 环境 owner 对 replicas、资源配额、节点选择、灰度策略和回滚窗口负责，服务 owner 对镜像和服务行为负责。

这层拆清楚后，服务团队可以高频提交源码，平台或 SRE 可以稳定治理环境，审计人员可以追溯“哪个 commit 构建了哪个
镜像、哪个 digest 被部署到哪个环境、哪次 GitOps 同步把它推到生产”。

### 2.1.17 Catalog、service.yaml 和 domain.yaml 的去重规则

catalog 的价值是发现和索引，不是制造新的手工台账。最稳的做法是让 `domain.yaml`、`service.yaml`、GitOps 和契约文件
成为字段真相源，catalog 通过同步、生成或校验来汇总。如果必须人工维护 catalog，也必须记录 sourceRef 和 lastSynced，
并由 CI 检查 catalog 与源契约是否漂移。

| 字段 | 主真相源 | catalog 中的角色 | 漂移处理 |
| ---- | -------- | ---------------- | -------- |
| 领域边界、领域 owner | `domains/{domain}/domain.yaml` | 展示领域地图和团队入口 | catalog 不得覆盖；冲突时阻断合并 |
| 服务 owner、生命周期、运行等级 | `service.yaml` | 展示服务卡片和 scorecard | catalog 只能派生或引用 |
| 源码位置 | 实际 Git 路径 / `sourceRoot` | 提供跳转入口 | 路径不可达时阻断 catalog 检查 |
| API / Event 契约 | `contracts/` 或领域内契约 | 提供 API 门户和消费者索引 | 契约缺失或版本不兼容时阻断发布 |
| GitOps 路径 | `infra/gitops/` | 提供环境入口和发布状态摘要 | catalog 不维护 replicas 和 digest |
| SLO、runbook、on-call | `service.yaml` + `governance/slo/` | 聚合到服务详情页 | 缺 owner、缺 runbook 或缺 SLO 时降 scorecard |
| 生产运行状态 | Kubernetes / Argo CD / Observability | 展示只读摘要 | 运行状态不回写为 catalog 真相 |

推荐的同步方向如下：

```text
domain.yaml + service.yaml + contracts/* + infra/gitops/*
  -> catalog/components/*
  -> Developer Portal / Scorecard / 审计导出
```

反方向更新只能用于辅助生成 PR，不能让 portal 表单直接无审查地改写领域契约、生产 GitOps 或治理证据。这样可以避免
“看起来所有系统都有信息，实际上每个系统都维护一份不同事实”的失控状态。

### 2.1.18 目录级说明文件和 AI 协作边界

企业仓库越来越多由人类、CI、平台机器人和 AI agent 共同维护。目录结构不仅要让人能看懂，也要让自动化工具知道哪里
能改、哪里不能改、改完要跑什么检查。推荐每个一级目录至少有 `README.md`，需要 AI 或自动化协作的关键目录再补
`AGENTS.md` 或等价维护说明。

| 文件 | 读者 | 应说明的内容 | 不应承担的职责 |
| ---- | ---- | ------------ | -------------- |
| `README.md` | 人类开发者、架构师、审计人员 | 目录用途、入口、常见流程、运行方式、参考链接 | 不作为机器契约唯一来源 |
| `AGENTS.md` | AI agent、自动化脚本维护者 | 可改范围、禁止事项、验证命令、目录边界、常见坑 | 不保存业务事实和生产状态 |
| `*.schema.json` | CI、生成器、审计导出 | 字段结构、类型、必填项和扩展边界 | 不解释业务背景 |
| `*.example.yaml` | 团队落地样例、测试夹具 | 最小可执行字段、跨文件一致性示例 | 不替代真实项目配置 |

目录级说明文件要短、准、可执行。它应该告诉后来者“这个目录为什么存在、谁负责、文件怎么放、改完跑什么门禁”，而不是
复制主架构文档。主文档说明原则，目录说明文件约束局部行为，schema 和 checker 负责机器验证。

### 2.1.19 不同规模企业的落地深度

目录结构可以分阶段落地，不能为了“看起来完整”一次性铺满所有目录。不同规模的组织应采用不同深度：

| 阶段 | 适用组织 | 必须具备 | 可以暂缓 |
| ---- | -------- | -------- | -------- |
| S0 起步 | 少量团队、少量服务 | `domains/`、`contracts/apis/`、`catalog/components/`、`infra/gitops/`、`governance/decisions/` | 完整平台门户、完整审计导出、全量 scorecard |
| S1 产品化 | 多领域、多服务、开始平台化 | `platform/golden-paths`、`service.yaml`、API/Event 契约、GitOps 环境分层、CODEOWNERS | 复杂 FinOps、全量 OSCAL、自动化证据新鲜度 |
| S2 规模化 | 多业务线、多团队、多环境 | Developer Portal、数据产品目录、AI 产品目录、供应链证据、风险/POA&M、scorecard | 少数低风险遗留系统可通过 catalog 指针接入 |
| S3 受监管 | 金融、医疗、政企、关键基础设施 | 审计导出、控制评估、签名验签、访问复核、证据新鲜度、事故复盘、合规映射 | 手工例外必须有到期和补偿控制 |

阶段越早，越要避免目录过度复杂；阶段越成熟，越要避免事实散落在聊天记录、平台 UI、人工表格和个人经验里。成熟度提升的
标志不是目录变多，而是更多关键事实可以被机器校验、被 portal 发现、被审计导出、被运行系统证明。

### 2.1.20 目录变更评审清单

新增、移动或删除目录时，必须先回答以下问题，再进入执行：

1. 这个目录是否有明确 owner；如果没有 owner，不应新增。
2. 这个目录是否承载新的真相源；如果只是分类更好看，不应新增。
3. 这个目录的机器消费方是谁；如果没有 CI、portal、GitOps、策略引擎或审计消费方，应先放入现有目录。
4. 这个目录是否会和已有目录维护同一字段；如果会，必须定义主真相源和派生方向。
5. 这个目录是否需要 CODEOWNERS、分支保护、必需检查或发布证据；如果需要，必须同步补门禁。
6. 这个目录是否影响现有服务、契约、GitOps 或审计导出；如果影响，必须补迁移计划和回滚路径。
7. 这个目录是否降低团队认知负载；如果只是增加文件层级和审批步骤，应回到平台产品化设计。

目录变更的验收不应只看“文件移动完成”。真正完成的标准是：旧路径有迁移说明，新路径有 owner 和说明文件，相关契约、
catalog、GitOps、治理证据和自动化检查都能找到新位置，并且没有同一事实在新旧路径双写。

### 2.1.21 目录结构的三类事实

企业级目录结构不是简单的文件分类，而是在仓库中表达三类事实：权威事实、派生事实和观察事实。把这三类事实混在一起，
是目录越做越乱的根因。

| 事实类型 | 定义 | 典型位置 | 变更方式 | 校验方式 |
| -------- | ---- | -------- | -------- | -------- |
| 权威事实 | 某个字段或行为的唯一真相源 | `domains/`、`contracts/`、`infra/gitops/`、`governance/` | 通过 PR、owner 审批和门禁修改 | schema、contract test、policy check、CODEOWNERS |
| 派生事实 | 从权威事实生成或同步出来的索引、视图、门户卡片 | `catalog/`、Developer Portal、审计导出包 | 自动生成或受控同步 | 漂移检测、sourceRef、lastSynced |
| 观察事实 | 运行系统在某一时刻观测到的实际状态 | Kubernetes、Argo CD、Flux、Observability、SIEM | 由运行系统产生，不手写入 Git | SLO、告警、运行探针、审计日志 |

因此，`catalog/components/customer-profile-service.yaml` 可以展示生产环境当前状态摘要，但不能成为生产副本数、镜像 digest
或资源配额的权威来源；`docs/` 可以解释领域设计，但不能替代 `domain.yaml`、OpenAPI、AsyncAPI 或数据产品契约；平台
门户可以提供修改入口，但最终仍应生成 PR，由对应权威目录完成审查、合并、部署和审计。

判断某个字段应该放在哪里时，优先使用以下规则：

1. 会直接改变业务行为的字段，放领域或 AI 产品的权威契约中。
2. 会直接改变生产运行状态的字段，放 `infra/gitops/` 或环境 IaC 中。
3. 会改变跨团队兼容性的字段，放 `contracts/` 或领域内等价契约中。
4. 会改变准入、风险、合规或例外处理的字段，放 `governance/` 中。
5. 只用于发现、导航、搜索和聚合展示的字段，放 `catalog/`，并指向权威来源。
6. 只用于解释背景、设计原因和操作说明的内容，放 `docs/` 或局部 `README.md`。

### 2.1.22 目录与自动化链路

成熟的目录结构必须能被工具链消费。否则它只是“看起来整齐”的文档目录，无法形成平台能力。

```text
service.yaml / domain.yaml / contracts/*
  -> CI 契约校验
  -> catalog 同步
  -> Developer Portal 展示
  -> scorecard 评分
  -> release gate 准入
  -> audit export 证据导出

Dockerfile / SBOM / provenance / signature
  -> CI 构建
  -> registry 入库
  -> 镜像签名和验签
  -> GitOps 引用 digest
  -> Kubernetes 准入控制

infra/gitops/environments/*
  -> Argo CD / Flux 同步
  -> runtime 状态观测
  -> SLO 和告警
  -> 事故响应和回滚证据

governance/* / 控制目录 / evidence/*
  -> policy check
  -> risk register / POA&M
  -> audit package
  -> 管理层例外和复核
```

每个一级目录都应至少接入一种自动化消费方：

| 目录 | 最低自动化消费方 | 未接入时的风险 |
| ---- | ---------------- | -------------- |
| `apps/` | CI、发布系统、前端监控 | 体验变更无法和 API、SLO、回滚证据关联 |
| `ai/` | Evals、LLM Gateway、AI observability | Prompt、Agent 和工具权限变成手工配置，无法审计 |
| `domains/` | 契约测试、服务构建、catalog 同步 | 领域边界停留在文档，服务和 owner 容易漂移 |
| `platform/` | 脚手架、portal、scorecard | 平台只是一组散装脚本，不能降低认知负载 |
| `contracts/` | 兼容性检查、代码生成、网关、策略引擎 | 跨团队协作依赖口头约定，breaking change 难以及时发现 |
| `catalog/` | Developer Portal、依赖图、审计导出 | 服务、资源和 owner 无法被统一发现 |
| `governance/` | 门禁脚本、审计导出、风险工作流 | 标准和例外无法闭环，审计只能补材料 |
| `infra/` | GitOps、Kubernetes、云平台、准入控制 | 生产状态依赖人工操作，回滚和追责困难 |

目录一旦进入企业级标准，就必须定义“谁消费它”。没有消费方的目录应先作为局部文档或实验目录，不应升级为一级标准目录。

### 2.1.23 资产生命周期和目录字段

服务、API、事件、数据产品、AI 产品、模型、Agent、平台能力和治理控制项都应有生命周期字段。生命周期不清楚，目录就会
不断堆积僵尸资产。

| 状态 | 含义 | 允许行为 | 必填证据 |
| ---- | ---- | -------- | -------- |
| `proposed` | 已提出但未进入生产依赖 | 可评审、可试点，不得被生产消费者强依赖 | owner、目标场景、风险初评、退出条件 |
| `active` | 正式运行并可被消费者依赖 | 可发布、可扩展、可进入 scorecard | SLO、runbook、契约、GitOps、监控、on-call |
| `deprecated` | 已宣布弃用但仍需兼容 | 不新增消费者，只允许安全修复和迁移支持 | 替代方案、迁移窗口、消费者清单、到期日 |
| `retired` | 已退役，不再承载生产职责 | 不允许被部署、调用或列入新依赖 | 下线证据、数据归档、DNS/API/topic 清理记录 |
| `exception` | 临时偏离标准 | 只能在到期日前带补偿控制运行 | 风险 owner、到期日、补偿控制、POA&M |

推荐在不同资产中统一保留以下字段名，减少跨目录理解成本：

```yaml
name: customer-profile-service
lifecycle: active
owner: team-customer
domain: customer
tier: tier-2
sourceRoot: domains/customer/services/customer-profile-service
contractRefs:
  - contracts/apis/customer-profile.openapi.yaml
gitopsRefs:
  - infra/gitops/environments/prod/customer/customer-profile-service
sloRef: governance/slo/tier-2.yaml
runbookRef: governance/playbooks/customer-profile-service.md
riskRefs:
  - governance/risk-register/risk-customer-profile.yaml
evidenceRefs:
  - governance/evidence/releases/customer-profile-service-2026-06.yaml
```

字段名可以按企业标准调整，但语义必须稳定。尤其是 `owner`、`lifecycle`、`sourceRoot`、`contractRefs`、`gitopsRefs`、
`sloRef`、`runbookRef` 和 `evidenceRefs`，应成为 catalog、scorecard、审计导出和 AI agent 协作的公共接口。

### 2.1.24 环境、租户和区域的目录表达

不要把环境差异混进服务源码。服务源码表达“服务是什么”，环境目录表达“它在某个环境如何运行”。多租户、多区域、多云和
受监管环境尤其要遵守这条边界。

推荐表达方式如下：

```text
infra/gitops/environments/
├── dev/
│   └── customer/customer-profile-service/
├── staging/
│   └── customer/customer-profile-service/
├── prod/
│   ├── region-cn-north/customer/customer-profile-service/
│   └── region-us-east/customer/customer-profile-service/
└── regulated/
    └── finance/customer/customer-profile-service/
```

环境目录应管理以下事实：

| 维度 | 应放环境目录 | 不应放服务源码 |
| ---- | ------------ | -------------- |
| 容量 | replicas、HPA、资源配额、GPU 配额 | 不同环境的生产容量 |
| 网络 | namespace、Ingress、Gateway、NetworkPolicy | 生产域名和网络放通细节 |
| 安全 | ServiceAccount、准入策略、镜像验签、Secret 引用 | 明文密钥和环境权限 |
| 发布 | digest、灰度策略、回滚窗口、冻结期 | 生产版本选择 |
| 合规 | 数据驻留、审计日志、加密、备份保留 | 监管环境专属例外 |

如果企业采用多仓 GitOps，也应保持同样结构，只是把 `infra/gitops/` 拆到独立环境仓。服务仓通过 `service.yaml.gitopsRefs`
或 catalog 指回环境仓路径，不能让服务仓单方面决定生产部署事实。

### 2.1.25 目录结构的常见反模式和修复

| 反模式 | 表现 | 后果 | 修复方式 |
| ------ | ---- | ---- | -------- |
| `shared/` 变成业务中台 | 所有领域都把通用业务逻辑塞进共享库 | 领域边界消失，升级牵一发动全身 | 只保留无业务语义工具；业务能力迁回领域服务或领域包 |
| `platform/` 接管业务部署 | 平台目录里维护每个业务服务的生产配置 | 平台团队成为发布瓶颈，服务 owner 失责 | 平台只提供模板和能力；环境期望状态放 `infra/gitops/` |
| `catalog/` 手工双写事实 | catalog 里手填 owner、路径、digest、SLO | portal 看起来完整，实际和源码/GitOps 漂移 | catalog 只引用或派生；CI 做 sourceRef 漂移检查 |
| `docs/` 替代契约 | README 写了 API、事件和数据口径，但无机器契约 | 消费者无法自动发现 breaking change | 建 OpenAPI、AsyncAPI、Schema 和 data contract |
| `infra/` 混入业务规则 | Helm values 或 Kustomize overlay 写业务开关和领域逻辑 | 运行团队被迫理解业务，回滚风险扩大 | 业务规则回到服务配置或领域策略；环境只管运行差异 |
| `ai/` 绕过领域边界 | Agent 直接读业务库或直接改核心状态 | AI 层成为隐形超级用户，审计和一致性失控 | Agent 只能通过 API、事件、数据产品和受控工具访问能力 |
| `governance/` 只有文档没有门禁 | 标准写得完整，但 CI、准入和审计不消费 | 规则无法执行，例外无法关闭 | 为控制项补 schema、checker、evidence 和 owner |

目录治理的原则是：能从结构上消除的混乱，不要靠培训解决；能被机器校验的事实，不要靠人工复核兜底；能由平台默认路径
生成的模板，不要让每个团队重新手写一遍。

### 2.1.26 2.1 的最终验收标准

评审 2.1 推荐目录结构时，应把问题问到可执行层，而不是停在“目录是否全面”：

1. 任意一个服务，从 catalog 入口能否追到源码、契约、GitOps、SLO、runbook、owner 和发布证据。
2. 任意一个生产 Pod，能否反向追溯到镜像 digest、SBOM、provenance、签名、构建 commit 和代码 owner。
3. 任意一个 API breaking change，能否自动识别消费者、触发兼容性门禁，并进入迁移或例外流程。
4. 任意一个数据产品，能否证明语义口径、质量规则、PII、血缘、访问授权和 AI 使用边界。
5. 任意一个 AI Agent，能否证明 Prompt 版本、工具权限、RAG 数据源、评估结果、护栏、人工确认点和事故响应路径。
6. 任意一个治理控制项，能否追到标准、schema、示例、checker、证据、风险、POA&M 和审计导出结果。
7. 任意一个目录变更，能否说明 owner、消费方、主真相源、派生方向、门禁、迁移方式和回滚方式。

如果这些问题可以被自动化工具回答大部分，目录结构就是企业级平台架构；如果只能靠人开会解释，目录结构仍然只是文档草图。

---

## 2.2 微服务容器分层真相源

每个微服务可以被构建成一个或多个容器镜像，但容器能力不应被放进单一目录统一管理。正确做法是按“源码、制品、部署期望状态、实际运行状态、目录发现、平台能力、治理规则”拆分真相源。

| 问题 | 真相源位置 |
| ---- | ---------- |
| 服务代码推荐放哪里 | 默认放 `domains/{domain}/services/{service}/`；若采用 `services/*`、`apps/*`、polyrepo 或独立服务仓，必须在 `service.yaml` / catalog 中声明源码路径 |
| Dockerfile / Containerfile 在哪里 | `domains/{domain}/services/{service}/Dockerfile` |
| 镜像本体在哪里 | Container Registry / Artifact Registry，不进入 Git 仓库 |
| 哪个镜像版本部署到 prod | `infra/gitops/environments/prod/...` |
| Kubernetes Deployment / Service / HPA 在哪里 | `infra/kubernetes/` 或 `infra/gitops/` |
| 服务属于哪个领域 | `domains/{domain}/domain.yaml` 和 `catalog/components/` |
| API / Event 契约在哪里 | `contracts/` 或 `domains/*/apis`、`domains/*/events` |
| CI/CD 模板在哪里 | `platform/ci-cd/` |
| 服务脚手架在哪里 | `platform/scaffolds/` |
| 运行标准在哪里 | `governance/standards/` |
| 当前运行状态在哪里 | Kubernetes / Argo CD / Flux / Observability，不是 Git 文档 |

推荐边界：

```text
服务源码与镜像构建定义：domains/*/services/* 或 catalog/sourceRoot 指向的服务仓库路径
镜像制品：container registry
部署期望状态：infra/gitops/* 或 infra/kubernetes/*
实际运行调度：Kubernetes
服务目录与 owner 关系：catalog/*
平台标准能力：platform/*
治理规则：governance/*
```

关键原则：

1. 服务目录是运行单元源头，不是环境部署真相源。
2. 镜像使用 tag 便于人类识别，生产准入和回滚必须能追溯到 digest。
3. GitOps 目录声明期望状态，不记录运行时实际状态。
4. catalog 负责发现、owner、依赖和成熟度，不替代 deployment manifest。
5. platform 负责模板、流水线、扫描、签名、准入和开发者体验，不接管业务服务部署细节。

## 3. 架构设计原则

### 3.1 业务结果端到端负责

业务流团队不只是提出需求，而是对客户体验、业务指标、服务稳定性和持续优化负责。技术团队不再只是被动交付项目，而是与业务共同运营产品。

### 3.2 领域能力产品化

用户、商品、订单、支付、履约、风控、营销等能力不应只是技术服务，而应作为长期运营的领域产品。每个领域产品都应具备清晰的边界、API、事件、数据产品、SLO 和业务指标。

### 3.3 平台能力自助化

平台团队不替业务团队写业务逻辑，而是提供可复用、可自助、可治理的工程能力，使业务团队可以快速创建服务、申请环境、发布应用、接入监控、配置权限和查看成本。

### 3.4 数据作为产品

数据不再只是中央数据团队统一抽取和加工的结果，而是由最理解业务的领域团队负责发布、解释和治理。数据产品必须可发现、可理解、可信任、可复用、可追责。

### 3.5 治理自动化

治理不应主要依赖人工审批，而应通过平台默认能力、CI/CD 质量门禁、Policy as Code、数据契约、安全扫描、成本规则和可观测性自动执行。

### 3.6 松耦合与清晰边界

系统之间通过标准 API、领域事件、数据契约和服务协议进行协作。禁止跨域直接访问数据库，禁止绕过领域边界调用内部实现。

### 3.7 演进式架构

架构不追求一次性大而全建设，而应通过重点领域、重点平台能力和重点数据产品逐步演进，避免把集中化模式换个名字重做一遍。

### 3.8 AI 原生但不旁路领域边界

AI 应用、Agent 和自动化决策必须建立在领域 API、领域事件、数据产品和受控工具之上。AI 层可以编排、解释、推荐和自动执行低风险动作，但不能直接绕过领域边界读写数据库，也不能把 Prompt、向量索引或 Agent 记忆变成新的业务真相源。

### 3.9 供应链可证明

软件交付不应只检查代码质量和漏洞，还必须证明产物从源码、构建、依赖、镜像、签名到部署的完整链路。生产发布必须能够回答：这个产物由谁构建、基于哪些依赖、生成了什么 SBOM、是否有可验证 provenance、是否经过签名验签和策略准入。

### 3.10 认知负载可管理

平台工程的目标不是堆工具，而是减少业务团队理解和操作底层复杂度的负担。每个 Golden Path、平台产品和治理规则都应检查是否降低团队认知负载；如果平台能力增加了配置、审批和排障复杂度，就必须回到产品化视角重新设计。

---

## 4. 分层架构说明

## 4.1 前台体验层

### 4.1.1 定位

前台体验层直接面向用户、客户、合作方、员工和运营人员，是企业数字化能力的外部表现。

### 4.1.2 主要组成

包括但不限于：

1. Web 网站。
2. 移动 App。
3. 小程序。
4. Open API 门户。
5. 运营后台。
6. 合作方门户。
7. 客服工作台。
8. 员工工作台。
9. 智能助手入口。

### 4.1.3 设计要求

前台体验层应重点关注用户体验、渠道一致性、性能、可用性和业务转化。不同渠道可以共享底层领域能力，但不应直接耦合底层领域服务的复杂接口。

### 4.1.4 责任边界

前台团队负责：

1. 客户旅程设计。
2. 页面与交互体验。
3. 渠道转化指标。
4. 前端性能体验。
5. 前端埋点与用户行为分析。
6. 与体验编排层的接口协作。

---

## 4.2 体验编排层

### 4.2.1 定位

体验编排层位于前台体验和领域能力之间，负责将多个领域能力组合为适合具体场景的体验接口。

### 4.2.2 主要组成

1. BFF，即 Backend for Frontend。
2. API Gateway。
3. GraphQL 网关。
4. 业务流程编排。
5. 事件订阅与通知。
6. 聚合查询服务。
7. 低代码流程配置。
8. 场景化 API。

### 4.2.3 设计要求

体验编排层应避免沉淀核心业务规则。核心业务规则应归属于领域能力产品层。体验编排层主要处理渠道适配、接口聚合、流程编排、权限上下文、协议转换和体验优化。

### 4.2.4 禁止事项

1. 禁止将领域核心规则长期堆积在 BFF 中。
2. 禁止绕过领域 API 直接访问领域数据库。
3. 禁止通过编排层形成新的集中式共享层。
4. 禁止将跨域一致性完全依赖同步调用。

---

## 4.3 AI 原生能力层

### 4.3.1 定位

AI 原生能力层位于体验编排、领域能力产品和数据产品网络之间，负责把大模型、Agent、RAG、特征、向量检索和受控工具组合为可运营、可评估、可审计的 AI 产品能力。

AI 层不是一个新的业务真相源。它必须通过领域 API 执行业务动作，通过领域事件感知业务状态，通过数据产品和特征产品获得可解释上下文，通过受治理工具调用完成自动化任务。

### 4.3.2 核心组成

AI 原生能力层包括：

1. AI 应用：智能客服、运营助手、研发助手、风控辅助、销售助手、知识问答和自动化运营。
2. Agent Runtime：负责 Agent 状态、工具调用、记忆、计划、重试、人工确认和隔离执行。
3. LLM Gateway：统一模型接入、模型路由、降级、限流、审计、成本控制和输出策略。
4. RAG 管道：文档摄取、切分、Embedding、索引、召回、重排、引用和上下文组装。
5. 向量存储：用于知识检索、相似度搜索、多模态检索和语义缓存。
6. PromptOps：Prompt 模板、版本、变更记录、评测样例、灰度和回滚。
7. Model Registry：模型、Embedding 模型、重排模型、批准状态、适用场景和风险等级。
8. Evaluation Pipeline：离线评测、在线评测、回归集、对抗样本、人工标注和质量阈值。
9. Guardrails：输入输出校验、PII 过滤、越权拦截、敏感动作确认、内容安全和策略执行。
10. AI Observability：Token、延迟、模型错误、幻觉率、引用命中率、工具调用、成本和用户反馈。
11. Tool Registry：AI 可调用工具、权限范围、幂等要求、超时、审计和危险等级。
12. Agent-to-Agent 协议适配：用于多 Agent 协作、任务交接和能力发现，但必须受平台策略约束。

### 4.3.3 AI Mesh 与领域网络关系

AI Mesh 是 AI 能力的分布式协作网络，不是集中式 AI 大脑。企业可以把每个领域中可复用的 AI 能力封装为 AI 产品，让它们通过统一网关、工具契约和治理策略互相协作。

```text
AI 应用 / Agent
    │
    ├── 调用领域 API：执行查询、创建、审批、取消、补偿等业务动作
    ├── 订阅领域事件：感知订单变化、支付结果、风控结果和履约状态
    ├── 消费数据产品：获取事实数据、聚合指标、标签、人群和业务口径
    ├── 消费特征产品：获取训练和推理一致的实时/离线特征
    ├── 检索向量索引：获取可引用知识、政策、文档、案例和历史记录
    └── 写入审计事件：记录 Prompt、上下文、模型、工具调用、输出和人工确认
```

AI Mesh 的边界原则：

1. 每个 AI 产品必须有 owner、业务目标、用户、风险等级、评估集和退出机制。
2. Agent 只能调用注册过的工具，工具必须声明权限、输入输出 Schema、幂等性、超时和审计字段。
3. AI 层不得直接读写领域数据库，所有业务动作必须经过领域 API 或受控工作流。
4. RAG 索引不得替代原始数据产品和领域知识库，索引必须可追溯到源文档、版本和授权策略。
5. 高风险动作必须有人类确认或双人复核，不能只依赖模型自我判断。
6. AI 产品必须支持灰度、A/B、回滚、降级到非 AI 流程和人工接管。

### 4.3.4 LLM Gateway 契约

LLM Gateway 是模型接入和治理的统一入口，避免各团队在应用里分散配置模型、密钥、成本和审计策略。

LLM Gateway 必须提供：

1. 模型路由：按场景、成本、延迟、质量和合规要求选择模型。
2. 凭证隔离：应用不直接持有模型供应商密钥。
3. 限流与预算：按团队、产品、环境、用户和模型设置配额。
4. 审计记录：记录请求元数据、模型版本、Prompt 版本、Token、工具调用和策略结果。
5. 降级策略：模型不可用、质量下降或成本异常时切换模型、缩小上下文或进入人工流程。
6. 内容策略：输入输出过滤、敏感信息识别、越权提示拦截和危险操作阻断。
7. 可观测性：统一暴露延迟、错误、Token、成本、拒绝率、重试率和质量反馈指标。

### 4.3.5 RAG 与向量索引标准

RAG 管道必须把“可回答”建立在“可追溯”之上。

RAG 标准包括：

1. 摄取源必须登记 owner、授权范围、更新频率、保留期限和数据分级。
2. 文档切分必须保留源链接、版本、时间、章节、权限标签和业务域。
3. Embedding 模型变更必须触发索引重建评估，避免召回质量无声下降。
4. 检索必须支持权限过滤，不能把无权访问的片段放入上下文。
5. 生成结果必须携带引用或证据来源，关键业务答案必须能回溯到源材料。
6. 召回、重排、生成和引用命中率必须纳入评估集。
7. RAG 索引必须支持删除、重建、过期和来源撤销，不能成为隐性数据湖。

### 4.3.6 Prompt、评估和发布门禁

Prompt 和 Agent 工作流属于生产资产，必须像代码一样管理版本和发布。

AI 发布门禁至少包括：

1. Prompt 版本、模型版本、工具版本和检索配置可追溯。
2. 离线评测集覆盖核心业务问题、边界问题、越权问题、幻觉诱导和成本边界。
3. 在线评测覆盖用户反馈、人工抽检、引用命中率、任务完成率和负反馈率。
4. 高风险场景必须有人类确认、回放审计和熔断策略。
5. 每次模型、Prompt、工具或 RAG 配置变更必须有回归评测。
6. 低质量输出、异常成本、越权调用、无引用回答和工具失败必须触发告警。

### 4.3.7 AI 产品标准目录

AI 产品必须以机器可读契约进入仓库、catalog 和治理流程。

```text
ai/applications/customer-service-agent/
├── ai-product.yaml
├── prompts/
│   ├── system.prompt.md
│   └── policy.prompt.md
├── agents/
│   └── customer-service-agent.yaml
├── tools/
│   └── tool-permissions.yaml
├── rag/
│   ├── sources.yaml
│   ├── chunking.yaml
│   └── retrieval.yaml
├── evals/
│   ├── regression.yaml
│   ├── adversarial.yaml
│   └── cost.yaml
├── guardrails/
│   └── policy.rego
├── observability/
│   └── dashboard.yaml
└── docs/
    ├── README.md
    └── runbook.md
```

`ai-product.yaml` 示例：

```yaml
name: customer-service-agent
owner: team-customer-experience
lifecycle: production
riskTier: high
users:
  - customer-service-operators
businessGoal:
  - reduce-average-handle-time
  - improve-first-contact-resolution
modelGateway:
  route: support-safe-default
  maxInputTokens: 16000
  maxOutputTokens: 2000
  monthlyBudgetUsd: 3000
tools:
  allowed:
    - tool:domain:order:get-order-status
    - tool:domain:customer:create-support-ticket
  requiresHumanApproval:
    - tool:domain:payment:refund
rag:
  sources: rag/sources.yaml
  retrieval: rag/retrieval.yaml
evals:
  regression: evals/regression.yaml
  adversarial: evals/adversarial.yaml
guardrails:
  piiPolicy: guardrails/policy.rego
observability:
  dashboard: observability/dashboard.yaml
slo:
  taskCompletionRate: ">= 85%"
  groundedAnswerRate: ">= 95%"
  toolErrorRate: "<= 2%"
  p95LatencyMs: 6000
```

### 4.3.8 Agent 协议与工具边界

Agent 协议层应解决“工具如何暴露、上下文如何传递、Agent 如何协作”的互操作问题，但不能替代权限、审计和业务边界。

建议分层：

| 协议层 | 解决问题 | 设计边界 |
| ------ | -------- | -------- |
| Tool / Context Protocol | 让模型或 Agent 发现工具、资源、Prompt 和上下文 | 不授予业务权限，只描述可调用能力 |
| Agent-to-Agent Protocol | 让不同 Agent 进行任务发现、委托、状态同步和结果回传 | 不允许绕过平台网关、审计和风险等级 |
| Domain API / Workflow | 执行真正业务动作 | 必须由领域团队拥有，并受权限和 SLO 约束 |

Agent 协议治理要求：

1. 所有工具进入 Tool Registry，声明 owner、输入输出 Schema、幂等性、超时、速率限制和危险等级。
2. Agent 调用工具必须经过 LLM Gateway 或 Agent Runtime 统一审计。
3. Agent 之间不能直接传递敏感数据，必须保留数据分级、用户权限和用途约束。
4. 多 Agent 协作必须有任务上限、循环上限、预算上限和人工接管点。
5. 协议适配器只做连接和编排，不承载领域业务规则。

### 4.3.9 微调治理工作流

微调不是默认选项。只有当 Prompt、RAG、工具调用、检索重排和模型路由无法稳定满足需求，并且业务收益足以覆盖训练、评估、合规和维护成本时，才应启动微调。

微调场景必须单独治理，因为它会把训练数据、模型权重、实验参数和评估结果变成新的生产资产。

推荐工作流：

1. 场景论证：说明为什么 Prompt / RAG / 工具编排不足以解决问题。
2. 数据授权：声明训练数据来源、owner、分级、PII、版权、保留期限和是否允许用于微调。
3. 数据准备：记录清洗、脱敏、去重、采样、标签质量和训练/验证/测试划分。
4. 实验追踪：记录基础模型、超参数、训练配置、数据版本、代码版本、运行环境和成本。
5. 评估门禁：使用独立评估集验证质量、安全、偏见、幻觉、越权、泄露和成本。
6. 模型登记：微调模型必须进入 Model Registry，拥有独立版本、风险等级、适用范围和回滚点。
7. 合规审查：高风险或敏感数据微调必须经过数据、安全、法务或合规负责人确认。
8. 灰度发布：微调模型先进入小流量或 shadow 评估，再替换生产模型。
9. 持续监控：监控模型漂移、质量回退、数据泄露、成本异常和用户反馈。
10. 退役机制：模型过期、数据授权撤销或质量下降时必须支持禁用、回滚和删除。

`fine-tuning-run.yaml` 示例：

```yaml
name: support-answer-style-tuning
owner: team-customer-experience
baseModel: vendor:model-name:2026-05
riskTier: R3
reason: prompt-and-rag-failed-to-meet-tone-consistency
trainingData:
  sourceDataProducts:
    - data-product:support:resolved-ticket-dialogs
  classification: confidential
  piiRemoved: true
  allowedUse:
    - supervised-fine-tuning
  disallowedUse:
    - foundation-model-training
experimentTracking:
  tracker: mlflow
  experimentId: support-answer-style-tuning-2026-06
  codeVersion: git:abc123
  dataVersion: dataset:v18
evals:
  quality: evals/support-quality.yaml
  safety: evals/support-safety.yaml
  regression: evals/support-regression.yaml
approval:
  dataOwner: team-support-data
  securityReviewer: team-security
  modelReviewer: team-ai-platform
deployment:
  shadowTrafficPercent: 5
  rollbackModel: vendor:model-name:2026-05
```

---

## 4.4 领域能力产品层

### 4.4.1 定位

领域能力产品层是企业数字化平台的核心层。它承载企业关键业务能力，并以领域产品的方式长期运营。

### 4.4.2 典型领域划分

企业可根据实际业务划分领域，常见包括：

| 领域   | 主要能力                |
| ---- | ------------------- |
| 用户域  | 注册、登录、账户、身份、会员、用户画像 |
| 商品域  | 商品资料、类目、属性、价格、上下架   |
| 订单域  | 购物车、下单、订单状态、订单履约协同  |
| 支付域  | 收款、退款、对账、支付渠道接入     |
| 履约域  | 库存、仓储、配送、签收、售后      |
| 风控域  | 交易风控、账户风控、反欺诈、风险评分  |
| 营销域  | 优惠券、活动、权益、推荐、触达     |
| 内容域  | 内容生产、审核、发布、标签、分发    |
| 客服域  | 工单、会话、服务记录、投诉处理     |
| 合作方域 | 合作方准入、合同、分账、结算      |

### 4.4.3 每个领域产品必须具备的内容

每个领域产品应至少包含：

1. 领域愿景和业务目标。
2. 领域边界和上下文图。
3. 业务 API。
4. 领域事件。
5. 领域模型。
6. 服务边界。
7. 数据产品。
8. SLO 和运行指标。
9. 权限模型。
10. 变更策略。
11. 版本管理策略。
12. 领域团队责任人。

### 4.4.4 领域服务交互方式

领域之间优先采用以下方式协作：

1. 同步 API：用于强一致、实时查询或明确请求响应的场景。
2. 领域事件：用于状态变化通知、异步解耦和最终一致性场景。
3. 数据产品：用于分析、报表、AI、特征和跨域洞察场景。
4. 工作流编排：用于跨领域长流程和补偿机制。

### 4.4.5 领域边界原则

1. 一个领域拥有自己的核心模型。
2. 一个领域拥有自己的核心数据。
3. 其他领域不能直接读写该领域数据库。
4. 跨领域协作通过 API、事件或数据产品完成。
5. 领域团队对业务规则、接口稳定性和运行质量负责。

### 4.4.6 领域产品标准目录

每个领域产品应有稳定目录，确保领域边界、运行责任和接口契约可追踪。

```text
domains/order/
├── domain.yaml
├── apis/
│   ├── public.openapi.yaml
│   └── internal.openapi.yaml
├── events/
│   └── order-status-changed.asyncapi.yaml
├── services/
│   ├── order-command-service/
│   ├── order-query-service/
│   └── order-workflow-worker/
├── workflows/
│   └── order-lifecycle.bpmn
├── data-products/
│   ├── order-facts/
│   └── order-status-snapshot/
├── policies/
│   ├── access.rego
│   └── retention.yaml
├── scorecards/
│   └── domain-readiness.yaml
└── docs/
    ├── README.md
    ├── domain-model.md
    ├── runbook.md
    └── decision-log.md
```

`domain.yaml` 示例：

```yaml
name: order
displayName: 订单领域
owner: team-order
lifecycle: production
businessCapability:
  - order-capture
  - order-lifecycle
  - order-query
boundedContext:
  upstream:
    - customer
    - product
    - payment
  downstream:
    - fulfillment
    - risk
interfaces:
  providesApis:
    - domain:order:orders-public-api
    - domain:order:orders-internal-api
  publishesEvents:
    - domain:order:order-created
    - domain:order:order-status-changed
  ownsDataProducts:
    - data-product:order:order-facts
    - data-product:order:order-status-snapshot
slo:
  availability: 99.95
  commandLatencyP95Ms: 300
  queryLatencyP95Ms: 200
governance:
  dataClassification: confidential
  pii: true
  architectureGate: tier-1-domain
```

### 4.4.7 领域服务运行契约

领域服务必须是可以独立启动、停止、测试、部署、扩缩容和回滚的运行边界。

```text
domains/order/services/order-command-service/
├── src/
├── tests/
├── deploy/
├── configs/
├── service.yaml
├── catalog-info.yaml
├── Dockerfile                         # 或 Containerfile
├── README.md
└── AGENTS.md
```

`service.yaml` 示例：

```yaml
name: order-command-service
domain: order
owner: team-order
lifecycle: production
runtime: service
entrypoints:
  http:
    port: 8080
  events:
    consumes:
      - domain:payment:payment-authorized
    publishes:
      - domain:order:order-created
dependencies:
  resources:
    - resource:order-primary-db
    - resource:order-event-topic
  apis:
    - domain:customer:customer-internal-api
dataAccess:
  owns:
    - order_primary_db
  reads:
    - customer_profile_view
container:
  dockerfile: Dockerfile
  imageRepository: registry.company.com/order/order-command-service
  tagPolicy: git-sha
  digestRequired: true
  sbomRequired: true
  provenanceRequired: true
  signatureRequired: true
resources:
  requests:
    cpu: "500m"
    memory: "512Mi"
  limits:
    cpu: "2"
    memory: "2Gi"
slo:
  availability: 99.95
  latencyP95Ms: 300
operations:
  health: /health
  readiness: /ready
  runbook: docs/runbook.md
  rollback: deploy/rollback.md
```

### 4.4.8 服务容器化边界

领域服务目录只保存“如何构建和运行这个服务”的源头信息，不保存镜像制品，也不保存每个环境的部署期望状态。

服务团队负责：

1. 服务代码、测试和启动入口。
2. Dockerfile / Containerfile。
3. `service.yaml` 中的端口、健康检查、依赖、资源诉求和镜像仓库声明。
4. 服务级 runbook、rollback 说明和本地调试方式。
5. 服务 API、事件和数据访问边界。

不应放在服务目录中的内容：

1. 生产镜像本体。
2. dev、staging、prod 的 Deployment 副本数和镜像 digest。
3. 环境级 Secret 值。
4. 集群级准入策略。
5. Argo CD / Flux 的环境同步状态。

---

## 4.5 数据产品网络层

### 4.5.1 定位

数据产品网络层负责将各领域产生的数据转化为可信、可发现、可理解、可复用的数据产品，为经营分析、业务运营、风险控制、AI 应用、特征服务、向量检索和管理决策提供支撑。

### 4.5.2 数据产品类型

| 类型                            | 说明                      | 示例                |
| ----------------------------- | ----------------------- | ----------------- |
| Source-aligned Data Product   | 源对齐数据产品，由领域团队基于原始业务数据发布 | 订单明细数据产品、支付流水数据产品 |
| Aggregate Data Product        | 聚合数据产品，对多个源数据产品进行汇总加工   | 用户交易汇总、商品销售汇总     |
| Consumer-aligned Data Product | 面向具体消费场景的数据产品           | 经营驾驶舱、风控特征集、营销人群包 |

### 4.5.3 数据产品基本要求

一个合格的数据产品应包含：

1. 数据产品名称。
2. 业务定义。
3. 数据拥有者。
4. 数据使用者。
5. 数据血缘。
6. 数据字段说明。
7. 口径说明。
8. 更新频率。
9. 数据质量规则。
10. 权限与分级。
11. SLA 或 SLO。
12. 使用示例。
13. 变更通知机制。
14. 下游依赖清单。
15. AI 消费声明：是否允许用于训练、Embedding、RAG、特征、评估或在线推理。
16. 训练-推理一致性要求：是否需要离线特征、在线特征和实时推理端点同步校验。

### 4.5.4 数据能力组成

数据产品网络层包括：

1. 数据目录。
2. 元数据管理。
3. 数据血缘。
4. 数据质量检测。
5. 指标平台。
6. 语义层。
7. 特征平台。
8. 在线特征存储。
9. 向量索引和检索服务。
10. 报表平台。
11. 实时数据服务。
12. AI 数据服务。
13. 数据权限管理。
14. 数据脱敏与审计。

### 4.5.5 数据治理原则

1. 谁产生核心业务数据，谁负责解释数据含义。
2. 谁发布数据产品，谁负责数据质量。
3. 核心指标必须有统一口径。
4. 重要数据必须有血缘、质量规则和变更通知。
5. 敏感数据必须分级、脱敏、授权和审计。
6. 数据消费必须可追踪、可监控、可问责。

### 4.5.6 数据产品标准目录

数据产品目录应把业务语义、技术 Schema、质量规则、血缘、访问策略和消费样例放在一起。

```text
domains/order/data-products/order-facts/
├── data-product.yaml
├── schema/
│   └── order-facts.schema.yaml
├── quality/
│   └── rules.yaml
├── lineage/
│   └── lineage.yaml
├── access/
│   └── policy.rego
├── examples/
│   └── sample.json
└── docs/
    ├── README.md
    └── semantics.md
```

`data-product.yaml` 示例：

```yaml
name: order-facts
domain: order
owner: team-order
type: source-aligned-data-product
lifecycle: production
description: 订单交易事实数据产品
schema: schema/order-facts.schema.yaml
semantics:
  grain: one row per order state transition
  primaryTime: order_event_time
quality:
  freshness: 5m
  completeness: ">= 99.9%"
  validityRules:
    - quality/rules.yaml
lineage:
  sources:
    - resource:order-event-log
  outputs:
    - dataset:analytics:revenue-mart
access:
  classification: confidential
  pii: true
  policy: access/policy.rego
consumers:
  - team-finance-analytics
  - team-risk-modeling
  - ai-product:customer-service-agent
aiUsage:
  allowed:
    - rag
    - feature-engineering
    - offline-evaluation
  disallowed:
    - foundation-model-training
featureServing:
  offlineStore: dataset:features:order-facts-offline
  onlineStore: feature:order:latest-order-risk
vectorIndex:
  enabled: false
slo:
  freshnessMinutes: 5
  availability: 99.9
```

### 4.5.7 数据平台与领域团队边界

数据平台团队不拥有所有业务数据，它提供让领域团队发布和消费数据产品的自助能力。

```text
领域团队：拥有数据语义、质量承诺、数据产品生命周期和消费方沟通。
数据平台团队：拥有数据目录、Schema Registry、血缘、质量检测、权限和计算平台。
治理团队：拥有分级分类、PII、指标口径、访问策略和跨域质量规则。
```

### 4.5.8 数据产品到 AI 的联动机制

数据产品网络必须显式服务 AI 原生能力层，而不是只把 AI 当成普通报表消费者。

推荐联动链路：

```text
领域事件 / 领域数据库变更
        │
        ▼
Source-aligned Data Product
        │
        ├── 指标和语义层：面向经营分析和产品运营
        ├── 离线特征：面向模型训练、批量评分和离线评估
        ├── 在线特征：面向实时推理、风控、推荐和个性化
        ├── 向量索引：面向 RAG、语义检索、多模态检索和相似案例
        └── 评估数据集：面向 Prompt、RAG、Agent 和模型回归测试
```

必须明确的架构机制：

1. 特征平台必须同时管理 offline store 和 online store，保证训练与推理使用同一业务定义。
2. 实时推理端点只能读取经过批准的在线特征、领域 API 和授权上下文，不能直接拼接数据库查询。
3. 向量索引必须声明来源数据产品、Embedding 模型、索引版本、权限过滤规则和重建策略。
4. AI 评估集应来自稳定数据产品和真实业务样本脱敏集，不能长期依赖人工临时样例。
5. 数据产品变更必须通知下游 AI 产品，并触发特征、索引和评估集的兼容性检查。
6. 数据产品 owner、AI 产品 owner 和模型 owner 必须共同签署高风险 AI 场景的上线门禁。

### 4.5.9 Lakehouse 到数据产品网络的过渡路径

并不是所有企业都能直接进入完整数据产品网络。对已有数据仓库、数据湖或 Lakehouse 的企业，推荐采用演进式路线：

| 阶段 | 当前形态 | 关键动作 | 禁止误区 |
| ---- | -------- | -------- | -------- |
| L0 | 数据仓库或数据湖分散建设 | 盘点表、任务、指标、owner 和下游消费 | 只迁技术栈，不改责任边界 |
| L1 | 建立 Lakehouse 统一存储和表格式 | 引入分层、Schema、血缘、质量和权限 | 把 Lakehouse 当成新的中央数据团队 |
| L2 | 识别高价值领域数据集 | 让领域团队声明业务语义、口径和质量规则 | 平台团队替领域解释业务含义 |
| L3 | 发布首批 Source-aligned Data Product | 建立数据产品契约、SLO、变更通知和消费样例 | 只发布表名，不发布产品契约 |
| L4 | 建立 Aggregate / Consumer-aligned Data Product | 围绕业务场景组织指标、特征、人群和报表 | 让聚合层反向污染源数据定义 |
| L5 | 形成联邦数据产品网络 | 把质量、权限、血缘、成本和 AI 消费接入自动化治理 | 重新集中审批所有数据变更 |

Lakehouse 的价值在于提供统一存储、开放表格式、批流处理和计算治理；数据产品网络的价值在于明确领域责任、语义契约和消费体验。两者不是替代关系，合理路径是先稳定底座，再逐步把高价值数据集产品化。

---

## 4.6 自助式平台工程层

### 4.6.1 定位

自助式平台工程层为业务团队、领域团队和数据团队提供统一的内部开发平台，降低工程复杂度，提高交付效率和治理一致性。

### 4.6.2 平台核心能力

平台工程层包括：

1. Developer Portal。
2. 服务模板和脚手架。
3. Golden Path。
4. CI/CD 流水线。
5. IaC 基础设施即代码。
6. GitOps 发布机制。
7. Kubernetes 或 Serverless 运行环境。
8. 服务网格。
9. API 管理。
10. 配置管理。
11. 密钥管理。
12. 日志、指标、链路追踪。
13. 告警管理。
14. 环境管理。
15. 成本管理。
16. 安全扫描。
17. 依赖漏洞检测。
18. 权限申请与审批自动化。
19. 发布准入门禁。
20. 研发效能度量。
21. SBOM、provenance、签名和验签能力。
22. AI Platform：模型网关、RAG 平台、评估流水线、Prompt 管理和 Agent 运行时。
23. 认知负载度量和平台用户研究。
24. 容器交付标准：镜像构建、镜像扫描、tag / digest 策略、Helm / Kustomize 模板和 GitOps 发布。

### 4.6.3 平台设计目标

平台团队的目标不是集中接管业务开发，而是让业务团队可以自助完成标准工程动作：

1. 自助创建服务。
2. 自助申请环境。
3. 自助配置数据库、缓存、消息队列。
4. 自助发布应用。
5. 自助接入日志、监控和告警。
6. 自助申请权限。
7. 自助查看成本。
8. 自助执行安全和合规检查。
9. 自助创建 AI 应用、RAG 管道和 Agent 工作流。
10. 自助生成 SBOM、构建 provenance、镜像签名和发布验签。
11. 自助生成标准 Dockerfile、Kubernetes base manifest 和环境级 GitOps overlay。

### 4.6.4 Golden Path

Golden Path 是平台团队为常见场景提供的推荐路径。例如：

1. 创建一个标准微服务。
2. 创建一个前端应用。
3. 创建一个数据产品。
4. 发布一个 API。
5. 接入统一认证。
6. 接入可观测性。
7. 部署到测试环境。
8. 部署到生产环境。
9. 配置弹性伸缩。
10. 配置告警规则。
11. 创建一个受治理的 AI 应用。
12. 创建一个 RAG 索引和评估集。
13. 接入 LLM Gateway、PromptOps 和 AI Observability。
14. 生成 SBOM、签名镜像并通过生产准入。
15. 创建一个容器化微服务并生成 dev / staging / prod GitOps overlay。

Golden Path 应尽量内置最佳实践，使团队默认走在安全、合规、稳定和高效的路径上。

### 4.6.5 平台产品契约

平台能力必须像产品一样运营，而不是只提供工具入口。

```yaml
name: domain-service-golden-path
type: platform-product
owner: team-platform
users:
  - stream-aligned-teams
  - domain-product-teams
solves:
  - create-service
  - register-service
  - configure-ci
  - provision-runtime
  - attach-observability
  - enforce-security-baseline
interfaces:
  portal: platform/portal/create-domain-service
  cli: platformctl service create
  template: platform/golden-paths/domain-service
slo:
  templateSuccessRate: ">= 99%"
  provisioningP95Minutes: 10
metrics:
  adoptionRate: weekly
  timeToFirstDeploy: daily
  failedOnboardingCount: daily
feedback:
  channel: "#platform-feedback"
  reviewCadence: biweekly
```

平台产品的验收标准：

1. 有明确内部用户。
2. 有自助入口或自动化接口。
3. 有文档和 onboarding path。
4. 有 SLO、采用率、反馈渠道和 roadmap。
5. 支持 escape hatch，但必须可审计。

### 4.6.6 容器交付 Golden Path

平台团队应提供容器交付 Golden Path，但不直接托管每个业务服务的部署状态。

容器交付 Golden Path 至少包括：

1. 标准服务脚手架：生成 `src/`、测试、Dockerfile、`service.yaml` 和 catalog descriptor。
2. 标准镜像构建：统一基础镜像、非 root 用户、多阶段构建、最小运行时和可复现构建参数。
3. 标准 CI：测试、lint、镜像构建、SBOM、provenance、漏洞扫描、许可证检查和签名。
4. 标准 Kubernetes base：Deployment、Service、HPA、PodDisruptionBudget、ServiceAccount 和 NetworkPolicy。
5. 标准环境 overlay：dev、staging、prod 使用不同 namespace、replicas、资源配额、ingress 和镜像 digest。
6. 标准 GitOps：通过 Argo CD、Flux 或等价能力同步环境期望状态。
7. 标准回滚：按镜像 digest、Git commit 和 GitOps revision 回滚。
8. 标准可观测性：默认接入日志、指标、trace、SLO、告警和运行面板。

### 4.6.7 平台产品经理与认知负载治理

平台工程必须有明确的平台产品经理或等价职责，负责把平台能力当成内部产品运营，而不是把平台做成工具集合。

Platform PM 负责：

1. 识别平台目标用户、关键旅程和高频痛点。
2. 定义 Golden Path 的成功指标、失败指标和用户反馈机制。
3. 维护平台产品路线图，避免平台团队只按工单堆功能。
4. 定期度量业务团队认知负载，包括 onboarding 难度、配置复杂度、排障复杂度和上下文切换成本。
5. 推动平台能力默认内置安全、可观测、成本、AI 治理和供应链门禁。

认知负载度量建议：

| 指标 | 说明 | 典型采集方式 |
| ---- | ---- | ------------ |
| Time to First Deploy | 新团队第一次成功部署所需时间 | 平台事件和 CI/CD 日志 |
| Self-service Success Rate | 自助流程不依赖人工支持的成功率 | Developer Portal 事件 |
| Support Ticket Rate | 每个 Golden Path 产生的支持工单数 | 工单系统和分类标签 |
| Context Switch Count | 完成标准任务需要切换的系统数量 | 用户访谈和行为埋点 |
| Onboarding Completion Time | 新成员掌握平台基本操作所需时间 | 培训记录和平台行为 |
| Perceived Cognitive Load | 团队主观复杂度评分 | 定期调研和复盘访谈 |

---

## 4.7 基础设施与云原生层

### 4.7.1 定位

基础设施与云原生层为上层业务系统、数据平台和工程平台提供稳定、安全、弹性和可观测的运行底座。

### 4.7.2 主要组成

1. 公有云、私有云或混合云。
2. Kubernetes 集群。
3. Serverless 平台。
4. 网络与负载均衡。
5. 存储服务。
6. 数据库服务。
7. 消息队列。
8. 缓存服务。
9. 搜索引擎。
10. 对象存储。
11. 容器镜像仓库。
12. 服务发现。
13. 灾备与备份。
14. 云安全服务。
15. 成本计量与资源配额。
16. GPU、推理加速和模型服务资源池。
17. 向量数据库、特征在线存储和高性能检索服务。
18. 软件供应链安全基础设施：制品库、签名服务、证明存储和策略准入。

### 4.7.3 基础设施原则

1. 标准化资源模型。
2. 环境隔离。
3. 最小权限。
4. 弹性伸缩。
5. 故障隔离。
6. 多可用区部署。
7. 自动化备份。
8. 可观测、可审计、可追溯。
9. 成本透明。
10. 基础设施即代码。
11. AI 推理资源必须有隔离、配额、成本归集和降级策略。
12. 生产制品必须支持签名验签、SBOM 查询和 provenance 追溯。

### 4.7.4 Kubernetes 与 GitOps 真相源

Kubernetes 管理实际运行状态，GitOps 管理期望部署状态。两者不应和服务源码目录混在一起。

推荐结构：

```text
infra/
├── kubernetes/
│   ├── base/
│   │   └── services/
│   │       └── customer-profile-service/
│   │           ├── deployment.yaml
│   │           ├── service.yaml
│   │           ├── hpa.yaml
│   │           ├── pdb.yaml
│   │           ├── network-policy.yaml
│   │           └── kustomization.yaml
│   └── policies/
└── gitops/
    └── environments/
        ├── dev/customer/customer-profile-service/kustomization.yaml
        ├── staging/customer/customer-profile-service/kustomization.yaml
        └── prod/customer/customer-profile-service/kustomization.yaml
```

环境级 GitOps overlay 负责：

1. 使用哪个镜像 digest。
2. 部署到哪个 namespace。
3. replicas、CPU / memory requests 和 limits。
4. HPA、PDB、Ingress / Gateway 和 ServiceAccount。
5. ConfigMap / Secret 引用。
6. Pod 安全、网络策略、节点选择、亲和性和容忍度。
7. 金丝雀、蓝绿、灰度或批次发布策略。

生产环境禁止只用可变 tag 作为部署依据。tag 可以用于可读性，实际准入、回滚和审计必须能定位到不可变 digest、Git commit 和构建 provenance。

---

## 5. 联邦治理平面

## 5.1 治理定位

联邦治理不是中央团队审批所有事情，而是在企业层面制定少量必要标准，并通过平台能力自动执行。

治理目标是：

1. 保证安全合规。
2. 保证系统稳定性。
3. 保证数据可信。
4. 保证接口一致性。
5. 保证成本可控。
6. 保证架构可演进。
7. 避免重复建设和失控扩张。
8. 保证 AI 应用可评估、可追溯、可审计和可降级。
9. 保证软件供应链产物可证明、可验签和可追责。

## 5.2 治理范围

联邦治理平面贯穿所有架构层，包括：

1. 身份与权限治理。
2. API 标准治理。
3. 事件标准治理。
4. 数据契约治理。
5. 数据安全治理。
6. 个人敏感信息治理。
7. 架构决策治理。
8. SLO 治理。
9. 成本治理。
10. 质量门禁。
11. 发布准入。
12. 合规审计。
13. Policy as Code。
14. 自动化检测。
15. AI 模型、Prompt、RAG、Agent 和工具调用治理。
16. 供应链安全、SBOM、provenance、签名和验签治理。

## 5.3 治理模式

治理采用“全局标准 + 领域自治 + 自动化护栏”的模式。

| 治理对象 | 全局规则              | 领域自治   |
| ---- | ----------------- | ------ |
| API  | 命名、鉴权、版本、错误码、限流   | 具体接口设计 |
| 事件   | Schema、命名、版本、兼容策略 | 具体事件含义 |
| 数据   | 分级、脱敏、血缘、质量规则     | 领域数据定义 |
| 安全   | 身份认证、最小权限、漏洞扫描    | 业务权限模型 |
| AI   | 模型准入、Prompt 版本、评估门禁、工具权限 | 场景设计、业务评估样本 |
| 供应链  | SBOM、provenance、签名验签、依赖锁定 | 组件选型、升级节奏 |
| 成本   | 标签、预算、告警、配额       | 资源使用策略 |
| 稳定性  | SLO、告警、演练、应急流程    | 领域服务承诺 |

## 5.4 自动化治理机制

治理规则应尽量固化到以下环节：

1. 代码提交阶段：静态扫描、依赖漏洞扫描、密钥泄露检测。
2. 构建阶段：镜像扫描、单元测试、质量门禁。
3. 发布阶段：变更审批、灰度发布、准入策略。
4. 运行阶段：SLO 监控、异常检测、成本告警。
5. 数据发布阶段：数据契约校验、质量规则校验、权限检查。
6. API 发布阶段：接口规范校验、文档生成、兼容性检测。
7. 事件发布阶段：Schema 校验、版本兼容性检测。
8. AI 发布阶段：Prompt 版本、评估集、RAG 权限、工具权限、成本预算和人工确认策略校验。
9. 制品发布阶段：SBOM 生成、provenance 生成、镜像签名、验签准入和 SLSA 等级校验。
10. 审计阶段：访问日志、变更日志、权限日志、数据使用日志、AI 调用日志和供应链证明日志。

## 5.5 治理资产目录

联邦治理需要把规则、决策、例外、风险和复盘沉淀为长期资产。

```text
governance/
├── standards/
│   ├── api-standard.md
│   ├── event-standard.md
│   ├── data-product-standard.md
│   ├── security-standard.md
│   ├── reliability-standard.md
│   └── cost-standard.md
├── decisions/
│   └── adr-0001-template.md
├── ownership/
│   ├── teams.yaml
│   ├── raci.yaml
│   └── escalation-policy.md
├── slo/
│   ├── tiering-policy.md
│   └── error-budget-policy.md
├── security/
│   ├── threat-model-template.md
│   └── data-classification.md
├── supply-chain/
│   ├── slsa-policy.md
│   ├── sbom-policy.md
│   └── signing-and-verification.md
├── ai-governance/
│   ├── ai-product-review.md
│   ├── fine-tuning-review.md
│   ├── model-risk-policy.md
│   ├── prompt-release-gate.md
│   └── agent-tool-policy.md
├── data-governance/
│   ├── data-product-review.md
│   ├── pii-policy.md
│   └── retention-policy.md
├── architecture-gates/
│   ├── production-readiness.yaml
│   ├── domain-readiness.yaml
│   └── data-product-readiness.yaml
├── migration/
│   ├── strangler-migration-policy.md
│   ├── deprecation-policy.md
│   └── compatibility-policy.md
├── evidence/
│   ├── releases/
│   ├── supply-chain/
│   ├── exceptions/
│   ├── compatibility/
│   ├── drift/
│   ├── audit-evidence-index.md
│   └── drill-evidence-template.md
├── risk-register/
├── postmortems/
└── playbooks/
    └── ai-incident-playbook.md
```

## 5.6 治理例外机制

例外不是口头豁免，必须有 owner、原因、风险、缓解措施和到期时间。

```yaml
exceptionId: EX-2026-001
owner: team-order
violatedRule: data-product-freshness-standard
reason: upstream provider does not support near-real-time delivery
risk: finance report may lag up to 60 minutes
expiry: 2026-09-01
mitigation:
  - show freshness timestamp in consumer dashboard
  - alert when freshness exceeds 60 minutes
reviewer: architecture-group
```

## 5.7 AI 治理门禁

AI 治理必须把模型、Prompt、检索、工具、数据和人工确认作为一个整体审查。

AI 产品进入生产前必须满足：

1. 明确风险等级、owner、业务目标、用户范围和退出机制。
2. 模型、Prompt、RAG 配置、工具版本和评估集可追溯。
3. 高风险工具调用声明权限、幂等、超时、审计、回滚和人工确认策略。
4. RAG 数据源完成分级分类、授权、引用追溯和撤销机制。
5. 离线评测和在线灰度指标达到门槛。
6. 成本预算、限流、降级和人工接管策略已配置。
7. 运行日志覆盖输入、输出、上下文、工具调用、策略结果和用户反馈。

AI 治理不应阻止团队使用模型，而应把模型使用变成可验证的工程过程。

### 5.7.1 AI 风险分级控制基线

AI 产品必须先分级，再决定评估、审批、审计和人工确认强度。风险分级不是为了阻止创新，而是为了避免把内部问答、客服辅助、自动退款、信贷审批和医疗建议放在同一套门禁里。

| 风险等级 | 典型场景 | 最低控制要求 |
| -------- | -------- | ------------ |
| R1 低风险 | 内部知识检索、文档摘要、研发辅助 | Prompt 版本、基础评估集、成本限额、日志审计 |
| R2 中风险 | 客服辅助、运营建议、销售线索整理 | RAG 权限过滤、引用追溯、人工抽检、灰度发布 |
| R3 高风险 | 自动退款、账户处置、风控建议、合同审查 | 人工确认、红队测试、回放审计、模型/Prompt/RAG 回归门禁 |
| R4 严格受控 | 信贷审批、医疗建议、招聘筛选、合规判定 | 法务/合规评审、影响评估、强人工复核、独立审计和退出机制 |
| R5 禁止或暂缓 | 无法解释的关键自动决策、无授权敏感数据训练 | 不得进入生产，除非完成专门风险接受和监管评估 |

风险等级必须写入 `ai-product.yaml`，并驱动 CI/CD、Developer Portal、LLM Gateway、Agent Runtime 和审计系统的默认策略。

### 5.7.2 AI 资产证据链

AI 资产必须具备证据链，否则无法做回归、复盘和合规审计。

每个生产 AI 产品至少保留：

1. 模型证据：模型名称、版本、供应商、批准状态、适用场景、限制和替代模型。
2. Prompt 证据：模板版本、变更记录、评估结果、灰度记录和回滚点。
3. 数据证据：RAG 来源、数据产品、特征产品、评估数据集、脱敏策略和授权范围。
4. 工具证据：工具 Schema、权限、幂等、超时、重试、人工确认和审计字段。
5. 运行证据：请求元数据、检索片段、模型输出、工具调用、策略判断、人工确认和用户反馈。
6. 风险证据：风险等级、威胁模型、红队结果、已知限制和风险接受记录。

建议维护 `ai-evidence.yaml`：

```yaml
aiProduct: customer-service-agent
riskTier: R3
model:
  gatewayRoute: support-safe-default
  approvedModels:
    - model: vendor:model-name
      version: "2026-05"
      approval: approved-for-support-assist
prompts:
  systemPrompt: prompts/system.prompt.md
  version: "2026.06.01"
rag:
  sources: rag/sources.yaml
  vectorIndex: vector:customer-support-policy:v12
  embeddingModel: embedding:model:v3
evals:
  regression: evals/regression.yaml
  redTeam: evals/adversarial.yaml
tools:
  registry: tools/tool-permissions.yaml
audit:
  traceRetentionDays: 180
  replayEnabled: true
governance:
  approval: governance/ai-governance/reviews/customer-service-agent.md
  expiry: 2026-12-01
```

### 5.7.3 微调治理门禁

微调模型不能继承基础模型的风险结论。任何微调都会改变模型行为边界，因此必须形成独立审查记录。

微调进入生产前必须满足：

1. 数据授权：训练数据允许用于指定微调目的，且禁止用途写入契约。
2. 数据治理：完成脱敏、去重、版权、PII、敏感字段和保留期限检查。
3. 实验追踪：每次训练可追溯到基础模型、数据版本、代码版本、超参数、环境和成本。
4. 独立评估：评估集不得与训练集混用，必须覆盖质量、安全、幻觉、偏见、越权和泄露。
5. 模型登记：微调模型必须有 Model Card、版本、owner、风险等级、适用场景和回滚模型。
6. 发布准入：高风险微调模型必须先 shadow 或灰度，再逐步放量。
7. 授权撤销：当数据授权撤销或发现污染数据时，必须能定位受影响模型并触发禁用或重训。

## 5.8 供应链安全门禁

供应链安全必须覆盖源码、依赖、构建、测试、制品、签名、部署和运行准入。

生产发布最低要求：

1. 依赖必须锁定版本，并进入漏洞扫描和许可证检查。
2. 每个发布制品必须生成 SBOM，至少覆盖直接依赖、传递依赖、版本、供应商和许可证信息。
3. 构建系统必须生成 provenance，记录源码、构建器、构建参数、依赖和制品摘要。
4. 容器镜像、部署包和关键二进制必须签名。
5. 生产准入必须执行验签、SBOM 策略、漏洞阈值和来源策略。
6. 高风险系统应逐步达到 SLSA Build Level 2，核心系统应规划达到 SLSA Build Level 3。
7. 供应链例外必须有 owner、到期时间、补救计划和风险接受记录。

## 5.9 Policy as Code 策略语言

联邦治理必须统一策略语言和执行入口，避免每个团队各写一套不可复用的策略。

推荐策略：

| 策略范围 | 推荐引擎 | 说明 |
| -------- | -------- | ---- |
| 跨平台治理、CI 门禁、数据访问、发布准入 | OPA / Rego | 适合通用 Policy as Code、单元测试和准入校验 |
| Kubernetes 资源策略 | OPA Gatekeeper 或 Kyverno | 适合集群准入、镜像验签、命名空间和资源限制 |
| 应用内细粒度授权 | Cedar 或等价授权策略语言 | 适合把应用权限模型从业务代码中剥离 |
| 云厂商原生权限 | IAM Policy | 只用于云资源权限，不替代企业级治理策略 |

原则：

1. 企业级默认策略语言必须少而稳定，不能让 Rego、Cedar、YAML 条件和自研 DSL 无边界混用。
2. 所有策略必须有 owner、测试用例、示例输入、示例输出、版本和回滚路径。
3. 生产策略变更必须进入 CI，至少执行语法检查、单元测试、关键路径用例和冲突检测。
4. 策略例外必须可审计，并有到期时间。
5. 如果采用多策略引擎，必须明确边界：谁负责准入、谁负责授权、谁负责数据访问、谁负责云资源。

---

## 6. 安全架构

## 6.1 安全目标

安全架构的目标是建立覆盖身份、网络、应用、数据、供应链和运行环境的纵深防御体系。

## 6.2 身份与访问控制

1. 统一身份认证。
2. 单点登录。
3. 多因素认证。
4. 最小权限原则。
5. 基于角色的访问控制。
6. 基于属性的访问控制。
7. 服务到服务认证。
8. 临时凭证和密钥轮换。
9. 权限申请、审批和审计。

## 6.3 应用安全

1. 安全编码规范。
2. 依赖漏洞扫描。
3. 镜像漏洞扫描。
4. API 鉴权。
5. 输入校验。
6. 敏感信息保护。
7. 防重放、防篡改、防越权。
8. Web 应用防护。
9. 灰度发布和快速回滚。
10. 安全测试自动化。

### 6.3.1 安全开发证据

安全开发不应只在上线前扫描一次，而应贯穿需求、设计、编码、构建、测试、发布和响应。

每个 Tier-1 服务至少保留：

1. 安全需求和威胁建模记录。
2. 安全设计评审记录。
3. 代码评审和静态分析结果。
4. 依赖、许可证、密钥和镜像扫描结果。
5. 安全测试、模糊测试或关键路径滥用用例。
6. 漏洞处置 SLA、例外审批和补救计划。
7. 生产事件响应和安全复盘记录。

平台应把这些证据自动挂接到 catalog 和发布准入，而不是让团队在审计时临时补材料。

## 6.4 数据安全

1. 数据分级分类。
2. 敏感数据识别。
3. 数据脱敏。
4. 数据加密。
5. 数据访问授权。
6. 数据使用审计。
7. 数据出境或外发控制。
8. 数据生命周期管理。
9. 备份与恢复。
10. 隐私合规。

## 6.5 云原生安全

1. 集群访问控制。
2. 命名空间隔离。
3. 网络策略。
4. 镜像签名。
5. 运行时安全。
6. Secret 管理。
7. Pod 安全策略。
8. 供应链安全。
9. 基础设施变更审计。
10. 异常行为检测。

## 6.6 供应链安全

供应链安全是生产发布的基线能力，不是可选增强项。

必须建立以下控制：

1. SLSA 分级目标：普通业务系统至少满足可审计构建和 provenance；核心系统逐步达到隔离构建、不可篡改日志和强身份构建器。
2. SBOM：每个生产制品生成 SPDX 或 CycloneDX 等标准格式 SBOM，并进入制品库和审计系统。
3. 镜像签名与验签：构建完成后签名，部署前由准入控制器验签。
4. Provenance：记录源码仓库、commit、构建器、构建参数、依赖摘要和产物摘要。
5. 依赖锁定：生产构建必须使用锁文件、固定版本或可复现依赖解析。
6. 漏洞策略：按 CVSS、可利用性、暴露面和业务等级设置阻断阈值。
7. 许可证策略：禁止未经批准的强传染许可证或未知许可证进入生产制品。
8. 制品不可变：生产制品一旦签名，不允许覆盖发布。
9. 准入控制：部署前校验签名、SBOM、provenance、漏洞阈值、基础镜像和策略标签。
10. 例外闭环：所有安全例外必须有到期时间和补救计划。

## 6.7 AI 安全

AI 安全覆盖模型输入、上下文、工具调用、输出、记忆、向量索引和供应商接入。

必须建立以下控制：

1. Prompt 注入防护：对用户输入、检索片段和工具返回内容进行来源标记和指令隔离。
2. 越权访问防护：RAG 检索、工具调用和领域 API 调用必须继承用户和服务权限。
3. 数据泄露防护：输入输出执行 PII、密钥、内部策略和敏感数据检测。
4. 工具滥用防护：高风险工具必须声明危险等级、幂等性、人工确认和审计。
5. 过度代理防护：Agent 计划、循环、重试、并发和成本必须有上限。
6. 模型供应商隔离：密钥、租户、日志保留和数据使用策略必须可控。
7. 评估与红队：核心 AI 产品必须有越权、幻觉、提示注入、错误引用和成本消耗测试。
8. 输出责任：关键业务输出必须可解释、可引用或可回放，不能只保留最终文本。

---

## 7. 可观测性与运行治理

## 7.1 可观测性目标

平台应具备统一的日志、指标、链路追踪、事件和告警能力，支持业务团队快速发现问题、定位问题和恢复服务。

## 7.2 可观测性内容

1. 应用日志。
2. 业务日志。
3. 系统指标。
4. 业务指标。
5. 链路追踪。
6. API 调用指标。
7. 数据质量指标。
8. 队列积压指标。
9. 数据库性能指标。
10. 用户体验指标。
11. 成本指标。
12. 安全事件指标。
13. AI 调用指标：Token、延迟、模型错误、工具调用、引用命中、幻觉反馈和成本。
14. 供应链指标：SBOM 覆盖率、签名覆盖率、验签失败率、漏洞阻断和 provenance 覆盖率。

## 7.3 SLO 体系

每个关键领域产品都应定义 SLO。常见指标包括：

| 指标    | 说明           |
| ----- | ------------ |
| 可用性   | 服务可正常提供能力的比例 |
| 延迟    | 请求响应时间       |
| 错误率   | 失败请求占比       |
| 吞吐量   | 单位时间处理能力     |
| 数据新鲜度 | 数据更新是否及时     |
| 数据准确性 | 数据是否符合质量规则   |
| 恢复时间  | 故障后恢复所需时间    |
| 变更失败率 | 发布引发故障的比例    |
| AI 任务完成率 | AI 产品完成目标任务的比例 |
| AI grounded rate | AI 输出能被引用或事实来源支撑的比例 |
| 供应链证明覆盖率 | 生产制品具备 SBOM、签名和 provenance 的比例 |

## 7.4 事件响应机制

应建立标准事件响应流程：

1. 异常发现。
2. 告警触发。
3. 影响范围判断。
4. 负责人确认。
5. 应急处理。
6. 临时恢复。
7. 根因分析。
8. 复盘改进。
9. 规则和平台能力修正。
10. 知识库沉淀。

## 7.5 AI 可观测性

AI 产品必须同时观测工程质量、业务质量和模型质量。

关键指标包括：

1. 请求量、Token 量、模型延迟和错误率。
2. 模型路由、重试、降级和拒绝率。
3. Prompt 版本、模型版本、检索配置和工具版本。
4. RAG 召回率、重排命中率、引用覆盖率和无引用输出比例。
5. Agent 工具调用成功率、人工确认率、循环中断率和超时率。
6. 用户反馈、人工抽检质量、幻觉反馈和任务完成率。
7. 单次任务成本、团队预算消耗、异常成本峰值和语义缓存命中率。

AI 可观测性必须支持回放，至少能还原输入元数据、检索片段、Prompt 版本、模型版本、工具调用、策略判断和最终输出。

## 7.6 AI 事件响应机制

AI 产品必须有独立事件响应 playbook。通用事件响应流程可以处理服务宕机和延迟，但不足以处理幻觉爆发、工具失控、模型供应商中断、RAG 索引污染和微调模型回退。

典型 AI 事件类型：

| 事件类型 | 典型表现 | 首要动作 |
| -------- | -------- | -------- |
| 幻觉率突然升高 | grounded rate 下降、用户负反馈升高 | 降级到上一版 Prompt / 模型 / 检索配置 |
| Prompt 注入成功 | 模型泄露策略、忽略系统指令或越权回答 | 阻断输入模式，回滚 Prompt，增加隔离和过滤 |
| 工具调用失控 | Agent 循环调用、重复退款、重复建单 | 关闭高风险工具，启用人工确认和速率限制 |
| RAG 索引污染 | 检索到过期、恶意或无权限片段 | 冻结索引，回滚向量索引版本，重建来源数据 |
| 模型供应商中断 | 延迟升高、错误率升高、质量异常 | 切换模型路由，缩小上下文，降级到人工流程 |
| 微调模型回退 | 特定任务质量下降或安全评估失败 | 下线微调模型，回退基础模型或上一个微调版本 |
| 成本失控 | Token、GPU、向量检索或工具调用异常增加 | 限流、降低模型等级、启用预算熔断 |
| 敏感信息泄露 | 输出 PII、密钥、内部策略或无权数据 | 关闭相关数据源，启动安全事件流程和审计 |

AI 事件响应步骤：

1. 分类：判断是模型、Prompt、RAG、工具、数据、供应商、成本还是权限事件。
2. 止血：切换模型路由、回滚 Prompt、冻结工具、关闭索引、限流或进入人工接管。
3. 取证：保留 trace、Prompt 版本、模型版本、检索片段、工具调用、策略日志和用户反馈。
4. 影响评估：识别受影响用户、业务动作、数据产品、工具、模型版本和时间窗口。
5. 修复：修正 Prompt、检索配置、工具权限、策略规则、索引来源或模型版本。
6. 回归：运行 AI 回归评估、红队用例、权限用例和成本用例。
7. 复盘：更新评估集、Guardrails、SLO、runbook、风险登记和治理门禁。

`governance/playbooks/ai-incident-playbook.md` 应至少包含：

1. 事件分级。
2. 负责人和升级路径。
3. 各类事件的止血动作。
4. 取证字段清单。
5. 回滚和降级矩阵。
6. 用户和监管沟通模板。
7. 复盘模板和门禁修正项。

## 7.7 可靠性分级与恢复目标

可靠性不能只写“高可用”。每个生产服务、数据产品、AI 产品和关键平台能力都必须声明可靠性等级，并把等级映射到 SLO、RTO、RPO、错误预算、on-call、发布策略和灾备演练。

默认分级：

| 等级 | 适用对象 | 可用性目标 | RTO | RPO | 值守要求 | 灾备演练 |
| ---- | -------- | ---------- | --- | --- | -------- | -------- |
| `Tier-1` | 收入、支付、履约、账户、安全、合规和关键客户路径 | 99.9% - 99.99% | <= 1 小时 | <= 15 分钟 | 7x24 on-call，明确升级路径 | 每季度至少一次 |
| `Tier-2` | 重要运营、内部核心流程、关键数据产品和中风险 AI 产品 | 99.5% - 99.9% | <= 4 小时 | <= 4 小时 | 工作时间值守，关键告警可升级 | 每半年至少一次 |
| `Tier-3` | 内部辅助工具、低风险后台、实验性能力和非关键报表 | 99.0% 或 best effort | <= 1 个工作日 | <= 24 小时 | 工作时间响应 | 每年至少一次桌面演练 |

分级规则：

1. 等级必须写入 `domain.yaml`、`service.yaml`、`data-product.yaml`、`ai-product.yaml` 或 catalog entry。
2. 服务不能声明高于关键下游依赖的可靠性等级，除非具备缓存、降级、异步补偿或替代路径。
3. `Tier-1` 必须具备 runbook、rollback、告警、容量水位、依赖降级、备份恢复和事故复盘。
4. 数据产品的 RPO 对应数据丢失窗口，freshness 对应数据新鲜度，二者不能混用。
5. AI 产品的 RTO 必须包含模型供应商切换、Prompt 回滚、RAG 索引回滚、工具冻结和人工接管时间。
6. RTO/RPO 必须通过演练、恢复测试或事故复盘验证，不能只写在文档里。

错误预算基线：

| 状态 | 触发条件 | 必须动作 |
| ---- | -------- | -------- |
| 正常 | 错误预算消耗低于 50% | 按正常发布节奏推进 |
| 关注 | 错误预算消耗达到 50% - 75% | 复查变更频率、告警噪声、依赖稳定性和容量水位 |
| 限制 | 错误预算消耗达到 75% - 100% | 暂停非关键发布，优先可靠性修复和降级演练 |
| 冻结 | 错误预算耗尽或连续重大事故 | 冻结功能发布，必须完成复盘、修复和治理门禁更新 |

`governance/slo/tiering-policy.md` 应至少包含：

1. Tier 定义和适用对象。
2. 可用性、延迟、错误率、RTO、RPO 和数据 freshness 目标。
3. on-call、升级路径和业务 owner。
4. 发布冻结条件和错误预算策略。
5. 备份、恢复、灾备演练和证据保存要求。
6. 例外审批和到期复审机制。

---

## 8. 组织与团队模型

## 8.1 团队类型

现代数字化平台建议采用以下团队结构：

| 团队类型                       | 职责                         |
| -------------------------- | -------------------------- |
| Stream-aligned Team        | 面向业务流，端到端交付客户价值            |
| Domain Product Team        | 负责领域能力产品、领域模型、API、事件和数据产品  |
| Platform Team              | 建设内部开发平台，降低业务团队复杂度         |
| Data Platform Team         | 提供数据平台、数据目录、质量检测、语义层和特征平台  |
| AI Product Team            | 负责 AI 产品、Agent、RAG、评估集和模型接入治理   |
| Enabling Team              | 短期赋能其他团队，提升云原生、数据、AI、安全等能力 |
| Complicated Subsystem Team | 负责高复杂专业系统，如搜索、推荐、风控模型、交易撮合 |
| Governance Team            | 制定全局规则，并推动治理自动化            |
| Security Team              | 负责安全策略、审计、风险管理和安全平台能力      |

## 8.2 责任划分

### 8.2.1 前台业务团队

负责：

1. 用户体验。
2. 业务流程。
3. 业务指标。
4. 渠道运营。
5. 需求优先级。
6. 客户反馈闭环。

### 8.2.2 领域团队

负责：

1. 领域能力规划。
2. 领域模型设计。
3. API 和事件发布。
4. 数据产品发布。
5. 服务稳定性。
6. 领域业务指标。
7. 领域架构演进。

### 8.2.3 平台团队

负责：

1. 内部开发平台。
2. Golden Path。
3. CI/CD。
4. 环境与资源管理。
5. 可观测性平台。
6. 平台安全能力。
7. 成本可视化。
8. 工程效率提升。
9. 供应链安全能力。
10. AI 平台能力。
11. 平台用户研究和认知负载降低。

### 8.2.4 数据团队

负责：

1. 数据平台能力。
2. 数据目录。
3. 数据质量框架。
4. 指标体系。
5. 语义层。
6. 特征平台。
7. 数据治理工具。
8. 数据消费体验。

### 8.2.5 AI 产品团队

负责：

1. AI 产品目标、用户和风险等级定义。
2. Agent 工作流、工具权限和人工确认策略。
3. Prompt 版本、评估集和发布回归。
4. RAG 数据源、索引、引用和权限过滤。
5. 模型接入、模型路由和质量评估。
6. AI 可观测性、成本和反馈闭环。
7. 与领域团队、数据团队和安全团队共同完成高风险 AI 场景上线门禁。

### 8.2.6 Platform PM

负责：

1. 定义平台产品战略、路线图和内部用户画像。
2. 管理 Golden Path 的采用率、成功率、满意度和失败原因。
3. 组织平台用户访谈、开发者体验调研和认知负载评估。
4. 协调平台工程、安全、数据、AI 和治理需求的优先级。
5. 防止平台团队退化为工单承接团队。

### 8.2.7 治理团队

负责：

1. 架构原则。
2. 标准制定。
3. 治理机制。
4. 合规要求。
5. 规则自动化。
6. 架构评审机制。
7. 治理效果度量。

## 8.3 RACI 决策权矩阵

RACI 用于明确“谁负责做、谁最终负责、谁必须参与、谁只需知会”。没有 RACI 的企业架构会退化成会议驱动：所有人都能提意见，但没人对结果负责。

定义：

1. `R` Responsible：直接执行和产出交付物的团队。
2. `A` Accountable：对最终结果负责并拥有批准权的角色，原则上每项决策只有一个最终 accountable owner。
3. `C` Consulted：必须咨询并纳入反馈的团队。
4. `I` Informed：需要被通知但不阻塞决策的团队。

企业级默认 RACI：

| 决策事项 | A | R | C | I | 必要证据 |
| -------- | - | - | - | - | -------- |
| 企业架构基线版本发布 | 架构组负责人 | 治理团队 | 平台、数据、安全、AI、领域代表 | 管理层、所有执行团队 | 版本记录、评审记录、门禁结果 |
| 新增或拆分核心领域 | 架构组负责人 | 领域团队 | 业务 owner、数据团队、平台团队、安全团队 | 受影响团队 | ADR、领域模型、依赖影响分析 |
| 新建生产服务 | 领域团队负责人 | 领域团队 | 平台团队、安全团队、SRE | 治理团队、相关消费者 | `service.yaml`、catalog entry、生产就绪门禁 |
| API breaking change | API owner | 领域团队 | 消费方、平台团队、治理团队 | 所有订阅方 | 兼容性报告、迁移计划、弃用日期 |
| 事件 Schema breaking change | 事件 owner | 领域团队 | 消费方、数据团队、平台团队 | 治理团队 | 消费者影响分析、Schema 迁移计划 |
| 数据产品发布 | 数据产品 owner | 领域团队 | 数据平台团队、安全团队、下游消费者 | 治理团队 | 数据契约、质量报告、权限策略 |
| 高风险 AI 产品上线 | 业务 owner | AI 产品团队 | 安全、法务/合规、数据团队、领域团队 | 平台团队、治理团队 | 风险分级、评估报告、回放证据、人工确认策略 |
| 平台 Golden Path 变更 | Platform PM | 平台团队 | 领域团队、安全团队、SRE、AI 团队 | 所有平台用户 | 迁移说明、用户影响、回滚路径 |
| 供应链安全准入策略变更 | 安全负责人 | 安全团队 | 平台团队、治理团队、领域代表 | 所有服务 owner | 策略测试、例外清单、阻断阈值 |
| GitOps 生产环境策略变更 | SRE / 环境 owner | 平台团队或 SRE | 安全团队、领域团队、治理团队 | 受影响服务 owner | GitOps diff、回滚计划、准入结果 |
| SLO 等级或 RTO/RPO 调整 | 业务 owner | 领域团队或平台 owner | SRE、治理团队、数据/AI owner | 管理层和消费者 | tiering policy、风险接受、演练证据 |
| 治理例外审批 | 治理负责人 | 申请团队 | 安全、平台、数据、AI 或 SRE | 受影响团队 | 例外原因、风险、缓解措施、到期时间 |

执行规则：

1. 每个生产系统、数据产品、AI 产品和平台能力必须有一个 accountable owner。
2. `A` 可以授权执行，但不能把最终责任转移给平台团队、治理团队或供应商。
3. 高风险 AI、安全、合规和供应链变更可以有多个必需审批门禁，但仍必须指定单一业务或技术 accountable owner。
4. RACI 变更本身必须进入架构决策记录或治理变更记录。
5. `governance/ownership/raci.yaml` 是机器可读 RACI 真相源，文档表格只作为说明。

---

## 9. 关键业务流程示例

## 9.1 新服务创建流程

1. 团队在 Developer Portal 选择服务模板。
2. 平台自动创建代码仓库。
3. 平台自动生成基础代码、CI/CD 流水线和部署配置。
4. 团队填写服务元数据、负责人和所属领域。
5. 平台自动接入日志、指标、链路追踪和告警。
6. 平台自动执行安全扫描和依赖检查。
7. 服务部署到测试环境。
8. 通过发布准入后进入生产环境。
9. 服务在服务目录中可见。
10. 后续运行质量纳入 SLO 监控。

## 9.2 新 API 发布流程

1. 领域团队设计 API。
2. API 文档和契约提交到 API 管理平台。
3. 平台自动检查命名、鉴权、版本和错误码规范。
4. 安全策略自动生效。
5. API 发布到网关。
6. 消费方通过门户申请使用。
7. 调用情况、错误率和延迟自动监控。
8. 版本变更自动通知下游消费者。

## 9.3 新数据产品发布流程

1. 领域团队定义数据产品。
2. 填写业务口径、字段含义、数据负责人和更新频率。
3. 配置数据质量规则。
4. 配置数据分级、脱敏和访问权限。
5. 平台自动检测血缘和质量。
6. 数据产品进入数据目录。
7. 消费方申请访问。
8. 数据使用行为被记录和审计。
9. 数据质量和使用情况持续监控。

## 9.4 跨领域业务流程

以“用户下单”为例：

1. 前台体验层提交下单请求。
2. 体验编排层完成渠道校验和上下文组装。
3. 订单域创建订单。
4. 商品域校验商品状态。
5. 库存域锁定库存。
6. 支付域发起支付。
7. 风控域进行交易风险评估。
8. 履约域接收订单履约事件。
9. 营销域核销优惠权益。
10. 数据产品网络沉淀订单、支付、履约和营销数据。
11. 经营分析、推荐模型和风控模型消费相关数据产品。

## 9.5 新 AI 产品发布流程

1. AI 产品团队定义业务目标、用户范围、风险等级和退出机制。
2. 领域团队确认可调用 API、事件、工具和业务动作边界。
3. 数据团队确认可消费数据产品、特征、向量索引和评估样本。
4. AI 团队提交 Prompt、Agent 工作流、RAG 配置、工具权限和评估集。
5. 平台自动执行 Prompt 回归、RAG 权限校验、工具权限校验和成本预算校验。
6. 安全团队执行提示注入、越权、数据泄露和高风险动作测试。
7. 产品进入灰度，持续观察任务完成率、grounded rate、人工确认率、用户反馈和成本。
8. 达到门禁后进入生产；不达标时回滚到上一个 Prompt、模型、检索或人工流程。
9. 所有模型调用、工具调用、评估结果和人工确认记录进入审计。

## 9.6 新微调模型发布流程

1. AI 产品团队提交微调必要性说明，证明 Prompt、RAG、工具和模型路由不足以满足目标。
2. 数据 owner 确认训练数据授权、分级、脱敏、保留期限和禁止用途。
3. AI 团队登记实验，记录基础模型、数据版本、代码版本、训练配置和成本。
4. 平台执行数据质量、PII、版权、泄露和训练/评估集隔离检查。
5. 模型通过独立评估集、安全用例、红队用例和业务验收。
6. 模型进入 Model Registry，生成 Model Card、风险等级、适用范围和回滚模型。
7. 模型进入 shadow 或灰度发布，观察质量、安全、成本和用户反馈。
8. 达到门禁后进入生产；不达标时回滚基础模型或上一版微调模型。
9. 微调数据授权撤销、数据污染或模型退化时，触发禁用、重训或退役流程。

## 9.7 供应链安全发布流程

1. 开发者提交代码并触发 CI。
2. CI 执行测试、静态扫描、依赖扫描、许可证检查和密钥扫描。
3. 构建系统使用受控构建器生成制品。
4. 构建系统生成 SBOM 和 provenance。
5. 制品进入镜像仓库或制品库后完成签名。
6. 发布前准入控制器执行验签、SBOM 策略、漏洞阈值和来源策略。
7. GitOps 或发布系统只部署通过准入的不可变制品。
8. 运行期持续监控新漏洞、异常行为和供应链策略漂移。

---

## 10. 技术标准

## 10.1 API 标准

1. API 必须有明确业务语义。
2. API 必须有版本管理。
3. API 必须有统一认证和授权。
4. API 必须有错误码规范。
5. API 必须有超时、限流和熔断策略。
6. API 必须有文档和示例。
7. API 变更必须评估兼容性。
8. 废弃 API 必须提前通知消费者。

## 10.2 事件标准

1. 事件命名必须体现领域和业务含义。
2. 事件必须有 Schema。
3. 事件必须有版本。
4. 事件必须有生产者和消费者记录。
5. 事件必须支持幂等处理。
6. 事件变更必须兼容已有消费者。
7. 关键事件必须纳入监控和审计。

## 10.3 数据标准

1. 核心数据必须有业务定义。
2. 核心指标必须有统一口径。
3. 数据产品必须有负责人。
4. 数据产品必须有质量规则。
5. 敏感字段必须标注。
6. 数据访问必须授权。
7. 数据使用必须可审计。
8. 重要数据变更必须通知下游。

### 10.3.1 数据契约最低字段

数据产品必须具备机器可读数据契约，不能只依赖表说明。

最低字段包括：

1. owner、domain、consumer、lifecycle。
2. schema、字段类型、nullable、枚举、主键和时间字段。
3. semantic grain、指标口径、业务定义和限制。
4. freshness、completeness、validity、uniqueness 和 accuracy 规则。
5. classification、PII、retention、access policy 和审计要求。
6. lineage、upstream、downstream 和 breaking change 通知策略。
7. AI usage policy：是否允许训练、Embedding、RAG、特征、评估和在线推理。
8. cost owner、SLO 和消费示例。

数据契约必须进入 CI，至少校验 schema 兼容、质量规则、权限策略和下游影响。

## 10.4 工程标准

1. 代码必须通过质量扫描。
2. 依赖必须通过漏洞检查。
3. 镜像必须通过安全扫描。
4. 发布必须经过自动化流水线。
5. 配置和密钥必须分离。
6. 生产变更必须可追踪。
7. 关键系统必须支持灰度发布和回滚。
8. 服务必须接入可观测性平台。

## 10.5 机器可读契约目录

所有跨团队、跨系统、跨领域的接口都应进入 `contracts/`，避免只靠口头约定、文档段落或代码注释协作。

```text
contracts/
├── apis/
│   ├── public/
│   ├── internal/
│   └── partner/
├── events/
│   ├── topics/
│   └── schemas/
├── schemas/
│   ├── json/
│   ├── proto/
│   └── avro/
├── datasets/
│   ├── products/
│   ├── quality-rules/
│   └── semantic-layer/
├── ai/
│   ├── tools/
│   ├── prompts/
│   ├── rag/
│   ├── evals/
│   ├── fine-tuning/
│   └── guardrails/
├── resources/
│   ├── terraform-modules/
│   ├── kubernetes-crds/
│   └── cloud-resources/
└── policies/
    ├── iam/
    ├── opa/
    └── data-access/
```

契约变更规则：

1. API breaking change 必须先完成消费者影响分析。
2. 事件 Schema 默认只允许向后兼容演进。
3. 数据产品 Schema 必须校验字段语义、类型、分级和质量规则。
4. AI 工具契约必须校验权限、Schema、幂等、超时、审计和人工确认策略。
5. 微调契约必须校验训练数据授权、实验追踪、评估集隔离、模型登记和回滚路径。
6. Policy 必须声明策略引擎、策略范围和测试用例，并通过语法、单元测试和关键路径场景测试。
7. 契约变更必须进入 CI，不能只停留在文档。

## 10.6 软件和数据资产目录

`catalog/` 让系统、服务、API、资源、数据产品、owner 和生命周期可发现。

```text
catalog/
├── systems/
├── components/
├── resources/
├── apis/
├── data-products/
├── ai-products/
├── models/
├── agents/
├── domains/
└── scorecards/
```

组件登记示例：

```yaml
name: order-command-service
kind: component
type: service
domain: order
system: order-system
owner: team-order
lifecycle: production
tier: tier-1
providesApis:
  - domain:order:orders-internal-api
publishesEvents:
  - domain:order:order-created
dependsOn:
  - resource:order-primary-db
  - api:customer-internal-api
  - topic:payment-authorized
runtime:
  platform: kubernetes
  namespace: order-prod
  deployment: order-command-service
  imageRepository: registry.company.com/order/order-command-service
  gitopsPath: infra/gitops/environments/prod/order/order-command-service
scorecards:
  productionReadiness: pass
  security: pass
  reliability: warn
```

核心规则：

1. 没有 catalog entry 的生产组件不能发布。
2. 没有 owner 的系统不能进入生产。
3. 没有 lifecycle 的资产不能被消费者依赖。
4. 资源必须可追溯到 owner、系统、环境和成本中心。
5. catalog 只能指向运行对象和 GitOps 路径，不能成为部署真相源。

## 10.7 AI 标准

1. AI 产品必须有 `ai-product.yaml`、owner、风险等级、SLO 和 runbook。
2. Prompt、模型、工具、RAG 和评估集必须版本化。
3. Agent 工具调用必须声明权限、Schema、幂等、超时、重试、审计和人工确认策略。
4. RAG 索引必须声明来源、授权、Embedding 模型、索引版本和重建策略。
5. 高风险 AI 输出必须支持引用、回放、人工确认或人工接管。
6. AI 发布必须通过离线评估、在线灰度、成本预算和安全门禁。
7. AI 调用必须接入统一可观测性和审计。
8. 模型供应商、日志保留、数据使用和跨境传输策略必须明确。

## 10.8 供应链安全标准

1. 生产构建必须可追溯到源码 commit、构建器、依赖和制品摘要。
2. 生产制品必须生成 SBOM。
3. 生产制品必须签名，部署前必须验签。
4. 依赖必须锁定版本，升级必须经过漏洞和许可证检查。
5. 基础镜像必须来自批准来源，并定期更新。
6. 高风险漏洞不得通过生产准入；例外必须有 owner、到期时间和补救计划。
7. 关键系统必须逐步达到更高 SLSA 构建等级。
8. 供应链证据必须可被审计系统查询和长期保留。

## 10.9 容器与 GitOps 标准

1. 每个生产微服务必须有服务目录、Dockerfile / Containerfile、`service.yaml` 和 catalog entry。
2. 镜像必须推送到受控 container registry，不进入 Git 仓库。
3. 镜像 tag 可以使用 git sha、语义版本或构建号，但生产部署必须可追溯到 digest。
4. Kubernetes manifest 必须声明 requests、limits、health check、readiness、ServiceAccount 和最小权限。
5. dev、staging、prod 的差异必须通过 GitOps overlay 表达，不能在服务代码里硬编码环境差异。
6. 生产部署必须经过 SBOM、provenance、签名验签、漏洞阈值和策略准入。
7. 环境期望状态由 `infra/gitops/` 或等价 GitOps 仓库管理，实际运行状态由 Kubernetes 和 GitOps controller 管理。
8. catalog 记录 owner、domain、runtime、namespace、deployment 和 GitOps 路径，但不直接承载 Deployment manifest。
9. 平台团队维护模板、流水线和准入策略；服务团队维护服务代码和服务运行契约；环境 owner 维护环境级 overlay。

## 10.10 可执行企业标准包

本节把前文的架构原则转成可执行标准的第一批落地口径。它的目标不是把所有企业都锁死在同一个目录里，而是明确字段权威、模板骨架、自动化门禁和漂移检测规则，避免团队各写一份相似但互相冲突的 YAML。

### 10.10.1 字段权威矩阵

同一个字段只能有一个权威真相源。其他位置可以引用、派生、缓存或展示，但不能反向覆盖权威字段。

| 对象 | 字段类型 | 权威真相源 | 可派生到 | 禁止事项 |
| ---- | -------- | ---------- | -------- | -------- |
| 领域 | domain id、边界、owner、上游、下游、能力地图 | `domains/{domain}/domain.yaml` | `catalog/domains/`、Developer Portal、治理看板 | 在 catalog 中重新定义领域边界 |
| 服务 | 服务名、所属领域、owner、端口、健康检查、依赖、资源诉求、SLO、runbook | `domains/{domain}/services/{service}/service.yaml` | `catalog/components/`、CI、平台门户、生产就绪门禁 | 在 GitOps overlay 或 catalog 中改服务 owner 和领域 |
| API | endpoint、operation、schema、版本、兼容策略、鉴权要求 | `contracts/apis/` 或 `domains/*/apis/` | API Portal、SDK 生成器、兼容性测试 | 只在 README 或代码注释里维护接口契约 |
| 事件 | topic、schema、生产者、消费者、幂等键、兼容策略 | `contracts/events/` 或 `domains/*/events/` | Schema Registry、事件目录、消费者影响分析 | 未声明消费者就发布 breaking change |
| 数据产品 | 产品身份、owner、语义粒度、质量规则、分级分类、血缘、freshness、AI 使用策略 | `domains/{domain}/data-products/{data-product}/data-product.yaml` | 数据目录、质量看板、AI 数据授权、成本看板 | 让数据目录替代数据产品契约 |
| 数据契约 | schema、字段语义、兼容策略、访问策略、质量断言 | `contracts/datasets/` | 数据平台、Schema Registry、质量检查、权限网关 | 只在报表或口头口径里维护数据语义 |
| AI 产品 | 风险等级、模型路由、Prompt 引用、RAG 引用、工具引用、评估集、护栏、人工确认 | `ai/applications/{ai-product}/ai-product.yaml` | AI catalog、LLM Gateway、Agent Runtime、审计系统 | 让 Agent 直接绕过领域 API 或工具注册表 |
| AI 契约 | 工具输入输出、Prompt 版本、RAG 来源、评估集、护栏策略、微调数据授权 | `contracts/ai/` | AI 发布门禁、LLM Gateway、Tool Registry、审计系统 | 把 Prompt 或工具权限只藏在应用代码里 |
| catalog | 展示名、生命周期、owner 引用、关系图、runtime 指针、scorecard 结果 | `catalog/`，其中关键字段从权威源生成或校验 | Developer Portal、审计报表、搜索和发现 | 把 catalog 当 Deployment、领域模型或数据契约真相源 |
| GitOps | 环境、namespace、镜像 digest、replicas、资源 overlay、灰度策略 | `infra/gitops/environments/{env}/...` 或独立 GitOps 仓 | Argo CD / Flux、发布审计、回滚记录 | 在服务目录中硬编码环境差异 |
| Kubernetes runtime | pod、deployment、service、live status、事件、当前副本和运行指标 | Kubernetes API 和可观测性平台 | 运行看板、SLO、事件响应 | 把运行时实际状态回写成 Git 中的期望状态 |
| 治理规则 | 标准、门禁、例外、ADR、风险接受、复盘和到期时间 | `governance/` | CI、Policy as Code、审计系统、架构评审 | 口头豁免或永久例外 |

字段流转规则：

1. `domain.yaml`、`service.yaml`、`data-product.yaml` 和 `ai-product.yaml` 是产品团队维护的源头契约。
2. `contracts/` 维护机器可校验的接口、事件、数据、AI 工具、Prompt、RAG 和策略契约。
3. catalog 优先由源头契约和 `contracts/` 生成或校验，人工维护字段只限展示、分组、关系补充和生命周期说明。
4. GitOps 只声明环境期望状态，不拥有服务业务身份、领域边界、API 语义和数据语义。
5. Kubernetes 和可观测性平台只代表实际运行状态，不应反向改写 GitOps 期望状态。
6. 治理规则必须能被 CI、Policy as Code、平台门户或审计系统消费，否则只是说明文。

### 10.10.2 Starter Kit 最小模板

企业启动试点时不应先创建完整目录树，而应先创建能被平台、catalog、GitOps 和治理门禁识别的最小模板。

```text
domains/{domain}/domain.yaml
domains/{domain}/services/{service}/service.yaml
domains/{domain}/data-products/{data-product}/data-product.yaml
ai/applications/{ai-product}/ai-product.yaml
contracts/apis/{api}.openapi.yaml
contracts/events/{event}.asyncapi.yaml
contracts/ai/tools/{tool}.yaml
catalog/components/{service}.yaml
catalog/data-products/{data-product}.yaml
catalog/ai-products/{ai-product}.yaml
governance/architecture-gates/production-readiness.yaml
governance/ownership/raci.yaml
governance/slo/tiering-policy.md
governance/migration/deprecation-policy.md
governance/evidence/releases/{service-release}.yaml
governance/evidence/supply-chain/{service-attestation}.yaml
governance/evidence/exceptions/{policy-exception}.yaml
governance/evidence/compatibility/{api-or-event-report}.yaml
governance/evidence/drift/{service-drift-report}.yaml
governance/control-plane/conformance-profile.yaml
governance/control-plane/control-plane.yaml
governance/control-plane/release-gate-decision.yaml
governance/control-plane/standards-baseline.yaml
governance/control-plane/version-governance.yaml
governance/evidence/verification/{baseline-verification-lock}.yaml
governance/evidence/baselines/{baseline-artifact-inventory}.yaml
governance/evidence/baselines/{baseline-release-evidence}.yaml
governance/evidence/compatibility/{baseline-compatibility-ledger}.yaml
governance/evidence/adoption/{baseline-adoption-ledger}.yaml
governance/evidence/support/{baseline-support-matrix}.yaml
governance/evidence/release-trains/{baseline-release-train}.yaml
governance/evidence/communications/{baseline-notification-ledger}.yaml
governance/evidence/rollback/{baseline-rollback-verification}.yaml
governance/evidence/conformance/{baseline-conformance-claim}.yaml
infra/gitops/environments/dev/{domain}/{service}/kustomization.yaml
infra/gitops/environments/prod/{domain}/{service}/kustomization.yaml
```

`domain.yaml` 最低字段：

```yaml
domain: order
name: Order Domain
owner: team-order
lifecycle: production
boundedContext: docs/domain-model.md
capabilities:
  - order-command
  - order-query
upstream:
  - customer
downstream:
  - payment
  - fulfillment
sloTier: tier-1
dataClassification: internal
architectureDecision:
  - governance/decisions/adr-0001-order-boundary.md
```

`service.yaml` 最低字段：

```yaml
service: order-command-service
domain: order
owner: team-order
lifecycle: production
tier: tier-1
runtime:
  type: kubernetes
  imageRepository: registry.company.com/order/order-command-service
  ports:
    http: 8080
  health:
    liveness: /healthz
    readiness: /readyz
resources:
  requests:
    cpu: 200m
    memory: 256Mi
  limits:
    cpu: "1"
    memory: 1Gi
dependencies:
  apis:
    - customer-profile-api
  events:
    publishes:
      - order-created
    subscribes:
      - payment-authorized
slo:
  availability: 99.9
  latencyP95Ms: 300
reliability:
  rto: 1h
  rpo: 15m
  onCall: governance/ownership/escalation-policy.md
  errorBudgetPolicy: governance/slo/error-budget-policy.md
  drillEvidence: governance/evidence/drills/order-command-service-2026-q2.md
runbook: docs/runbook.md
rollback: docs/rollback.md
```

`data-product.yaml` 最低字段：

```yaml
dataProduct: order-facts
domain: order
owner: team-order
lifecycle: production
tier: tier-2
consumers:
  - revenue-dashboard
  - customer-service-agent
schema: schema/order-facts.schema.yaml
semanticGrain: one row per order state transition
freshness: 15m
quality:
  completeness: ">= 99.5%"
  validity: ">= 99.0%"
  uniqueness: order_event_id
  accuracy: reconciled with payment settlement daily
classification:
  level: confidential
  pii:
    - customer_id
retention: 2y
accessPolicy:
  policy: governance/data-governance/order-facts-access.rego
  approvalRequired: true
audit:
  enabled: true
  logRetention: 2y
lineage:
  upstream:
    - order-command-service
  downstream:
    - revenue-dashboard
    - customer-service-agent
aiUsage:
  allowed:
    - rag
    - evaluation
  disallowed:
    - foundation-model-training
cost:
  owner: team-order
  allocationTag: cost.domain.order
slo:
  freshness: 15m
  availability: 99.5
```

`ai-product.yaml` 最低字段：

```yaml
aiProduct: customer-service-agent
owner: team-support-ai
lifecycle: beta
riskTier: R3
businessGoal: assist support agents with grounded answers
model:
  gatewayRoute: support-safe-default
  approvedModel: vendor-support-model
  modelVersion: "2026-05"
prompts:
  system: prompts/system.prompt.md
rag:
  sources: rag/sources.yaml
  vectorIndex: vector:customer-support-policy:v12
tools:
  - tool: refund-preview
    riskLevel: high
    requiresHumanApproval: true
evals:
  regression: evals/regression.yaml
  redTeam: evals/red-team.yaml
guardrails:
  policy: guardrails/policy.rego
observability:
  traceRetentionDays: 180
  replayEnabled: true
slo:
  taskCompletionRate: ">= 85%"
  groundedAnswerRate: ">= 95%"
  toolErrorRate: "<= 2%"
  p95LatencyMs: 6000
budget:
  monthlyUsd: 3000
  costPerSuccessfulTaskUsd: 0.12
  owner: team-support-ai
fallback:
  degradedMode: human-support-queue
  humanHandoff: support-workbench
  rollbackPrompt: prompts/system.previous.prompt.md
providerPolicy:
  logRetention: 30d
  dataTrainingOptOut: true
  crossBorderReview: governance/security/cross-border-ai-review.md
dataUsePolicy:
  allowed:
    - rag
    - evaluation
  disallowed:
    - foundation-model-training
runbook:
  incident: governance/playbooks/ai-incident-playbook.md
  rollback: docs/rollback.md
```

V2.43 starter kit 还提供以下可执行契约模板：

1. `api-contract.yaml`：API producer、consumer、auth、版本和兼容策略。
2. `event-contract.yaml`：事件 topic、schema、幂等键、投递语义和消费者。
3. `ai-tool-contract.yaml`：AI 工具输入输出、风险等级、人工确认、权限、审计和运行限制。
4. `rag-index-contract.yaml`：RAG 来源、Embedding、切分、访问控制、刷新和删除策略。
5. `fine-tuning-contract.yaml`：微调数据授权、实验追踪、评估、发布门禁和回滚。
6. `fine-tuning-run.yaml`：单次微调运行的数据授权、数据准备、实验 run、评估、模型登记、审批、灰度发布、监控和退役证据。
7. `repository-change-control.yaml` 与 `repository-protection-runbook.md`：CODEOWNERS、受保护分支、PR 审查、必需检查、签名提交、禁止直推、发布 tag 保护、远端保护状态验证、标准整改、break-glass、POA&M 和风险登记。
8. `gitops-deployment.yaml`：环境、namespace、镜像 digest、资源、ServiceAccount、Pod 安全、网络策略、HPA、PDB、配置引用、发布策略和供应链准入。
9. `catalog-data-product.yaml`、`catalog-ai-product.yaml`：catalog 指针、owner、生命周期和运行索引。
10. `scorecard.yaml`：生产就绪、供应链、运行证据和复审周期。
11. `release-evidence.yaml`：发布版本、commit、GitOps revision、镜像 digest、catalog 指针、pipeline run、测试和批准证据。
12. `supply-chain-attestation.yaml`：构建来源、source control、SLSA 等级、builder identity、SBOM、provenance、签名、证书、透明日志、漏洞扫描、OpenSSF Scorecard 和验签命令。
13. `policy-exception.yaml`：治理例外、补偿控制、批准日期、到期日期、补救计划和过期自动阻断要求。
14. `api-compatibility-report.yaml`：API 版本兼容、消费者影响、breaking change 明细、豁免状态和发布决策。
15. `event-compatibility-report.yaml`：事件 Schema 兼容、消费者影响、重放要求、豁免状态和发布决策。
16. `gitops-drift-report.yaml`：GitOps 期望状态、运行观测状态、镜像/config/policy 漂移和发布阻断决策。
17. `extension-policy.yaml`：严格 schema 下的受控扩展前缀、审批记录、默认拒绝和未知字段行为。
18. `feature-flag-control.yaml`：Feature Flag、评估上下文、灰度策略、Kill Switch、SLO 燃尽回滚和曝光事件。
19. `ai-threat-model.yaml`：OWASP LLM / Agentic AI、MCP 工具边界、Prompt Injection 测试、红队结果和残余风险接受。
20. `lineage-event.yaml`：数据产品运行血缘事件、producer job、run state、输入输出数据集、schema 和质量证据。
21. `platform-product-metrics.yaml`：Platform PM、Golden Path、采用率、开发者满意度、认知负载、自助完成率和平台 SLO。
22. `privacy-impact-assessment.yaml`：隐私影响评估、处理目的、合法基础、主体权利、删除传播和 AI 使用限制。
23. `tenant-boundary.yaml`：租户、namespace、ServiceAccount、Secret 范围、ResourceQuota、NetworkPolicy 和准入策略。
24. `recovery-drill-evidence.yaml`：恢复演练、RTO/RPO 目标、实际恢复结果、备份、恢复日志和复盘证据。
25. `policy-test-report.yaml`：策略引擎、策略版本、测试总数、失败数、阻断决策和执行命令证据。
26. `genai-observability-contract.yaml`：OpenTelemetry GenAI、模型路由、Token、成本、工具调用、RAG span、日志脱敏和留存。
27. `ai-incident-playbook.yaml`：AI 事件响应 playbook、幻觉爆发、工具循环、RAG 索引污染、供应商中断、成本异常、检测、遏制、降级、回滚、工具 Kill Switch 和复盘。
28. `cost-allocation-evidence.yaml`：成本周期、owner、allocation tag、标签覆盖率、未分摊成本、成本来源和优化行动。
29. `identity-access-review.yaml`：身份源、角色、权限范围、特权身份、break-glass、MFA 和访问复核证据。
30. `secrets-rotation-evidence.yaml`：Secret provider、KMS、静态加密、轮换周期、轮换结果和泄露扫描证据。
31. `vulnerability-remediation-evidence.yaml`：漏洞 ID、严重度、KEV 状态、修复 SLA、残余风险和发布准入决策。
32. `incident-postmortem.yaml`：事故影响、检测/恢复时间、根因、纠正行动、runbook 更新、门禁反哺和关闭审批。
33. `evidence-freshness-policy.yaml`：证据最大年龄、按类型过期策略、必需证据、CI 执行和过期阻断策略。
34. `control-evidence-map.yaml`：控制项 ID、证据路径、状态、新鲜度、必需性和阻断属性。
35. `audit-export-manifest.yaml`：审计导出包范围、内容清单、验证结果、签名要求和留存复审。
36. `control-assessment-report.yaml`：控制评估范围、评估人、控制结果、发现项、整改、剩余风险和签署状态。
37. `baseline-change-record.yaml`：架构基线变更版本、前序版本、决策记录、影响分析、审批、验证命令、回滚计划和留存复审。
38. `architecture-decision-record.yaml`：ADR 上下文、备选方案、取舍、决策、关联控制项、风险、POA&M、复审和留存。
39. `oscal-export-profile.yaml`：OSCAL catalog、component-definition、SSP、assessment-results 和 POA&M 交换映射。
40. `audit-export-gate.yaml`：审计导出命令、本地质量门禁、输出不变量、OSCAL 摘要一致性和留存复审。
41. `audit-export-integrity.yaml`：审计导出生成物、SHA-256 摘要、源制品哈希和防篡改校验。
42. `audit-export-provenance.yaml`：审计导出 subject、构建定义、导出命令、源码提交和源证据依赖追溯。
43. `audit-export-signing-policy.yaml`：审计导出 provenance payload 摘要、Cosign 签名交接、验签命令和本地门禁边界。
44. `audit-export-signature-receipt.yaml`：审计导出外部签名完成后的 payload 摘要、bundle 摘要、证书身份、透明日志和验签结果。
45. `poam-record.yaml`：POA&M 发现项、责任人、整改行动、里程碑、证据、签署和复审。
46. `risk-register.yaml`：企业架构风险、处理策略、关联控制项、关联 POA&M、缓解行动、残余风险和复审。
47. `ai-evidence.yaml`：AI 产品证据账本、模型、Prompt、RAG、工具、评估、威胁模型、观测、事件响应、数据使用、审批、留存和复审。
48. `conformance-profile.yaml`：资产合规等级、风险画像、数据敏感度、AI 风险、监管强度、必须门禁和裁剪边界。
49. `control-plane.yaml`：企业执行控制面总账、控制项、证据、owner、阻断级别、自动化状态、复核周期和退出标准。
50. `release-gate-decision.yaml`：门禁决策、通过、阻断、条件放行、例外、break-glass、回滚要求和复核证据。
51. `standards-baseline.yaml`：外部标准版本、稳定性分级、采纳等级、适用范围、复核周期、升级门禁和回滚策略。
52. `version-governance.yaml`：基线身份、发布通道、源 commit、release tag、兼容窗口、冻结策略、升级门禁和回滚入口。
53. `baseline-release-evidence.yaml`：基线晋级决策、不可变引用、漂移复核、冻结检查、审计导出摘要、验签结果和回滚验证。
54. `baseline-compatibility-ledger.yaml`：消费者影响、受影响契约、迁移状态、弃用截止、例外、POA&M 和风险接受。
55. `baseline-adoption-ledger.yaml`：基线采用范围、采纳目标、当前基线、目标基线、采纳状态、逾期、例外和整改证据。
56. `baseline-support-matrix.yaml`：基线支持状态、维护窗口、安全补丁、EOL、冻结口径、最低可接受基线和例外。
57. `baseline-release-train.yaml`：基线候选窗口、冻结窗口、晋级日期、通知节奏、黑窗、紧急补丁和发布日历。
58. `baseline-conformance-claim.yaml`：资产声明基线、适用门禁、证据路径、例外、签署、复核和采纳总账回写。
59. `baseline-artifact-inventory.yaml`：基线源制品、schema、示例、控制项、证据模板、脚本、生成物、外部引用、SHA-256、签名状态和导出关系。
60. `baseline-verification-lock.yaml`：基线校验命令、runner 镜像、工具版本、策略包、schema validator、签名验签工具和审计导出生成环境。
61. `baseline-notification-ledger.yaml`：基线通知对象、通知渠道、送达回执、影响确认、异议、补发、例外审批和冻结前完成状态。
62. `baseline-exception-ledger.yaml`：基线级例外来源、受影响资产、owner、到期、风险接受、POA&M、补偿控制、阻断状态和关闭证据。
63. `baseline-rollback-verification.yaml`：上一基线、回滚目标 tag/commit、GitOps revision、审计导出恢复、烟测结果、恢复耗时、验证时效和阻断策略。
64. `baseline-readiness-scorecard.yaml`：基线晋级硬门禁、评分维度、证据路径、权重、阈值、阻断项和 baseline/frozen 最终判定。
65. `baseline-lifecycle-state-machine.yaml`：基线状态集合、允许迁移、禁止迁移、前置证据、审批责任、状态回写和迁移审计记录。

### 10.10.3 自动化门禁映射

门禁必须尽量前移到提交、构建、发布和运行阶段。人工评审只处理边界争议、风险接受和复杂权衡。

| 阶段 | 自动化门禁 | 输入 | 阻断条件 |
| ---- | ---------- | ---- | -------- |
| 提交 | Markdown、YAML、Schema、Policy 语法检查 | 文档、契约、策略文件 | 语法错误、坏链接、缺失必填字段 |
| Pull Request | API / Event / Data / AI 契约兼容性检查 | `contracts/`、`domains/`、`ai/`、兼容性报告 | breaking change 无消费者影响分析 |
| 构建 | 单元测试、依赖锁定、漏洞、许可证、密钥扫描 | 源码、锁文件、Dockerfile | 高危漏洞、未知许可证、密钥泄露 |
| 制品 | SBOM、provenance、镜像签名、基础镜像策略 | 镜像、构建日志、制品摘要、供应链证明 | 无 SBOM、无签名、来源不可证明 |
| 基线制品清单 | 源文档、schema、示例、控制项、证据模板、脚本、生成物、外部引用和摘要 | `baseline-artifact-inventory.yaml`、Git tree、starter kit、审计导出 | 基线包含未登记文件、必需制品摘要漂移、导出包缺源制品、签名覆盖不完整 |
| 基线验证环境 | 校验命令、runner 镜像、工具版本、策略包、schema validator、验签工具和生成环境 | `baseline-verification-lock.yaml`、CI runner、Makefile、policy bundle、validator | runner 未锁定、工具版本漂移、策略包摘要不一致、验签工具未固定 |
| 漏洞修复 | CVE / KEV、修复 SLA、残余风险、发布准入 | `vulnerability-remediation-evidence.yaml`、扫描器、制品库 | 高危漏洞未修复、SLA 超期、残余风险无审批 |
| 发布 | GitOps diff、策略准入、资源配额、SLO 和 runbook 校验 | GitOps overlay、catalog、service.yaml、发布证据 | 无 owner、无 runbook、无 digest、资源未声明 |
| 基线发布 | 晋级决策、冻结复核、漂移检查、不可变引用、签名验签和回滚验证 | `baseline-release-evidence.yaml`、`version-governance.yaml`、审计导出、Git tag | 无晋级证据、tag 与 commit 不一致、漂移复核缺失、回滚未验证 |
| 基线兼容 | 消费者影响、迁移窗口、弃用截止、未迁移对象和例外闭环 | `baseline-compatibility-ledger.yaml`、API/Event/Data/AI 兼容性报告、catalog | breaking change 无消费者清单、迁移到期仍未完成、例外无到期或 POA&M |
| 基线采纳 | 领域、平台、数据、AI、GitOps 和生产资产的目标基线、采用状态和逾期整改 | `baseline-adoption-ledger.yaml`、catalog、control assessment、scorecard | 关键资产采纳状态 unknown、L3/L4 资产逾期无例外、采用证据只停留在口头确认 |
| 基线支持 | 支持状态、维护窗口、安全补丁窗口、EOL、最低可接受基线和例外闭环 | `baseline-support-matrix.yaml`、version governance、release evidence、adoption ledger | 旧基线 EOL 后仍被 L3/L4 使用、安全补丁窗口结束后继续放行、新项目采用 maintenance/security-only/eol 基线 |
| 基线发布列车 | 候选窗口、冻结窗口、晋级日期、通知节奏、黑窗、紧急补丁入口和依赖证据 | `baseline-release-train.yaml`、version governance、support matrix、compatibility ledger、adoption ledger | 临时发版、无通知升级、冻结期合入非紧急变更、黑窗发布、紧急补丁缺事后补证 |
| 基线通知确认 | 通知对象、渠道、送达、确认、异议、补发、例外和冻结前完成状态 | `baseline-notification-ledger.yaml`、release train、compatibility ledger、adoption ledger、risk register | 关键 owner 未确认、通知失败无补发、异议未关闭、例外无审批、冻结前仍有 unknown |
| 基线回滚验证 | 上一基线、回滚目标、Git/tag/GitOps revision、审计导出恢复、烟测、证据摘要和验证时效 | `baseline-rollback-verification.yaml`、release evidence、version governance、GitOps、审计导出 | 回滚目标不可检出、GitOps revision 不存在、审计导出恢复失败、烟测失败或验证过期 |
| 基线例外总账 | 例外来源、受影响资产、owner、风险接受、POA&M、补偿控制、到期、关闭证据和冻结阻断 | `baseline-exception-ledger.yaml`、compatibility/adoption/support/notification/rollback ledgers、release gate、risk register | 例外散落未聚合、过期仍放行、阻断例外无 owner、条件放行无风险接受或 POA&M |
| 基线符合性声明 | 资产声明采用的基线、门禁等级、证据路径、例外、签署和复核 | `baseline-conformance-claim.yaml`、catalog、service/data/ai/product contract、adoption ledger | 中央采纳总账没有资产侧声明、资产声明过期、声明基线低于支持矩阵最低要求 |
| 访问复核 | 身份源、角色、特权权限、break-glass、MFA、复核报告 | `identity-access-review.yaml`、IAM、Kubernetes RBAC | 生产权限未复核、break-glass 无 MFA、特权账号无审计 |
| 密钥治理 | Secret provider、KMS、静态加密、轮换周期、泄露扫描 | `secrets-rotation-evidence.yaml`、密钥系统、扫描器 | 密钥未轮换、无静态加密、发现泄露仍放行 |
| 渐进式发布 | Feature Flag、Kill Switch、曝光事件、SLO 燃尽回滚 | `feature-flag-control.yaml`、GitOps、observability | 无关闭开关、无默认变体、无成功指标、无回滚条件 |
| AI 发布 | 评估集、红队、RAG 权限、工具权限、人工确认策略 | `ai-product.yaml`、`contracts/ai/` | 高风险工具无人工确认、评估未达标 |
| AI 证据账本 | 模型、Prompt、RAG、工具、评估、威胁模型、观测、事件响应、数据使用、审批和复审 | `ai-evidence.yaml`、`ai-product.yaml`、`ai-tool-contract.yaml`、`rag-index-contract.yaml`、`genai-observability-contract.yaml` | AI 证据分散、模型版本错配、工具权限和事件响应证据无法按产品聚合 |
| AI 安全 | Prompt Injection、工具同意、出站限制、残余风险接受 | `ai-threat-model.yaml`、`ai-tool-contract.yaml`、评估证据 | 高风险工具无同意、红队失败、风险接受过期 |
| AI 事件响应 | 幻觉爆发、工具循环、RAG 污染、供应商中断、成本异常、检测、遏制、降级、回滚和复盘 | `ai-incident-playbook.yaml`、`ai-product.yaml`、`ai-threat-model.yaml`、`genai-observability-contract.yaml` | 高风险 AI 无 playbook、触发器不全、无法人工接管或回滚 |
| 隐私工程 | DPIA、合法基础、主体权利、删除传播、AI 使用限制 | `privacy-impact-assessment.yaml`、数据产品、RAG 删除证据 | 有 PII 但无 DPIA、删除无法传播到向量索引、训练退出未声明 |
| 租户隔离 | namespace、ServiceAccount、Secret 范围、ResourceQuota、NetworkPolicy 默认拒绝 | `tenant-boundary.yaml`、GitOps、Kubernetes policy | 生产 namespace 无配额、默认放通网络、服务账号越界 |
| 数据发布 | schema、质量规则、权限、血缘、freshness 校验 | `data-product.yaml`、数据契约 | 无质量规则、无分级分类、无下游通知 |
| 数据运行 | 运行血缘、producer job、input/output dataset、质量证据 | `lineage-event.yaml`、调度系统、数据质量报告 | 无运行事件、血缘断裂、输出数据产品不匹配 |
| 恢复演练 | RTO/RPO、备份、恢复日志、数据丢失校验、复盘证据 | `recovery-drill-evidence.yaml`、备份系统、SRE 复盘 | 只声明目标无演练、恢复耗时超标、数据丢失未验证 |
| 策略测试 | OPA / Cedar / Kyverno 策略测试、失败数、阻断决策 | `policy-test-report.yaml`、Policy as Code 测试结果 | 策略无测试、失败用例未阻断、策略和准入证据不一致 |
| GenAI 观测 | Token、成本、工具调用、RAG span、trace 属性、日志脱敏 | `genai-observability-contract.yaml`、OpenTelemetry、AI gateway | 无 Token 成本指标、工具调用不可追踪、Prompt 日志未脱敏 |
| 平台运营 | Golden Path 采用率、开发者满意度、认知负载、平台 SLO | `platform-product-metrics.yaml`、平台门户、问卷和工单数据 | 认知负载过高、平台 SLO 不达标、改进行动无 owner |
| FinOps | 成本标签覆盖、未分摊成本、云/AI/数据成本、优化行动 | `cost-allocation-evidence.yaml`、OpenCost / FOCUS / 云账单 | 成本无 owner、标签覆盖不足、未分摊成本持续存在 |
| 事故复盘 | 影响、根因、检测/恢复时间、纠正行动、门禁反哺 | `incident-postmortem.yaml`、SRE 复盘、告警系统 | 事故未关闭、runbook 未更新、门禁未反哺 |
| 证据生命周期 | 证据最大年龄、按类型过期策略、CI 执行、过期阻断 | `evidence-freshness-policy.yaml`、审计索引、CI | 过期证据继续准入、关键证据不是必需项 |
| 控制证据映射 | 控制项 ID、证据路径、状态、新鲜度、必需性、阻断属性 | `control-evidence-map.yaml`、控制目录、CI | 控制项无证据、证据过期、非阻断控制被误放行 |
| 执行控制面 | 合规等级、控制项、证据、owner、阻断级别、自动化状态、复核周期和退出标准 | `conformance-profile.yaml`、`control-plane.yaml`、`release-gate-decision.yaml`、控制目录、CI | 不同团队用不同放行口径、条件放行无证据、例外过期仍继续发布 |
| 标准基线 | 外部标准名称、版本、稳定性、采纳等级、适用范围、owner、复核周期和升级门禁 | `standards-baseline.yaml`、参考资料、ADR、控制面 | 直接追随 latest、把 Development 状态规范当生产硬门禁、升级无兼容评估 |
| 版本控制面 | 基线 ID、版本、发布通道、source commit、release tag、兼容窗口、冻结状态和回滚入口 | `version-governance.yaml`、版本清单、tag、ADR、审计导出 | tag 漂移、版本复用、发布证据版本不一致、冻结基线被直接修改 |
| 基线生命周期状态机 | 状态集合、允许迁移、禁止迁移、迁移审批、状态回写和回滚入口 | `baseline-lifecycle-state-machine.yaml`、`version-governance.yaml`、`baseline-release-evidence.yaml`、`release-gate-decision.yaml` | 人工改状态、越级晋级、冻结后回退、状态机和版本控制面不一致 |
| 审计导出 | 架构版本、控制数量、starter kit 数量、导出内容、验证结果、签名、留存 | `audit-export-manifest.yaml`、审计包、签名系统 | 导出包范围不明、缺关键文件、未验证通过、未签名 |
| 审计导出自动化 | 校验命令、导出脚本、JSON 包、Markdown 报告、OSCAL 摘要、完整性清单、provenance statement、签名策略和验签回执契约 | `审计导出命令`、导出脚本、build 输出 | 审计包只能手工拼接、未先校验、缺制品哈希、生成来源、签名策略或验签回执 |
| 控制评估报告 | 评估范围、评估人、控制结果、发现项、整改、剩余风险、签署 | `control-assessment-report.yaml`、控制目录、证据映射、审计导出清单 | 只有证据无结论、发现项无人负责、未签署仍声称通过 |
| 架构基线变更 | 版本、前序版本、变更级别、影响分析、审批、验证、回滚、留存 | `baseline-change-record.yaml`、版本清单、控制目录、CI | 基线升级无审批、验证命令缺失、无法回滚到上一基线 |
| 架构决策记录 | ADR、上下文、备选方案、取舍、控制项、风险、POA&M、复审和留存 | `architecture-decision-record.yaml`、`baseline-change-record.yaml`、控制目录、风险登记、POA&M 记录 | 重大变更无 ADR、ADR 未关联控制项或风险、复审过期 |
| OSCAL 交换映射 | catalog、component-definition、SSP、assessment-results、POA&M、导出摘要 | `oscal-export-profile.yaml`、`oscal-summary.json`、审计导出脚本 | 只能内部阅读、不能对接 GRC、监管或外部审计工具 |
| POA&M 整改计划 | 发现项、控制项、严重度、责任人、行动、里程碑、证据、签署和复审 | `poam-record.yaml`、`oscal-summary.json`、控制评估报告 | 发现项只在报告正文里、整改无里程碑、OSCAL POA&M 视图无独立来源 |
| 企业架构风险登记 | 风险、严重度、可能性、影响、owner、处理策略、关联控制项、关联 POA&M、残余风险和复审 | `risk-register.yaml`、`oscal-summary.json`、控制目录、POA&M 记录 | 风险只在会议纪要里、无 owner、无控制项映射、残余风险无人接受 |
| 审计导出门禁 | 本地质量门禁、导出命令、输出不变量、pair 数、控制数、OSCAL 摘要一致性 | `audit-export-gate.yaml`、`审计导出门禁命令`、`make test` | 有导出脚本但未进入门禁、输出数量和版本不一致、OSCAL 摘要未验证 |
| 审计导出完整性 | 生成物 SHA-256、源制品哈希、完整性清单、防篡改校验 | `audit-export-integrity.yaml`、`audit-export-integrity.json`、审计导出门禁 | 审计包交接后无法证明未被篡改、生成物哈希缺失、源制品和导出包断链 |
| 审计导出 provenance | in-toto statement、SLSA provenance、subject digest、构建定义、源码提交和源证据依赖 | `audit-export-provenance.yaml`、`audit-export-provenance.json`、审计导出门禁 | 审计包知道哈希但不知道来源、生成上下文不可证明、无法绑定签名 payload |
| 审计导出签名策略 | provenance payload 摘要、签名方式、验签命令、bundle 路径和透明日志要求 | `audit-export-signing-policy.yaml`、`audit-export-signing-policy.json`、审计导出门禁 | 声称需要签名但没有 payload 摘要、验签路径或外部签名交接 |
| 审计导出签名验签回执 | 签名策略绑定、payload 摘要、bundle 摘要、证书身份、OIDC issuer、透明日志和验签结果 | `audit-export-signature-receipt.yaml`、签名系统、验签日志 | 外部签名完成后没有可审计回执、证书身份和透明日志不可追溯 |
| 运行 | SLO、成本、漂移、异常调用、供应链策略漂移 | runtime、observability、audit、漂移报告 | 错误预算耗尽、成本超预算、策略漂移 |

### 10.10.4 漂移检测规则

可执行标准必须能发现“文档这么写、运行不是这样”的漂移。

必须检测的漂移：

1. `service.yaml` 的 owner、domain、端口、依赖和 catalog entry 不一致。
2. catalog 指向的 GitOps 路径不存在，或 GitOps 路径指向的服务没有 catalog entry。
3. GitOps 使用的镜像 tag 无法解析到不可变 digest。
4. 生产 Deployment 的镜像 digest 与 GitOps 期望状态不一致。
5. 生产 Deployment 的 ConfigMap / Secret hash、ServiceAccount、NetworkPolicy、Pod 安全策略或准入策略与 GitOps 期望状态不一致。
6. Kubernetes runtime 存在未登记到 catalog 的长期运行工作负载。
7. 数据产品 schema 与实际表结构或数据契约不一致。
8. AI 产品运行中的 Prompt、模型、RAG 索引或工具版本与 `ai-product.yaml` 不一致。
9. 策略例外超过到期时间仍在生产准入中生效。

漂移处理规则：

1. 发现漂移后先判断权威真相源，再决定修正 Git、catalog、runtime 还是治理例外。
2. 运行时紧急修复必须在事后回写 GitOps 或形成 incident / postmortem，不能长期保留手工状态。
3. catalog 漂移优先通过重新生成或重新校验修复，不应手工覆盖源头契约。
4. 涉及生产安全、AI 高风险工具、数据权限和供应链证明的漂移必须阻断发布。

### 10.10.5 控制项覆盖清单

可执行企业标准不能只证明“字段存在”，还要证明关键控制项确实被 schema、example 和 checker 覆盖。

V2.6 起，控制项覆盖清单由以下文件维护；V2.7 起，严格 schema 控制项进入同一清单；V2.8 起，扩展策略、发布开关、AI 威胁模型、运行血缘和平台产品指标也进入同一清单；V2.9 起，隐私影响评估、租户隔离、恢复演练、策略测试、GenAI 观测和成本分摊证据也进入同一清单；V2.10 起，访问复核、密钥轮换、漏洞修复、事故复盘和证据新鲜度也进入同一清单；V2.11 起，控制证据映射和审计导出清单也进入同一清单；V2.12 起，审计导出自动化命令也进入同一清单；V2.13 起，控制评估报告也进入同一清单；V2.14 起，架构基线变更记录也进入同一清单；V2.15 起，OSCAL 交换映射也进入同一清单；V2.16 起，审计导出门禁也进入同一清单；V2.17 起，审计导出完整性清单也进入同一清单；V2.18 起，审计导出 provenance statement 也进入同一清单；V2.19 起，审计导出签名策略也进入同一清单；V2.20 起，审计导出签名验签回执也进入同一清单；V2.21 起，POA&M 整改计划也进入同一清单；V2.22 起，企业架构风险登记也进入同一清单；V2.23 起，架构决策记录也进入同一清单；V2.24 起，AI 事件响应 playbook 也进入同一清单；V2.25 起，AI 证据账本也进入同一清单；V2.26 起，微调运行证据也进入同一清单；V2.27 起，仓库变更控制和远端保护漂移整改也进入同一清单；V2.28 起，合规等级、执行控制面和门禁决策也进入同一清单；V2.29 起，外部标准版本锁定和升级门禁也进入同一清单；V2.30 起，版本控制面和基线发布不变量也进入同一清单；V2.31 起，基线发布证据包、晋级决策、冻结复核和版本漂移复核也进入同一清单；V2.32 起，基线兼容性总账、消费者迁移和未迁移风险闭环也进入同一清单；V2.33 起，基线采纳总账、组织采纳状态、逾期整改和例外闭环也进入同一清单；V2.34 起，基线支持矩阵、维护窗口、安全补丁、EOL 和最低可接受基线也进入同一清单；V2.35 起，基线发布列车、候选窗口、冻结窗口、晋级日期、通知节奏、黑窗和紧急补丁也进入同一清单；V2.36 起，资产级基线符合性声明、资产自声明、证据绑定、例外和采纳总账回写也进入同一清单；V2.37 起，基线制品清单、源制品摘要、必需性、签名状态、导出关系和未登记制品阻断也进入同一清单；V2.38 起，基线验证环境锁定、校验命令、runner 镜像、工具版本、策略包、validator 和验签工具也进入同一清单；V2.39 起，基线通知确认总账、通知对象、送达回执、影响确认、异议、例外和冻结前完成状态也进入同一清单；V2.40 起，基线回滚验证记录、上一基线检出、GitOps revision 恢复、审计导出恢复、烟测结果和验证时效也进入同一清单；V2.41 起，基线例外总账、例外来源聚合、风险接受、POA&M、过期阻断和冻结准入也进入同一清单；V2.42 起，基线就绪评分卡、硬门禁、评分维度、证据绑定和最终准入判定也进入同一清单；V2.43 起，基线生命周期状态机、允许迁移、禁止迁移、迁移审批、状态回写和迁移审计证据也进入同一清单：

```text
内部控制项覆盖清单
```

该清单采用轻量控制目录结构，不替代完整 OSCAL 实施。它至少记录：

1. 控制项 ID、分类、标题和控制声明。
2. 控制项对齐的参考来源，例如 NIST OSCAL、SLSA、NIST SSDF。
3. 必须存在的文档、schema、example 或脚本。
4. 必须出现在 schema `required` 和 `properties` 中的字段。
5. 必须出现在 YAML example 中的字段。
6. 必须出现在 checker 中的自动化证据规则。

控制项覆盖清单用于回答：

| 问题 | 证明方式 |
| ---- | -------- |
| 文档说生产服务必须有 RTO/RPO，机器是否能证明 | 控制项要求 `service.schema.json` 和 `service.example.yaml` 包含 `reliability.rto`、`reliability.rpo` |
| 文档说架构基线仓库必须受保护，机器是否能证明 | 控制项要求 `repository-change-control.schema.json`、示例和 runbook 包含 CODEOWNERS、受保护分支、必需检查、签名提交、禁止直推、远端验证、漂移整改、POA&M 和风险登记 |
| 文档说数据产品必须有访问审计，机器是否能证明 | 控制项要求 `data-product.schema.json` 和示例包含 `accessPolicy`、`audit`、`retention` |
| 文档说 AI 产品必须可降级和控成本，机器是否能证明 | 控制项要求 `ai-product.schema.json` 和示例包含 `budget`、`fallback`、`providerPolicy` |
| 文档说 AI 产品证据必须可追踪，机器是否能证明 | 控制项要求 `ai-evidence.schema.json` 和示例包含模型、Prompt、RAG、工具、评估、威胁模型、观测、事件响应、数据使用、审批和复审 |
| 文档说企业不同风险等级必须使用不同门禁，机器是否能证明 | 控制项要求 `conformance-profile.schema.json`、`control-plane.schema.json` 和 `release-gate-decision.schema.json` 绑定等级、证据、阻断级别、例外和复核 |
| 文档说外部标准不能直接追随 latest，机器是否能证明 | 控制项要求 `standards-baseline.schema.json` 和示例包含标准名称、版本、稳定性、采纳等级、复核周期和升级门禁 |
| 文档说基线版本必须可追溯且不可复用，机器是否能证明 | 控制项要求 `version-governance.schema.json` 和示例包含基线 ID、发布通道、源 commit、release tag、兼容窗口、冻结策略和回滚入口 |
| 文档说基线发布必须有晋级、冻结和漂移复核证据，机器是否能证明 | 控制项要求 `baseline-release-evidence.schema.json` 和示例包含晋级决策、不可变引用、漂移复核、审计导出摘要、验签结果和回滚验证 |
| 文档说 breaking change 必须有消费者迁移闭环，机器是否能证明 | 控制项要求 `baseline-compatibility-ledger.schema.json` 和示例包含消费者、受影响契约、迁移状态、弃用截止、例外、POA&M 和风险接受 |
| 文档说企业级基线必须被组织采纳，机器是否能证明 | 控制项要求 `baseline-adoption-ledger.schema.json` 和示例包含采纳范围、目标、当前基线、目标基线、采纳状态、截止日期、例外和整改证据 |
| 文档说旧基线不能无限期被使用，机器是否能证明 | 控制项要求 `baseline-support-matrix.schema.json` 和示例包含支持状态、维护窗口、安全补丁窗口、EOL、最低可接受基线、例外和阻断规则 |
| 文档说基线发布必须按列车和冻结窗口执行，机器是否能证明 | 控制项要求 `baseline-release-train.schema.json` 和示例包含候选窗口、冻结窗口、晋级日期、通知节奏、黑窗、紧急补丁和依赖证据 |
| 文档说采纳总账必须来自资产侧声明，机器是否能证明 | 控制项要求 `baseline-conformance-claim.schema.json` 和示例包含资产 ID、声明基线、证据路径、签署、例外、复核和采纳总账回写 |
| 文档说基线由哪些源制品构成，机器是否能证明 | 控制项要求 `baseline-artifact-inventory.schema.json` 和示例包含制品路径、类型、摘要、必需性、签名状态、导出关系和未登记制品阻断 |
| 文档说同一基线必须用同一验证环境复现，机器是否能证明 | 控制项要求 `baseline-verification-lock.schema.json` 和示例包含命令、runner 镜像、工具版本、策略包摘要、schema validator、验签工具和生成环境 |
| 文档说冻结前必须完成消费者通知确认，机器是否能证明 | 控制项要求 `baseline-notification-ledger.schema.json` 和示例包含通知对象、渠道、送达、确认、异议、例外、补发和冻结前完成状态 |
| 文档说回滚路径必须实际可恢复，机器是否能证明 | 控制项要求 `baseline-rollback-verification.schema.json` 和示例包含上一基线、回滚目标、Git/tag/GitOps revision、审计导出恢复、烟测结果和验证时效 |
| 文档说基线例外不能散落和过期放行，机器是否能证明 | 控制项要求 `baseline-exception-ledger.schema.json` 和示例包含例外来源、owner、到期日、风险接受、POA&M、阻断状态、关闭证据和冻结准入 |
| 文档说基线是否可以晋级必须有最终判定，机器是否能证明 | 控制项要求 `baseline-readiness-scorecard.schema.json` 和示例包含硬门禁、评分维度、权重、证据路径、阻断项、baseline/frozen 阈值和最终判定 |
| 文档说基线状态不能被人工随意改写，机器是否能证明 | 控制项要求 `baseline-lifecycle-state-machine.schema.json` 和示例包含状态集合、允许迁移、禁止迁移、迁移证据、审批责任、回写目标和审计记录 |
| 文档说 AI 事件响应必须有专门 playbook，机器是否能证明 | 控制项要求 `ai-incident-playbook.schema.json` 和示例包含触发器、检测、遏制、降级、回滚、RAG 恢复、工具 Kill Switch 和复盘 |
| 文档说 GitOps 必须有运行安全，机器是否能证明 | 控制项要求 `gitops-deployment.schema.json` 和示例包含 `serviceAccount`、`security`、`scaling` |
| 文档说供应链必须有漏洞和 Scorecard 证据，机器是否能证明 | 控制项要求 `supply-chain-attestation.schema.json` 和示例包含 `vulnerability`、`scorecard` |
| 文档说 starter kit 必须拒绝未知字段，机器是否能证明 | 控制项要求 checker 包含 `additionalProperties must be false` 和 `unexpected field` 证据 |
| 文档说严格 schema 必须有扩展出口，机器是否能证明 | 控制项要求 `extension-policy.schema.json` 和示例包含受控前缀、审批和默认拒绝策略 |
| 文档说生产灰度必须可关闭，机器是否能证明 | 控制项要求 `feature-flag-control.schema.json` 和示例包含 `killSwitch`、`rollbackOnSloBurn` 和曝光事件 |
| 文档说 AI 产品必须做威胁建模，机器是否能证明 | 控制项要求 `ai-threat-model.schema.json` 和示例包含 OWASP、MCP、红队、工具同意和残余风险 |
| 文档说数据产品必须有运行血缘，机器是否能证明 | 控制项要求 `lineage-event.schema.json` 和示例包含 job、run、inputs、outputs、schema 和质量证据 |
| 文档说平台工程必须作为产品运营，机器是否能证明 | 控制项要求 `platform-product-metrics.schema.json` 和示例包含 Platform PM、Golden Path、满意度、认知负载和改进行动 |
| 文档说含 PII 的数据产品必须做隐私影响评估，机器是否能证明 | 控制项要求 `privacy-impact-assessment.schema.json` 和示例包含 DPIA、主体权利、删除传播和 AI 使用限制 |
| 文档说生产租户必须有隔离和配额，机器是否能证明 | 控制项要求 `tenant-boundary.schema.json` 和示例包含 ResourceQuota、NetworkPolicy 默认拒绝和准入策略 |
| 文档说 RTO/RPO 必须被演练证明，机器是否能证明 | 控制项要求 `recovery-drill-evidence.schema.json` 和示例包含目标、实际恢复结果、备份、恢复日志和复盘 |
| 文档说策略准入必须可测试，机器是否能证明 | 控制项要求 `policy-test-report.schema.json` 和示例包含策略引擎、测试数、失败数和执行命令 |
| 文档说 GenAI 必须可观测，机器是否能证明 | 控制项要求 `genai-observability-contract.schema.json` 和示例包含 Token、成本、工具调用、RAG span 和日志脱敏 |
| 文档说成本必须可分摊，机器是否能证明 | 控制项要求 `cost-allocation-evidence.schema.json` 和示例包含标签覆盖率、未分摊成本、总成本和优化行动 |
| 文档说生产访问必须复核，机器是否能证明 | 控制项要求 `identity-access-review.schema.json` 和示例包含身份源、角色、break-glass、MFA 和复核结论 |
| 文档说生产密钥必须轮换，机器是否能证明 | 控制项要求 `secrets-rotation-evidence.schema.json` 和示例包含 KMS、静态加密、轮换结果和泄露扫描 |
| 文档说高危漏洞必须修复，机器是否能证明 | 控制项要求 `vulnerability-remediation-evidence.schema.json` 和示例包含 SLA、修复日期、残余风险和发布准入 |
| 文档说生产事故必须复盘反哺，机器是否能证明 | 控制项要求 `incident-postmortem.schema.json` 和示例包含根因、行动项、runbook 更新和门禁更新 |
| 文档说证据不能过期继续准入，机器是否能证明 | 控制项要求 `evidence-freshness-policy.schema.json` 和示例包含最大年龄、过期阻断和 CI 执行 |
| 文档说每个控制项都必须有可追踪证据，机器是否能证明 | 控制项要求 `control-evidence-map.schema.json` 和示例覆盖全部控制项 ID、证据路径、状态和新鲜度 |
| 文档说审计包必须可导出和复核，机器是否能证明 | 控制项要求 `audit-export-manifest.schema.json` 和示例包含范围、内容、验证、签名和留存 |
| 文档说审计包必须能由仓库生成，机器是否能证明 | 控制项要求 审计导出脚本、Makefile 入口和 checker 自动化检查 |
| 文档说控制必须被评估和签署，机器是否能证明 | 控制项要求 `control-assessment-report.schema.json` 和示例包含控制结果、发现项、整改、剩余风险和签署 |
| 文档说基线变更必须受控，机器是否能证明 | 控制项要求 `baseline-change-record.schema.json` 和示例包含影响分析、审批、验证命令和回滚计划 |
| 文档说重大架构变更必须有 ADR，机器是否能证明 | 控制项要求 `architecture-decision-record.schema.json` 和示例包含上下文、备选方案、取舍、控制项、风险、POA&M 和复审 |
| 文档说审计证据必须可交换，机器是否能证明 | 控制项要求 `oscal-export-profile.schema.json`、示例和导出脚本覆盖 OSCAL 五类视图 |
| 文档说发现项必须进入 POA&M 整改计划，机器是否能证明 | 控制项要求 `poam-record.schema.json`、示例和导出脚本覆盖发现项、行动、里程碑、证据和 OSCAL POA&M 输出 |
| 文档说架构风险必须登记和复审，机器是否能证明 | 控制项要求 `risk-register.schema.json`、示例和导出脚本覆盖风险、控制项、POA&M、缓解行动、残余风险和复审 |
| 文档说审计导出必须进入质量门禁，机器是否能证明 | 控制项要求 `audit-export-gate.schema.json`、审计导出门禁脚本和 `make test` 覆盖输出不变量 |
| 文档说审计包交接后必须可防篡改复核，机器是否能证明 | 控制项要求 `audit-export-integrity.schema.json`、导出脚本和门禁覆盖生成物 SHA-256 摘要 |
| 文档说审计包必须能证明生成来源，机器是否能证明 | 控制项要求 `audit-export-provenance.schema.json`、导出脚本和门禁覆盖 subject digest、构建定义、源码提交和源证据依赖 |

`starter kit 校验命令` 必须校验控制清单自身，并校验清单中声明的 schema 字段、example 字段和 checker 证据确实存在。

### 10.10.6 企业执行控制面

企业执行控制面的目标，是把“这个标准是否真的落地”从文档判断变成门禁判断。它不替代具体工具，而是定义所有工具必须对齐的共同控制协议。

控制面由三类文件组成：

```text
governance/control-plane/conformance-profile.yaml
governance/control-plane/control-plane.yaml
governance/control-plane/release-gate-decision.yaml
```

`conformance-profile.yaml` 定义资产需要执行到什么强度：

```yaml
profile: regulated-ai-prod
appliesTo:
  assetTypes:
    - service
    - data-product
    - ai-product
  environments:
    - prod
risk:
  businessCriticality: tier-1
  dataSensitivity: confidential
  aiRiskTier: R3
  internetFacing: true
requiredGateLevel: L4
requiredEvidence:
  - owner
  - service-contract
  - api-compatibility
  - data-contract
  - ai-evaluation
  - sbom
  - provenance
  - signature-verification
  - gitops-diff
  - slo
  - runbook
  - rollback
  - incident-playbook
  - audit-export
allowedExceptions:
  maxActiveDays: 30
  requiresRiskAcceptance: true
  requiresCompensatingControl: true
review:
  cadence: quarterly
  owner: architecture-governance-board
```

`control-plane.yaml` 汇总控制项、证据、阻断级别和自动化状态：

```yaml
controlPlane:
  version: V2.28
  owner: architecture-governance-board
  defaultProfile: standard-prod
controls:
  - id: EA-REL-001
    title: Production service has owner, SLO and runbook
    appliesTo:
      - service
    gateLevel: L2
    blocking: true
    evidence:
      - domains/{domain}/services/{service}/service.yaml
      - catalog/components/{service}.yaml
      - governance/evidence/releases/{release}.yaml
    automation:
      status: enforced
      command: service-contract-check
    freshness:
      maxAgeDays: 90
    exception:
      allowed: false
  - id: EA-AI-004
    title: High-risk AI product has evaluation, threat model and incident playbook
    appliesTo:
      - ai-product
    gateLevel: L4
    blocking: true
    evidence:
      - ai/applications/{ai-product}/ai-product.yaml
      - contracts/ai/threat-models/{ai-product}.yaml
      - governance/playbooks/{ai-product}-incident-playbook.yaml
      - governance/evidence/ai/{ai-product}-evidence.yaml
    automation:
      status: measured
      command: ai-release-gate
    freshness:
      maxAgeDays: 30
    exception:
      allowed: true
      maxActiveDays: 14
      requiresHumanApproval: true
```

`release-gate-decision.yaml` 记录每次门禁结果：

```yaml
decision:
  id: gate-2026-06-02-order-command-service
  asset: order-command-service
  profile: regulated-ai-prod
  environment: prod
  result: conditional-pass
  decidedAt: 2026-06-02T07:30:00+08:00
  decidedBy: release-captain
checks:
  passed:
    - sbom
    - provenance
    - signature-verification
    - gitops-diff
  failed:
    - recovery-drill-freshness
exceptions:
  - id: ex-2026-q2-recovery-drill
    expiresAt: 2026-06-16T23:59:59+08:00
    riskAcceptedBy: sre-lead
    compensatingControl: on-call manual recovery drill scheduled
requiredActions:
  - owner: team-order
    due: 2026-06-10
    action: complete recovery drill and attach evidence
rollback:
  required: true
  plan: docs/rollback.md
```

门禁等级采用五级：

| 等级 | 含义 | 适用对象 | 最低要求 |
| ---- | ---- | -------- | -------- |
| `L0` | 记录级 | 实验、非生产、一次性验证 | owner、生命周期、退出日期 |
| `L1` | 契约级 | 低风险内部服务、内部数据集 | 机器可读契约、catalog、基础测试 |
| `L2` | 发布级 | 普通生产服务和数据产品 | CI、SLO、runbook、GitOps、发布证据 |
| `L3` | 证明级 | Tier-1 服务、机密数据、外部接口 | SBOM、provenance、签名验签、恢复演练、控制证据映射 |
| `L4` | 受控级 | 高风险 AI、受监管流程、关键资金链路 | 独立审批、红队、审计导出、POA&M、风险接受和季度复核 |

门禁结果只能使用以下五类：

| 结果 | 含义 | 是否允许发布 | 必须附带 |
| ---- | ---- | ------------ | -------- |
| `pass` | 所有阻断项通过 | 是 | 自动化证据和审计索引 |
| `conditional-pass` | 非阻断项缺失或证据临近过期 | 是 | 到期行动、owner、补偿控制 |
| `fail` | 阻断项失败 | 否 | 失败项、修复建议、重新验证命令 |
| `exception` | 经授权的风险接受 | 视等级而定 | 到期时间、批准人、补偿控制、POA&M |
| `break-glass` | 生产紧急处置 | 临时允许 | 事故编号、最短有效期、事后复盘和回补证据 |

执行规则：

1. `L3` 和 `L4` 资产不得仅凭人工评审发布，必须有机器证据和签署记录。
2. `conditional-pass` 不能连续出现两次；第二次必须转为 `fail` 或正式例外。
3. 所有 `exception` 必须有到期时间、风险接受人、补偿控制和关闭条件。
4. `break-glass` 只能用于生产事故或监管时限，必须在 24 到 72 小时内补齐复盘和证据。
5. 证据过期视为证据缺失；关键证据过期必须阻断同等级资产的新发布。
6. 每季度必须抽样复核 `L3` / `L4` 资产，复核结果进入 `control-assessment-report.yaml`。
7. 控制面本身的变更必须走 ADR、CODEOWNERS、受保护分支和基线变更记录。

可执行验收标准：

1. 任意生产资产都能找到自己的 `conformance-profile`。
2. 任意阻断控制都能从 `control-plane` 追溯到证据路径、自动化状态和 owner。
3. 任意发布都能找到 `release-gate-decision`，并能解释为什么通过、阻断或例外放行。
4. 任意例外都能找到到期时间、补偿控制、风险接受人和关闭证据。
5. 任意审计导出都能包含控制面版本、门禁决策摘要、开放例外和 POA&M 状态。

### 10.10.7 外部标准版本锁定与升级策略

企业标准不能直接引用“latest”。外部标准、规范、语义约定和工具能力都必须先进入版本锁定清单，再进入控制面、门禁和审计证据。

标准基线由 `standards-baseline.yaml` 维护：

```yaml
standardBaseline:
  version: V2.29
  owner: architecture-governance-board
  reviewCadence: quarterly
standards:
  - id: slsa
    name: Supply-chain Levels for Software Artifacts
    pinnedVersion: v1.2
    status: approved
    adoptionLevel: enforce
    sourceUrl: https://slsa.dev/spec/v1.2/
    reviewedAt: "2026-06-02"
    appliesTo:
      - supply-chain-attestation
      - audit-export-provenance
    minimumGateLevel: L3
    upgradePolicy:
      requiresAdr: true
      requiresCompatibilityReview: true
      rollout: phased
  - id: otel-genai
    name: OpenTelemetry Semantic Conventions for Generative AI
    pinnedVersion: semconv-1.41.0
    status: development
    adoptionLevel: observe
    sourceUrl: https://opentelemetry.io/docs/specs/semconv/gen-ai/
    reviewedAt: "2026-06-02"
    appliesTo:
      - genai-observability-contract
      - ai-evidence
    minimumGateLevel: L2
    upgradePolicy:
      requiresAdr: false
      requiresCompatibilityReview: true
      rollout: opt-in
```

采纳等级分为四类：

| 等级 | 含义 | 是否可阻断发布 | 示例 |
| ---- | ---- | -------------- | ---- |
| `reference` | 仅作为设计参考，不进入门禁 | 否 | 白皮书、方法论、非规范文章 |
| `observe` | 进入观测和证据字段，但不作为硬阻断 | 否 | Development 状态语义约定、实验性 Agent 协议 |
| `gate` | 进入门禁，但允许阶段性例外 | 是 | API 兼容、数据质量、GenAI trace 覆盖率 |
| `enforce` | 强制执行，例外必须有风险接受和到期时间 | 是 | SLSA provenance、SBOM、签名验签、生产 GitOps digest |

稳定性分级：

| 状态 | 处理方式 |
| ---- | -------- |
| `approved` / `stable` | 可以进入 `gate` 或 `enforce`，但仍需锁定版本 |
| `draft` / `release-candidate` | 默认进入 `gate`，不得直接设为全局 `enforce` |
| `concept-note` / `community-preview` | 默认进入 `observe` 或 `reference`，不得作为强制门禁 |
| `development` / `experimental` | 默认只能 `observe`，生产阻断必须有 ADR 和灰度窗口 |
| `deprecated` | 禁止新项目采用，既有项目必须给出迁移截止日期 |

基线升级流程：

1. 识别外部标准新版本、状态变化、废弃说明和向后兼容风险。
2. 由 owner 生成标准升级影响分析，列出受影响契约、控制项、工具和证据字段。
3. 对 `gate` / `enforce` 标准必须形成 ADR 或基线变更记录。
4. 先在非生产 profile 或低风险资产上灰度，验证 CI、导出包、catalog 和观测字段兼容性。
5. 灰度通过后更新 `standards-baseline.yaml`、控制项覆盖清单和相关门禁。
6. 如果升级导致审计字段、证据格式或策略结果变化，必须生成迁移说明和回滚路径。

当前建议锁定的关键标准基线：

| 标准 | 建议状态 | 采纳等级 | 说明 |
| ---- | -------- | -------- | ---- |
| SLSA v1.2 | approved | enforce | 用于 provenance、构建来源和供应链证明 |
| SPDX 3.0.1 / CycloneDX 1.7 | stable | enforce | 用于 SBOM 生成和制品审计 |
| Sigstore / Cosign | stable | enforce | 用于镜像、provenance 和审计导出签名验签 |
| NIST AI RMF 1.0 + NIST AI 600-1 | stable | gate | 用于 AI 风险治理、评估和管理闭环 |
| NIST AI RMF Critical Infrastructure Profile Concept Note | concept-note | observe | 用于关键基础设施 AI 场景观察和预研，不作为稳定强制门禁 |
| OpenTelemetry Semantic Conventions 1.41.0 / GenAI SemConv | development | observe | 用于 GenAI trace、Token、模型和工具调用观测，生产字段需版本锁定 |
| OWASP LLM / Agentic AI | active | gate | 用于威胁模型、红队和工具权限门禁 |
| Kubernetes / OpenGitOps | stable | enforce | 用于运行期望状态、漂移检测和 GitOps 发布控制 |
| CNCF Platform Engineering Maturity Model | reference | reference | 用于平台成熟度评估，不直接阻断发布 |

禁止事项：

1. 禁止在生产门禁中使用未锁定版本的外部标准。
2. 禁止把 `development` 状态规范直接设为全局强制阻断。
3. 禁止把 `concept-note`、白皮书、社区预览或供应商路线图当作稳定合规要求。
4. 禁止标准升级只改文档、不改 checker、证据字段和迁移说明。
5. 禁止一个团队私自升级共享门禁标准，导致其他团队 CI 或审计导出漂移。

### 10.10.8 版本控制面和基线发布协议

`version-governance.yaml` 是架构基线发布的控制面。它不存放正文内容，而是把版本、Git、证据和门禁绑定成同一条可验证事实链。

```yaml
versionGovernance:
  baselineId: mea-v2.43-20260602
  documentVersion: V2.43
  releaseChannel: candidate
  status: Baseline Candidate
  owner: architecture-governance-board
  sourceCommit: <git-sha-of-baseline-commit>
  releaseTag: architecture/v2.43-candidate
  tagSigned: true
  effectiveFrom: 2026-06-02
  supersedes: V2.42
  compatibility:
    changeLevel: minor
    backwardCompatible: true
    compatibilityWindow: P90D
    migrationRequired: false
  linkedBaselines:
    versionManifest: governance/control-plane/version-manifest.yaml
    controlCoverage: governance/control-plane/control-coverage.yaml
    standardsBaseline: governance/control-plane/standards-baseline.yaml
    auditExportManifest: governance/evidence/audit-export/audit-export-manifest.yaml
    lifecycleStateMachine: governance/evidence/baselines/baseline-lifecycle-state-machine.yaml
    compatibilityLedger: governance/evidence/compatibility/baseline-compatibility-ledger.yaml
    adoptionLedger: governance/evidence/adoption/baseline-adoption-ledger.yaml
    supportMatrix: governance/evidence/support/baseline-support-matrix.yaml
    releaseTrain: governance/evidence/release-trains/baseline-release-train.yaml
    readinessScorecard: governance/evidence/baselines/baseline-readiness-scorecard.yaml
    exceptionLedger: governance/evidence/exceptions/baseline-exception-ledger.yaml
    notificationLedger: governance/evidence/communications/baseline-notification-ledger.yaml
    rollbackVerification: governance/evidence/rollback/baseline-rollback-verification.yaml
    conformanceClaims: governance/evidence/conformance/baseline-conformance-claim.yaml
    artifactInventory: governance/evidence/baselines/baseline-artifact-inventory.yaml
    verificationLock: governance/evidence/verification/baseline-verification-lock.yaml
  gates:
    required:
      - make sync-doc-toc
      - make test
      - git diff --check
    releaseDecision: governance/control-plane/release-gate-decision.yaml
  freezePolicy:
    canFreezeAfter:
      - architecture-review-approved
      - audit-export-generated
      - open-critical-findings-zero
    emergencyPatchAllowed: true
  rollback:
    previousBaseline: V2.42
    rollbackCommit: <git-sha-of-previous-baseline>
    rollbackTag: architecture/v2.42-candidate
    rollbackGuide: governance/evidence/baseline-changes/baseline-change-record.yaml
    rollbackVerification: governance/evidence/rollback/baseline-rollback-verification.yaml
```

执行规则：

1. `documentVersion` 必须等于主文档版本、版本清单版本和审计导出版本。
2. `baselineId` 一经发布不得复用；同一 `baselineId` 不得指向不同 commit。
3. `releaseTag` 必须指向 `sourceCommit`，生产级基线必须使用签名 tag。
4. `releaseChannel=baseline` 或 `frozen` 时，必须有 `release-gate-decision.yaml`、基线生命周期状态机、基线验证环境锁、基线制品清单、基线就绪评分卡、基线例外总账、通知确认总账、回滚验证记录和审计导出清单。
5. `changeLevel=major` 或 `breaking` 时，必须引用 ADR、迁移计划、弃用策略和消费者影响分析。
6. `compatibilityWindow` 到期后，未迁移消费者必须转入例外、POA&M 或风险接受记录。
7. 回滚不能只写“回退上一版”，必须指向可 checkout 的 commit、tag、GitOps revision 或制品 digest。

可执行验收标准：

1. 任意基线都能从 `version-governance.yaml` 追溯到源 commit、release tag、版本清单、基线生命周期状态机、基线就绪评分卡、基线例外总账、通知确认总账、回滚验证记录、验证环境锁、基线制品清单和审计导出。
2. 任意冻结基线都能证明没有被直接修改；后续变更只能通过补丁或新基线替代。
3. 任意 breaking change 都能找到兼容窗口、消费者清单、迁移说明和回滚入口。
4. 任意 emergency patch 都能找到事故或安全编号、补丁范围、事后复盘和补齐证据。

### 10.10.9 基线发布证据包与版本漂移复核

`baseline-release-evidence.yaml` 是基线从 `candidate` 晋级到 `baseline` 或 `frozen` 的证据包。它不替代 `version-governance.yaml`，而是证明版本控制面声明的事实已经被验证。

```yaml
baselineReleaseEvidence:
  evidenceId: bre-20260602-mea-v243
  baselineId: mea-v2.43-20260602
  documentVersion: V2.43
  owner: architecture-governance-board
  promotion:
    fromChannel: candidate
    toChannel: baseline
    requestedBy: architecture-governance-board
    approvedBy:
      - platform-lead
      - security-lead
      - data-governance-lead
    decision: pass
    decidedAt: 2026-06-02T10:30:00+08:00
  immutableRefs:
    sourceCommit: <git-sha-of-baseline-commit>
    releaseTag: architecture/v2.43-candidate
    tagSignatureVerified: true
    auditExportDigest: sha256:<audit-export-digest>
    controlCoverageDigest: sha256:<control-coverage-digest>
    lifecycleStateMachineDigest: sha256:<baseline-lifecycle-state-machine-digest>
    artifactInventoryDigest: sha256:<baseline-artifact-inventory-digest>
    verificationLockDigest: sha256:<baseline-verification-lock-digest>
    readinessScorecardDigest: sha256:<baseline-readiness-scorecard-digest>
    exceptionLedgerDigest: sha256:<baseline-exception-ledger-digest>
    notificationLedgerDigest: sha256:<baseline-notification-ledger-digest>
    rollbackVerificationDigest: sha256:<baseline-rollback-verification-digest>
  invariants:
    documentVersionMatchesManifest: true
    controlCoverageMatchesManifest: true
    lifecycleTransitionAllowed: true
    artifactInventoryMatchesGitTree: true
    verificationLockMatchesRunner: true
    readinessScorecardPassesHardGates: true
    exceptionLedgerHasNoExpiredBlockingException: true
    notificationLedgerCompleteBeforeFreeze: true
    rollbackVerificationMatchesPreviousBaseline: true
    starterKitPairCountMatches: true
    forbiddenLocalAssetsAbsentFromRemote: true
    noLatestExternalStandardInGate: true
  driftReview:
    reviewedAt: 2026-06-02T10:00:00+08:00
    reviewer: architecture-governance-board
    driftStatus: none
    checkedRefs:
      - governance/control-plane/version-governance.yaml
      - governance/control-plane/standards-baseline.yaml
      - governance/control-plane/control-plane.yaml
      - governance/evidence/baselines/baseline-lifecycle-state-machine.yaml
      - governance/evidence/verification/baseline-verification-lock.yaml
      - governance/evidence/baselines/baseline-readiness-scorecard.yaml
      - governance/evidence/exceptions/baseline-exception-ledger.yaml
      - governance/evidence/baselines/baseline-artifact-inventory.yaml
      - governance/evidence/release-trains/baseline-release-train.yaml
      - governance/evidence/communications/baseline-notification-ledger.yaml
      - governance/evidence/rollback/baseline-rollback-verification.yaml
      - governance/evidence/conformance/baseline-conformance-claim.yaml
      - governance/evidence/audit-export/audit-export-manifest.yaml
    findings:
      critical: 0
      high: 0
      medium: 0
  freezeReview:
    eligibleForFrozen: false
    readinessScore: 96
    readinessLevel: ready-for-baseline
    openCriticalFindings: 0
    activeBlockingExceptions: 0
    expiredExceptions: 0
    missingRequiredAcknowledgements: 0
    activeNotificationObjections: 0
    openExceptions:
      blocking: 0
      expiringWithinDays: 14
  rollback:
    verified: true
    previousBaseline: V2.42
    rollbackTag: architecture/v2.42-candidate
    rollbackGuide: governance/evidence/baseline-changes/baseline-change-record.yaml
    rollbackVerification: governance/evidence/rollback/baseline-rollback-verification.yaml
  verification:
    commands:
      - make sync-doc-toc
      - make test
      - git diff --check
      - git ls-tree -r --name-only origin/develop -- docs/references/modern-enterprise-architecture-kit
    result: pass
```

晋级矩阵：

| 晋级路径 | 必须证明 | 阻断条件 |
| -------- | -------- | -------- |
| `draft -> candidate` | 版本号、变更摘要、影响面、索引同步和基础门禁通过 | 文档版本和索引不一致 |
| `candidate -> baseline` | `baseline-lifecycle-state-machine.yaml`、`baseline-release-evidence.yaml`、基线就绪评分卡、版本控制面、验证环境锁、审计导出、控制覆盖和 tag 验签通过 | 状态机未允许迁移、缺少证据包、就绪评分卡未通过、验证环境未锁定、tag 漂移、控制覆盖不一致 |
| `baseline -> frozen` | 状态机允许迁移、冻结复核、开放关键发现为 0、就绪评分达到 frozen 阈值、例外总账无过期阻断、独立回滚验证和审计导出摘要一致 | 状态机禁止迁移、仍有 critical/high 风险、就绪评分不足、证据过期、例外过期、阻断例外未关闭、回滚未验证 |
| `baseline -> emergency-patch` | 事故或安全编号、补丁范围、最小影响分析、补齐证据期限和复盘 owner | 无事故编号、补丁长期化、事后未补 ADR 或复盘 |

执行规则：

1. `baseline-release-evidence.yaml` 必须追加写入，不得覆盖历史基线证据。
2. `immutableRefs.sourceCommit`、`releaseTag`、生命周期状态机摘要、验证环境锁摘要、基线制品清单摘要、基线就绪评分卡摘要、基线例外总账摘要、审计导出摘要和控制覆盖摘要必须来自同一基线。
3. 任意禁推本地资产出现在远端树中，`forbiddenLocalAssetsAbsentFromRemote` 必须为 `false`，并阻断基线晋级。
4. `frozen` 晋级必须先完成漂移复核、基线就绪评分卡和基线例外总账复核；如果存在关键漂移、评分不足、过期例外或阻断例外，只能创建 POA&M 或风险接受，不能冻结。
5. 回滚验证必须指向 `baseline-rollback-verification.yaml`，并证明上一基线 tag、commit、GitOps revision、审计导出和烟测结果有效，不能只写自然语言说明。

可执行验收标准：

1. 任意基线晋级都能找到一份对应的 `baseline-release-evidence.yaml`。
2. 任意证据包都能证明版本清单、生命周期状态机、验证环境锁、基线制品清单、基线就绪评分卡、基线例外总账、控制覆盖、标准基线和审计导出摘要一致。
3. 任意冻结基线都能证明开放关键发现为 0、就绪评分达到 frozen 阈值、过期阻断例外为 0，且回滚路径已经验证。
4. 任意审计人员都能从证据包直接定位 source commit、release tag、验签结果和验证命令。

### 10.10.10 基线兼容性总账与消费者迁移闭环

`baseline-compatibility-ledger.yaml` 是版本控制面的消费者影响总账。它不替代单个 API、事件、数据产品或 AI 产品的兼容性报告，而是把这些报告汇总到基线级别，回答“谁会被这次基线影响、何时迁移、到期后如何治理”。

```yaml
baselineCompatibilityLedger:
  ledgerId: bcl-20260602-mea-v243
  baselineId: mea-v2.43-20260602
  documentVersion: V2.43
  owner: architecture-governance-board
  change:
    changeLevel: minor
    backwardCompatible: true
    compatibilityWindow: P90D
    deprecationDeadline: 2026-09-02
  impactedContracts:
    - contract: api:order-command:v2
      type: api
      owner: team-order
      compatibilityReport: governance/evidence/compatibility/order-command-api-v2.yaml
      breaking: false
    - contract: event:order-created:v3
      type: event
      owner: team-order
      compatibilityReport: governance/evidence/compatibility/order-created-event-v3.yaml
      breaking: false
  consumers:
    - consumer: customer-service-workbench
      owner: team-support
      impact: sdk-upgrade-required
      currentVersion: order-command:v1
      targetVersion: order-command:v2
      migrationStatus: in-progress
      dueDate: 2026-08-15
      evidence:
        - governance/evidence/compatibility/customer-service-workbench-migration.yaml
    - consumer: revenue-dashboard
      owner: team-revenue-data
      impact: no-change
      currentVersion: order-created:v2
      targetVersion: order-created:v3
      migrationStatus: not-required
      dueDate: null
  unresolved:
    count: 0
    blockers: []
  exceptions:
    allowed: true
    active:
      - id: ex-compat-2026-001
        consumer: legacy-erp-adapter
        expiresAt: 2026-07-15T23:59:59+08:00
        riskAcceptedBy: enterprise-architecture-lead
        poam: governance/evidence/poam/poam-record.yaml
  gateDecision:
    result: pass
    blockingUnmigratedConsumers: 0
    expiredExceptions: 0
    decisionRef: governance/control-plane/release-gate-decision.yaml
```

兼容状态只能使用以下值：

| 状态 | 含义 | 是否阻断 |
| ---- | ---- | -------- |
| `not-impacted` | 已证明不受影响 | 否 |
| `not-required` | 受影响但无需迁移动作 | 否 |
| `planned` | 已排期但未开始 | 视到期日而定 |
| `in-progress` | 正在迁移，有 owner 和证据 | 视到期日而定 |
| `completed` | 已完成迁移并有验证证据 | 否 |
| `exception` | 经批准暂缓迁移 | 例外过期后阻断 |
| `blocked` | 迁移被依赖、预算或技术问题阻塞 | 是 |
| `unknown` | 无法确认影响或 owner | 是 |

执行规则：

1. `Major`、`Breaking` 和任何带 `compatibilityWindow` 的基线，必须提供 `baseline-compatibility-ledger.yaml`。
2. 每个受影响契约必须链接对应的 API、事件、数据产品、AI 产品或平台兼容性报告。
3. 每个生产消费者必须有 owner、当前版本、目标版本、迁移状态、到期日和证据路径。
4. 到期后仍处于 `planned`、`in-progress`、`blocked` 或 `unknown` 的消费者必须转入例外、POA&M 或风险接受。
5. `unknown` consumer 不能进入 `baseline` 或 `frozen` 通道；必须先补 catalog、日志、网关、Schema Registry 或数据血缘证据。
6. 删除旧版本前必须证明生产流量、事件消费、数据血缘或模型调用已经归零，或有签署的风险接受记录。

可执行验收标准：

1. 任意 breaking change 都能从基线级总账追到具体消费者和兼容性报告。
2. 任意未迁移消费者都有到期时间、owner、例外或 POA&M。
3. 任意冻结基线都不存在 `unknown` 或过期未处理的消费者迁移状态。
4. 任意删除旧版本的动作都能证明无生产消费者，或有明确风险接受。

### 10.10.11 基线采纳总账与组织级版本落地

`baseline-adoption-ledger.yaml` 是企业级基线的组织采纳总账。它不证明“基线已经发布”，而是证明“哪些团队、系统、模板、环境和生产资产已经真正采用了这条基线”。

```yaml
baselineAdoptionLedger:
  ledgerId: bal-20260602-mea-v243
  baselineId: mea-v2.43-20260602
  documentVersion: V2.43
  owner: architecture-governance-board
  scope:
    requiredBy: 2026-10-01
    appliesTo:
      conformanceProfiles:
        - standard-prod
        - regulated-ai-prod
      gateLevels:
        - L2
        - L3
        - L4
      assetTypes:
        - domain
        - service
        - data-product
        - ai-product
        - platform-golden-path
        - gitops-environment
  summary:
    totalTargets: 4
    adopted: 2
    inProgress: 1
    exceptions: 1
    overdue: 0
    unknown: 0
  targets:
    - target: domain:order
      owner: team-order
      currentBaseline: V2.35
      targetBaseline: V2.43
      conformanceProfile: standard-prod
      gateLevel: L3
      adoptionStatus: in-progress
      dueDate: 2026-08-30
      evidence:
        - domains/order/domain.yaml
        - governance/evidence/conformance/order-domain-baseline-claim.yaml
        - governance/control-plane/version-governance.yaml
        - governance/evidence/control-assessments/order-domain-v243.yaml
    - target: ai-product:customer-service-agent
      owner: team-support-ai
      currentBaseline: V2.43
      targetBaseline: V2.43
      conformanceProfile: regulated-ai-prod
      gateLevel: L4
      adoptionStatus: adopted
      dueDate: 2026-07-15
      evidence:
        - ai/applications/customer-service-agent/ai-product.yaml
        - governance/evidence/conformance/customer-service-agent-baseline-claim.yaml
        - governance/evidence/ai/customer-service-agent-evidence.yaml
        - governance/control-plane/release-gate-decision.yaml
    - target: platform-golden-path:microservice
      owner: platform-team
      currentBaseline: V2.43
      targetBaseline: V2.43
      conformanceProfile: standard-prod
      gateLevel: L2
      adoptionStatus: adopted
      dueDate: 2026-07-01
      evidence:
        - platform/golden-paths/microservice/template.yaml
        - governance/evidence/conformance/microservice-golden-path-baseline-claim.yaml
        - governance/evidence/platform/microservice-golden-path-v243.yaml
  exceptions:
    active:
      - id: ex-adoption-2026-001
        target: service:legacy-billing-adapter
        reason: strangler migration still active
        expiresAt: 2026-09-15T23:59:59+08:00
        riskAcceptedBy: enterprise-architecture-lead
        poam: governance/evidence/poam/legacy-billing-adapter-poam.yaml
  gateDecision:
    result: conditional-pass
    blockingUnknownTargets: 0
    overdueL3L4Targets: 0
    expiredExceptions: 0
```

采纳状态只能使用以下值：

| 状态 | 含义 | 是否阻断 |
| ---- | ---- | -------- |
| `not-started` | 已识别目标但尚未启动采用 | 视截止日期和等级而定 |
| `in-progress` | 正在采用，有 owner、截止日期和证据 | 视截止日期和等级而定 |
| `adopted` | 已采用目标基线并通过对应门禁 | 否 |
| `exception` | 经批准暂缓采用 | 例外过期后阻断 |
| `blocked` | 采用被技术、预算、组织或迁移问题阻塞 | 是 |
| `overdue` | 超过截止日期仍未采用 | 对 L3/L4 阻断 |
| `unknown` | 无法确认当前基线或 owner | 是 |
| `not-applicable` | 明确不适用且有理由 | 否 |

执行规则：

1. 企业级 `baseline` 或 `frozen` 发布必须有采纳范围、采纳目标和采用截止日期。
2. L3 / L4 资产不得以 `unknown`、逾期 `in-progress` 或逾期 `not-started` 状态进入下一轮冻结基线。
3. 采纳证据必须来自 catalog、control assessment、scorecard、GitOps、模板版本或资产契约，不能只来自会议纪要。
4. 平台 Golden Path 采用必须证明模板版本、脚手架版本、CI 模板、policy bundle 和开发者门户入口一致。
5. 逾期目标必须转入例外、POA&M 或风险登记，并声明到期日和关闭条件。
6. 采纳总账必须进入季度复核；连续两次未采用的 L3/L4 目标必须升级给架构治理委员会。

可执行验收标准：

1. 任意企业基线都能列出应采用它的领域、平台、数据、AI、GitOps 和生产资产范围。
2. 任意目标资产都能证明当前基线、目标基线、owner、截止日期、采纳状态和证据路径。
3. 任意逾期或阻塞采纳都有例外、POA&M 或风险接受。
4. 任意冻结基线都不存在 L3/L4 资产的 `unknown` 或过期采纳状态。

### 10.10.12 基线支持矩阵与版本生命周期收口

`baseline-support-matrix.yaml` 是架构基线的生命周期支持矩阵。它不证明“新基线已经发布”，而是证明“旧基线还是否允许继续使用、还能获得什么类型的维护、何时必须迁移或退役”。

```yaml
baselineSupportMatrix:
  matrixId: bsm-20260602-mea-v243
  owner: architecture-governance-board
  currentBaseline: V2.43
  minimumAcceptedBaselines:
    L2: V2.31
    L3: V2.35
    L4: V2.43
  baselines:
    - version: V2.43
      baselineId: mea-v2.43-20260602
      channel: candidate
      supportState: active
      supportFrom: 2026-06-02
      supportUntil: 2026-12-31
      securityPatchUntil: 2027-03-31
      allowedForNewProjects: true
      allowedGateLevels:
        - L2
        - L3
        - L4
      requiredAdoptionLedger: governance/evidence/adoption/baseline-adoption-ledger.yaml
      requiredArtifactInventory: governance/evidence/baselines/baseline-artifact-inventory.yaml
      requiredVerificationLock: governance/evidence/verification/baseline-verification-lock.yaml
      requiredLifecycleStateMachine: governance/evidence/baselines/baseline-lifecycle-state-machine.yaml
      requiredReadinessScorecard: governance/evidence/baselines/baseline-readiness-scorecard.yaml
      requiredExceptionLedger: governance/evidence/exceptions/baseline-exception-ledger.yaml
      requiredRollbackVerification: governance/evidence/rollback/baseline-rollback-verification.yaml
    - version: V2.33
      baselineId: mea-v2.33-20260602
      channel: superseded
      supportState: maintenance
      supportFrom: 2026-06-02
      supportUntil: 2026-09-30
      securityPatchUntil: 2026-12-31
      allowedForNewProjects: false
      allowedGateLevels:
        - L2
      migrationTarget: V2.43
    - version: V2.31
      baselineId: mea-v2.31-20260602
      channel: superseded
      supportState: security-only
      supportFrom: 2026-06-02
      supportUntil: 2026-07-31
      securityPatchUntil: 2026-09-30
      allowedForNewProjects: false
      allowedGateLevels:
        - L2
      migrationTarget: V2.43
  exceptions:
    active:
      - id: ex-support-2026-001
        baseline: V2.30
        target: service:legacy-billing-adapter
        reason: strangler migration still active
        expiresAt: 2026-08-15T23:59:59+08:00
        riskAcceptedBy: enterprise-architecture-lead
        poam: governance/evidence/poam/legacy-billing-adapter-poam.yaml
  gates:
    blockNewProjectsOnUnsupportedBaseline: true
    blockL3L4BelowMinimum: true
    requireSecurityPatchForSecurityOnly: true
    blockEolBaselineInReleaseGate: true
```

支持状态只能使用以下值：

| 状态 | 含义 | 允许变更 |
| ---- | ---- | -------- |
| `active` | 当前推荐基线，可用于新项目和升级目标 | 功能、标准、控制项、安全补丁和勘误 |
| `maintenance` | 仍在维护，但不建议新项目采用 | 兼容性修复、安全补丁、关键勘误 |
| `security-only` | 只接受安全、合规和关键事故修复 | 安全补丁、监管要求、生产事故补丁 |
| `frozen` | 冻结为审计、招标或监管口径 | 勘误和紧急安全补丁，禁止语义变更 |
| `superseded` | 已被新基线替代 | 迁移说明、兼容性说明、风险接受 |
| `eol` | 生命周期结束 | 不允许继续发布，只允许迁移或退役 |

执行规则：

1. 新项目不得采用 `maintenance`、`security-only`、`superseded` 或 `eol` 基线。
2. L3 / L4 资产不得低于 `minimumAcceptedBaselines`，除非存在未过期例外、POA&M 和风险接受。
3. `security-only` 基线只能接受安全、合规和关键事故补丁，不得接收新功能、新标准或新平台能力。
4. `eol` 基线不能通过发布门禁；运行中资产只能执行迁移、降级、隔离或退役动作。
5. `frozen` 基线不得直接改核心语义；任何实质变更必须生成新基线并在支持矩阵中声明替代关系。
6. 支持矩阵必须在每次基线发布、冻结、紧急补丁和季度架构复核前更新。

可执行验收标准：

1. 任意历史基线都能查到支持状态、维护截止、安全补丁截止和迁移目标。
2. 任意 L3/L4 资产都能证明自己不低于最低可接受基线，或拥有未过期例外。
3. 任意新项目都不能从门禁中选择不再允许新建的旧基线。
4. 任意 EOL 基线都不能作为 release gate 的通过条件。

### 10.10.13 基线发布列车与版本节奏治理

`baseline-release-train.yaml` 是架构基线的发布日历和节奏控制文件。它不替代 `version-governance.yaml`，而是约束“什么时候可以进入候选、什么时候冻结、什么时候晋级、什么时候通知消费者、什么时候只能走紧急补丁”。

```yaml
baselineReleaseTrain:
  trainId: brt-2026-q3-enterprise-architecture
  owner: architecture-governance-board
  cadence: quarterly
  timezone: Asia/Shanghai
  currentBaseline: V2.43
  trainWindow:
    proposalCutoff: 2026-06-10
    candidateStart: 2026-06-17
    changeFreezeStart: 2026-06-24
    baselineDecision: 2026-07-01
    adoptionStart: 2026-07-02
    nextTrainOpens: 2026-09-01
  stages:
    - name: proposal
      allowedChangeLevels:
        - minor
        - major
        - breaking
      requiredEvidence:
        - baseline-change-record
        - architecture-decision-record
    - name: candidate
      allowedChangeLevels:
        - editorial
        - minor
      requiredEvidence:
        - version-governance
        - lifecycle-state-machine
        - verification-lock
        - artifact-inventory
        - readiness-scorecard
        - control-coverage
        - compatibility-ledger
        - exception-ledger
        - notification-ledger
        - rollback-verification
        - support-matrix
    - name: freeze
      allowedChangeLevels:
        - editorial
        - emergency-patch
      requiredEvidence:
        - lifecycle-state-machine
        - verification-lock
        - artifact-inventory
        - readiness-scorecard
        - baseline-release-evidence
        - exception-ledger
        - notification-ledger
        - rollback-verification
        - release-gate-decision
        - audit-export-manifest
    - name: baseline
      allowedChangeLevels:
        - emergency-patch
      requiredEvidence:
        - signed-tag
        - signature-receipt
        - adoption-ledger
  plannedBaselines:
    - version: V2.43
      baselineId: mea-v2.43-20260602
      releaseChannel: candidate
      targetChannel: baseline
      sourceCommit: <git-sha-of-baseline-commit>
      releaseTag: architecture/v2.43-candidate
      requiredLedgers:
        - governance/evidence/baselines/baseline-lifecycle-state-machine.yaml
        - governance/evidence/verification/baseline-verification-lock.yaml
        - governance/evidence/baselines/baseline-artifact-inventory.yaml
        - governance/evidence/baselines/baseline-readiness-scorecard.yaml
        - governance/evidence/compatibility/baseline-compatibility-ledger.yaml
        - governance/evidence/adoption/baseline-adoption-ledger.yaml
        - governance/evidence/support/baseline-support-matrix.yaml
        - governance/evidence/exceptions/baseline-exception-ledger.yaml
        - governance/evidence/communications/baseline-notification-ledger.yaml
        - governance/evidence/rollback/baseline-rollback-verification.yaml
        - governance/evidence/conformance/baseline-conformance-claim.yaml
      notification:
        firstNotice: 2026-06-10
        freezeNotice: 2026-06-24
        decisionNotice: 2026-07-01
        channels:
          - architecture-portal
          - platform-developer-portal
          - engineering-leads-mailing-list
      gateDecision: governance/control-plane/release-gate-decision.yaml
  blackoutWindows:
    - from: 2026-06-29T00:00:00+08:00
      to: 2026-07-01T23:59:59+08:00
      reason: baseline-decision-window
      blockNonEmergency: true
  emergencyPatch:
    allowed: true
    requires:
      - incidentId
      - securityOrComplianceJustification
      - minimalScope
      - rollbackPlan
      - postIncidentReviewDueDate
    maxEvidenceBackfillDays: 5
  gates:
    blockOutOfTrainBaseline: true
    blockFreezeWindowSemanticChange: true
    blockBlackoutNonEmergencyChange: true
    requireReadinessScorecardBeforeBaseline: true
    blockBaselineOnReadinessScoreFailure: true
    requireConsumerNoticeBeforeFreeze: true
    requireNotificationLedgerBeforeFreeze: true
    requireExceptionLedgerBeforeFreeze: true
    blockFreezeOnExpiredException: true
    requireRollbackVerificationBeforeBaseline: true
    blockFreezeOnMissingRequiredAck: true
```

发布列车阶段语义：

| 阶段 | 含义 | 允许动作 |
| ---- | ---- | -------- |
| `proposal` | 进入本轮列车的提案收集期 | 新增变更提案、ADR、影响分析和消费者识别 |
| `candidate` | 候选基线成形期 | 小范围补齐证据、修正示例、修复兼容性差距 |
| `freeze` | 冻结复核期 | 只允许勘误、门禁修复和紧急补丁，不允许语义扩张 |
| `baseline` | 正式基线放行期 | 打签名 tag、导出审计包、启动采纳总账 |
| `emergency-patch` | 安全、合规或生产事故补丁通道 | 最小范围补丁，事后补齐 ADR、复盘和证据 |

执行规则：

1. 企业级基线不得绕过发布列车直接从草案进入 `baseline` 或 `frozen`。
2. `changeFreezeStart` 之后禁止合入改变语义、职责、门禁或目录真相源的变更，除非走 `emergency-patch`。
3. 黑窗期间只能发布安全、合规或生产事故补丁；普通优化、文档扩展和新控制项必须进入下一轮列车。
4. 进入冻结前必须完成消费者通知，生成 `baseline-notification-ledger.yaml`，并确保 `baseline-compatibility-ledger.yaml` 没有 `unknown` 或过期阻塞项。
5. 进入正式基线前必须完成 `baseline-verification-lock.yaml`、`baseline-artifact-inventory.yaml`、`baseline-readiness-scorecard.yaml`、`baseline-exception-ledger.yaml`、`baseline-notification-ledger.yaml`、`baseline-rollback-verification.yaml`、`baseline-release-evidence.yaml`、`baseline-support-matrix.yaml`、审计导出和签名验签回执。
6. 紧急补丁必须在 `maxEvidenceBackfillDays` 内补齐复盘、ADR 或基线变更记录，不能成为长期发布通道。

可执行验收标准：

1. 任意企业基线都能追溯到所属发布列车、候选窗口、冻结窗口和晋级日期。
2. 任意冻结期后的语义变更都有紧急补丁理由、事故编号、回滚计划和补证截止。
3. 任意黑窗内的变更都能证明是安全、合规或生产事故补丁。
4. 任意消费者都能证明在冻结前收到通知、完成影响确认，或有明确的例外和风险接受记录。
5. 任意正式基线都能证明上一基线可检出、GitOps revision 可恢复、审计导出可回放并通过最小烟测。

### 10.10.14 资产级基线符合性声明

`baseline-conformance-claim.yaml` 是单个资产对企业架构基线的自声明。它不替代组织级 `baseline-adoption-ledger.yaml`，而是让采纳总账有资产侧证据来源，避免中央台账靠人工手填。

```yaml
baselineConformanceClaim:
  claimId: bcc-20260602-order-command-service-v243
  asset:
    id: service:order-command-service
    type: service
    domain: order
    owner: team-order
    sourceRoot: domains/order/services/order-command-service
    catalogRef: catalog/components/order-command-service.yaml
  claimedBaseline:
    version: V2.43
    baselineId: mea-v2.43-20260602
    releaseTrain: governance/evidence/release-trains/baseline-release-train.yaml
    supportMatrix: governance/evidence/support/baseline-support-matrix.yaml
    lifecycleStateMachine: governance/evidence/baselines/baseline-lifecycle-state-machine.yaml
    artifactInventory: governance/evidence/baselines/baseline-artifact-inventory.yaml
    verificationLock: governance/evidence/verification/baseline-verification-lock.yaml
    readinessScorecard: governance/evidence/baselines/baseline-readiness-scorecard.yaml
    exceptionLedger: governance/evidence/exceptions/baseline-exception-ledger.yaml
    rollbackVerification: governance/evidence/rollback/baseline-rollback-verification.yaml
  conformance:
    profile: standard-prod
    gateLevel: L3
    claimStatus: conformant
    claimedAt: 2026-07-02T10:00:00+08:00
    expiresAt: 2026-10-02T23:59:59+08:00
    signedBy:
      - team-order-tech-lead
      - platform-governance-reviewer
  evidence:
    contracts:
      - domains/order/services/order-command-service/service.yaml
      - contracts/apis/order-command.openapi.yaml
      - contracts/events/order-created.asyncapi.yaml
    runtime:
      - infra/gitops/environments/prod/order/order-command-service/kustomization.yaml
      - governance/evidence/drift/order-command-service-drift.yaml
    controls:
      - governance/evidence/control-assessments/order-command-service-v243.yaml
      - governance/control-plane/release-gate-decision.yaml
    supplyChain:
      - governance/evidence/supply-chain/order-command-service-attestation.yaml
  exceptions:
    active: []
  rollup:
    adoptionLedger: governance/evidence/adoption/baseline-adoption-ledger.yaml
    rollupStatus: included
    lastReconciledAt: 2026-07-02T11:00:00+08:00
```

声明状态只能使用以下值：

| 状态 | 含义 | 是否计入采纳 |
| ---- | ---- | ------------ |
| `conformant` | 资产已经满足声明基线和门禁等级 | 是 |
| `conditional` | 资产有未关闭例外，但已被风险接受 | 条件计入 |
| `non-conformant` | 资产未满足声明基线或关键证据缺失 | 否 |
| `expired` | 声明过期，必须重新评估 | 否 |
| `not-applicable` | 资产明确不适用该基线，且有理由 | 不计入分母 |

执行规则：

1. L3 / L4 资产不得只出现在采纳总账中，必须有资产侧 `baseline-conformance-claim.yaml`。
2. 符合性声明必须绑定 `baselineId`、`releaseTrain`、`supportMatrix`、catalog 指针和证据路径。
3. `claimStatus=conformant` 时不得存在过期例外、缺失控制评估或低于最低可接受基线的版本。
4. `claimStatus=conditional` 必须引用未过期例外、POA&M 或风险接受记录，并声明关闭日期。
5. 声明过期后不得继续在 `baseline-adoption-ledger.yaml` 中计为 `adopted`。
6. 采纳总账必须能从每个目标资产回查到对应的符合性声明，符合性声明也必须能回写自己的 rollup 状态。

可执行验收标准：

1. 任意 L3/L4 资产都能找到一份未过期的基线符合性声明。
2. 任意采纳总账中的 `adopted` 目标都能追溯到资产侧 `conformant` 声明。
3. 任意 `conditional` 声明都有例外、POA&M 或风险接受，并有关闭日期。
4. 任意低于支持矩阵最低可接受基线的资产都不能声明为 `conformant`。

### 10.10.15 基线制品清单与可复现冻结

`baseline-artifact-inventory.yaml` 是企业架构基线的源制品物料清单。它不替代 `audit-export-manifest.yaml`，而是先回答“这一版基线由哪些源文件和模板构成”；审计导出清单再回答“这些源制品被导出了哪些交付包”。

```yaml
baselineArtifactInventory:
  inventoryId: bai-20260602-mea-v243
  baselineId: mea-v2.43-20260602
  documentVersion: V2.43
  owner: architecture-governance-board
  sourceCommit: <git-sha-of-baseline-commit>
  releaseTag: architecture/v2.43-candidate
  generatedAt: 2026-06-02T12:00:00+08:00
  digestAlgorithm: sha256
  scope:
    requiredArtifactTypes:
      - document
      - schema
      - example
      - control
      - evidence-template
      - validation-command
      - generated-output
      - external-reference
    excludePatterns:
      - build/**
      - .git/**
      - docs/references/modern-enterprise-architecture-kit/**
      - docs/references/modern-enterprise-architecture-controls.json
      - docs/references/modern-enterprise-architecture-version.json
  artifacts:
    - path: docs/references/modern-enterprise-architecture-template.md
      type: document
      required: true
      owner: architecture-governance-board
      digest: sha256:<document-digest>
      signed: true
      exportedTo:
        - build/modern-enterprise-architecture-audit/audit-export.md
    - path: governance/control-plane/version-governance.yaml
      type: control
      required: true
      owner: architecture-governance-board
      digest: sha256:<version-governance-digest>
      signed: true
      exportedTo:
        - build/modern-enterprise-architecture-audit/audit-export.json
    - path: governance/evidence/baselines/baseline-lifecycle-state-machine.yaml
      type: evidence-template
      required: true
      owner: architecture-governance-board
      digest: sha256:<lifecycle-state-machine-digest>
      signed: true
      exportedTo:
        - build/modern-enterprise-architecture-audit/audit-export.json
    - path: governance/evidence/verification/baseline-verification-lock.yaml
      type: control
      required: true
      owner: architecture-governance-board
      digest: sha256:<verification-lock-digest>
      signed: true
      exportedTo:
        - build/modern-enterprise-architecture-audit/audit-export.json
    - path: governance/evidence/rollback/baseline-rollback-verification.yaml
      type: evidence-template
      required: true
      owner: architecture-governance-board
      digest: sha256:<rollback-verification-digest>
      signed: true
      exportedTo:
        - build/modern-enterprise-architecture-audit/audit-export.json
    - path: governance/evidence/baselines/baseline-readiness-scorecard.yaml
      type: evidence-template
      required: true
      owner: architecture-governance-board
      digest: sha256:<readiness-scorecard-digest>
      signed: true
      exportedTo:
        - build/modern-enterprise-architecture-audit/audit-export.json
    - path: governance/evidence/exceptions/baseline-exception-ledger.yaml
      type: evidence-template
      required: true
      owner: architecture-governance-board
      digest: sha256:<exception-ledger-digest>
      signed: true
      exportedTo:
        - build/modern-enterprise-architecture-audit/audit-export.json
    - path: governance/evidence/conformance/baseline-conformance-claim.yaml
      type: evidence-template
      required: true
      owner: architecture-governance-board
      digest: sha256:<conformance-claim-digest>
      signed: true
      exportedTo:
        - build/modern-enterprise-architecture-audit/audit-export.json
  generatedOutputs:
    - path: build/modern-enterprise-architecture-audit/audit-export.json
      digest: sha256:<audit-export-json-digest>
      generatedBy: 审计导出命令
      sourceArtifacts:
        - docs/references/modern-enterprise-architecture-template.md
        - governance/control-plane/version-governance.yaml
  externalReferences:
    - name: SLSA v1.2
      lockedVersion: v1.2
      adoptionLevel: enforce
      referenceDigest: sha256:<reference-snapshot-digest>
  gates:
    requiredArtifactsPresent: true
    artifactDigestsMatchGitTree: true
    noUndeclaredRequiredArtifacts: true
    generatedOutputsMatchSources: true
    signaturesVerified: true
```

制品类型只能使用以下值：

| 类型 | 含义 | 典型位置 |
| ---- | ---- | -------- |
| `document` | 人类可读基线正文和索引 | `docs/` |
| `schema` | 机器可读契约约束 | starter kit schema |
| `example` | 可执行或可校验示例 | starter kit example |
| `control` | 控制面、控制覆盖或门禁决策 | `governance/control-plane/` |
| `evidence-template` | 审计、评估、例外、采纳、符合性或发布证据模板 | `governance/evidence/` |
| `validation-command` | 生成或校验基线的命令声明 | Makefile、脚本、runbook |
| `generated-output` | 由命令生成的审计导出或完整性输出 | `build/` |
| `external-reference` | 锁定版本的外部标准或参考资料快照 | 标准基线、ADR、引用清单 |

执行规则：

1. 企业级 `baseline`、`frozen` 和正式审计导出必须有基线制品清单。
2. 清单必须绑定 `baselineId`、`sourceCommit`、`releaseTag`、摘要算法和生成时间。
3. 所有必需源制品必须有路径、类型、owner、摘要、必需性和导出关系。
4. `required=true` 制品缺失、摘要漂移或 owner 缺失时，不得晋级到 `baseline` 或 `frozen`。
5. 未登记但被审计导出引用的源制品必须阻断导出，除非明确列入允许的 exclude pattern。
6. 本地禁推资产可以存在于 exclude pattern，但不得进入远端树、源制品清单、审计导出包或签名 payload。
7. 生成物必须能反向追溯到源制品集合；源制品变更后必须重新生成导出包、完整性清单和签名策略。

可执行验收标准：

1. 任意基线都能列出本次发布包含的源文档、schema、示例、控制项、证据模板、脚本、生成物和外部引用。
2. 任意审计导出包都能从生成物摘要反查到源制品摘要和生成命令。
3. 任意必需制品摘要漂移、缺失或未签名时，基线晋级会被阻断。
4. 任意本地禁推资产都能证明不在远端树、不在基线制品清单、不在导出包、不在签名 payload。

### 10.10.16 基线验证环境锁定

`baseline-verification-lock.yaml` 是企业架构基线的验证环境锁文件。它不替代 `Makefile`、CI 配置或脚本，而是把“用什么环境、什么命令、什么工具版本验证当前基线”固定成可审计证据，避免校验器或 runner 漂移导致同一基线结果不一致。

```yaml
baselineVerificationLock:
  lockId: bvl-20260602-mea-v243
  baselineId: mea-v2.43-20260602
  documentVersion: V2.43
  owner: architecture-governance-board
  sourceCommit: <git-sha-of-baseline-commit>
  releaseTag: architecture/v2.43-candidate
  generatedAt: 2026-06-02T12:15:00+08:00
  runner:
    type: container
    image: registry.company.com/platform/architecture-baseline-runner@sha256:<runner-image-digest>
    os: ubuntu-24.04
    architecture: amd64
    networkPolicy: no-unpinned-downloads
  commands:
    - name: docs-toc
      command: make sync-doc-toc
      required: true
      expectedResult: pass
    - name: repo-test
      command: make test
      required: true
      expectedResult: pass
    - name: whitespace
      command: git diff --check
      required: true
      expectedResult: pass
    - name: forbidden-assets
      command: git ls-tree -r --name-only origin/develop -- docs/references/modern-enterprise-architecture-kit
      required: true
      expectedResult: empty
  tools:
    markdownlint:
      version: 0.48.0
      source: npm
      digest: sha256:<markdownlint-package-digest>
    python:
      version: 3.12.x
      source: runner-image
    jsonSchemaValidator:
      name: ajv
      version: 8.x
      digest: sha256:<validator-digest>
    policyEngines:
      - name: opa
        version: 1.x
        bundleDigest: sha256:<opa-policy-bundle-digest>
      - name: kyverno
        version: 1.x
        bundleDigest: sha256:<kyverno-policy-bundle-digest>
    signing:
      cosignVersion: 2.x
      certificateIdentity: architecture-release-bot
      transparencyLog: rekor
  inputs:
    lifecycleStateMachine: governance/evidence/baselines/baseline-lifecycle-state-machine.yaml
    artifactInventory: governance/evidence/baselines/baseline-artifact-inventory.yaml
    readinessScorecard: governance/evidence/baselines/baseline-readiness-scorecard.yaml
    exceptionLedger: governance/evidence/exceptions/baseline-exception-ledger.yaml
    standardsBaseline: governance/control-plane/standards-baseline.yaml
    controlCoverage: governance/control-plane/control-coverage.yaml
  outputs:
    auditExport:
      path: build/modern-enterprise-architecture-audit/audit-export.json
      generatedBy: 审计导出命令
    integrity:
      path: build/modern-enterprise-architecture-audit/audit-export-integrity.json
    provenance:
      path: build/modern-enterprise-architecture-audit/audit-export-provenance.json
  gates:
    runnerImagePinnedByDigest: true
    noUnpinnedToolDownload: true
    toolVersionsLocked: true
    policyBundlesPinned: true
    validatorVersionsLocked: true
    signingToolsLocked: true
```

锁定对象至少包括：

| 对象 | 最低要求 | 阻断条件 |
| ---- | -------- | -------- |
| Runner | 使用不可变镜像 digest 或等价 runner 快照 | 只写 `latest`、OS 版本不明、架构不明 |
| 命令 | 列出命令、是否必需、预期结果和输出路径 | 关键命令只在文档正文出现，锁文件没有记录 |
| 工具 | 记录名称、版本、来源和摘要 | 校验器、签名工具或策略引擎未固定版本 |
| 策略包 | 记录 bundle digest、适用范围和生效时间 | OPA / Kyverno / Cedar 策略包漂移 |
| Schema validator | 记录 validator 名称、版本和行为模式 | 不同 validator 对同一 schema 行为不一致 |
| 签名验签工具 | 记录版本、身份、证书策略和透明日志要求 | 验签工具或证书身份不可复现 |

执行规则：

1. 企业级 `baseline`、`frozen` 和正式审计导出必须有验证环境锁。
2. `baseline-verification-lock.yaml` 必须绑定 `baselineId`、`sourceCommit`、`releaseTag` 和 `baseline-artifact-inventory.yaml`。
3. 任何验证命令、runner 镜像、策略包、schema validator 或签名工具升级，都必须形成基线变更记录或 ADR。
4. 锁文件中的 runner、工具、策略包和 validator 不得使用 `latest`、浮动主版本或未固定来源。
5. 审计导出、完整性清单和 provenance 必须记录使用的验证锁摘要。
6. 如果当前环境无法复现验证锁，基线只能停留在 `candidate`，不得晋级到 `baseline` 或 `frozen`。

可执行验收标准：

1. 任意基线都能证明自己由哪套 runner、命令、工具版本、策略包和 validator 校验。
2. 任意验证失败都能判断是源制品变化、工具链变化、runner 变化还是策略包变化。
3. 任意审计导出都能追溯到验证锁摘要，证明生成环境没有漂移。
4. 任意工具链升级都能找到影响分析、验证结果、回滚路径和新的锁文件。

### 10.10.17 基线通知确认总账

`baseline-notification-ledger.yaml` 是企业架构基线发布前的通知确认总账。它不替代邮件、IM、门户公告或会议纪要，而是把这些通知行为统一沉淀为可审计证据，证明受影响 owner 在冻结前已经收到通知、理解影响、确认迁移责任，或者已经提出异议并进入例外、POA&M 或风险接受。

```yaml
baselineNotificationLedger:
  ledgerId: bnl-20260602-mea-v243
  baselineId: mea-v2.43-20260602
  documentVersion: V2.43
  owner: architecture-governance-board
  releaseTrain: governance/evidence/release-trains/baseline-release-train.yaml
  compatibilityLedger: governance/evidence/compatibility/baseline-compatibility-ledger.yaml
  adoptionLedger: governance/evidence/adoption/baseline-adoption-ledger.yaml
  exceptionLedger: governance/evidence/exceptions/baseline-exception-ledger.yaml
  notificationWindow:
    firstNoticeAt: 2026-06-10T09:00:00+08:00
    freezeNoticeAt: 2026-06-24T09:00:00+08:00
    acknowledgementDueAt: 2026-06-24T18:00:00+08:00
    baselineDecisionAt: 2026-07-01T10:00:00+08:00
  targetAudience:
    - audienceId: domain-order-owner
      ownerType: domain-owner
      required: true
      team: team-order
      contact: order-tech-lead
      impactedAssets:
        - service:order-command-service
        - data-product:order-facts
      impactSources:
        - governance/evidence/compatibility/baseline-compatibility-ledger.yaml
        - governance/evidence/adoption/baseline-adoption-ledger.yaml
      expectedAckBy: 2026-06-24T18:00:00+08:00
    - audienceId: platform-gitops-owner
      ownerType: platform-owner
      required: true
      team: platform-runtime
      contact: gitops-platform-lead
      impactedAssets:
        - platform-capability:gitops-runtime
      expectedAckBy: 2026-06-24T18:00:00+08:00
  notifications:
    - noticeId: notice-first-20260610
      noticeType: first-notice
      sentAt: 2026-06-10T09:00:00+08:00
      sentBy: architecture-release-bot
      contentDigest: sha256:<release-note-digest>
      channels:
        - architecture-portal
        - platform-developer-portal
        - engineering-leads-mailing-list
      recipients:
        - audienceId: domain-order-owner
          deliveryStatus: delivered
          deliveredAt: 2026-06-10T09:01:00+08:00
          acknowledgementStatus: acknowledged
          acknowledgedBy: order-tech-lead
          acknowledgedAt: 2026-06-10T11:20:00+08:00
          impactAccepted: true
          objections: []
        - audienceId: platform-gitops-owner
          deliveryStatus: delivered
          deliveredAt: 2026-06-10T09:02:00+08:00
          acknowledgementStatus: acknowledged
          acknowledgedBy: gitops-platform-lead
          acknowledgedAt: 2026-06-10T12:05:00+08:00
          impactAccepted: true
          objections: []
    - noticeId: notice-freeze-20260624
      noticeType: freeze-notice
      sentAt: 2026-06-24T09:00:00+08:00
      sentBy: architecture-release-bot
      contentDigest: sha256:<freeze-note-digest>
      recipients:
        - audienceId: domain-order-owner
          deliveryStatus: delivered
          acknowledgementStatus: acknowledged
          acknowledgedBy: order-tech-lead
          acknowledgedAt: 2026-06-24T11:00:00+08:00
          impactAccepted: true
          objections: []
  objections:
    active: []
    resolved:
      - objectionId: obj-20260610-001
        raisedBy: data-platform-owner
        raisedAt: 2026-06-10T15:00:00+08:00
        reason: data-product lineage rule needs migration sample
        resolution: migration sample added before freeze
        resolvedAt: 2026-06-18T17:00:00+08:00
        resolvedBy: architecture-governance-board
  exceptions:
    active: []
  summary:
    requiredRecipients: 2
    delivered: 2
    acknowledged: 2
    missingAcknowledgements: 0
    activeObjections: 0
    activeExceptions: 0
    readyForFreeze: true
  gates:
    blockFreezeOnMissingRequiredAck: true
    blockFreezeOnFailedDelivery: true
    blockBaselineOnActiveObjection: true
    requireExceptionForWaivedAck: true
    requireContentDigestForEachNotice: true
```

确认状态只能使用以下值：

| 状态 | 含义 | 是否阻断 |
| ---- | ---- | -------- |
| `pending` | 已识别为通知对象，但尚未发送或尚无送达证据 | 是 |
| `delivered` | 通知已送达，但尚未完成影响确认 | 关键对象阻断 |
| `acknowledged` | 已确认收到并理解影响 | 否 |
| `objected` | 已提出异议或风险问题 | 是，直到关闭或风险接受 |
| `waived` | 确认要求被批准豁免 | 不阻断，但必须有例外和到期日 |
| `failed` | 通知投递失败 | 是 |
| `expired` | 超过确认截止时间仍未确认 | 是 |

执行规则：

1. `targetAudience` 必须来自 `baseline-compatibility-ledger.yaml`、`baseline-adoption-ledger.yaml`、catalog owner、GitOps 环境 owner 和安全/审计相关方，不能只手工列邮件名单。
2. 每条通知必须记录 `noticeType`、`sentAt`、`channels`、`contentDigest` 和 recipients；没有内容摘要的通知不能作为冻结证据。
3. `required=true` 的对象必须在 `acknowledgementDueAt` 前达到 `acknowledged`，除非存在未过期例外、POA&M 或风险接受。
4. 任意 `objected` 状态必须进入 `objections`，并在冻结前关闭、转例外或进入风险接受；不能用会议口头结论覆盖异议。
5. 任意 `failed` 或 `expired` 状态必须有补发、升级通知或例外审批；关键 owner 未确认时不得进入 `freeze`。
6. 发布证据包必须记录 `baseline-notification-ledger.yaml` 的摘要，证明冻结复核使用的是同一份通知确认总账。

可执行验收标准：

1. 任意企业级基线都能列出所有必须通知和必须确认的领域、平台、数据、AI、GitOps、安全和审计对象。
2. 任意通知都能证明发送时间、渠道、内容摘要、送达结果和确认人。
3. 任意未确认对象都能证明补发、例外、POA&M 或风险接受，而不是停留在 unknown。
4. 任意冻结基线都能证明 `missingAcknowledgements=0` 且 `activeObjections=0`，或存在明确的风险接受记录。

### 10.10.18 基线回滚验证记录

`baseline-rollback-verification.yaml` 是企业架构基线从候选进入正式基线前的回滚验证记录。它不替代回滚计划、Git tag、GitOps 历史或审计导出包，而是把这些入口做一次实际验证，并把结果固化为可审计证据。

```yaml
baselineRollbackVerification:
  verificationId: brv-20260602-mea-v243
  baselineId: mea-v2.43-20260602
  documentVersion: V2.43
  owner: architecture-governance-board
  currentBaseline:
    version: V2.43
    releaseTag: architecture/v2.43-candidate
    sourceCommit: <git-sha-of-baseline-commit>
    releaseEvidence: governance/evidence/baselines/baseline-release-evidence.yaml
  rollbackTarget:
    version: V2.42
    baselineId: mea-v2.42-20260602
    releaseTag: architecture/v2.42-candidate
    sourceCommit: <git-sha-of-previous-baseline>
    supportState: active
    supportMatrix: governance/evidence/support/baseline-support-matrix.yaml
  verificationWindow:
    verifiedAt: 2026-06-02T13:00:00+08:00
    expiresAt: 2026-07-02T23:59:59+08:00
    verifiedBy:
      - architecture-release-bot
      - platform-sre-reviewer
  checks:
    - checkId: git-tag-checkout
      command: git checkout architecture/v2.41-candidate
      expectedResult: pass
      result: pass
      evidenceDigest: sha256:<git-checkout-log-digest>
    - checkId: audit-export-restore
      command: 审计导出命令
      expectedResult: pass
      result: pass
      evidenceDigest: sha256:<audit-export-restore-digest>
    - checkId: gitops-revision-restore
      environment: staging
      targetRevision: <gitops-revision-of-previous-baseline>
      expectedResult: synced
      result: synced
      evidenceDigest: sha256:<gitops-restore-log-digest>
    - checkId: smoke-validation
      target: baseline-reference-stack
      command: make test
      expectedResult: pass
      result: pass
      evidenceDigest: sha256:<smoke-test-log-digest>
  recoveryResult:
    result: pass
    recoveryTimeMinutes: 18
    dataLossObserved: false
    blockingFailures: 0
    warnings: 0
  artifacts:
    rollbackGuide: governance/evidence/baseline-changes/baseline-change-record.yaml
    releaseEvidence: governance/evidence/baselines/baseline-release-evidence.yaml
    lifecycleStateMachine: governance/evidence/baselines/baseline-lifecycle-state-machine.yaml
    artifactInventory: governance/evidence/baselines/baseline-artifact-inventory.yaml
    verificationLock: governance/evidence/verification/baseline-verification-lock.yaml
    readinessScorecard: governance/evidence/baselines/baseline-readiness-scorecard.yaml
    exceptionLedger: governance/evidence/exceptions/baseline-exception-ledger.yaml
    auditExportManifest: governance/evidence/audit-export/audit-export-manifest.yaml
  gates:
    blockBaselineIfRollbackTargetMissing: true
    blockFrozenIfVerificationExpired: true
    requireGitopsRevisionForRuntimeRollback: true
    requireAuditExportRollbackEvidence: true
    requireSmokeValidationForReferenceStack: true
```

验证状态只能使用以下值：

| 状态 | 含义 | 是否阻断 |
| ---- | ---- | -------- |
| `pass` | 检查项按预期完成，证据摘要已记录 | 否 |
| `fail` | 检查项执行失败或结果不符合预期 | 是 |
| `skipped` | 因明确范围不适用而跳过 | 条件阻断，必须说明理由和批准人 |
| `not-applicable` | 当前基线没有对应运行面或制品类型 | 否，但必须有范围说明 |
| `expired` | 验证窗口已过期，需要重新执行 | 是 |
| `blocked` | 缺少前置制品、权限或环境，无法执行验证 | 是 |

执行规则：

1. `baseline-rollback-verification.yaml` 必须绑定当前基线和上一基线的 `baselineId`、`releaseTag`、`sourceCommit` 和支持状态。
2. 回滚目标必须在支持矩阵中处于 `active`、`maintenance`、`security-only` 或 `frozen`，不得指向 `eol` 基线。
3. Git 回滚必须证明上一基线 tag 或 commit 可检出；GitOps 回滚必须证明目标 revision 存在并可同步。
4. 审计导出恢复必须证明上一基线仍能生成或读取对应导出包，且摘要能与历史证据对上。
5. 参考栈烟测必须覆盖文档门禁、starter kit 校验、审计导出门禁和至少一个 GitOps 恢复验证。
6. `verificationWindow.expiresAt` 过期后，基线不得晋级到 `frozen`，必须重新生成回滚验证记录。
7. 任意 `fail`、`expired` 或 `blocked` 必须进入 POA&M、风险登记或 release gate 阻断，不能被发布证据包覆盖。

可执行验收标准：

1. 任意正式基线都能找到一份未过期的 `baseline-rollback-verification.yaml`。
2. 任意回滚验证都能证明上一基线 tag/commit 可检出，并能定位 GitOps revision 或明确声明不适用。
3. 任意审计人员都能从记录中看到恢复命令、预期结果、实际结果、证据摘要和验证窗口。
4. 任意失败的回滚验证都会阻断 `baseline` 或 `frozen` 晋级，直到有修复证据、例外审批或风险接受。

### 10.10.19 基线例外总账

`baseline-exception-ledger.yaml` 是企业架构基线级别的例外聚合总账。它不替代单个控制项、单个资产或单个策略的
`policy-exception.yaml`，而是把分散在兼容性、采纳、支持矩阵、通知确认、回滚验证、门禁决策、执行控制面、风险登记和
POA&M 中的例外统一收敛到同一份基线证据，回答“哪些例外还有效、哪些已经过期、哪些会阻断冻结、谁接受风险、何时关闭”。

```yaml
baselineExceptionLedger:
  ledgerId: bel-20260602-mea-v243
  baselineId: mea-v2.43-20260602
  documentVersion: V2.43
  owner: architecture-governance-board
  generatedAt: 2026-06-02T13:30:00+08:00
  linkedEvidence:
    versionGovernance: governance/control-plane/version-governance.yaml
    lifecycleStateMachine: governance/evidence/baselines/baseline-lifecycle-state-machine.yaml
    releaseGateDecision: governance/control-plane/release-gate-decision.yaml
    controlPlane: governance/control-plane/control-plane.yaml
    compatibilityLedger: governance/evidence/compatibility/baseline-compatibility-ledger.yaml
    adoptionLedger: governance/evidence/adoption/baseline-adoption-ledger.yaml
    supportMatrix: governance/evidence/support/baseline-support-matrix.yaml
    releaseTrain: governance/evidence/release-trains/baseline-release-train.yaml
    notificationLedger: governance/evidence/communications/baseline-notification-ledger.yaml
    rollbackVerification: governance/evidence/rollback/baseline-rollback-verification.yaml
    conformanceClaims: governance/evidence/conformance/baseline-conformance-claim.yaml
    riskRegister: governance/evidence/risk/risk-register.yaml
    poamRegister: governance/evidence/poam/poam-record.yaml
  exceptionPolicy:
    defaultMaxAgeDays: 90
    blockExpiredExceptions: true
    blockFrozenOnBlockingException: true
    blockFrozenOnHighResidualRisk: true
    requireOwnerForEveryException: true
    requirePoamForBlockingException: true
    requireRiskAcceptanceForConditionalPass: true
    requireCloseEvidenceForClosedException: true
  exceptions:
    active:
      - exceptionId: ex-baseline-2026-001
        source: baseline-adoption-ledger
        sourceRef: governance/evidence/adoption/baseline-adoption-ledger.yaml
        affectedAsset: service:legacy-billing-adapter
        controlIds:
          - MEA-VERSION-ADOPTION
          - MEA-BASELINE-SUPPORT
        severity: medium
        residualRisk: low
        gateImpact: conditional-pass
        owner: legacy-platform-owner
        reason: strangler migration still active
        openedAt: 2026-06-02T10:00:00+08:00
        expiresAt: 2026-09-15T23:59:59+08:00
        riskAcceptedBy: enterprise-architecture-lead
        riskAcceptanceRef: governance/evidence/risk/legacy-billing-risk-acceptance.yaml
        poam: governance/evidence/poam/legacy-billing-adapter-poam.yaml
        compensatingControls:
          - read-only traffic
          - daily reconciliation
          - canary traffic capped at 5 percent
        closeCriteria:
          - migration completed
          - conformance claim regenerated
          - production traffic on old baseline equals zero
    blocking: []
    expired: []
    closed:
      - exceptionId: ex-baseline-2026-000
        source: baseline-compatibility-ledger
        affectedAsset: api:order-command:v1
        closedAt: 2026-06-18T17:00:00+08:00
        closedBy: architecture-governance-board
        closeEvidence: governance/evidence/compatibility/order-command-api-v2.yaml
  summary:
    activeCount: 1
    blockingCount: 0
    expiredCount: 0
    highResidualRiskCount: 0
    conditionalPassCount: 1
    readyForBaseline: true
    readyForFrozen: true
  gates:
    blockBaselineOnExpiredException: true
    blockBaselineOnUnknownOwner: true
    blockFrozenOnBlockingException: true
    blockFrozenOnHighResidualRisk: true
    requirePoamForBlockingException: true
    requireRiskAcceptanceForConditionalPass: true
    requireExceptionLedgerDigestInReleaseEvidence: true
```

例外状态只能使用以下值：

| 状态 | 含义 | 是否阻断 |
| ---- | ---- | -------- |
| `active` | 例外仍有效，未超过到期日，且有 owner、风险接受和关闭条件 | 视风险等级和门禁影响而定 |
| `conditional-pass` | 例外允许本轮发布通过，但必须有风险接受、补偿控制和 POA&M | 不阻断 `baseline`，通常阻断或限制 `frozen` |
| `blocking` | 例外会阻断基线晋级、冻结或生产发布 | 是 |
| `expired` | 例外超过到期日或证据过期 | 是 |
| `closed` | 例外已关闭，且有关闭证据 | 否 |
| `rejected` | 例外申请未被批准 | 是，除非风险通过其他路径关闭 |

执行规则：

1. `baseline-exception-ledger.yaml` 必须聚合 `baseline-compatibility-ledger.yaml`、`baseline-adoption-ledger.yaml`、`baseline-support-matrix.yaml`、`baseline-notification-ledger.yaml`、`baseline-rollback-verification.yaml`、`release-gate-decision.yaml`、`control-plane.yaml`、风险登记和 POA&M 中的例外。
2. 每个例外必须有来源、受影响资产、控制项、owner、严重度、残余风险、到期时间、补偿控制、关闭条件和证据路径。
3. `conditional-pass` 必须有风险接受人和 POA&M；缺少任何一个字段都必须降级为 `blocking`。
4. `expired`、`blocking` 或 `high residual risk` 例外不得进入 `frozen`，除非通过正式风险接受并声明补偿控制、关闭期限和审计可接受性。
5. 例外关闭必须有 `closeEvidence`，不能只写“已处理”或依赖会议纪要。
6. 发布证据包必须记录 `baseline-exception-ledger.yaml` 的摘要，并在冻结复核中声明 `expiredCount=0`、`blockingCount=0`。

可执行验收标准：

1. 任意企业级基线都能列出所有活跃、过期、阻断、条件放行和已关闭例外。
2. 任意例外都能追溯到原始来源、风险接受、POA&M、补偿控制和关闭条件。
3. 任意过期或阻断例外都会阻断 `baseline` 或 `frozen` 晋级，直到关闭、续期、降级或正式风险接受。
4. 任意冻结基线都能证明没有散落在其他账本中但未进入总账的活跃例外。
5. 任意审计人员都能从总账直接判断当前基线是否满足冻结准入，而不需要逐个翻兼容、采纳、支持、通知和门禁记录。

### 10.10.20 基线就绪评分卡

`baseline-readiness-scorecard.yaml` 是企业架构基线晋级前的最终就绪判定。它不替代版本控制面、发布证据包、控制项覆盖、
基线制品清单、验证环境锁或例外总账，而是把这些证据按硬门禁和评分维度统一汇总，避免出现“每份局部证据都存在，
但没有人能明确判断是否可以进入 baseline 或 frozen”的状态。

```yaml
baselineReadinessScorecard:
  scorecardId: brs-20260602-mea-v243
  baselineId: mea-v2.43-20260602
  documentVersion: V2.43
  owner: architecture-governance-board
  generatedAt: 2026-06-02T14:00:00+08:00
  scoringPolicy:
    minimumBaselineScore: 90
    minimumFrozenScore: 95
    blockOnCriticalFinding: true
    blockOnArtifactDigestDrift: true
    blockOnVerificationLockDrift: true
    blockOnExpiredException: true
    blockOnRollbackUnverified: true
    blockOnMissingRequiredNotification: true
    blockOnForbiddenRemoteAssets: true
    scoreCannotOverrideHardGate: true
  evidenceInputs:
    versionGovernance: governance/control-plane/version-governance.yaml
    lifecycleStateMachine: governance/evidence/baselines/baseline-lifecycle-state-machine.yaml
    releaseEvidence: governance/evidence/baselines/baseline-release-evidence.yaml
    controlCoverage: governance/control-plane/control-coverage.yaml
    artifactInventory: governance/evidence/baselines/baseline-artifact-inventory.yaml
    verificationLock: governance/evidence/verification/baseline-verification-lock.yaml
    exceptionLedger: governance/evidence/exceptions/baseline-exception-ledger.yaml
    notificationLedger: governance/evidence/communications/baseline-notification-ledger.yaml
    rollbackVerification: governance/evidence/rollback/baseline-rollback-verification.yaml
    auditExportManifest: governance/evidence/audit-export/audit-export-manifest.yaml
    repositoryChangeControl: governance/control-plane/repository-change-control.yaml
  dimensions:
    - id: version-identity
      weight: 10
      score: 100
      status: pass
      evidence:
        - governance/control-plane/version-governance.yaml
    - id: control-coverage
      weight: 15
      score: 96
      status: pass
      evidence:
        - governance/control-plane/control-coverage.yaml
    - id: artifact-integrity
      weight: 15
      score: 98
      status: pass
      evidence:
        - governance/evidence/baselines/baseline-artifact-inventory.yaml
        - build/modern-enterprise-architecture-audit/audit-export-integrity.json
    - id: verification-reproducibility
      weight: 10
      score: 95
      status: pass
      evidence:
        - governance/evidence/verification/baseline-verification-lock.yaml
    - id: exception-health
      weight: 15
      score: 94
      status: conditional-pass
      evidence:
        - governance/evidence/exceptions/baseline-exception-ledger.yaml
    - id: compatibility-and-adoption
      weight: 10
      score: 93
      status: conditional-pass
      evidence:
        - governance/evidence/compatibility/baseline-compatibility-ledger.yaml
        - governance/evidence/adoption/baseline-adoption-ledger.yaml
    - id: notification-readiness
      weight: 8
      score: 100
      status: pass
      evidence:
        - governance/evidence/communications/baseline-notification-ledger.yaml
    - id: rollback-readiness
      weight: 10
      score: 97
      status: pass
      evidence:
        - governance/evidence/rollback/baseline-rollback-verification.yaml
    - id: audit-and-supply-chain
      weight: 7
      score: 96
      status: pass
      evidence:
        - governance/evidence/audit-export/audit-export-manifest.yaml
        - governance/evidence/audit-export/audit-export-signature-receipt.yaml
  hardGates:
    failed: []
    warnings:
      - id: adoption-exception-open
        source: governance/evidence/exceptions/baseline-exception-ledger.yaml
        impact: does-not-block-baseline-but-limits-frozen
  summary:
    weightedScore: 96
    readinessLevel: ready-for-baseline
    readyForBaseline: true
    readyForFrozen: false
    frozenBlockers:
      - freeze-window-not-started
    blockingFindings: 0
    expiredExceptions: 0
    forbiddenRemoteAssets: 0
  decision:
    candidateToBaseline: pass
    baselineToFrozen: not-ready
    decidedBy: architecture-governance-board
    decisionRef: governance/control-plane/release-gate-decision.yaml
```

就绪状态只能使用以下值：

| 状态 | 含义 | 是否允许晋级 |
| ---- | ---- | ------------ |
| `not-ready` | 评分不足或硬门禁未通过 | 否 |
| `ready-for-candidate` | 可进入候选评审，但不能用于生产基线 | 只允许低风险试点 |
| `ready-for-baseline` | 满足 baseline 阈值和全部 baseline 硬门禁 | 允许进入 baseline |
| `ready-for-frozen` | 满足 frozen 阈值、冻结窗口和全部冻结硬门禁 | 允许进入 frozen |
| `blocked` | 存在 critical finding、过期例外、回滚失败、禁推资产或制品漂移 | 否 |
| `expired` | 评分卡证据超过有效期，需要重新生成 | 否 |

执行规则：

1. `baseline-readiness-scorecard.yaml` 必须在 `candidate -> baseline` 和 `baseline -> frozen` 前生成，并写入 `baseline-release-evidence.yaml` 的不可变摘要。
2. 每个评分维度必须有 `weight`、`score`、`status` 和证据路径；评分维度权重总和必须等于 100。
3. 硬门禁失败不能被平均分覆盖；只要存在 critical finding、过期例外、回滚未验证、制品摘要漂移或禁推资产进入远端，最终判定必须为 `blocked`。
4. `ready-for-baseline` 不等于 `ready-for-frozen`。冻结还必须满足更高分数、冻结窗口、通知确认、例外总账和审计导出要求。
5. `conditional-pass` 维度必须能追溯到风险接受、POA&M、补偿控制和关闭日期，不能只靠人工签字放行。
6. 评分卡必须进入季度复核；任何评分策略、权重或硬门禁变化都必须形成基线变更记录或 ADR。

可执行验收标准：

1. 任意基线晋级都能找到对应的 `baseline-readiness-scorecard.yaml`。
2. 任意评分卡都能证明权重总和为 100，且每个维度都有证据路径和状态。
3. 任意硬门禁失败都会把最终判定置为 `blocked`，不会被总分掩盖。
4. 任意 `ready-for-frozen` 结论都能证明分数达到 frozen 阈值、过期例外为 0、阻断项为 0、回滚验证未过期且审计导出可验签。
5. 任意审计人员都能从评分卡直接判断基线处于 `not-ready`、`ready-for-baseline` 还是 `ready-for-frozen`，不需要人工重新拼装所有证据。

### 10.10.21 基线生命周期状态机

`baseline-lifecycle-state-machine.yaml` 是企业架构基线状态迁移的唯一控制面。它不替代 `version-governance.yaml`、
`baseline-release-evidence.yaml` 或 `release-gate-decision.yaml`，而是规定哪些状态可以迁移、哪些状态永远禁止直达、
每次迁移必须引用哪些证据、由谁审批、迁移后必须回写哪些账本，避免“状态字段被人工改了，但证据链没有跟着变”的版本治理失效。

```yaml
baselineLifecycleStateMachine:
  machineId: blsm-20260602-mea-v243
  baselineId: mea-v2.43-20260602
  documentVersion: V2.43
  owner: architecture-governance-board
  generatedAt: 2026-06-02T14:30:00+08:00
  currentState:
    state: candidate
    enteredAt: 2026-06-02T14:30:00+08:00
    source: governance/control-plane/version-governance.yaml
    releaseTag: architecture/v2.43-candidate
    sourceCommit: <git-sha-of-baseline-commit>
  states:
    - state: draft
      terminal: false
      productionAllowed: false
      description: 文档或契约仍在探索，不能作为执行基线。
    - state: candidate
      terminal: false
      productionAllowed: low-risk-pilot-only
      description: 已具备执行口径，等待晋级评审。
    - state: baseline
      terminal: false
      productionAllowed: true
      description: 已批准作为企业执行基线。
    - state: frozen
      terminal: false
      productionAllowed: true
      description: 已冻结供审计、招标、监管或规模化推广使用。
    - state: emergency-patch
      terminal: false
      productionAllowed: controlled-only
      description: 安全、合规或生产事故紧急补丁通道。
    - state: superseded
      terminal: false
      productionAllowed: existing-assets-only
      description: 已被新基线替代，只允许迁移期存量使用。
    - state: eol
      terminal: true
      productionAllowed: false
      description: 已停止支持，不得新建或继续用于生产。
  allowedTransitions:
    - from: draft
      to: candidate
      requiredEvidence:
        - baseline-change-record
        - version-governance
        - control-coverage
        - make-test
      approvers:
        - architecture-document-owner
      sideEffects:
        - update-doc-index
        - update-version-manifest
    - from: candidate
      to: baseline
      requiredEvidence:
        - baseline-release-evidence
        - baseline-readiness-scorecard
        - baseline-artifact-inventory
        - baseline-verification-lock
        - baseline-exception-ledger
        - baseline-rollback-verification
        - release-gate-decision
        - signed-release-tag
      approvers:
        - platform-lead
        - security-lead
        - data-governance-lead
        - architecture-governance-board
      sideEffects:
        - update-version-governance-status
        - write-release-evidence-digest
        - notify-owners
    - from: baseline
      to: frozen
      requiredEvidence:
        - frozen-window-open
        - baseline-readiness-scorecard-ready-for-frozen
        - notification-ledger-complete
        - expired-exceptions-zero
        - rollback-verification-not-expired
        - audit-export-signature-receipt
      approvers:
        - architecture-governance-board
        - audit-lead
        - security-lead
      sideEffects:
        - freeze-source-commit
        - freeze-audit-export
        - lock-support-matrix
    - from: baseline
      to: superseded
      requiredEvidence:
        - successor-baseline-approved
        - baseline-support-matrix-updated
        - adoption-migration-plan
      approvers:
        - architecture-governance-board
      sideEffects:
        - update-support-state
        - notify-consumers
    - from: frozen
      to: superseded
      requiredEvidence:
        - successor-frozen-or-baseline-approved
        - audit-retention-plan
        - migration-deadline
      approvers:
        - architecture-governance-board
        - audit-lead
      sideEffects:
        - retain-frozen-evidence
        - update-support-state
    - from: baseline
      to: emergency-patch
      requiredEvidence:
        - incident-or-security-ticket
        - patch-scope
        - rollback-verification
        - postmortem-owner
      approvers:
        - security-lead
        - platform-lead
      sideEffects:
        - create-emergency-patch-record
        - schedule-postmortem
    - from: emergency-patch
      to: baseline
      requiredEvidence:
        - patch-evidence-complete
        - postmortem-complete
        - regression-gates-pass
      approvers:
        - architecture-governance-board
      sideEffects:
        - merge-patch-evidence
        - update-release-evidence
    - from: superseded
      to: eol
      requiredEvidence:
        - zero-production-adoption
        - support-matrix-eol-date-reached
        - migration-ledger-closed
      approvers:
        - architecture-governance-board
        - platform-lead
      sideEffects:
        - block-new-adoption
        - archive-baseline-evidence
  forbiddenTransitions:
    - from: draft
      to: baseline
      reason: 必须先进入 candidate 并完成晋级证据。
    - from: draft
      to: frozen
      reason: 草案不能直接冻结。
    - from: candidate
      to: frozen
      reason: 必须先成为 baseline。
    - from: frozen
      to: draft
      reason: 冻结基线不得回退为草案，只能补丁、替代或退役。
    - from: frozen
      to: baseline
      reason: 冻结状态不可降级；后续变更必须走补丁或新基线。
    - from: eol
      to: baseline
      reason: EOL 基线不可复活，必须创建新 baseline ID。
  transitionAttempts:
    - transitionId: blsm-transition-20260602-001
      from: candidate
      to: baseline
      requestedBy: architecture-governance-board
      requestedAt: 2026-06-02T14:35:00+08:00
      decision: pass
      decidedAt: 2026-06-02T15:00:00+08:00
      decisionRef: governance/control-plane/release-gate-decision.yaml
      evidence:
        releaseEvidence: governance/evidence/baselines/baseline-release-evidence.yaml
        readinessScorecard: governance/evidence/baselines/baseline-readiness-scorecard.yaml
        artifactInventory: governance/evidence/baselines/baseline-artifact-inventory.yaml
        verificationLock: governance/evidence/verification/baseline-verification-lock.yaml
        exceptionLedger: governance/evidence/exceptions/baseline-exception-ledger.yaml
        rollbackVerification: governance/evidence/rollback/baseline-rollback-verification.yaml
      guardResults:
        transitionAllowed: true
        requiredEvidencePresent: true
        hardGatesPass: true
        forbiddenRemoteAssets: 0
      writeBack:
        versionGovernanceStatus: baseline
        supportMatrixState: active
        releaseEvidenceDigestUpdated: true
```

生命周期状态只能使用以下值：

| 状态 | 含义 | 生产使用 |
| ---- | ---- | -------- |
| `draft` | 设计草案或未完成契约 | 禁止 |
| `candidate` | 候选基线，可低风险试点 | 仅低风险试点 |
| `baseline` | 已批准执行基线 | 允许 |
| `frozen` | 冻结审计或规模化推广口径 | 允许，但只能补丁或替代 |
| `emergency-patch` | 紧急补丁状态 | 受控允许 |
| `superseded` | 被新基线替代 | 仅存量迁移期 |
| `eol` | 停止支持 | 禁止 |

执行规则：

1. 所有状态迁移必须先在 `allowedTransitions` 中声明；不在允许表中的迁移默认拒绝。
2. `forbiddenTransitions` 是硬禁止，即使有人工审批也不能绕过；必须创建新基线或走补丁通道。
3. 每次迁移必须写入 `transitionAttempts`，记录 `from`、`to`、请求人、批准人、证据路径、决策、状态回写和失败原因。
4. `currentState.state` 必须与 `version-governance.yaml` 的 `releaseChannel/status`、`baseline-release-evidence.yaml` 的晋级决策和 `baseline-support-matrix.yaml` 的支持状态一致。
5. `candidate -> baseline` 不能缺少就绪评分卡、验证环境锁、制品清单、例外总账、回滚验证和 release gate 决策。
6. `baseline -> frozen` 必须证明冻结窗口开启、就绪评分达到 frozen 阈值、通知确认完成、过期例外为 0、回滚验证未过期且审计导出可验签。
7. `emergency-patch` 只能用于安全、合规或生产事故，必须有事故编号、补丁范围、回滚验证、事后复盘 owner 和补证期限。
8. `eol` 为终态，不允许重新进入 `baseline`；需要重新启用时必须生成新 baseline ID、发布证据和状态机。

可执行验收标准：

1. 任意基线状态都能从状态机查到当前状态、进入时间、来源 commit、release tag 和回写目标。
2. 任意状态迁移都能证明它在 `allowedTransitions` 中，且不在 `forbiddenTransitions` 中。
3. 任意失败、拒绝或被阻断的迁移都能留下 `transitionAttempts`，并能追溯到缺失证据或硬门禁失败。
4. 任意审计人员都能直接判断当前基线是否只是候选、已经 baseline、已经 frozen、已被替代还是 EOL。
5. 任意状态漂移都会被门禁阻断：状态机、版本控制面、发布证据、支持矩阵和采纳总账不能出现互相矛盾的状态。

## 10.11 仓库拓扑剖面

目录结构可以按企业规模、团队自治程度和合规要求裁剪，但真相源边界不能裁剪。仓库拓扑的选择应先看 ownership、变更频率、权限隔离、发布节奏和审计要求，而不是看团队偏好的 Git 管理方式。

推荐剖面：

| 拓扑 | 适用场景 | 优点 | 风险 | 必须保留的边界 |
| ---- | -------- | ---- | ---- | -------------- |
| 单仓 monorepo | 领域数量较少、平台能力统一、团队协作密集 | 原子变更、统一门禁、全局重构容易 | 仓库膨胀、权限隔离难、CI 成本高 | 目录 owner、CODEOWNERS、路径级门禁、catalog 生成规则 |
| 多仓 polyrepo | 团队自治强、服务生命周期差异大、权限隔离要求高 | 权限清晰、发布独立、仓库轻 | 契约漂移、版本对齐难、跨仓变更复杂 | contracts registry、catalog 聚合、跨仓兼容性检查 |
| 平台独立仓 | 平台团队独立运营 Golden Path、模板和工具链 | 平台产品化清晰，模板可版本化 | 平台与业务仓割裂 | 平台模板版本、迁移说明、使用方影响分析 |
| GitOps 独立仓 | 生产环境权限严格、需要环境 owner 审核 | 环境期望状态可审计，权限隔离强 | 应用代码和部署变更不同步 | 镜像 digest、GitOps revision、服务契约和 catalog 指针 |
| 数据产品独立仓 | 数据平台集中、数据契约和质量规则独立演进 | 数据治理和血缘清晰 | 领域 owner 责任被稀释 | 数据产品 owner、领域映射、数据契约和消费通知 |
| AI 产品独立仓 | AI 产品迭代快、评估集和 Prompt 需要独立生命周期 | Prompt/RAG/评估可单独治理 | AI 旁路领域边界 | 工具注册、数据授权、风险等级和审计链路 |

选择规则：

1. 生产 GitOps 推荐独立权限边界；是否独立仓取决于审计和环境 owner 要求。
2. 契约可以集中仓管理，也可以随领域仓管理，但必须进入统一 catalog 和兼容性校验。
3. 平台模板必须有版本，业务仓必须能声明自己使用的模板版本和迁移状态。
4. 多仓模式必须有跨仓变更协议，包括 API、事件、数据产品、AI 工具和 GitOps 变更。
5. 不允许用仓库边界掩盖领域边界不清；仓库拆分不能替代 DDD 和 owner 设计。

`governance/migration/repository-topology-policy.md` 应至少包含：

1. 仓库拓扑选择标准。
2. 权限和 CODEOWNERS 规则。
3. 跨仓契约发布流程。
4. GitOps 仓权限和审计要求。
5. 平台模板版本和迁移策略。

## 10.12 迁移、兼容与弃用策略

现代化架构不能要求企业一次性重写全部系统。迁移策略必须默认支持渐进式替换、双写校验、流量切换、消费者迁移和可回退发布。

### 10.12.1 旧系统绞杀迁移

绞杀迁移的默认流程：

1. 识别旧系统能力边界、数据写入点、外部接口和批处理任务。
2. 在 catalog 中登记旧系统 owner、依赖、风险等级和目标迁移状态。
3. 使用 API Gateway、BFF、事件桥接或数据同步把新能力接入边缘流量。
4. 对读路径先建立查询模型、缓存或数据产品，避免直接跨库读旧系统。
5. 对写路径先建立幂等键、事件补偿、对账和回滚机制。
6. 以场景、客户群、区域、渠道或能力为单位逐步切流。
7. 每次切流保留回退路径、监控指标和业务验收口径。
8. 完成迁移后清理旧接口、旧任务、旧数据同步和例外权限。

禁止事项：

1. 不允许新服务直接共享旧系统数据库作为长期方案。
2. 不允许没有对账和补偿机制的双写进入生产关键路径。
3. 不允许只迁移代码、不迁移 owner、SLO、runbook、catalog 和数据契约。
4. 不允许旧系统退役后保留无 owner 的影子任务、同步脚本和访问权限。

### 10.12.2 API、事件和数据产品弃用

弃用不是删除通知，而是受控迁移过程。

| 对象 | 弃用前要求 | 通知对象 | 最短观察期 | 删除前门禁 |
| ---- | ---------- | -------- | ---------- | ---------- |
| API | 新版本契约、兼容说明、迁移示例、消费者列表 | API 消费方、平台门户、SDK owner | 至少一个发布周期 | 无生产消费者或风险接受记录 |
| 事件 | 新 Schema、消费者影响分析、重放策略 | 事件消费者、数据平台、领域 owner | 至少两个消费周期 | 消费者迁移完成，死信和积压清零 |
| 数据产品 | 新数据产品或字段映射、质量对比、血缘影响 | 下游报表、模型、AI 产品、数据消费者 | 至少一个数据结算周期 | 下游质量和口径验收通过 |
| AI 模型 / Prompt | 新版本评估、回放对比、回滚模型 | AI 产品 owner、业务 owner、安全团队 | 灰度期结束 | 评估通过，旧版本无生产流量 |
| 平台 Golden Path | 新模板版本、迁移脚本、兼容窗口 | 所有使用团队 | 至少一个季度 | 迁移完成或例外到期 |

`governance/migration/deprecation-policy.md` 应至少包含：

1. 弃用对象、owner 和替代方案。
2. 影响范围和消费者清单。
3. 通知渠道、观察期和迁移截止日期。
4. 兼容策略、回滚路径和风险接受记录。
5. 删除前验证证据和审计留存要求。

基线级兼容性和消费者迁移状态必须进入 `baseline-compatibility-ledger.yaml`。单个 API、事件、数据产品或 AI 产品的兼容性报告只说明局部事实；基线兼容性总账必须证明这些局部事实已经汇总成版本发布门禁。

### 10.12.3 数据、AI 和平台能力退役

退役流程必须处理数据、权限、成本和审计尾部：

1. 数据产品退役必须确认保留期限、归档位置、删除策略、下游血缘和 AI 使用授权。
2. AI 产品退役必须冻结模型路由、Prompt、RAG 索引、工具权限和审计日志保留策略。
3. 平台能力退役必须提供替代 Golden Path、迁移窗口、自动化迁移脚本和例外清单。
4. 基础设施退役必须确认 DNS、证书、密钥、网络策略、备份、成本标签和监控告警全部清理。
5. 所有退役动作必须回写基线兼容性总账，证明生产消费者已经迁移、归零或进入风险接受。

## 10.13 验证包与审计证据清单

可执行企业标准必须能被验证。没有验证包，架构文档只能证明“写过”，不能证明“做到”。

### 10.13.1 最小验证包

每个试点领域至少提供以下验证包：

本仓库提供第一批可执行 starter kit：

```text
内部 starter kit
```

该目录的 schema 和示例由以下命令校验：

```bash
starter kit 校验命令
```

该命令是仓库内零依赖 starter gate，用于校验版本清单、控制项覆盖清单、76 组示例的 JSON Schema 子集、YAML 示例、嵌套必填字段、格式约束、数值阈值、严格 schema 模式、基线生命周期状态机、基线就绪评分卡、基线例外总账、基线回滚验证记录、基线通知确认总账、基线验证环境锁定、基线制品清单、基线符合性声明、基线发布列车、基线支持矩阵、基线采纳总账、基线兼容性总账、基线发布证据包、版本控制面、外部标准版本锁定、企业执行控制面、合规等级、门禁决策、仓库变更控制、远端保护漂移整改、访问复核、密钥轮换、漏洞修复、事故复盘、证据新鲜度、AI 证据账本、微调运行证据、AI 事件响应 playbook、控制证据映射、审计导出清单、审计导出自动化命令、控制评估报告、架构基线变更记录、架构决策记录、OSCAL 交换映射、POA&M 整改计划、企业架构风险登记、审计导出门禁、审计导出完整性清单、审计导出 provenance statement、审计导出签名策略、审计导出签名验签回执、未知字段阻断、证据链字段和示例间一致性。企业生产落地时应优先接入成熟校验器，例如 JSON Schema draft 2020-12 validator、YAML parser、OpenAPI / AsyncAPI checker、OPA / Cedar / Kyverno policy test、SLSA / Sigstore verifier、OpenTelemetry collector、OpenCost / FOCUS 工具链、IAM / Secret 管理系统、漏洞管理平台、事故管理系统、OSCAL 工具链和 GitOps diff 工具；本仓库脚本只作为 starter kit 的最小可执行证明。

审计导出包由以下命令生成：

```bash
审计导出命令
```

默认输出：

```text
build/modern-enterprise-architecture-audit/audit-export.json
build/modern-enterprise-architecture-audit/audit-export.md
build/modern-enterprise-architecture-audit/oscal-summary.json
build/modern-enterprise-architecture-audit/audit-export-integrity.json
build/modern-enterprise-architecture-audit/audit-export-provenance.json
```

导出输出不变量由以下命令校验，并已经进入 `make test`：

```bash
审计导出门禁命令
```

```text
governance/evidence/releases/{service-release}.yaml
governance/evidence/supply-chain/{service-attestation}.yaml
governance/evidence/exceptions/{policy-exception}.yaml
governance/evidence/compatibility/{api-or-event-report}.yaml
governance/evidence/drift/{service-drift-report}.yaml
governance/evidence/lineage/{data-product-run}.yaml
governance/evidence/platform/{platform-product-period}.yaml
governance/evidence/privacy/{privacy-assessment}.yaml
governance/evidence/recovery/{recovery-drill}.yaml
governance/evidence/policy-tests/{policy-test-report}.yaml
governance/evidence/cost/{cost-allocation-period}.yaml
governance/evidence/access/{access-review}.yaml
governance/evidence/secrets/{secrets-rotation}.yaml
governance/evidence/vulnerabilities/{vulnerability-remediation}.yaml
governance/postmortems/{incident-postmortem}.md
governance/evidence/freshness/{freshness-report}.json
governance/evidence/control-map/{control-evidence-map}.yaml
governance/control-plane/{conformance-profile}.yaml
governance/control-plane/{control-plane}.yaml
governance/control-plane/{release-gate-decision}.yaml
governance/control-plane/{standards-baseline}.yaml
governance/control-plane/{version-governance}.yaml
governance/evidence/baselines/{baseline-lifecycle-state-machine}.yaml
governance/evidence/verification/{baseline-verification-lock}.yaml
governance/evidence/baselines/{baseline-artifact-inventory}.yaml
governance/evidence/baselines/{baseline-readiness-scorecard}.yaml
governance/evidence/baselines/{baseline-release-evidence}.yaml
governance/evidence/compatibility/{baseline-compatibility-ledger}.yaml
governance/evidence/adoption/{baseline-adoption-ledger}.yaml
governance/evidence/support/{baseline-support-matrix}.yaml
governance/evidence/release-trains/{baseline-release-train}.yaml
governance/evidence/exceptions/{baseline-exception-ledger}.yaml
governance/evidence/communications/{baseline-notification-ledger}.yaml
governance/evidence/rollback/{baseline-rollback-verification}.yaml
governance/evidence/conformance/{baseline-conformance-claim}.yaml
governance/evidence/audit-export/{audit-export-manifest}.yaml
governance/evidence/control-assessments/{control-assessment-report}.yaml
governance/evidence/baseline-changes/{baseline-change-record}.yaml
governance/evidence/architecture-decisions/{architecture-decision-record}.yaml
governance/evidence/oscal/{oscal-export-profile}.yaml
governance/evidence/audit-export/{audit-export-signing-policy}.yaml
governance/evidence/audit-evidence-index.md
governance/evidence/drill-evidence-template.md
catalog/components/{service}.yaml
catalog/data-products/{data-product}.yaml
catalog/ai-products/{ai-product}.yaml
contracts/apis/{api}.openapi.yaml
contracts/events/{event}.asyncapi.yaml
contracts/datasets/{data-product}.yaml
contracts/ai/tools/{tool}.yaml
contracts/release/feature-flags/{flag}.yaml
contracts/ai/threat-models/{ai-product}.yaml
contracts/ai/observability/{ai-product}.yaml
contracts/data/lineage/{data-product-run}.yaml
contracts/privacy/{data-product}.yaml
infra/gitops/environments/prod/{domain}/{service}/kustomization.yaml
infra/kubernetes/tenancy/{tenant-boundary}.yaml
infra/kubernetes/rbac/{identity-access-review}.yaml
```

验证命令应至少覆盖：

```bash
make lint
make check-links
make check-doc-structure
make check-metadata
make check-ai-citation
starter kit 校验命令
审计导出门禁命令
审计导出命令
```

企业落地时还应补充：

1. OpenAPI / AsyncAPI 兼容性检查。
2. JSON Schema / Proto / Avro 兼容性检查。
3. 数据契约质量规则和权限策略检查。
4. AI 评估集、红队和工具权限检查。
5. SBOM、provenance、签名和验签检查。
6. GitOps diff、Policy as Code 和 Kubernetes 准入检查。
7. catalog 生成、字段权威和漂移检测。
8. RTO/RPO 恢复演练证据检查。
9. 隐私影响评估、主体删除传播和向量索引删除证据检查。
10. 租户隔离、ResourceQuota、NetworkPolicy 默认拒绝和准入策略检查。
11. GenAI trace、Token、成本、工具调用和 RAG span 覆盖检查。
12. 成本标签覆盖、未分摊成本和单位成本分摊检查。
13. 访问复核、特权账号、break-glass 和 MFA 审计检查。
14. Secret 加密、轮换、泄露扫描和 KMS 证据检查。
15. 高危漏洞、KEV、修复 SLA、残余风险和发布阻断检查。
16. 事故复盘、纠正行动、runbook 更新和门禁反哺检查。
17. 审计证据最大年龄、过期动作和 CI 阻断检查。
18. 控制项到证据路径、状态、新鲜度和阻断属性的映射检查。
19. 合规等级、执行控制面、门禁决策、例外放行、break-glass 和季度复核检查。
20. 审计导出包范围、内容、验证结果、签名和留存复审检查。
21. 审计导出 JSON / Markdown 包生成、关键制品哈希和导出命令检查。
22. 控制评估报告、发现项、整改时限、剩余风险和签署状态检查。
23. 架构基线变更影响分析、审批、验证命令、回滚计划和留存复审检查。
24. OSCAL catalog、component-definition、SSP、assessment-results、POA&M 映射和 `oscal-summary.json` 输出检查。
25. POA&M 发现项、整改行动、里程碑、证据、签署和 OSCAL POA&M 输出一致性检查。
26. 企业架构风险登记、关联控制项、关联 POA&M、缓解行动、残余风险、复审和审计导出风险视图一致性检查。
27. 审计导出 JSON、Markdown、OSCAL 摘要的版本、pair 数、控制数和评估状态不变量检查。
28. 审计导出生成物 SHA-256 摘要、源制品哈希和完整性清单防篡改检查。
29. 审计导出 provenance subject digest、构建定义、源码提交和源证据依赖检查。
30. 审计导出签名策略、payload 摘要、验签命令、bundle 路径和外部签名交接检查。
31. 审计导出签名验签回执、bundle 摘要、证书身份、OIDC issuer、透明日志和验签结果检查。
32. 基线回滚验证、上一基线检出、GitOps revision 恢复、审计导出恢复、烟测结果和验证时效检查。
33. 基线例外总账、例外来源、到期日、风险接受、POA&M、阻断状态、关闭证据和冻结准入检查。
34. 基线就绪评分卡、硬门禁、评分维度、权重、阈值、证据路径、阻断项和 baseline/frozen 最终判定检查。

### 10.13.2 审计证据索引

审计证据不应在审计前临时收集，应由平台和流水线持续生成。

| 证据类型 | 来源 | 生产者 | 保留要求 |
| -------- | ---- | ------ | -------- |
| 架构版本证据 | 本文档版本记录、ADR、评审记录 | 治理团队 | 至少保留到下一主版本废弃后 |
| 服务发布证据 | CI、制品库、GitOps、catalog | 服务团队和平台团队 | 覆盖每次生产发布 |
| 供应链证据 | SBOM、provenance、签名、验签日志 | 平台团队和安全团队 | 按合规周期保留 |
| 数据产品证据 | 数据契约、质量报告、血缘、访问审计 | 领域团队和数据平台团队 | 覆盖每次数据产品发布 |
| AI 产品证据 | 风险分级、评估集、Prompt 版本、RAG 来源、回放 trace | AI 产品团队 | 按风险等级保留 |
| 可靠性证据 | SLO、错误预算、演练记录、事故复盘 | 服务 owner 和 SRE | 覆盖每个 Tier-1 / Tier-2 资产 |
| 成本证据 | 成本标签、预算、异常告警、单位成本 | 平台团队和 FinOps owner | 覆盖每个成本周期 |
| 访问证据 | IAM / RBAC、权限复核、break-glass、MFA 审计 | 安全团队、SRE 和服务 owner | 覆盖每个访问复核周期 |
| 密钥证据 | Secret provider、KMS、轮换记录、泄露扫描 | 平台团队和安全团队 | 覆盖每个轮换周期 |
| 漏洞证据 | 扫描结果、KEV、修复 SLA、残余风险和发布准入 | 安全团队和服务 owner | 覆盖每个高危发现 |
| 事故证据 | 事故时间线、根因、行动项、runbook 和门禁更新 | SRE 和服务 owner | 事故关闭后继续保留一个审计周期 |
| 控制映射证据 | 控制目录、证据路径、状态、新鲜度和阻断属性 | 治理团队和平台团队 | 覆盖每个基线版本 |
| 审计导出证据 | 导出范围、内容清单、验证结果、签名和留存复审 | 治理团队和安全团队 | 覆盖每次正式审计导出 |
| 审计导出自动化证据 | 导出命令、JSON 包、Markdown 报告、OSCAL 摘要、POA&M 整改视图、风险登记视图、完整性清单、provenance statement、签名策略、验签回执契约和校验结果 | 治理团队和平台团队 | 覆盖每次正式审计导出 |
| 审计导出门禁证据 | 本地质量门禁、输出不变量、OSCAL 摘要一致性和 `make test` 纳入状态 | 治理团队和平台团队 | 覆盖每次正式审计导出 |
| 审计导出完整性证据 | 生成物 SHA-256、源制品哈希、完整性清单和防篡改校验结果 | 治理团队和平台团队 | 覆盖每次正式审计导出 |
| 审计导出 provenance 证据 | in-toto statement、SLSA provenance、subject digest、构建定义、源码提交和源证据依赖 | 治理团队和平台团队 | 覆盖每次正式审计导出 |
| 审计导出签名策略证据 | provenance payload 摘要、签名方式、验签命令、bundle 路径和透明日志要求 | 治理团队、安全团队和平台团队 | 覆盖每次正式审计导出 |
| 审计导出签名验签回执证据 | 签名策略绑定、payload 摘要、bundle 摘要、证书身份、OIDC issuer、透明日志和验签结果 | 治理团队、安全团队和平台团队 | 覆盖每次正式审计导出 |
| 控制评估证据 | 控制结果、发现项、整改、剩余风险、签署和下次评估日期 | 治理团队和独立评估人 | 覆盖每个基线版本和正式审计周期 |
| 基线变更证据 | 版本、前序版本、影响分析、审批、验证命令、回滚和留存复审 | 治理团队和架构组 | 覆盖每次基线升级 |
| OSCAL 交换证据 | OSCAL 模型映射、导出摘要、控制目录、评估结果、POA&M 状态和风险登记状态 | 治理团队和安全团队 | 覆盖每次正式审计导出 |
| POA&M 整改计划证据 | 发现项、控制项、责任人、整改行动、里程碑、证据、签署和复审 | 治理团队、安全团队和控制 owner | 覆盖每个发现项和正式审计周期 |
| 企业架构风险登记证据 | 风险、严重度、可能性、影响、owner、处理策略、关联控制项、关联 POA&M、残余风险和复审 | 治理团队、安全团队和风险 owner | 覆盖每个架构风险和正式审计周期 |
| 基线就绪评分卡证据 | 硬门禁、评分维度、权重、证据路径、阻断项、baseline/frozen 阈值和最终判定 | 治理团队、平台团队、安全团队和架构组 | 覆盖每次企业基线晋级、冻结、紧急补丁和季度复核 |
| 基线例外总账证据 | 例外来源、受影响资产、owner、到期日、风险接受、POA&M、补偿控制、阻断状态和关闭证据 | 治理团队、控制 owner 和风险 owner | 覆盖每次企业基线晋级、冻结、紧急补丁和季度复核 |
| 基线回滚验证证据 | 上一基线、回滚目标 tag/commit、GitOps revision、审计导出恢复、烟测结果和验证时效 | 治理团队、平台团队和 SRE | 覆盖每次企业基线晋级、冻结和紧急补丁 |
| 例外证据 | 例外申请、风险接受、到期复审、关闭记录 | 治理团队 | 例外关闭后继续保留一个审计周期 |

`governance/evidence/audit-evidence-index.md` 应至少记录：

1. 证据名称和证据类型。
2. 对应系统、领域、数据产品、AI 产品或平台能力。
3. owner、生成时间、保留期限和存储位置。
4. 关联版本、commit、GitOps revision、制品 digest 或模型版本。
5. 审计状态、例外状态和下一次复审日期。

---

## 11. 架构决策机制

## 11.1 架构决策记录

重要架构决策必须形成 ADR，即 Architecture Decision Record。每条 ADR 应包含：

1. 背景。
2. 问题。
3. 备选方案。
4. 决策结果。
5. 影响范围。
6. 风险。
7. 后续行动。
8. 决策日期。
9. 决策人。

## 11.2 架构评审范围

不是所有变更都需要人工架构评审。建议仅对以下事项进行评审：

1. 新增核心领域。
2. 跨多个领域的重大流程变更。
3. 核心数据模型变更。
4. 高风险安全变更。
5. 大规模基础设施变更。
6. 影响多个团队的 API 或事件变更。
7. 重大技术选型。
8. 高成本资源投入。
9. 高风险 AI 产品、Agent 工具或模型供应商接入。
10. 供应链安全门禁、构建器、制品库或签名策略变更。

## 11.3 自动化优先原则

凡是可以标准化和自动化检测的规则，不应长期依赖人工评审。架构评审应聚焦于复杂权衡、边界争议和重大风险，而不是格式检查和重复审批。

---

## 12. 成本治理

## 12.1 成本治理目标

成本治理不是单纯压缩资源，而是让资源使用与业务价值透明对应。

## 12.2 成本治理要求

1. 所有资源必须打成本标签。
2. 成本必须能按团队、领域、环境和应用归集。
3. 高成本资源必须有预算和告警。
4. 闲置资源必须自动识别。
5. 测试环境应支持自动休眠或释放。
6. 关键业务应建立成本与业务指标的关联。
7. 平台应提供成本看板。
8. 成本异常必须通知负责人。
9. AI 成本必须按产品、团队、模型、Token、向量检索、推理资源和环境归集。
10. GPU、向量数据库、在线特征存储和高频推理端点必须设置预算、配额和闲置检测。

## 12.3 FinOps 运行机制

成本治理必须从“月末看账单”升级为“架构设计、平台默认值和运行优化”。

推荐采用 FinOps 的三类动作：

1. Inform：把成本按团队、领域、产品、环境、模型、数据产品和 AI 产品透明归集。
2. Optimize：优化闲置资源、过度配置、重复模型调用、低命中缓存、无效向量索引和低利用 GPU。
3. Operate：把预算、异常、配额、单位成本和业务指标纳入持续运营。

AI 场景需要额外跟踪：

1. cost per AI task。
2. cost per successful task。
3. token cost per product。
4. vector retrieval cost。
5. feature serving cost。
6. GPU utilization。
7. cache hit rate。
8. fallback to human cost。

成本数据建议对齐开放成本字段规范，至少保证 provider、account、service、resource、tag、usage、cost、currency、period 和 owner 可被统一查询。

---

## 13. 度量指标体系

## 13.1 业务指标

1. 用户增长。
2. 转化率。
3. 活跃度。
4. 客单价。
5. 订单量。
6. 支付成功率。
7. 履约时效。
8. 客户满意度。

## 13.2 技术指标

1. 服务可用性。
2. 响应延迟。
3. 错误率。
4. 变更频率。
5. 变更失败率。
6. 平均恢复时间。
7. 部署成功率。
8. 资源利用率。

## 13.3 数据指标

1. 数据准确性。
2. 数据完整性。
3. 数据及时性。
4. 数据一致性。
5. 数据质量规则通过率。
6. 数据产品使用量。
7. 数据访问审计覆盖率。
8. 指标口径一致性。

## 13.4 平台指标

1. 自助服务使用率。
2. 服务创建耗时。
3. 环境申请耗时。
4. 发布流水线成功率。
5. 平台可用性。
6. 平台用户满意度。
7. 工单减少率。
8. Golden Path 覆盖率。
9. Time to First Deploy。
10. 自助流程成功率。
11. 团队认知负载评分。

## 13.5 AI 指标

1. AI 产品采用率。
2. 任务完成率。
3. grounded answer rate。
4. 引用命中率。
5. 幻觉反馈率。
6. Prompt / RAG / Agent 回归通过率。
7. 工具调用成功率。
8. 人工确认率。
9. Token 成本。
10. 单任务成本。
11. 模型路由降级率。
12. 高风险策略拦截率。
13. 风险等级分布。
14. 人工复核通过率。
15. 红队用例通过率。
16. 可回放链路覆盖率。
17. 微调模型线上回退次数。
18. AI 事件平均恢复时间。
19. 高风险工具熔断次数。

## 13.6 供应链安全指标

1. SBOM 覆盖率。
2. provenance 覆盖率。
3. 签名覆盖率。
4. 部署验签通过率。
5. 漏洞阻断次数。
6. 高危漏洞修复时长。
7. 依赖锁定覆盖率。
8. 未批准基础镜像使用次数。
9. 供应链例外过期数量。

## 13.7 成本与 FinOps 指标

1. cloud cost per domain。
2. cloud cost per product。
3. AI cost per successful task。
4. GPU utilization。
5. idle resource cost。
6. untagged resource rate。
7. budget variance。
8. cost anomaly count。
9. unit cost per business transaction。
10. forecast accuracy。

## 13.8 性能、成本与规模检查

现代企业数字化平台必须把性能和成本作为治理对象，而不是上线后再补救。

### 13.8.1 复杂度与热点

必须检查：

1. 领域 API 是否处在核心请求链路。
2. 跨领域调用是否形成串行长链。
3. 读路径是否需要查询模型、缓存或物化视图。
4. 写路径是否需要事件驱动和最终一致性。
5. 数据产品是否存在全量扫描、重复计算或过度拉取。
6. AI 场景是否存在重复模型调用、高 token 成本或不可控上下文膨胀。

### 13.8.2 I/O 和外部依赖

以下问题必须显式标记为风险：

1. N+1 API 调用。
2. N+1 数据库查询。
3. 同步调用链过长。
4. 无超时、无重试边界。
5. 无幂等保护。
6. 无背压和限流。
7. 数据管道重复抽取。
8. 无缓存失效策略。

### 13.8.3 数据与存储

必须检查：

1. 每个领域服务是否拥有清晰的数据写入边界。
2. 查询是否有索引、分页和字段裁剪。
3. 大数据处理是否使用 streaming、chunking 或增量计算。
4. 数据产品是否声明 freshness、quality 和 cost owner。
5. 高价值指标是否有可追溯口径和血缘。
6. RAG 向量索引是否存在重复构建、无权限过滤或无法删除的隐性存储。
7. 在线特征是否存在训练-推理偏斜、延迟失控或无降级路径。

### 13.8.4 验证指标

性能和成本结论应通过以下指标验证：

1. p95 / p99 latency。
2. throughput。
3. error rate。
4. saturation。
5. queue lag。
6. cache hit rate。
7. data freshness。
8. pipeline cost。
9. model token cost。
10. cloud cost per domain / product / environment。
11. AI task cost。
12. vector search latency。
13. feature serving latency。
14. SBOM and provenance coverage。

---

## 14. 落地路线图

## 14.1 第一阶段：现状评估与目标蓝图

目标是识别当前系统、团队、数据和平台能力的真实状态。

主要工作：

1. 盘点业务系统。
2. 盘点核心业务流程。
3. 识别领域边界。
4. 盘点数据资产。
5. 盘点平台能力。
6. 评估交付效率。
7. 评估安全和治理风险。
8. 形成目标架构蓝图。

输出物：

1. 现状架构图。
2. 系统依赖图。
3. 领域候选清单。
4. 数据资产清单。
5. 平台能力成熟度评估。
6. 目标架构蓝图。
7. 优先级路线图。

## 14.2 第二阶段：选择试点领域

目标是选择一个高价值、边界相对清晰、依赖可控的领域进行试点。

建议优先选择：

1. 订单域。
2. 会员域。
3. 商品域。
4. 支付域。
5. 营销域。

试点范围不宜过大，应聚焦于一个可验证的业务闭环。

输出物：

1. 领域模型。
2. API 契约。
3. 事件契约。
4. 数据产品定义。
5. SLO 指标。
6. 团队责任边界。
7. 试点复盘报告。

## 14.3 第三阶段：建设内部开发平台

目标是让团队可以通过自助方式完成标准工程动作。

优先建设能力：

1. Developer Portal。
2. 服务模板。
3. CI/CD。
4. 环境管理。
5. 日志和监控。
6. 告警。
7. 权限申请。
8. 安全扫描。
9. 成本看板。
10. SBOM、签名验签和供应链证明。
11. LLM Gateway、RAG 平台和 AI 评估流水线。
12. 容器交付 Golden Path 和 GitOps 环境模板。

输出物：

1. 平台门户。
2. Golden Path。
3. 服务目录。
4. 发布流水线。
5. 可观测性看板。
6. 平台使用手册。
7. 平台运营指标。
8. 供应链安全门禁。
9. AI 平台最小可用能力。
10. 标准 Kubernetes base 和环境级 GitOps overlay。

## 14.4 第四阶段：数据产品化

目标是将关键领域数据转化为可信数据产品。

主要工作：

1. 建立数据目录。
2. 定义数据产品模板。
3. 建立数据质量规则。
4. 建立指标口径管理。
5. 建立数据血缘。
6. 建立数据权限管理。
7. 发布首批核心数据产品。
8. 建立离线特征、在线特征和向量索引的标准路径。
9. 定义数据产品面向 AI 消费的授权和变更通知机制。

输出物：

1. 数据产品目录。
2. 指标字典。
3. 数据质量看板。
4. 数据血缘图。
5. 权限审批流程。
6. 数据消费指南。
7. 特征产品模板。
8. 向量索引模板。
9. AI 评估数据集模板。

## 14.5 第五阶段：治理自动化

目标是将治理规则固化到平台和工具链中。

主要工作：

1. API 规范自动校验。
2. 事件 Schema 自动校验。
3. 数据契约自动校验。
4. 安全扫描自动化。
5. 发布准入门禁。
6. 成本标签校验。
7. SLO 监控。
8. 合规审计自动化。
9. AI 发布门禁自动化。
10. SBOM、provenance、签名和验签自动化。

输出物：

1. Policy as Code 规则库。
2. 自动化质量门禁。
3. 安全合规看板。
4. 成本治理看板。
5. 架构治理流程。
6. 审计报告模板。
7. AI 治理门禁。
8. 供应链安全准入策略。

## 14.6 第六阶段：AI 原生能力试点

目标是在一个低到中等风险场景中验证 AI 原生能力层，而不是一开始把 AI 接入所有关键流程。

建议优先选择：

1. 智能客服辅助。
2. 运营知识问答。
3. 内部研发助手。
4. 风控分析辅助。
5. 销售线索整理。

主要工作：

1. 定义 AI 产品目标、用户、风险等级和退出机制。
2. 接入 LLM Gateway、PromptOps、RAG、评估流水线和 AI Observability。
3. 将数据产品、特征产品、向量索引和领域工具纳入统一契约。
4. 建立提示注入、越权、幻觉、错误引用和成本消耗测试。
5. 灰度上线并持续观察任务完成率、grounded rate、人工确认率和成本。
6. 复盘 AI 产品质量、治理成本和团队认知负载。

输出物：

1. 首个 AI 产品。
2. Prompt 与评估集仓库。
3. RAG 数据源和向量索引。
4. Agent 工具权限清单。
5. AI 可观测性看板。
6. AI 发布复盘报告。

## 14.7 第七阶段：规模化推广

目标是将试点经验推广到更多业务域和团队。

主要工作：

1. 复制领域产品模式。
2. 扩展平台能力。
3. 扩展数据产品网络。
4. 扩展 AI 原生能力。
5. 建立平台运营机制。
6. 建立团队能力培训机制。
7. 建立持续改进机制。

输出物：

1. 企业级领域地图。
2. 领域产品组合。
3. 数据产品网络。
4. 平台能力地图。
5. 团队能力模型。
6. 成熟度评估报告。
7. AI 产品组合和治理报告。

## 14.8 最小落地清单

新项目不应一开始把所有目录做满。先从能够建立 owner、contract、catalog、gate 和 runtime baseline 的最小文件开始。

```text
governance/standards/engineering-standard.md
governance/ownership/teams.yaml
governance/ownership/raci.yaml
governance/slo/tiering-policy.md
governance/architecture-gates/production-readiness.yaml
governance/control-plane/conformance-profile.yaml
governance/control-plane/control-plane.yaml
governance/control-plane/release-gate-decision.yaml
governance/control-plane/standards-baseline.yaml
governance/control-plane/version-governance.yaml
governance/evidence/baselines/README.md
governance/evidence/adoption/README.md
governance/evidence/support/README.md
governance/evidence/release-trains/README.md
governance/evidence/conformance/README.md
governance/migration/deprecation-policy.md
governance/evidence/releases/README.md
governance/evidence/supply-chain/README.md
governance/evidence/exceptions/README.md
governance/evidence/compatibility/README.md
governance/evidence/drift/README.md
contracts/apis/README.md
contracts/events/README.md
contracts/datasets/README.md
contracts/ai/README.md
catalog/systems/README.md
catalog/components/README.md
catalog/ai-products/README.md
domains/example/domain.yaml
domains/example/services/example-service/service.yaml
domains/example/services/example-service/Dockerfile
ai/applications/example-ai-product/ai-product.yaml
platform/golden-paths/README.md
platform/supply-chain/README.md
infra/kubernetes/base/services/example-service/kustomization.yaml
infra/gitops/environments/dev/example/example-service/kustomization.yaml
infra/gitops/environments/prod/example/example-service/kustomization.yaml
```

最小落地目标：

1. 所有生产服务有 owner。
2. 所有跨域接口有契约。
3. 所有生产组件进入 catalog。
4. 所有关键服务有 SLO 和 runbook。
5. 所有生产发布有回滚路径。
6. 所有数据产品有业务语义、质量规则和访问策略。
7. 所有生产 AI 产品有评估集、工具权限、RAG 来源和可观测性。
8. 所有生产制品有 SBOM、签名和可追溯构建证据。
9. 所有容器化服务有镜像构建定义、GitOps 期望状态和 catalog runtime 指针。
10. 所有 Tier-1 / Tier-2 资产有 RTO、RPO、错误预算、on-call 和灾备演练要求。
11. 所有重大决策有 RACI owner 和必要评审证据。
12. 所有 API、事件、数据产品、AI 产品和平台能力有迁移、弃用和退役规则。
13. 所有生产发布有可追溯的验证包和审计证据索引。
14. 所有生产资产有合规等级画像、控制面记录和门禁决策证据。
15. 所有生产门禁引用的外部标准都有版本锁定、稳定性等级和升级门禁。
16. 所有生产基线都有唯一基线 ID、发布通道、源 commit、release tag、兼容窗口和回滚入口。
17. 所有基线晋级都有发布证据包，能证明不可变引用、漂移复核、审计摘要、验签结果和回滚验证。
18. 所有重大或破坏性基线变更都有兼容性总账，能证明消费者影响、迁移状态、弃用截止和未迁移风险。
19. 所有企业级基线都有采纳总账，能证明目标资产是否已采用、逾期、例外或进入整改。
20. 所有企业级基线都有支持矩阵，能证明支持状态、维护窗口、安全补丁、EOL、最低可接受基线和例外。
21. 所有企业级基线都有发布列车，能证明候选窗口、冻结窗口、晋级日期、通知节奏、黑窗和紧急补丁入口。
22. 所有 L3/L4 资产都有基线符合性声明，能证明资产声明基线、证据路径、例外、签署和采纳总账回写。
23. 所有企业级基线都有制品清单，能证明源文档、schema、示例、控制项、证据模板、脚本、生成物、外部引用、摘要和签名状态。
24. 所有企业级基线都有验证环境锁，能证明 runner、命令、工具版本、策略包、validator、验签工具和生成环境可复现。
25. 所有企业级基线都有通知确认总账，能证明受影响 owner 在冻结前收到通知、完成影响确认，或已有例外、POA&M 或风险接受。
26. 所有企业级基线都有回滚验证记录，能证明上一基线可检出、GitOps revision 可恢复、审计导出可回放、烟测通过且验证未过期。
27. 所有企业级基线都有例外总账，能证明活跃、过期、阻断、条件放行和已关闭例外都有 owner、风险接受、POA&M、补偿控制和关闭证据。
28. 所有企业级基线都有就绪评分卡，能证明硬门禁、评分维度、证据路径、阻断项、baseline/frozen 阈值和最终准入判定。

---

## 15. 风险与应对策略

| 风险       | 表现             | 应对策略               |
| -------- | -------------- | ------------------ |
| 平台集中化   | 平台团队重新变成需求承接中心 | 明确平台只做自助能力，不接管业务逻辑 |
| 领域边界不清   | 服务拆分过细或过粗      | 通过领域建模和业务流程分析逐步校准  |
| 数据产品无人负责 | 数据目录有了，但质量无人管  | 将数据产品责任纳入领域团队职责    |
| 治理过重     | 审批流程拖慢交付       | 优先自动化治理，减少人工审批     |
| 平台不好用    | 团队绕过平台自己搭工具    | 将平台作为产品运营，持续收集反馈   |
| 指标形式化    | SLO 和业务指标只做展示  | 将指标纳入团队复盘和改进机制     |
| 技术先行     | 只建设工具，不改变责任模式  | 架构、组织、流程和度量同步推进    |
| 迁移成本过高   | 老系统复杂，难以一次性重构  | 采用渐进式迁移和绞杀者模式      |
| AI 黑盒化    | Prompt、模型和工具调用不可追溯 | 建立 AI 产品契约、评估集、审计和回放 |
| AI 旁路领域边界 | Agent 直接访问数据库或内部实现 | 只允许调用注册工具、领域 API 和受控工作流 |
| 训练-推理偏斜  | 离线训练和在线推理使用不同口径 | 建立离线/在线特征统一定义和漂移监控 |
| 供应链证据缺失  | 制品无法证明来源和依赖       | 强制 SBOM、provenance、签名和验签 |
| 平台认知负载过高 | 平台功能多但团队不会用       | Platform PM 运营用户旅程和 Golden Path |
| 容器真相源混乱  | 服务目录、部署目录、catalog 和运行状态互相覆盖 | 按源码、镜像、GitOps、Kubernetes、catalog、platform 分层管理 |
| 门禁口径漂移    | 不同团队对同一风险使用不同放行规则，例外长期不过期 | 用合规等级、控制面总账和门禁决策记录统一 pass、fail、exception 和 break-glass 口径 |
| 外部标准漂移    | 生产门禁直接追随 latest，实验性规范变化导致证据格式和 CI 结果不稳定 | 锁定标准版本、标记稳定性、分级采纳，并通过 ADR 和灰度升级 |
| 版本基线漂移    | 文档版本、tag、状态机、审计导出、控制清单和发布证据互相对不上 | 用版本控制面和生命周期状态机绑定 baseline ID、source commit、release tag、允许迁移、兼容窗口和回滚入口 |
| 基线晋级证据缺失 | candidate、baseline 和 frozen 状态切换只有口头结论，没有不可变引用、漂移复核和回滚验证 | 用基线发布证据包记录晋级决策、签名验签、审计摘要、漂移检查和回滚证明 |
| 消费者迁移失控    | breaking change 已经发布，但消费者清单、迁移到期、例外和风险接受没有统一总账 | 用基线兼容性总账聚合契约影响、消费者迁移、未迁移阻断和 POA&M |
| 基线采纳失控    | 企业标准发布了，但领域、平台、数据、AI 和生产资产仍停留在旧基线或采纳状态不可见 | 用基线采纳总账跟踪采用范围、当前基线、目标基线、截止日期、例外和整改 |
| 旧基线长期滞留    | 旧基线没有维护窗口和 EOL，L3/L4 资产长期停留在过期版本 | 用基线支持矩阵声明支持状态、最低可接受基线、安全补丁窗口、迁移目标和 EOL 阻断 |
| 基线发布失控      | 版本升级靠临时会议推进，冻结期仍合入语义变更，消费者通知滞后 | 用基线发布列车约束候选窗口、冻结窗口、晋级日期、黑窗、通知节奏和紧急补丁入口 |
| 采纳证据空心化    | 中央采纳总账显示已采用，但资产仓库没有自己的基线声明和证据路径 | 用基线符合性声明要求资产自声明基线、证据、例外、签署和 rollup 回写 |
| 基线物料不完整    | 签名和审计导出只覆盖部分文件，源 schema、示例或控制项漏入漏出 | 用基线制品清单记录源制品、摘要、必需性、导出关系和未登记制品阻断 |
| 验证环境漂移      | 同一基线在不同 runner、validator 或策略包下得到不同门禁结果 | 用基线验证环境锁固定命令、工具版本、runner 镜像、策略包摘要和验签工具 |
| 通知确认缺失      | 发布列车写了通知节奏，但关键 owner 没有确认影响，异议也没有进入例外或风险接受 | 用基线通知确认总账记录对象、送达、确认、异议、补发、例外和冻结前阻断 |
| 回滚验证空心化    | 文档有回滚字段，但上一基线不可检出、GitOps revision 不存在或审计导出无法恢复 | 用基线回滚验证记录绑定上一基线、回滚目标、GitOps revision、审计导出恢复、烟测结果和验证时效 |
| 例外放行失控      | 例外散落在兼容、采纳、通知、支持、门禁和风险记录里，过期或阻断后仍被发布放行 | 用基线例外总账聚合来源、到期、风险接受、POA&M、补偿控制、关闭证据和冻结阻断 |
| 基线就绪误判      | 局部证据都存在，但没有统一评分和硬门禁，导致未就绪基线被平均分或人工口头判断放行 | 用基线就绪评分卡绑定硬门禁、评分维度、阈值、证据路径、阻断项和最终准入判定 |

---

## 16. 成熟度模型

| 等级      | 特征                       |
| ------- | ------------------------ |
| L1 初始级  | 系统烟囱化，交付依赖人工，数据分散，治理靠审批  |
| L2 规范级  | 建立基础规范，部分系统服务化，开始统一发布和监控 |
| L3 平台级  | 建立内部开发平台，常见工程动作可以自助完成，供应链证据和基础门禁开始自动生成 |
| L4 产品级  | 领域能力、数据能力和首批 AI 能力产品化，控制面能按资产等级阻断或放行发布 |
| L5 自适应级 | 平台、治理、数据、AI、供应链和组织形成持续演进机制，门禁决策、例外、POA&M 和季度复核可闭环 |

---

## 17. 目标状态

本架构最终希望形成以下状态：

1. 业务团队能够快速验证和交付客户价值。
2. 领域能力可以被多个业务场景稳定复用。
3. 数据产品可信、可发现、可消费。
4. 平台能力自助化，减少工单和人工依赖。
5. 治理规则自动化执行，减少低价值审批。
6. 系统运行状态透明，问题可快速定位和恢复。
7. 成本、质量、安全和效率可度量。
8. 架构可以持续演进，而不是依赖一次性大重构。
9. AI 产品可评估、可审计、可回放、可降级，并受到领域边界约束。
10. 生产制品具备 SBOM、签名、provenance 和可验证发布准入。
11. 任意生产发布都能追溯到合规等级、控制项、门禁决策、例外状态和审计证据。
12. 任意外部标准升级都能追溯到版本锁定、影响分析、灰度验证、ADR 和回滚路径。
13. 任意架构基线都能追溯到唯一 baseline ID、source commit、release tag、版本证据包和上一基线回滚入口。
14. 任意基线晋级都能证明不可变引用、漂移复核、开放关键发现、审计导出摘要、验签结果和回滚验证。
15. 任意重大或破坏性基线变更都能证明消费者影响、迁移状态、例外、POA&M、风险接受和弃用截止。
16. 任意企业级基线都能证明组织采纳范围、目标资产采用状态、逾期整改、例外和风险接受。
17. 任意历史基线都能证明支持状态、维护截止、安全补丁截止、EOL、最低可接受基线和迁移目标。
18. 任意企业级基线都能证明所属发布列车、候选窗口、冻结窗口、晋级日期、通知节奏、黑窗和紧急补丁入口。
19. 任意 L3/L4 资产都能证明自己的基线符合性声明、证据路径、签署状态、例外状态和采纳总账回写。
20. 任意企业级基线都能证明自己的源制品全集、摘要、签名状态、导出关系和禁推资产排除状态。
21. 任意企业级基线都能证明自己的验证环境、命令、工具链、策略包、validator 和验签工具没有漂移。
22. 任意企业级基线都能证明受影响 owner 的通知、送达、确认、异议、例外和冻结前完成状态。
23. 任意企业级基线都能证明上一基线可检出、GitOps revision 可恢复、审计导出可回放、烟测通过且验证未过期。
24. 任意企业级基线都能证明所有例外已进入统一总账，且没有过期、无 owner、无风险接受或未关闭的阻断例外。
25. 任意企业级基线都能证明自己的最终就绪评分、硬门禁、阻断项和 baseline/frozen 晋级判定。
26. 任意企业级基线都能证明自己的状态来自生命周期状态机，且每次状态迁移都有允许路径、审批责任、证据引用、状态回写和禁止迁移校验。

---

## 18. 总结

现代企业数字化平台不是一个单一系统，也不是一个巨大共享服务系统，而是一套由领域能力、AI 原生能力、数据产品、内部平台、云原生基础设施、供应链安全和联邦治理共同构成的企业级能力体系。

它的核心转变包括：

1. 从项目交付转向产品运营。
2. 从集中式共享服务转向领域产品网络。
3. 从人工运维转向平台自助。
4. 从中央数据加工转向数据产品化。
5. 从人工审批治理转向自动化护栏。
6. 从技术部门单独负责转向业务技术共同负责结果。
7. 从孤立 AI 试验转向受治理的 AI 产品网络。
8. 从信任构建过程转向验证构建证据和制品来源。

最终目标是让企业在业务快速变化、系统规模扩大、数据复杂度上升和安全合规要求增强的情况下，仍然能够保持高效交付、稳定运行、可信数据和可持续演进。

---

## 19. 深度调研对标结论

本节用于把行业资料转成架构决策，避免参考资料只作为链接堆积。

## 19.1 对标矩阵

| 对标来源 | 关键结论 | 本文档落点 |
| -------- | -------- | ---------- |
| Semantic Versioning / Conventional Commits / Keep a Changelog | 版本号、提交语义和变更记录必须表达兼容性、影响面和升级意图 | 增加 `version-governance.yaml`、`baseline-lifecycle-state-machine.yaml`、`baseline-readiness-scorecard.yaml`、`baseline-rollback-verification.yaml`、`baseline-notification-ledger.yaml`、`baseline-verification-lock.yaml`、`baseline-artifact-inventory.yaml`、`baseline-conformance-claim.yaml`、`baseline-release-train.yaml`、`baseline-support-matrix.yaml`、`baseline-compatibility-ledger.yaml`、发布通道、生命周期状态机、基线不变量、就绪评分、回滚验证、通知确认、验证锁、制品清单、资产声明、发布节奏、支持窗口、兼容窗口、消费者迁移和回滚入口 |
| DORA 2025 | AI 辅助交付必须与组织能力、平台能力和可度量交付质量一起治理 | 补齐 AI 指标、Platform PM、认知负载和 AI 发布门禁 |
| CNCF Platform Engineering Maturity Model | 平台工程成熟度核心是自助、产品化、治理和可度量能力 | 保留 Developer Portal、Golden Path、平台产品契约和平台指标 |
| Team Topologies | 降低团队认知负载是平台团队存在的核心理由之一 | 增加认知负载度量、Platform PM 和平台用户研究 |
| Data Mesh | 数据应由领域负责，并通过产品化、平台自助和联邦治理规模化 | 保留领域数据产品责任、数据契约、联邦治理和数据平台边界 |
| Lakehouse / Open Table Format | 企业通常先需要稳定存储、表格式、血缘和批流底座，再进入完整数据产品网络 | 增加 Lakehouse 到数据产品网络的过渡路径 |
| Feature Store | 训练和推理使用同一特征定义，是避免线上模型偏差的关键机制 | 增加离线特征、在线特征、实时推理端点和训练-推理偏斜检查 |
| OWASP LLM Top 10 | Prompt 注入、敏感信息泄露、过度代理、向量/Embedding 风险和成本消耗是 LLM 应用核心风险 | 增加 AI 安全、Guardrails、工具权限、RAG 权限和成本治理 |
| OWASP Agentic AI | Agent 风险集中在工具误用、过度权限、目标偏移、上下文污染和不可控自动化 | 增加 AI 威胁模型、工具同意、人工确认、出站限制和红队证据 |
| NIST AI RMF / GenAI Profile | AI 风险管理需要覆盖治理、映射、度量和管理闭环 | 增加 AI 风险等级、评估集、审计、回放和人工接管 |
| ISO/IEC 42001 | AI 管理体系要求企业把 AI 风险、责任、过程和持续改进纳入管理系统 | 增加 AI 风险分级、资产证据链和治理到期复审 |
| EU AI Act | 高风险 AI 场景需要更强的数据治理、透明度、人工监督和记录保存 | 增加 R4/R5 风险等级、人工复核和受限场景控制 |
| OpenTelemetry GenAI | 生成式 AI 需要标准化观测模型、Token、模型、系统、操作和成本指标 | 增加 `genai-observability-contract.yaml`、AI Observability 与 GenAI 指标 |
| OpenTelemetry GenAI Stability | GenAI semantic conventions 仍处于 Development 状态，生产基线必须锁定版本并控制 opt-in | 增加 `standards-baseline.yaml`，把 Development 状态标准默认设为 observe 而不是全局 enforce |
| MCP / A2A | Agent 生态正在走向工具、上下文和 Agent 协作协议化 | 增加 Agent 协议与工具边界，避免协议绕过治理 |
| OpenFeature | Feature Flag 需要标准化评估上下文、默认值、hook、tracking 和 provider 边界 | 增加发布开关、Kill Switch、曝光事件、灰度策略和 SLO 燃尽回滚 |
| OpenLineage | 数据运行血缘需要以 Job、Run、Dataset、输入输出和事件为核心证据 | 增加 `lineage-event.yaml` 和数据产品运行血缘门禁 |
| CNCF Platforms White Paper | 平台应作为产品服务业务团队，降低认知负载并提高自助交付能力 | 增加 Platform PM、Golden Path、开发者满意度、认知负载和平台产品指标 |
| NIST Privacy Framework | 隐私风险需要围绕数据处理目的、主体权利、控制、沟通和保护形成管理闭环 | 增加 `privacy-impact-assessment.yaml`、DPIA、删除传播和 AI 使用限制 |
| Kubernetes Multi-tenancy / ResourceQuota | 多团队或多租户 Kubernetes 需要 namespace、配额、网络隔离和准入策略配合 | 增加 `tenant-boundary.yaml`、ResourceQuota、NetworkPolicy 默认拒绝和准入策略证据 |
| NIST Cybersecurity Framework 2.0 | 企业安全运营需要把识别、保护、检测、响应和恢复连接成证据闭环 | 增加访问复核、密钥轮换、漏洞修复、事故复盘和证据新鲜度控制项 |
| NIST SP 800-61 | 事件响应需要准备、检测分析、遏制恢复和事后活动闭环 | 增加 `incident-postmortem.yaml`、纠正行动、runbook 更新和门禁反哺 |
| NIST OSCAL / NIST SP 800-128 | 安全和合规控制应尽量使用机器可读目录、实施状态、评估结果、配置变更控制和证据包组织 | 增加 `control-evidence-map.yaml`、`audit-export-manifest.yaml`、`control-assessment-report.yaml`、`baseline-change-record.yaml`、`oscal-export-profile.yaml` 和审计导出证据 |
| Kubernetes Secrets | Kubernetes Secret 需要加密、访问控制、轮换和外部密钥系统配合 | 增加 `secrets-rotation-evidence.yaml`、KMS、轮换和泄露扫描证据 |
| CISA KEV Catalog | 已知被利用漏洞需要优先、限期、可证明地处置 | 增加 `vulnerability-remediation-evidence.yaml`、KEV 状态、修复 SLA 和残余风险 |
| SLSA / SBOM / Sigstore | 现代供应链安全必须证明构建来源、依赖、产物和签名验签链路 | 增加 SBOM、provenance、签名、验签和发布准入 |
| NIST SSDF / CISA Secure by Design | 安全应前移到需求、设计、编码、构建、测试、发布和响应全链路 | 增加安全开发证据、威胁建模和安全准入材料 |
| NIST AI RMF Critical Infrastructure Profile Concept Note | 高风险、关键基础设施相关 AI 场景需要更强的生命周期风险管理和可追溯实践 | 将关键基础设施 AI 相关资料纳入标准基线观察项，不直接当作稳定强制门禁 |
| FinOps Framework / FOCUS / OpenCost | 成本治理需要统一成本语义、分摊、优化和持续运营 | 增加 `cost-allocation-evidence.yaml`、FinOps 运行机制、成本分摊证据和 AI 单任务成本指标 |
| Open Data Contract | 数据产品需要机器可读契约来约束 Schema、语义、质量、权限和变更 | 增加数据契约最低字段和 CI 校验要求 |
| MLflow / Model Cards | 微调模型需要实验追踪、模型登记、评估结果和模型说明卡 | 增加微调治理工作流、微调发布流程和模型证据链 |
| Google SAIF / AI Incident Response | AI 系统需要面向模型、数据、Prompt、工具和供应商的专门响应流程 | 增加 AI 事件响应机制和 playbook 模板 |
| OPA / Cedar / Kyverno | Policy as Code 需要明确策略语言和执行边界 | 增加策略语言统一口径和策略引擎分工 |
| Kubernetes / OpenGitOps | 容器运行状态和部署期望状态应分离，部署声明需要版本化、可审计和可回滚 | 增加微服务容器分层真相源、Kubernetes base 和 GitOps overlay |
| OCI Image Spec / Container Registry | 镜像制品应放在 registry 中，生产部署需要可追溯到不可变 digest | 增加镜像 tag / digest、registry 和供应链证据要求 |
| Backstage Catalog | 服务目录用于发现、owner、依赖和运行指针，不应成为 deployment manifest 真相源 | 增加 catalog runtime 指针和部署真相源边界 |

## 19.2 研究后的架构判断

1. AI Mesh 是本文档采用的架构归纳，不是单一正式标准。落地时应使用更具体的协议和平台能力承载它，例如 Tool Registry、MCP、A2A、LLM Gateway、Agent Runtime 和统一审计。
2. 数据产品网络和 AI 原生能力不能分离建设。没有数据产品、特征产品、向量索引和评估数据集，AI 产品会退化为 Prompt 工程和不可追溯试验。
3. 平台工程不是工具堆叠。真正的内部平台必须减少认知负载，并把安全、供应链、可观测性、成本和 AI 治理作为默认路径。
4. Lakehouse 不是 Data Mesh 的反面。Lakehouse 更像底座，Data Mesh 更像责任和消费模型；企业应先稳定数据底座，再把高价值数据集逐步产品化。
5. 供应链安全不应停留在漏洞扫描。2026 年企业级基线应至少覆盖 SBOM、provenance、签名、验签和准入策略。
6. AI 治理不应只交给合规团队。它必须进入开发、评估、灰度、运行、成本和复盘流程，否则模型能力越强，系统不可控面越大。
7. AI 风险分级必须影响工程默认值。低风险场景强调效率，高风险场景强调人工监督、记录保存、独立评审和退出机制。
8. 成本已经成为架构属性。模型调用、GPU、向量数据库、在线特征和评估流水线必须像延迟、可用性和安全一样被设计和度量。
9. 数据契约是数据产品网络的工程抓手。没有机器可读契约，Data Mesh 会退化为目录和口头语义。
10. 安全开发证据应自动生成和挂接 catalog。人工补审计材料说明平台治理还没有真正产品化。
11. 微调治理必须独立于基础模型治理。微调会改变模型行为，必须重新做数据授权、实验追踪、评估、登记和发布准入。
12. AI 事件响应必须有专门 playbook。AI 故障经常不是服务宕机，而是质量退化、工具失控、检索污染、模型供应商异常或成本失控。
13. Policy as Code 的价值在于统一规则执行和测试，不在于每个团队自由选择策略语言。
14. 微服务容器不是一个目录里的对象，而是一组跨源码、制品库、GitOps、Kubernetes、catalog 和治理规则的可追溯链路。
15. 生产部署必须从“使用哪个 tag”升级为“使用哪个 digest、由谁构建、通过了什么证明、由哪个 GitOps revision 推进”。

## 19.3 当前文档仍需按企业场景裁剪

本文档提供目标架构和落地基线，但不同企业仍应按以下因素裁剪：

1. 行业合规强度：金融、医疗、政务和跨境业务需要更高 AI 审计、数据出境和供应链证明要求。
2. 数据成熟度：如果当前只有基础数据仓库，应先走 Lakehouse 和数据产品试点，不应直接全量推 Data Mesh。
3. AI 风险等级：内部知识问答、客服辅助、自动退款、信贷审批和医疗建议的治理等级完全不同。
4. 团队能力：平台、数据、安全和 AI 团队不成熟时，应优先做 Golden Path 和小范围试点。
5. 成本边界：GPU、模型调用、向量检索、在线特征和评估流水线必须有预算和配额。

---

## 20. 参考资料

- AWS Prescriptive Guidance: Internal Developer Platform
  <https://docs.aws.amazon.com/prescriptive-guidance/latest/internal-developer-platform/introduction.html>
- CNCF TAG App Delivery: Platform Engineering Maturity Model
  <https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/>
- Thoughtworks Technology Radar: Platform Engineering Product Teams
  <https://www.thoughtworks.com/en-us/radar/techniques/platform-engineering-product-teams>
- Martin Fowler: Data Mesh Principles and Logical Architecture
  <https://martinfowler.com/articles/data-mesh-principles.html>
- Team Topologies: Key Concepts
  <https://teamtopologies.com/key-concepts>
- Backstage Docs: Software Catalog System Model
  <https://backstage.io/docs/features/software-catalog/system-model/>
- Backstage Docs: Kubernetes Plugin
  <https://backstage.io/docs/features/kubernetes/>
- Kubernetes Documentation: Workloads
  <https://kubernetes.io/docs/concepts/workloads/>
- Kubernetes Documentation: Images
  <https://kubernetes.io/docs/concepts/containers/images/>
- OpenGitOps Principles
  <https://opengitops.dev/>
- Semantic Versioning 2.0.0
  <https://semver.org/spec/v2.0.0.html>
- Conventional Commits 1.0.0
  <https://www.conventionalcommits.org/en/v1.0.0/>
- Keep a Changelog
  <https://keepachangelog.com/>
- Argo CD Documentation
  <https://argo-cd.readthedocs.io/>
- Flux Documentation
  <https://fluxcd.io/flux/>
- Open Container Initiative Image Specification
  <https://github.com/opencontainers/image-spec>
- OpenAPI Specification
  <https://spec.openapis.org/oas/latest.html>
- AsyncAPI Specification
  <https://www.asyncapi.com/docs/reference/specification/latest>
- OpenTelemetry Documentation
  <https://opentelemetry.io/docs/>
- OpenTelemetry Semantic Conventions for Generative AI Systems
  <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- OpenTelemetry Semantic Conventions 1.41.0
  <https://opentelemetry.io/docs/specs/semconv/>
- DORA Research: 2025 DORA Report
  <https://dora.dev/research/2025/dora-report/>
- SLSA Specification v1.2
  <https://slsa.dev/spec/v1.2/>
- CISA: Software Bill of Materials
  <https://www.cisa.gov/sbom>
- SPDX
  <https://spdx.dev/>
- SPDX Specifications
  <https://spdx.dev/use/specifications/>
- CycloneDX
  <https://cyclonedx.org/>
- CycloneDX Specification Overview
  <https://cyclonedx.org/specification/overview/>
- Sigstore Cosign
  <https://docs.sigstore.dev/cosign/>
- Sigstore Policy Controller
  <https://docs.sigstore.dev/policy-controller/overview/>
- OpenSSF Scorecard
  <https://github.com/ossf/scorecard>
- NIST AI Risk Management Framework
  <https://www.nist.gov/itl/ai-risk-management-framework>
- NIST AI 600-1: Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile
  <https://doi.org/10.6028/NIST.AI.600-1>
- NIST AI RMF Profile on Trustworthy AI in Critical Infrastructure Concept Note
  <https://www.nist.gov/programs-projects/concept-note-ai-rmf-profile-trustworthy-ai-critical-infrastructure>
- NIST SP 800-218: Secure Software Development Framework
  <https://csrc.nist.gov/pubs/sp/800/218/final>
- NIST Privacy Framework
  <https://www.nist.gov/privacy-framework>
- NIST Cybersecurity Framework 2.0
  <https://www.nist.gov/cyberframework>
- NIST SP 800-61 Rev. 2: Computer Security Incident Handling Guide
  <https://csrc.nist.gov/pubs/sp/800/61/r2/final>
- NIST OSCAL
  <https://pages.nist.gov/OSCAL/>
- CISA: Secure by Design
  <https://www.cisa.gov/securebydesign>
- CISA: Known Exploited Vulnerabilities Catalog
  <https://www.cisa.gov/known-exploited-vulnerabilities-catalog>
- ISO/IEC 42001 Artificial Intelligence Management System
  <https://www.iso.org/standard/81230.html>
- European Commission: AI Act
  <https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai>
- OWASP Top 10 for Large Language Model Applications
  <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- OWASP Generative AI Security
  <https://genai.owasp.org/>
- Model Context Protocol Specification
  <https://modelcontextprotocol.io/specification/2025-06-18>
- Agent2Agent Protocol
  <https://github.com/a2aproject/A2A>
- OpenFeature Specification
  <https://openfeature.dev/specification/>
- OpenLineage Documentation
  <https://openlineage.io/docs/>
- CNCF TAG App Delivery: Platforms White Paper
  <https://tag-app-delivery.cncf.io/whitepapers/platforms/>
- Kubernetes Documentation: Multi-tenancy
  <https://kubernetes.io/docs/concepts/security/multi-tenancy/>
- Kubernetes Documentation: Resource Quotas
  <https://kubernetes.io/docs/concepts/policy/resource-quotas/>
- Kubernetes Documentation: Secrets
  <https://kubernetes.io/docs/concepts/configuration/secret/>
- MLflow: AI Engineering Platform for LLMs and Agents
  <https://mlflow.org/docs/latest/genai/>
- MLflow Tracking
  <https://mlflow.org/docs/latest/ml/tracking/>
- Hugging Face Model Cards
  <https://huggingface.co/docs/hub/model-cards>
- Google Secure AI Framework
  <https://saif.google/>
- Open Policy Agent
  <https://github.com/open-policy-agent/opa>
- Cedar Policy Language
  <https://docs.cedarpolicy.com/>
- Kyverno
  <https://kyverno.io/docs/>
- Feast: Open Source Feature Store
  <https://docs.feast.dev/>
- Apache Iceberg
  <https://iceberg.apache.org/>
- Milvus GitHub Repository
  <https://github.com/milvus-io/milvus>
- FinOps Framework
  <https://www.finops.org/framework/>
- FOCUS: FinOps Open Cost and Usage Specification
  <https://focus.finops.org/>
- OpenCost Documentation
  <https://opencost.io/docs/>
- Open Data Contract Standard
  <https://bitol-io.github.io/open-data-contract-standard/latest/>
- Google SRE Workbook: Implementing SLOs
  <https://sre.google/workbook/implementing-slos/>
