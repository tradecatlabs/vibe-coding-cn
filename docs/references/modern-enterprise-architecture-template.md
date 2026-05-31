# 现代企业数字化平台架构说明文档

**文档版本**：V1.0
**适用对象**：企业管理层、产品负责人、架构师、研发负责人、数据负责人、平台团队、安全合规团队
**适用范围**：中大型企业数字化平台建设、业务系统重构、平台工程建设、数据产品化、组织协同机制设计
**文档定位**：本文件用于说明现代企业数字化平台的总体架构、核心组成、团队职责、治理机制、技术原则和落地路径。

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

现代企业数字化平台由六个纵向层级和一个横向治理平面组成。

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
三、领域能力产品层
用户域 / 商品域 / 订单域 / 支付域 / 履约域 / 风控域 / 营销域 / 内容域
        │
        ▼
四、数据产品网络层
Source-aligned Data Product / Aggregate Data Product / Consumer-aligned Data Product
指标层 / 语义层 / 特征层 / 报表 / AI 数据服务
        │
        ▼
五、自助式平台工程层
Developer Portal / Golden Path / CI/CD / IaC / GitOps / Kubernetes / 可观测性
        │
        ▼
六、基础设施与云原生层
Cloud / Kubernetes / Network / Storage / Database / Queue / Cache / Search

横向贯穿：
联邦治理平面
身份权限 / API 标准 / 数据契约 / 安全策略 / 合规审计 / 架构决策
SLO / 成本规则 / 质量门禁 / Policy as Code / 自动化检测
```

架构核心可以概括为：

> 现代企业数字化平台 = 前台体验 + 体验编排 + 领域能力产品 + 数据产品网络 + 自助式平台工程 + 云原生基础设施 + 联邦治理。

## 2.1 推荐项目目录结构

落到工程仓库时，应把不同类型的“真相源”分开，避免把架构、契约、运行、治理和文档混成一个目录。

```text
repo/
├── apps/                                # 前台体验：Web、App、后台、门户、AI 体验
│   ├── web/
│   ├── mobile/
│   ├── admin/
│   ├── partner-portal/
│   ├── open-api-portal/
│   └── ai-experiences/
│
├── domains/                             # 领域能力产品网络
│   ├── customer/
│   │   ├── domain.yaml                  # 领域边界、owner、SLO、上下游依赖
│   │   ├── apis/                        # 领域 API 契约
│   │   ├── events/                      # 领域事件契约
│   │   ├── services/                    # 领域服务运行单元
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
├── platform/                            # 内部开发平台和自助工程能力
│   ├── portal/
│   ├── golden-paths/
│   ├── scaffolds/
│   ├── orchestration/
│   ├── ci-cd/
│   ├── environments/
│   ├── observability/
│   ├── security/
│   ├── data-platform/
│   ├── ai-platform/
│   ├── cost/
│   ├── developer-tools/
│   ├── scorecards/
│   └── docs/
│
├── contracts/                           # 跨团队机器可读契约
│   ├── apis/
│   ├── events/
│   ├── schemas/
│   ├── datasets/
│   ├── resources/
│   └── policies/
│
├── catalog/                             # 软件、资源、API、数据产品和 owner 目录
│   ├── systems/
│   ├── components/
│   ├── resources/
│   ├── apis/
│   ├── data-products/
│   ├── domains/
│   └── scorecards/
│
├── governance/                          # 联邦治理资产
│   ├── standards/
│   ├── decisions/
│   ├── ownership/
│   ├── slo/
│   ├── security/
│   ├── data-governance/
│   ├── architecture-gates/
│   ├── risk-register/
│   ├── postmortems/
│   └── playbooks/
│
├── infra/                               # 云原生基础设施和运行底座
│   ├── cloud/
│   ├── kubernetes/
│   ├── gitops/
│   ├── networking/
│   ├── databases/
│   ├── messaging/
│   ├── storage/
│   ├── secrets/
│   ├── disaster-recovery/
│   └── environments/
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
| `domains/` | 业务能力、领域模型、领域服务和数据产品真相 | 平台通用工具、跨域集中审批 |
| `platform/` | 内部开发者体验和自助工程能力真相 | 业务规则和领域模型 |
| `contracts/` | API、事件、Schema、数据集和策略契约真相 | 普通说明文档 |
| `catalog/` | 系统、组件、资源、owner 和生命周期真相 | 运行逻辑 |
| `governance/` | 标准、决策、门禁、风险和复盘真相 | 业务代码 |
| `infra/` | 云资源、运行环境、安全、网络和灾备真相 | 业务逻辑 |
| `shared/` | 无业务语义的薄复用真相 | 领域模型和业务流程 |

