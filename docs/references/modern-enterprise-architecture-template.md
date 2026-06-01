# 现代企业数字化平台架构说明文档

**文档版本**：V2.1
**适用对象**：企业管理层、产品负责人、架构师、研发负责人、数据负责人、平台团队、安全合规团队
**适用范围**：中大型企业数字化平台建设、业务系统重构、平台工程建设、数据产品化、组织协同机制设计
**文档定位**：本文件用于说明现代企业数字化平台的总体架构、核心组成、团队职责、治理机制、技术原则和落地路径。
**专项修订**：V2.1 在 V2.0 starter kit 基础上增强 schema 嵌套约束、格式校验、跨文件一致性检查和 CI 门禁口径。

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
| `V2.1` | `Baseline Candidate` | 用作可执行企业标准起点；包含 starter kit、schema、示例、嵌套约束、跨文件一致性和自动化校验入口 |

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
4. 索引同步：同步更新 `docs/README.md`、`docs/references/README.md`、`metadata/taxonomy.yml` 和 AI 引用语料入口。
5. 链接校验：仓库内 Markdown 链接和锚点必须通过检查。
6. 格式校验：Markdown lint 和文档结构检查必须通过。
7. 回滚入口：保留上一版本引用、Git commit 或变更记录，保证可以回退到上一基线。

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

### 0.6 版本记录

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

### 0.7 V2.1 可执行企业标准路线图

V2.0 已将 V1.9 的文档化基线转化为第一批可执行资产。V2.1 继续把字段约束、示例一致性和远程 CI 门禁补强为可执行口径。后续 `V2.x` 迭代应继续扩大 schema 覆盖、补充示例仓库，并把平台、catalog、GitOps 和审计系统连接起来。

V2.1 起点包括：

1. 真相源字段矩阵：明确 `domain.yaml`、`service.yaml`、`ai-product.yaml`、`data-product.yaml`、catalog、GitOps 和 runtime 的字段权威。
2. 契约模板：提供服务、领域、数据产品、AI 产品、Agent 工具、RAG、微调、GitOps 和生产就绪模板。
3. 自动化门禁：把 API、事件、数据契约、AI 门禁、SBOM、签名、SLO、成本标签和 catalog entry 纳入 CI。
4. RACI：明确架构组、领域团队、平台团队、数据团队、安全团队、AI 产品团队、SRE 和业务 owner 的决策权。
5. 仓库拓扑剖面：覆盖 monorepo、多仓、独立 GitOps 仓、平台仓和数据仓的适配模式。
6. 可靠性分级：补齐 Tier-1 / Tier-2 / Tier-3、RTO、RPO、灾备演练、错误预算和 on-call 升级路径。
7. 迁移与弃用：定义旧系统绞杀迁移、API 版本弃用、数据产品兼容、AI 模型退役和平台能力下线流程。
8. 验证包：提供 `make test`、schema 校验、示例仓库和审计证据清单，证明标准可以落地执行。
9. Starter Kit：提供 `docs/references/modern-enterprise-architecture-kit/` 下的 schema、示例、嵌套字段校验、格式校验和示例跨文件一致性检查。

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
│   ├── release-evidence-checklist.md
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
governance/evidence/release-evidence-checklist.md
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
runbook: docs/runbook.md
rollback: docs/rollback.md
```

`data-product.yaml` 最低字段：

```yaml
dataProduct: order-facts
domain: order
owner: team-order
lifecycle: production
schema: schema/order-facts.schema.yaml
semanticGrain: one row per order state transition
freshness: 15m
quality:
  completeness: ">= 99.5%"
  uniqueness: order_event_id
classification:
  level: confidential
  pii:
    - customer_id
lineage:
  upstream:
    - order-command-service
  downstream:
    - revenue-dashboard
aiUsage:
  allowed:
    - rag
    - evaluation
  disallowed:
    - foundation-model-training
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
prompts:
  system: prompts/system.prompt.md
rag:
  sources: rag/sources.yaml
  vectorIndex: vector:customer-support-policy:v12
tools:
  - tool: refund-preview
    requiresHumanApproval: true
evals:
  regression: evals/regression.yaml
  redTeam: evals/red-team.yaml
guardrails:
  policy: guardrails/policy.rego
observability:
  traceRetentionDays: 180
  replayEnabled: true
