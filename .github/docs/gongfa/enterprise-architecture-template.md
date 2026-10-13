<a id="reference-engineering-practice-enterprise-monorepo-multi-repo-reference-architecture-template"></a>
# Enterprise Monorepo / Multi-Repo Reference Architecture Template

版本：v1.3
定位：国际通用企业级参考模型
适用：中大型工程组织、Platform Engineering、Internal Developer Platform (IDP)、Platform Services、
多产品线、AI / Data / Cloud Native systems

---

##### 1. 总体原则

企业级项目架构不应只按“frontend / backend / infrastructure / docs”粗分，而应按长期稳定的
enterprise truth sources 与 operating surfaces 划分：

| 顶层目录                 | International description                         | Truth / boundary type             |
| -------------------- | ------------------------------------------------- | --------------------------------- |
| `governance/`        | Engineering Governance: standards, owners, ADRs, SLOs, risks, reviews, gates | Engineering governance truth      |
| `contracts/`         | Interface Contract Registry: APIs, events, schemas, datasets, resources, policies | Machine-readable contract truth   |
| `catalog/`           | Software Catalog / Asset Inventory: systems, components, resources, owners, lifecycle | Software asset ownership truth    |
| `infra/`             | Infrastructure and Operations: infrastructure, runtime, delivery, observability, security, cost | Operational foundation truth      |
| `internal-platform/` | Internal Developer Platform (IDP): paved roads, templates, self-service, portal | Developer experience truth        |
| `middle-platform/`   | Platform Services / Shared Capabilities: data, API, compute, AI, messaging, identity | Reusable platform capability truth |
| `services/`          | Deployable Service Runtime: APIs, workers, jobs, bots, publishers, service-owned adapters | Runtime service boundary truth    |
| `products/`          | Product Surfaces: web, mobile, bot, admin, reporting, user/operator workflows | Product delivery truth            |
| `shared/`            | Thin Shared Libraries / SDKs: low-level libraries, SDKs, fixtures | Thin reuse boundary               |

> 最终模型：
> **governance + contracts + catalog + infra + internal-platform + middle-platform + services + products**
> `shared/` 是辅助层，不应膨胀成新的 platform service 或 product backend。

---

##### 2. 推荐目录结构