---

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

## 4.3 领域能力产品层

### 4.3.1 定位

领域能力产品层是企业数字化平台的核心层。它承载企业关键业务能力，并以领域产品的方式长期运营。

### 4.3.2 典型领域划分

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

### 4.3.3 每个领域产品必须具备的内容

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

### 4.3.4 领域服务交互方式

领域之间优先采用以下方式协作：

1. 同步 API：用于强一致、实时查询或明确请求响应的场景。
2. 领域事件：用于状态变化通知、异步解耦和最终一致性场景。
3. 数据产品：用于分析、报表、AI、特征和跨域洞察场景。
4. 工作流编排：用于跨领域长流程和补偿机制。

### 4.3.5 领域边界原则

1. 一个领域拥有自己的核心模型。
2. 一个领域拥有自己的核心数据。
3. 其他领域不能直接读写该领域数据库。
4. 跨领域协作通过 API、事件或数据产品完成。
5. 领域团队对业务规则、接口稳定性和运行质量负责。

### 4.3.6 领域产品标准目录

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

### 4.3.7 领域服务运行契约

领域服务必须是可以独立启动、停止、测试、部署、扩缩容和回滚的运行边界。

```text
domains/order/services/order-command-service/
├── src/
├── tests/
├── deploy/
├── configs/
├── service.yaml
├── catalog-info.yaml
├── Dockerfile
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
slo:
  availability: 99.95
  latencyP95Ms: 300
operations:
  health: /health
  readiness: /ready
  runbook: docs/runbook.md
  rollback: deploy/rollback.md
```

---

## 4.4 数据产品网络层

### 4.4.1 定位

数据产品网络层负责将各领域产生的数据转化为可信、可发现、可理解、可复用的数据产品，为经营分析、业务运营、风险控制、AI 应用和管理决策提供支撑。

### 4.4.2 数据产品类型

| 类型                            | 说明                      | 示例                |
| ----------------------------- | ----------------------- | ----------------- |
| Source-aligned Data Product   | 源对齐数据产品，由领域团队基于原始业务数据发布 | 订单明细数据产品、支付流水数据产品 |
| Aggregate Data Product        | 聚合数据产品，对多个源数据产品进行汇总加工   | 用户交易汇总、商品销售汇总     |
| Consumer-aligned Data Product | 面向具体消费场景的数据产品           | 经营驾驶舱、风控特征集、营销人群包 |

### 4.4.3 数据产品基本要求

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

### 4.4.4 数据能力组成

数据产品网络层包括：

1. 数据目录。
2. 元数据管理。
3. 数据血缘。
4. 数据质量检测。
5. 指标平台。
6. 语义层。
7. 特征平台。
8. 报表平台。
9. 实时数据服务。
10. AI 数据服务。
11. 数据权限管理。
12. 数据脱敏与审计。

### 4.4.5 数据治理原则

1. 谁产生核心业务数据，谁负责解释数据含义。
2. 谁发布数据产品，谁负责数据质量。
3. 核心指标必须有统一口径。
4. 重要数据必须有血缘、质量规则和变更通知。
5. 敏感数据必须分级、脱敏、授权和审计。
6. 数据消费必须可追踪、可监控、可问责。

### 4.4.6 数据产品标准目录

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
slo:
  freshnessMinutes: 5
  availability: 99.9