```

### 10.10.3 自动化门禁映射

门禁必须尽量前移到提交、构建、发布和运行阶段。人工评审只处理边界争议、风险接受和复杂权衡。

| 阶段 | 自动化门禁 | 输入 | 阻断条件 |
| ---- | ---------- | ---- | -------- |
| 提交 | Markdown、YAML、Schema、Policy 语法检查 | 文档、契约、策略文件 | 语法错误、坏链接、缺失必填字段 |
| Pull Request | API / Event / Data / AI 契约兼容性检查 | `contracts/`、`domains/`、`ai/` | breaking change 无消费者影响分析 |
| 构建 | 单元测试、依赖锁定、漏洞、许可证、密钥扫描 | 源码、锁文件、Dockerfile | 高危漏洞、未知许可证、密钥泄露 |
| 制品 | SBOM、provenance、镜像签名、基础镜像策略 | 镜像、构建日志、制品摘要 | 无 SBOM、无签名、来源不可证明 |
| 发布 | GitOps diff、策略准入、资源配额、SLO 和 runbook 校验 | GitOps overlay、catalog、service.yaml | 无 owner、无 runbook、无 digest、资源未声明 |
| AI 发布 | 评估集、红队、RAG 权限、工具权限、人工确认策略 | `ai-product.yaml`、`contracts/ai/` | 高风险工具无人工确认、评估未达标 |
| 数据发布 | schema、质量规则、权限、血缘、freshness 校验 | `data-product.yaml`、数据契约 | 无质量规则、无分级分类、无下游通知 |
| 运行 | SLO、成本、漂移、异常调用、供应链策略漂移 | runtime、observability、audit | 错误预算耗尽、成本超预算、策略漂移 |

### 10.10.4 漂移检测规则

可执行标准必须能发现“文档这么写、运行不是这样”的漂移。

必须检测的漂移：

1. `service.yaml` 的 owner、domain、端口、依赖和 catalog entry 不一致。
2. catalog 指向的 GitOps 路径不存在，或 GitOps 路径指向的服务没有 catalog entry。
3. GitOps 使用的镜像 tag 无法解析到不可变 digest。
4. 生产 Deployment 的镜像 digest 与 GitOps 期望状态不一致。
5. Kubernetes runtime 存在未登记到 catalog 的长期运行工作负载。
6. 数据产品 schema 与实际表结构或数据契约不一致。
7. AI 产品运行中的 Prompt、模型、RAG 索引或工具版本与 `ai-product.yaml` 不一致。
8. 策略例外超过到期时间仍在生产准入中生效。

漂移处理规则：

1. 发现漂移后先判断权威真相源，再决定修正 Git、catalog、runtime 还是治理例外。
2. 运行时紧急修复必须在事后回写 GitOps 或形成 incident / postmortem，不能长期保留手工状态。
3. catalog 漂移优先通过重新生成或重新校验修复，不应手工覆盖源头契约。
4. 涉及生产安全、AI 高风险工具、数据权限和供应链证明的漂移必须阻断发布。

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

### 10.12.3 数据、AI 和平台能力退役

退役流程必须处理数据、权限、成本和审计尾部：

1. 数据产品退役必须确认保留期限、归档位置、删除策略、下游血缘和 AI 使用授权。
2. AI 产品退役必须冻结模型路由、Prompt、RAG 索引、工具权限和审计日志保留策略。
3. 平台能力退役必须提供替代 Golden Path、迁移窗口、自动化迁移脚本和例外清单。
4. 基础设施退役必须确认 DNS、证书、密钥、网络策略、备份、成本标签和监控告警全部清理。

## 10.13 验证包与审计证据清单

可执行企业标准必须能被验证。没有验证包，架构文档只能证明“写过”，不能证明“做到”。

### 10.13.1 最小验证包

每个试点领域至少提供以下验证包：

本仓库提供第一批可执行 starter kit：

```text
docs/references/modern-enterprise-architecture-kit/
```

该目录的 schema 和示例由以下命令校验：

```bash
make check-modern-architecture-kit
```

该命令是仓库内零依赖 starter gate，用于校验本仓库示例的 JSON Schema 子集、YAML 示例、嵌套必填字段、格式约束和示例间一致性。企业生产落地时应优先接入成熟校验器，例如 JSON Schema draft 2020-12 validator、YAML parser、OpenAPI / AsyncAPI checker、OPA / Cedar / Kyverno policy test 和 GitOps diff 工具；本仓库脚本只作为 starter kit 的最小可执行证明。

```text
governance/evidence/release-evidence-checklist.md
governance/evidence/audit-evidence-index.md
governance/evidence/drill-evidence-template.md
catalog/components/{service}.yaml
catalog/data-products/{data-product}.yaml
catalog/ai-products/{ai-product}.yaml
contracts/apis/{api}.openapi.yaml
contracts/events/{event}.asyncapi.yaml
contracts/datasets/{data-product}.yaml
contracts/ai/tools/{tool}.yaml
infra/gitops/environments/prod/{domain}/{service}/kustomization.yaml
```

验证命令应至少覆盖：

```bash
make lint
make check-links
make check-doc-structure
make check-metadata
make check-ai-citation
make check-modern-architecture-kit
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
governance/migration/deprecation-policy.md
governance/evidence/release-evidence-checklist.md
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

---

## 16. 成熟度模型