```text
repo/
├── governance/                         # Engineering Governance: standards, owners, ADRs, SLOs, risks, reviews, gates
│   ├── standards/                      # Engineering, security, coding, architecture standards
│   ├── decisions/                      # ADR: Architecture Decision Records
│   ├── ownership/                      # Owners, RACI, on-call, escalation paths
│   ├── slo/                            # SLI, SLO, error budget, service level objectives
│   ├── risks/                          # Risk register, threat model, compliance risks
│   ├── gates/                          # Release, security, quality, architecture gates
│   ├── change-records/                 # Task trees, migration evidence, rollback runbooks
│   └── postmortems/                    # Incident reviews, action items, long-term fixes
│
├── contracts/                          # Interface Contract Registry: the machine-readable truth across boundaries
│   ├── apis/                           # OpenAPI, GraphQL schema, RPC IDL
│   ├── events/                         # AsyncAPI, event definitions, topics, subscription contracts
│   ├── schemas/                        # JSON Schema, Proto, Avro, Parquet schema
│   ├── datasets/                       # Dataset contracts, data products, quality rules, lineage
│   ├── resources/                      # Cloud resources, K8s CRDs, Terraform module interfaces
│   └── policies/                       # OPA, Rego, IAM policies, data access policies
│
├── catalog/                            # Software Catalog / Asset Inventory: systems, components, resources, APIs, owners, lifecycle
│   ├── systems/                        # System definitions: product domains, platform domains, business systems
│   ├── components/                     # Component definitions: services, libraries, jobs, frontend apps
│   ├── resources/                      # Resource definitions: DB, queue, bucket, cache, cluster
│   ├── domains/                        # Domain definitions: business, technology, platform domains
│   └── scorecards/                     # Health, maturity, security, reliability scorecards
│
├── infra/                              # Infrastructure and Operations
│   ├── control-plane/                  # Topology, lifecycle, state control, cluster management
│   ├── resource-plane/                 # Compute, network, storage, database, queue
│   ├── runtime-plane/                  # Worker, daemon, job, scheduler, queue consumer
│   ├── delivery-plane/                 # CI/CD, artifacts, release, rollback, environment promotion
│   ├── observability/                  # Logs, metrics, traces, health, alerts, dashboards
│   ├── security/                       # Secrets, IAM, policy enforcement, audit
│   ├── container/                      # Docker image matrix, Compose entry points, registry policy
│   ├── kubernetes/                     # K8s base, workloads, policies, networking, operations
│   ├── gitops/                         # Argo CD / Flux desired state, promotion, rollback
│   ├── environments/                   # Local, dev, staging, production, DR
│   ├── disaster-recovery/              # Backup, restore, runbook, game day
│   └── cost/                           # FinOps, budget, resource ownership, cost attribution
│
├── internal-platform/                  # Internal Developer Platform (IDP), not a business capability platform
│   ├── portal/                         # Backstage-style developer portal
│   ├── templates/                      # Golden paths, scaffolding, service templates
│   ├── orchestration/                  # Provisioning, workflow, automation
│   ├── developer-tools/                # CLI, SDK, diagnostics, local development tools
│   ├── scorecards/                     # Service health, quality, security, maturity scorecards
│   └── docs/                           # Platform user docs, onboarding guides, FAQ
│
├── middle-platform/                    # Platform Services / Shared Capabilities for multiple product surfaces
│   ├── data-platform/                  # Ingestion, quality, lineage, catalog, serving
│   ├── api-platform/                   # Gateway, query, auth, rate limit, schema
│   ├── compute-platform/               # Batch, stream, derived jobs, task execution
│   ├── ai-platform/                    # LLM, prompt, tool, context, eval, agent runtime
│   ├── messaging-platform/             # Notification, event, subscription, push
│   ├── integration-platform/           # External APIs, webhooks, provider adapters
│   ├── identity-platform/              # Account, AuthN, AuthZ, tenant
│   ├── search-platform/                # Indexing, retrieval, ranking
│   └── experimentation-platform/       # A/B testing, feature flags, experiment metrics
│
├── services/                           # Deployable Service Runtime, grouped by domain and deployable boundary
│   ├── query/                          # Query/API services and read facades
│   │   └── query-api/
│   ├── data/                           # Data ingestion workers, sync jobs, source adapters
│   │   └── source-worker/
│   ├── compute/                        # Derived compute, batch jobs, stream processors
│   │   └── derived-worker/
│   ├── channels/                       # Bot, chat, webhook or notification channel services
│   │   └── chat-bot/
│   ├── publishing/                     # External publishing and export services
│   │   └── report-publisher/
│   └── domain-specific/                # Optional business or technical domain service group
│       └── domain-service/
│
├── products/                           # Product Surfaces for users, operators, or business workflows
│   ├── web/                            # Web product surface
│   ├── mobile/                         # Mobile product surface
│   ├── bot/                            # Bot, agent, chat surface
│   ├── admin/                          # Admin and operations console
│   └── reporting/                      # Reporting, BI, business analytics surface
│
├── shared/                             # Thin Shared Libraries / SDKs; only stable low-level reuse belongs here
│   ├── libraries/                      # General-purpose low-level libraries
│   ├── sdks/                           # External or internal SDKs
│   └── test-fixtures/                  # Cross-domain test fixtures
│
├── tools/                              # Developer Tooling: codegen, lint, verify, migration helpers
├── scripts/                            # Repo automation entry points
│   └── gates/                          # Executable repo gates for structure, contracts, runtime readiness
├── tests/                              # Cross-cutting tests that do not belong to one service
│   └── repo-gates/                     # Repository structure and architecture guard tests
├── docs/                               # Documentation Hub; does not replace governance/contracts/catalog
└── ci/ or .github/                     # CI workflow entry points
```

---

##### 3. 顶层目录职责说明

##### 3.1 `governance/`: Engineering Governance

用于承载组织级 Engineering Governance，不放业务代码。

应包含：