```

### 4.4.7 数据平台与领域团队边界

数据平台团队不拥有所有业务数据，它提供让领域团队发布和消费数据产品的自助能力。

```text
领域团队：拥有数据语义、质量承诺、数据产品生命周期和消费方沟通。
数据平台团队：拥有数据目录、Schema Registry、血缘、质量检测、权限和计算平台。
治理团队：拥有分级分类、PII、指标口径、访问策略和跨域质量规则。
```

---

## 4.5 自助式平台工程层

### 4.5.1 定位

自助式平台工程层为业务团队、领域团队和数据团队提供统一的内部开发平台，降低工程复杂度，提高交付效率和治理一致性。

### 4.5.2 平台核心能力

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

### 4.5.3 平台设计目标

平台团队的目标不是集中接管业务开发，而是让业务团队可以自助完成标准工程动作：

1. 自助创建服务。
2. 自助申请环境。
3. 自助配置数据库、缓存、消息队列。
4. 自助发布应用。
5. 自助接入日志、监控和告警。
6. 自助申请权限。
7. 自助查看成本。
8. 自助执行安全和合规检查。

### 4.5.4 Golden Path

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

Golden Path 应尽量内置最佳实践，使团队默认走在安全、合规、稳定和高效的路径上。

### 4.5.5 平台产品契约

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

---

## 4.6 基础设施与云原生层

### 4.6.1 定位

基础设施与云原生层为上层业务系统、数据平台和工程平台提供稳定、安全、弹性和可观测的运行底座。

### 4.6.2 主要组成

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

### 4.6.3 基础设施原则

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

## 5.3 治理模式

治理采用“全局标准 + 领域自治 + 自动化护栏”的模式。

| 治理对象 | 全局规则              | 领域自治   |
| ---- | ----------------- | ------ |
| API  | 命名、鉴权、版本、错误码、限流   | 具体接口设计 |
| 事件   | Schema、命名、版本、兼容策略 | 具体事件含义 |
| 数据   | 分级、脱敏、血缘、质量规则     | 领域数据定义 |
| 安全   | 身份认证、最小权限、漏洞扫描    | 业务权限模型 |
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
8. 审计阶段：访问日志、变更日志、权限日志、数据使用日志。

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
├── data-governance/
│   ├── data-product-review.md
│   ├── pii-policy.md
│   └── retention-policy.md
├── architecture-gates/
│   ├── production-readiness.yaml
│   ├── domain-readiness.yaml
│   └── data-product-readiness.yaml
├── risk-register/
├── postmortems/
└── playbooks/
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

### 8.2.5 治理团队

负责：

1. 架构原则。
2. 标准制定。
3. 治理机制。
4. 合规要求。
5. 规则自动化。
6. 架构评审机制。
7. 治理效果度量。

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
4. Policy 必须通过语法、单元测试和关键路径场景测试。
5. 契约变更必须进入 CI，不能只停留在文档。

## 10.6 软件和数据资产目录

`catalog/` 让系统、服务、API、资源、数据产品、owner 和生命周期可发现。

```text
catalog/
├── systems/
├── components/
├── resources/
├── apis/
├── data-products/
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

## 13.5 性能、成本与规模检查

现代企业数字化平台必须把性能和成本作为治理对象，而不是上线后再补救。

### 13.5.1 复杂度与热点

必须检查：

1. 领域 API 是否处在核心请求链路。
2. 跨领域调用是否形成串行长链。
3. 读路径是否需要查询模型、缓存或物化视图。
4. 写路径是否需要事件驱动和最终一致性。
5. 数据产品是否存在全量扫描、重复计算或过度拉取。
6. AI 场景是否存在重复模型调用、高 token 成本或不可控上下文膨胀。

### 13.5.2 I/O 和外部依赖

以下问题必须显式标记为风险：

1. N+1 API 调用。
2. N+1 数据库查询。
3. 同步调用链过长。
4. 无超时、无重试边界。
5. 无幂等保护。
6. 无背压和限流。
7. 数据管道重复抽取。
8. 无缓存失效策略。