| 等级      | 特征                       |
| ------- | ------------------------ |
| L1 初始级  | 系统烟囱化，交付依赖人工，数据分散，治理靠审批  |
| L2 规范级  | 建立基础规范，部分系统服务化，开始统一发布和监控 |
| L3 平台级  | 建立内部开发平台，常见工程动作可以自助完成，供应链证据开始自动生成 |
| L4 产品级  | 领域能力、数据能力和首批 AI 能力产品化，团队对结果负责 |
| L5 自适应级 | 平台、治理、数据、AI、供应链和组织形成持续演进机制 |

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
| DORA 2025 | AI 辅助交付必须与组织能力、平台能力和可度量交付质量一起治理 | 补齐 AI 指标、Platform PM、认知负载和 AI 发布门禁 |
| CNCF Platform Engineering Maturity Model | 平台工程成熟度核心是自助、产品化、治理和可度量能力 | 保留 Developer Portal、Golden Path、平台产品契约和平台指标 |
| Team Topologies | 降低团队认知负载是平台团队存在的核心理由之一 | 增加认知负载度量、Platform PM 和平台用户研究 |
| Data Mesh | 数据应由领域负责，并通过产品化、平台自助和联邦治理规模化 | 保留领域数据产品责任、数据契约、联邦治理和数据平台边界 |
| Lakehouse / Open Table Format | 企业通常先需要稳定存储、表格式、血缘和批流底座，再进入完整数据产品网络 | 增加 Lakehouse 到数据产品网络的过渡路径 |
| Feature Store | 训练和推理使用同一特征定义，是避免线上模型偏差的关键机制 | 增加离线特征、在线特征、实时推理端点和训练-推理偏斜检查 |
| OWASP LLM Top 10 | Prompt 注入、敏感信息泄露、过度代理、向量/Embedding 风险和成本消耗是 LLM 应用核心风险 | 增加 AI 安全、Guardrails、工具权限、RAG 权限和成本治理 |
| NIST AI RMF / GenAI Profile | AI 风险管理需要覆盖治理、映射、度量和管理闭环 | 增加 AI 风险等级、评估集、审计、回放和人工接管 |
| ISO/IEC 42001 | AI 管理体系要求企业把 AI 风险、责任、过程和持续改进纳入管理系统 | 增加 AI 风险分级、资产证据链和治理到期复审 |
| EU AI Act | 高风险 AI 场景需要更强的数据治理、透明度、人工监督和记录保存 | 增加 R4/R5 风险等级、人工复核和受限场景控制 |
| OpenTelemetry GenAI | 生成式 AI 需要标准化观测模型、Token、模型、系统、操作和成本指标 | 增加 AI Observability 与 GenAI 指标 |
| MCP / A2A | Agent 生态正在走向工具、上下文和 Agent 协作协议化 | 增加 Agent 协议与工具边界，避免协议绕过治理 |
| SLSA / SBOM / Sigstore | 现代供应链安全必须证明构建来源、依赖、产物和签名验签链路 | 增加 SBOM、provenance、签名、验签和发布准入 |
| NIST SSDF / CISA Secure by Design | 安全应前移到需求、设计、编码、构建、测试、发布和响应全链路 | 增加安全开发证据、威胁建模和安全准入材料 |
| FinOps Framework / FOCUS | 成本治理需要统一成本语义、分摊、优化和持续运营 | 增加 FinOps 运行机制和 AI 单任务成本指标 |
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
- DORA Research: 2025 DORA Report
  <https://dora.dev/research/2025/dora-report/>
- SLSA Specification v1.2
  <https://slsa.dev/spec/v1.2/>
- CISA: Software Bill of Materials
  <https://www.cisa.gov/sbom>
- SPDX
  <https://spdx.dev/>
- CycloneDX
  <https://cyclonedx.org/>
- Sigstore Cosign
  <https://docs.sigstore.dev/cosign/>
- Sigstore Policy Controller
  <https://docs.sigstore.dev/policy-controller/overview/>
- OpenSSF Scorecard
  <https://scorecard.dev/>
- NIST AI Risk Management Framework
  <https://www.nist.gov/itl/ai-risk-management-framework>
- NIST AI 600-1: Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile
  <https://doi.org/10.6028/NIST.AI.600-1>
- NIST SP 800-218: Secure Software Development Framework
  <https://csrc.nist.gov/pubs/sp/800/218/final>
- CISA: Secure by Design
  <https://www.cisa.gov/securebydesign>
- ISO/IEC 42001 Artificial Intelligence Management System
  <https://www.iso.org/standard/81230.html>
- European Commission: AI Act
  <https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai>
- OWASP Top 10 for Large Language Model Applications
  <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- OpenTelemetry Semantic Conventions for Generative AI Systems
  <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- Model Context Protocol Specification
  <https://modelcontextprotocol.io/specification/2025-06-18>
- Agent2Agent Protocol
  <https://github.com/a2aproject/A2A>
- MLflow: AI Engineering Platform for LLMs and Agents
  <https://mlflow.org/docs/latest/genai/>
- MLflow Tracking
  <https://mlflow.org/docs/latest/ml/tracking/>
- Hugging Face Model Cards
  <https://huggingface.co/docs/hub/model-cards>
- Google Secure AI Framework
  <https://saif.google/>
- Open Policy Agent
  <https://www.openpolicyagent.org/docs/latest/>
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
- Open Data Contract Standard
  <https://bitol-io.github.io/open-data-contract-standard/latest/>
- Google SRE Workbook: Implementing SLOs
  <https://sre.google/workbook/implementing-slos/>