```text
governance/
├── standards/
│   ├── engineering-standard.md
│   ├── security-standard.md
│   ├── data-standard.md
│   └── api-standard.md
├── decisions/
│   └── adr-0001-record-template.md
├── ownership/
│   ├── owners.yaml
│   └── escalation-policy.md
├── slo/
│   ├── slo-template.yaml
│   └── error-budget-policy.md
├── risks/
│   └── risk-register.yaml
├── gates/
│   ├── release-gate.yaml
│   ├── security-gate.yaml
│   └── architecture-gate.yaml
├── change-records/
│   └── migration-record-template.md
└── postmortems/
    └── postmortem-template.md
```

核心规则：

* 架构决策必须进入 `decisions/`，以 ADR 形式长期留痕
* Owner、RACI、on-call 与 escalation path 必须进入 `ownership/`
* 生产系统必须定义 SLO
* 架构迁移、服务化拆分、运行时接入必须留下 task tree、evidence report 和 rollback runbook
* 事故必须有复盘和行动项
* 发布、安全、质量、架构门禁应尽量机器可执行

---

##### 3.2 `contracts/`: Interface Contract Registry

用于放置 machine-readable interface contracts，避免 API、events、schemas、datasets、
resources、policies 散落在代码注释或普通文档里。

推荐结构：

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
│   ├── data-products/
│   ├── quality-rules/
│   └── lineage/
├── resources/
│   ├── terraform-modules/
│   ├── kubernetes-crds/
│   └── cloud-resources/
└── policies/
    ├── iam/
    ├── opa/
    └── data-access/
```

核心规则：

* API 变更必须先更新契约
* 事件字段变更必须兼容旧消费者
* Dataset contract 必须声明 owner、schema、quality rules、lifecycle
* Policy 应尽量以 policy-as-code 形式机器可执行
* Contract change 必须进入 CI 校验

---

##### 3.3 `catalog/`: Software Catalog / Asset Inventory

用于记录 systems、components、resources、APIs、domains、owners、lifecycle。

推荐结构：

```text
catalog/
├── systems/
│   └── payment-system.yaml
├── components/
│   └── payment-api.yaml
├── resources/
│   └── payment-db.yaml
├── domains/
│   └── finance-domain.yaml
└── scorecards/
    ├── production-readiness.yaml
    ├── security-scorecard.yaml
    └── reliability-scorecard.yaml
```

每个资产建议至少包含：

```yaml
name: payment-api
type: service
system: payment-system
domain: finance
owner: team-payment
lifecycle: production
tier: tier-1
dependsOn:
  - resource:payment-db
  - api:identity-api
providesApis:
  - payment-public-api
consumesApis:
  - identity-internal-api
slo:
  availability: 99.9
  latency_p95_ms: 300