### 13.5.3 数据与存储

必须检查：

1. 每个领域服务是否拥有清晰的数据写入边界。
2. 查询是否有索引、分页和字段裁剪。
3. 大数据处理是否使用 streaming、chunking 或增量计算。
4. 数据产品是否声明 freshness、quality 和 cost owner。
5. 高价值指标是否有可追溯口径和血缘。

### 13.5.4 验证指标

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

输出物：

1. 平台门户。
2. Golden Path。
3. 服务目录。
4. 发布流水线。
5. 可观测性看板。
6. 平台使用手册。
7. 平台运营指标。

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

输出物：

1. 数据产品目录。
2. 指标字典。
3. 数据质量看板。
4. 数据血缘图。
5. 权限审批流程。
6. 数据消费指南。

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

输出物：

1. Policy as Code 规则库。
2. 自动化质量门禁。
3. 安全合规看板。
4. 成本治理看板。
5. 架构治理流程。
6. 审计报告模板。

## 14.6 第六阶段：规模化推广

目标是将试点经验推广到更多业务域和团队。

主要工作：

1. 复制领域产品模式。
2. 扩展平台能力。
3. 扩展数据产品网络。
4. 建立平台运营机制。
5. 建立团队能力培训机制。
6. 建立持续改进机制。

输出物：

1. 企业级领域地图。
2. 领域产品组合。
3. 数据产品网络。
4. 平台能力地图。
5. 团队能力模型。
6. 成熟度评估报告。

## 14.7 最小落地清单

新项目不应一开始把所有目录做满。先从能够建立 owner、contract、catalog、gate 和 runtime baseline 的最小文件开始。

```text
governance/standards/engineering-standard.md
governance/ownership/teams.yaml
governance/architecture-gates/production-readiness.yaml
contracts/apis/README.md
contracts/events/README.md
contracts/datasets/README.md
catalog/systems/README.md
catalog/components/README.md
domains/example/domain.yaml
domains/example/services/example-service/service.yaml
platform/golden-paths/README.md
infra/environments/README.md
```

最小落地目标：

1. 所有生产服务有 owner。
2. 所有跨域接口有契约。
3. 所有生产组件进入 catalog。
4. 所有关键服务有 SLO 和 runbook。
5. 所有生产发布有回滚路径。
6. 所有数据产品有业务语义、质量规则和访问策略。

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

---

## 16. 成熟度模型

| 等级      | 特征                       |
| ------- | ------------------------ |
| L1 初始级  | 系统烟囱化，交付依赖人工，数据分散，治理靠审批  |
| L2 规范级  | 建立基础规范，部分系统服务化，开始统一发布和监控 |
| L3 平台级  | 建立内部开发平台，常见工程动作可以自助完成    |
| L4 产品级  | 领域能力和数据能力产品化，团队对结果负责     |
| L5 自适应级 | 平台、治理、数据和组织形成持续演进机制      |

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

---

## 18. 总结

现代企业数字化平台不是一个单一系统，也不是一个巨大共享服务系统，而是一套由领域能力、数据产品、内部平台、云原生基础设施和联邦治理共同构成的企业级能力体系。

它的核心转变包括：

1. 从项目交付转向产品运营。
2. 从集中式共享服务转向领域产品网络。
3. 从人工运维转向平台自助。
4. 从中央数据加工转向数据产品化。
5. 从人工审批治理转向自动化护栏。
6. 从技术部门单独负责转向业务技术共同负责结果。

最终目标是让企业在业务快速变化、系统规模扩大、数据复杂度上升和安全合规要求增强的情况下，仍然能够保持高效交付、稳定运行、可信数据和可持续演进。

---

## 19. 参考资料

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
- OpenAPI Specification
  <https://spec.openapis.org/oas/latest.html>
- AsyncAPI Specification
  <https://www.asyncapi.com/docs/reference/specification/latest>
- OpenTelemetry Documentation
  <https://opentelemetry.io/docs/>