```

核心规则：

* 没有 owner 的 system 不允许进入 production
* 没有 catalog entry 的 service 不应接入 release pipeline
* Resource 必须能追溯到 system、team、cost center
* Lifecycle 必须明确：experimental、development、production、deprecated、retired

---

##### 3.4 `infra/`: Infrastructure and Operations

`infra/` 负责 Infrastructure and Operations：运行、交付、安全、观测、灾备和成本，
不承载业务逻辑。

推荐结构：

```text
infra/
├── control-plane/
├── resource-plane/
├── runtime-plane/
├── delivery-plane/
├── observability/
├── security/
├── container/
│   ├── image-matrix.yaml               # image name、build context、platform、owner、runtime
│   ├── compose.yaml                    # local / integration orchestration entry point
│   └── registries.yaml                 # registry、tag policy、retention、signing policy
├── kubernetes/
│   ├── base/                           # namespace、RBAC、quota、limit range、storage class
│   ├── workloads/                      # shared workload conventions and reusable manifests
│   ├── networking/                     # ingress、gateway、service mesh、network policy
│   ├── policies/                       # admission, security, resource and deployment policies
│   └── operations/                     # cluster runbooks, upgrade, backup, recovery, diagnostics
├── gitops/
│   ├── apps/                           # Argo CD / Flux application definitions
│   ├── environments/                   # env overlays and promotion targets
│   └── sync-waves/                     # dependency order and rollout sequencing
├── environments/
│   ├── local/
│   ├── dev/
│   ├── staging/
│   ├── production/
│   └── dr/
├── disaster-recovery/
└── cost/
```

核心规则：

* Environment configuration 必须显式分离
* Production change 必须可审计、可回滚
* Tier-1 resources 必须有 backup、restore plan、game day 记录
* Observability 应覆盖 logs、metrics、traces、alerts、dashboards
* Cost 必须能归因到 owner、system、environment
* `infra/container/` 管镜像矩阵、Compose 总入口和 registry policy；每个服务仍保留自己的 `Dockerfile`
* `infra/kubernetes/` 管集群级 K8s 基线、策略、网络和运维；服务级 workload intent 留在各自 `services/<domain>/<service>/deploy/`
* `infra/gitops/` 管 desired state、environment promotion、sync order 和 rollback，不应放业务逻辑
* 生产环境检查必须区分 read-only inspection 与 deployment/change；没有明确授权时只允许只读取证，不做远端变更

---

##### 3.5 `internal-platform/`: Internal Developer Platform (IDP)

这是 Internal Developer Platform (IDP)，不是 business domain platform，也不是某个 product backend。
它服务的是内部开发者，目标是用 paved roads、self-service 和 automation 降低交付复杂度。

推荐结构：

```text
internal-platform/
├── portal/
├── templates/
├── orchestration/
├── developer-tools/
├── scorecards/
└── docs/
```

典型能力：

* Service scaffolding templates
* Golden paths / paved roads
* Self-service resource provisioning
* Service registration
* CI/CD onboarding
* Release operation entry points
* Service health scorecards
* Diagnostics tooling
* Developer documentation

核心规则：

* 不能把业务能力塞进 `internal-platform/`
* 模板应默认符合治理、安全、观测、发布标准
* 平台能力要以产品方式运营，有 adoption、usage、feedback、SLO

---

##### 3.6 `middle-platform/`: Platform Services / Shared Capabilities

`middle-platform/` 对应国际语境中的 Platform Services / Shared Capabilities。
它提供多个 product surfaces 可复用的平台能力，不直接承载最终用户工作流，也不服务某一个单一产品。

推荐结构：

```text
middle-platform/
├── data-platform/
├── api-platform/
├── compute-platform/
├── ai-platform/
├── messaging-platform/
├── integration-platform/
├── identity-platform/
├── search-platform/
└── experimentation-platform/
```

各平台职责：

| 子平台                         | 职责                                         |
| --------------------------- | ------------------------------------------ |
| `data-platform/`            | Ingestion、quality、lineage、catalog、serving |
| `api-platform/`             | Gateway、auth、rate limit、schema、query layer |
| `compute-platform/`         | Batch、stream、job orchestration、derived compute |
| `ai-platform/`              | LLM、prompt、tool、context、eval、agent runtime |
| `messaging-platform/`       | Notification、events、subscriptions、push |
| `integration-platform/`     | External APIs、webhooks、provider adapters |
| `identity-platform/`        | Account、AuthN、AuthZ、tenant |
| `search-platform/`          | Indexing、retrieval、ranking、search |
| `experimentation-platform/` | A/B testing、feature flags、experiment metrics |

核心规则：

* 可以依赖 `infra/`
* 可以通过 contracts 暴露能力给 `products/`
* 不应依赖 `products/`
* 不应承载某个单一 product surface 的专属业务逻辑
* Platform capability 必须产品化：contract、docs、SLO、owner、onboarding path 都要明确

---

##### 3.7 `services/`: Deployable Service Runtime

`services/` 承载可以独立运行、测试、部署、扩缩容和回滚的 runtime units。
它回答“系统里到底有哪些服务，以及每个服务的责任、入口、数据边界、依赖和部署形态是什么”。

推荐结构：

```text
services/
├── query/
│   └── query-api/
├── data/
│   └── source-worker/
├── compute/
│   └── derived-worker/
├── channels/
│   └── chat-bot/
├── publishing/
│   └── report-publisher/
└── domain-specific/
    └── domain-service/
```

每个 service root 建议至少包含：

```text
service-name/
├── src/
├── tests/
├── deploy/
│   ├── compose.yaml                    # service-level local/integration runtime intent
│   └── k8s.yaml                        # service-level simple workload intent; larger setups may use helm/kustomize
├── docs/
├── service.yaml                        # owner、lifecycle、entrypoints、data access、dependencies、runtime
├── Dockerfile
├── entrypoint.sh
├── README.md
└── AGENTS.md
```

核心规则：

* 一个 service root 必须对应一个清晰的 runtime boundary
* API、worker、cronjob、daemon、bot、publisher 都可以是 service，但 library / SDK / template 不应伪装成 service
* `services/<domain>/<service>/service.yaml` 应声明 owner、lifecycle、entrypoints、ports、data access、dependencies、SLO、deploy、rollback
* `services/<domain>/<service>/deploy/compose.yaml` 和 `services/<domain>/<service>/deploy/k8s.yaml` 用于声明服务级 runtime intent
* 每个 service root 应至少能提供 start、stop、health、test、verify、build image 和 deploy dry-run 的标准入口
* `services/` 可以实现 `middle-platform/` 暴露的能力，也可以支撑 `products/` 的交付面，但不能绕过 `contracts/` 和 `catalog/`
* 容器化、Compose、Kubernetes 或 systemd 只应作用在边界清楚的 service root 上

---

##### 3.8 `products/`: Product Surfaces

Product Surfaces 直接面向 end users、operators 或具体 business workflows。

推荐结构：

```text
products/
├── web/
├── mobile/
├── bot/
├── admin/
└── reporting/
```

核心规则：

* Product surface 可以消费 `services/` 或 `middle-platform/` 暴露的 capabilities
* Product team 可以使用 `internal-platform/` 提供的开发、发布、自助能力
* Product surface 不应直接绕过 contracts 访问底层 resources
* Product-specific logic 留在产品内，不要污染 Platform Services
* 多产品复用前，先证明确实跨 product surfaces 稳定复用

---

##### 3.9 `shared/`: Thin Shared Libraries / SDKs

`shared/` 是最容易变成 `common` 垃圾桶的目录，必须严格限制。

允许放：

```text
shared/
├── libraries/
├── sdks/
└── test-fixtures/
```

适合放：

* 无业务语义的 low-level libraries
* SDK
* 类型工具
* 通用测试夹具
* Codegen runtime
* 跨域稳定 protocol adapters

不适合放：

* 业务规则
* 产品流程
* 领域模型
* 随手抽出来的 common helper
* 只有两个调用方的临时共享逻辑

核心规则：

> `shared/` 必须是 thin shared layer。
> 一旦它开始承载业务语义，就说明边界设计已经失控。

---

##### 4. 跨层依赖规则

推荐依赖方向：

```text
products / product surfaces
   ↓
services / deployable runtime services
   ↓
middle-platform / platform services
   ↓
infra

internal-platform / IDP
   ↓
infra

contracts  ← referenced by all layers
catalog    ← registered by all layers
governance ← constrains all layers
shared     ← provides only thin low-level reuse
```

##### 强制边界规则

| 规则 | 说明 |
| --- | --- |
| `products` 只能消费 `services` / `middle-platform` / `internal-platform` 暴露的接口 | 不直接绕过 contracts 访问底层 resources |
| `services` 是 deployable runtime boundary | 每个服务必须声明 owner、entrypoints、dependencies、data access、deploy、rollback |
| `middle-platform` 可以依赖 `infra` | 但不能依赖 `products` |
| `internal-platform` 服务内部开发者 | 不承载 business domain capabilities |
| `infra` 不写业务逻辑 | 只负责 runtime、delivery、security、observability、cost |
| `contracts` 是 Interface Contract Registry | API、event、schema、dataset、resource、policy 都应机器可读 |
| `catalog` 是 Software Catalog / Asset Inventory | System、component、resource、owner、lifecycle 必须可查 |
| `governance` 是 Engineering Governance truth | Standard、ADR、SLO、postmortem、gate 不可散落 |
| `shared` 必须是 thin shared layer | 不允许变成 `common` 垃圾桶 |

---

##### 5. 推荐门禁

##### 5.1 架构门禁

进入生产前必须满足：

```text
- 已登记 catalog
- 已指定 owner
- 已定义 lifecycle
- 已声明 service boundary 和依赖关系
- 已定义 API / event / dataset / resource 契约
- 已有最小 SLO
- 已有日志、指标、追踪或健康检查
- 已有发布与回滚方案
- 已通过安全基线检查
```

##### 5.2 契约门禁

```text
- API schema 校验
- Event schema 兼容性校验
- Dataset schema 兼容性校验
- Policy 语法校验
- Breaking change 检测
- Consumer impact 分析
```

##### 5.3 运行门禁

```text
- Health check
- Readiness check
- Alert rule
- Dashboard
- Error budget
- Runbook
- Backup policy
- Rollback policy
```

---

##### 6. 每个服务的推荐最小结构

适用于 `services/<domain>/<service>/` 下的 deployable service。
`products/` 或 `middle-platform/` 内部若仍直接承载可部署服务，也应先迁入或映射到同等 service root contract。

```text
service-name/
├── src/
├── tests/
├── configs/
│   ├── local/
│   ├── dev/
│   ├── staging/
│   └── production/
├── docs/
│   ├── README.md
│   ├── runbook.md
│   └── troubleshooting.md
├── deploy/
│   ├── compose.yaml
│   ├── k8s.yaml
│   ├── helm/
│   ├── kustomize/
│   └── terraform/
├── contracts/
│   └── README.md                      # 本服务私有契约说明；正式契约仍进入 repo/contracts
├── service.yaml                       # 服务运行契约：owner、entrypoints、data access、dependencies、deploy、rollback
├── catalog-info.yaml
├── CODEOWNERS
└── README.md
```

服务级 README 建议包含：

```text
#### Service Name

##### Purpose
这个 service / component 解决什么问题。

##### Owner
Team、owner、on-call 与 escalation path。

##### Runtime
Runtime、dependencies、ports、environment variables。

##### Contracts
提供哪些 APIs、events、datasets 或 resources。

##### Dependencies
依赖哪些 services、resources、external systems。

##### SLO
Availability、latency、error rate、throughput 等目标。

##### Observability
Logs、metrics、traces、dashboards、alerts。

##### Deployment
Release、rollback、environment promotion rules。

##### Runbook
Common failures、diagnosis steps、recovery steps。

##### Lifecycle
experimental / development / production / deprecated / retired。
```

---

##### 7. 成熟度分阶段落地

不建议一开始就把所有目录做满。更现实的落地方式是分阶段推进。

##### Phase 1：Minimum Enterprise Baseline

先落地：

```text
governance/
contracts/
catalog/
infra/
services/
products/
shared/
```

必须具备：

```text
- Owner
- Catalog entry
- API / Event / Schema contracts
- Service runtime contracts
- Per-service Dockerfile, entrypoint and deploy skeleton
- Container image matrix and Compose aggregate entry point
- Kubernetes and GitOps skeleton, before production rollout
- CI
- Base environments
- Base observability
- Release and rollback
```

##### Phase 2：Platform Engineering

增加：

```text
internal-platform/
middle-platform/
```

重点建设：

```text
- Golden paths / paved roads
- Service templates
- Self-service provisioning
- Developer portal
- Data platform
- API platform
- Identity platform
- Messaging platform
- Service catalog / service scorecards
- Runtime readiness scorecards
```

##### Phase 3：Governance Automation

强化：

```text
- Scorecard
- Policy as Code
- Contract testing
- SLO automation
- Cost attribution
- Security posture management
- Incident review automation
```

---

##### 8. 常见反模式

| 反模式 | 问题 |
| --- | --- |
| 把所有公共代码放进 `shared/common` | 很快变成无法治理的 common dumping ground |
| `infra` 里写业务逻辑 | Infrastructure 与 Product Surfaces 边界失控 |
| `middle-platform` 服务某一个产品 | Platform Services 退化成 product backend |
| 把 library、template 或脚本目录伪装成 `services` | Runtime boundary 虚假，后续 Docker/Kubernetes 只会放大耦合 |
| 还没确认服务边界就先上容器编排 | 只是把耦合系统搬进更复杂的运行环境 |
| 只有 Dockerfile，没有 service contract | 镜像能构建，但没人知道 owner、入口、依赖、数据权限和回滚方式 |
| 每个服务各写一套 Kubernetes 规则 | 集群策略、资源限制、探针、网络和安全基线会漂移 |
| GitOps 里混入手工补丁和业务逻辑 | desired state 失真，回滚和审计都不可靠 |
| 生产检查和生产变更没有分开 | 只读巡检可能误变成部署动作，风险不可审计 |
| 没有 `contracts` | 跨团队协作靠口头约定和代码注释 |
| 没有 `catalog` | 系统多了以后找不到 owner、dependency、lifecycle |
| 没有 `governance` | 目录结构会慢慢腐烂 |
| 只有 Portal，没有 platform capability | 只是入口，不是 IDP |
| 只有文档，没有 machine-readable contracts | 无法自动校验和治理 |
| 所有团队直接操作底层 resources | 平台无法形成抽象和复用 |
| SLO 只写在 PPT 里 | 不能参与 release gate、alerting、incident review |

---

##### 9. 推荐判定标准

一个目录是否应该存在，按以下问题判断：

##### 是否进入 `governance/`

```text
它是否定义 organization-level standards、decisions、gates、risks、SLO、postmortems？
```

是，则进入 `governance/`。

##### 是否进入 `contracts/`

```text
它是否是跨 team、layer、system 的 machine-readable interface contract？
```

是，则进入 `contracts/`。

##### 是否进入 `catalog/`

```text
它是否描述 systems、components、resources、owners、lifecycle？
```

是，则进入 `catalog/`。

##### 是否进入 `infra/`

```text
它是否负责 runtime、delivery、environments、resources、security、observability、cost？
```

是，则进入 `infra/`。

##### 是否进入 `internal-platform/`

```text
它是否服务 internal developers，提供 paved roads、self-service、developer experience？
```

是，则进入 `internal-platform/`。

##### 是否进入 `middle-platform/`

```text
它是否是多个 product surfaces 可复用的 platform capability，而不是某个产品的业务逻辑？
```

是，则进入 `middle-platform/`。

##### 是否进入 `services/`

```text
它是否是可以独立启动、停止、健康检查、测试、部署、扩缩容、回滚的 runtime unit？
```

是，则进入 `services/<domain>/<service>/`。

##### 是否进入 `infra/container/`

```text
它是否定义跨服务复用的 image matrix、Compose aggregate、registry、tag、retention 或 signing policy？
```

是，则进入 `infra/container/`。

##### 是否进入 `infra/kubernetes/`

```text
它是否定义 cluster-level Kubernetes baseline、namespace、RBAC、quota、networking、policy、shared workload convention 或 operations runbook？
```

是，则进入 `infra/kubernetes/`。单个服务自己的 workload intent 仍优先放在 `services/<domain>/<service>/deploy/`。

##### 是否进入 `infra/gitops/`

```text
它是否定义 desired state、environment overlay、promotion、sync order、rollback 或 Argo CD / Flux application？
```

是，则进入 `infra/gitops/`。

##### 是否进入 `products/`

```text
它是否直接面向 users、operators、channels、business workflows？
```

是，则进入 `products/`。

##### 是否进入 `shared/`

```text
它是否是无 business semantics、low-level、stable、cross-domain 的 thin reuse？
```

是，才进入 `shared/`。

---

##### 10. 最终判断

这个模型的关键不是目录多，而是把企业软件系统中不同类型的“真相”分开：

```text
governance        = Engineering Governance truth
contracts         = Interface Contract truth
catalog           = Software Catalog / Asset Inventory truth
infra             = Infrastructure and Operations truth
internal-platform = Internal Developer Platform (IDP) truth
middle-platform   = Platform Services / Shared Capabilities truth
services          = Deployable Service Runtime truth
products          = Product Surfaces truth
```

所以，较完善的企业级项目架构不应只是“四层架构”，而应是：

```text
governance
+ contracts
+ catalog
+ infra
+ internal-platform
+ middle-platform
+ services
+ products
```

再配一个严格受控、极薄的：

```text
shared
```

这是一套更接近现代 Platform Engineering、SRE、GitOps、Software Catalog、Data Governance、
Security Governance 与 IDP 共识的参考模型。实际落地时可以裁剪，但不建议混淆这些边界。
