# 开源网络安全 Agent 供应链：首轮综合分析

检索截面：`2026-08-13`。

## 结论先行

正确终态不是一个“会自己黑站的万能 Agent”，而是一个薄的安全证据控制面：

```text
                    untrusted generators
        ┌────────────────────────────────────────┐
        │ Amass/Subfinder/httpx/Nuclei/ZAP/...  │
        └───────────────────┬────────────────────┘
                            │ observations/candidates
┌────────────┐      ┌───────▼────────┐      ┌──────────────────┐
│ ScopeGrant │─────▶│ Policy Runtime │─────▶│ Independent      │
│ + ROE      │      │ + Tool Adapter │      │ ValidationRun    │
└────────────┘      └───────┬────────┘      └────────┬─────────┘
                            │                         │
                     ┌──────▼─────────────────────────▼──────┐
                     │ Append-only Evidence + Promotion Gate │
                     └──────────────────┬────────────────────┘
                                        │ derived view
                               ┌────────▼─────────┐
                               │ ConfirmedFinding │
                               └──────────────────┘
```

扫描器、Agent 和漏洞管理平台都是可替换消费者或生成器。授权、权限、证据和晋升规则必须由本项目持有。

### Future-Optimal framing

- **目标终态（Target end state）**：一个只接受有效 `ScopeGrant`、把扫描器输出降格为候选、以独立验证和不可变证据派生 `ConfirmedFinding` 的薄控制面。
- **真实约束（Real constraints）**：书面授权、网络副作用、最小权限、证据脱敏、工具与规则供应链、许可证、成本预算和可复查性。
- **惯性约束（Inertia constraints）**：把“安全 Agent”想象成万能渗透机器人、按工具热度堆栈、把多 Agent/Kubernetes/图数据库当成先进性的惯性；这些不是本轮硬约束。
- **删除清单（Kill list）**：删除 Agent 自授权、扫描器自证、手工写入 confirmed finding、浮动工具/模板版本、无界并发、默认主动高风险动作和双份候选状态。
- **迁移切片（Migration slice）**：先以本地 Juice Shop 单目标证明 ScopeGrant → CandidateFinding → 独立 ValidationRun → Evidence → ConfirmedFinding，再按实测缺口增加资产发现、异构验证和运营平台。
- **证明点（Proof point）**：已知 ground truth 可以通过完整证据链晋升，所有越权、自证、篡改和失效负例均被拒绝。
- **推翻条件（Falsifier）**：若机器输出、可脱敏重放或独立 predicate 无法稳定区分误报，则放弃当前组合，改用更窄漏洞类别或异构 verifier。

## 1. 候选分布

机器目录当前有 `46` 个代表性候选：

- `18 mvp`：允许进入本地隔离样例；
- `15 pilot`：价值明确但先校准；
- `10 reference`：只研究，不进入默认工具面；
- `3 hold`：关键风险尚未闭合。

分数不是“排行榜”。一个高速工具可能很成熟，却因为授权和网络影响只得到 `hold`；一个数据标准不会找漏洞，却因证据互操作进入 `mvp`。

## 2. 三条架构法则

### R1 — 授权先于发现

`OpenNetworkObservation ∩ ScopeGrant = AuthorizedAssetSpace`。

资产发现结果只是来源观察。域名、IP、ASN、云资源或第三方托管关系必须先与书面授权和资产归属求交，才能成为主动工具输入。模型不能自行扩大范围。

### R2 — 候选与实证分离

扫描器输出只能创建 `CandidateFinding`。实证视图至少要求：

- 有效且未过期的 `ScopeGrant`；
- 候选与验证引用同一个 canonical Asset；
- `ValidationRun` 与候选生成 run 独立；
- 证据绑定工具/规则/模板版本、参数摘要、时间、请求响应或 artifact digest；
- 当前没有后续 invalidation；
- 高风险类别满足人工审批或专门策略。

### R3 — 证据守恒

`ConfirmedFinding` 是派生视图，不是可手工写入的第二套真相源。原始产物、脱敏派生物、验证结论和失效记录只追加；证据断链、范围失效或 verifier 失败时，结论自动退出实证视图。

## 3. 首个纵向样例

首轮不需要 Kubernetes、多 Agent、图数据库或完整漏洞运营平台。最小闭环为：

| 角色 | 选择 | 原因 |
|---|---|---|
| 本地 ground truth | OWASP Juice Shop | 可重建、已知漏洞、MIT、避免对公网动作 |
| 目标观察 | 静态 ScopeGrant + httpx | 不引入子域/端口复杂度，JSONL 与限速清楚 |
| 候选生成 | Nuclei + 固定签名的 HTTP 模板子集 | DSL、JSONL、请求响应和模板版本可绑定 |
| 独立验证 | 最小安全 HTTP 重放 adapter | 只重放批准请求并检查明确 predicate，不再跑同一 Nuclei template |
| 工具供应链 | Cosign + checksum + OCI digest | 验证镜像/artifact 来源，拒绝浮动 tag |
| 证据格式 | 原始工具输出 + 项目 JSON envelope | 原始证据不丢失；项目只做适配与准入 |

这个切片故意不使用 `Subfinder/Katana/Naabu`：本地单目标已经足够证明候选—验证—证据链，扩大资产面不会验证新的核心假设。

### Proof point

同一个已知 Juice Shop 行为能够经过：

```text
有效 ScopeGrant
  -> Nuclei CandidateFinding
  -> 独立 HTTP ValidationRun
  -> 两套版本绑定证据
  -> ConfirmedFinding 派生视图
```

同时，以下负例必须无法晋升：目标越界、模板无签名/未固定、验证器与生成器同一 run、响应 predicate 不满足、证据过期或原始 artifact digest 不匹配。

### Falsifier

如果现有工具不能提供稳定机器输出、请求响应不能安全脱敏重放，或独立验证无法区分误报，则当前组合被推翻，需要换成 ZAP/Greenbone 或更窄的漏洞类别。

## 4. 第二阶段候选组合

### Web/API

`httpx/Katana -> Nuclei -> ZAP -> DefectDojo`

- Katana 负责端点候选，不提交表单或 headless 动作作为默认值。
- Nuclei 负责模板候选；code/headless/DAST 模板单独审批。
- ZAP 作为异构 DAST 验证器，不因为两个工具同时告警就自动确认。
- DefectDojo 只消费已分级 finding，负责去重与运营，不拥有原始证据真相。

### 网络资产

`Amass/Subfinder -> httpx -> Naabu/Nmap -> Greenbone`

- 被动发现优先；所有结果先与授权求交。
- Naabu/Nmap 只在端口和速率 allowlist 内运行。
- Greenbone 适合深度网络 pilot，但部署、feed 和许可按组件管理。

### 源码与供应链

`Gitleaks + Semgrep + Trivy/OSV + Syft/Grype -> Dependency-Track`

- 秘密、SAST、SCA 和 SBOM 是不同证据能力，不压成单一严重度。
- Semgrep CE 的跨文件能力有明确天花板；需要数据流时试点 Joern。
- Trivy、OSV、Grype 的结果用于交叉差异和适用性分析，不做多数投票。
- Dependency-Track 负责持续组件运营，不宣布漏洞可达。

### 云与 IaC

`Trivy/Checkov -> Prowler`

- 先做本地 IaC，只读云账户放到独立 pilot。
- Prowler 只能拿短时效、最小权限、账户级 allowlist 的只读角色。

## 5. 现有 Agent 项目：吸收机制，不复制产品

| 项目 | 值得吸收 | 主动拒绝 |
|---|---|---|
| CAI | 安全领域工具 schema、HITL、trace、prompt injection 研究 | 把 guardrail 只放在提示词；宽 shell/SSH 默认开放 |
| PentAGI | 可恢复 flow、任务状态、沙箱、停止/修补接口 | 多 Agent 即默认架构、云服务和本地状态混成真相源 |
| Strix | 本地 run、headless、PoC/reproduction、源码+运行态组合 | 自动利用、自动修复提交、供应链自动拉取不经验证 |
| PentestGPT | benchmark 血缘、会话持久化、Docker-first | benchmark 分数外推生产、遥测默认进入敏感环境 |
| Nettacker | 模块化和 API 形态 | 爆破、规避、扫描模块共享同一低门槛权限 |

本项目默认采用单 Agent、窄工具、显式状态机。只有真实评测证明覆盖率、上下文或吞吐瓶颈后，才升级多 Agent。

## 6. 供应链门禁

任何工具进入执行面前必须满足：

1. 固定不可变 release/commit/OCI digest；
2. 验证 checksum、签名或 Sigstore bundle；
3. 生成或取得 SBOM，记录许可证与关键依赖；
4. engine、模板/规则、插件、数据库分别固定；
5. 关闭自动更新和运行时远程下载；
6. 镜像不挂载宿主 Docker socket，除非单独审批；
7. 用负例证明越权目标、无签名规则和过宽参数会 fail closed；
8. upstream advisory 触发版本失效和重评。

2026 年 Trivy 官方安全通告显示，攻击者能够发布恶意 release 并重写 Action tags。正确教训不是“禁用 Trivy”，而是任何安全工具本身都必须被当作高价值供应链输入。

## 7. 证据模型建议

内部最小 envelope：

```text
Evidence
├── subject: canonical asset / finding / artifact digest
├── producer: tool + version + image digest
├── rule: template/rule id + source commit + signature status
├── scope: ScopeGrant digest + valid_at
├── execution: run id + config digest + started/finished
├── artifacts: raw/sanitized locators + SHA-256
├── observation: structured predicate facts
├── verifier: independent actor/tool/run
└── lifecycle: valid / invalidated / superseded
```

不要一开始强迫所有扫描器输出统一大 schema。保留原始格式，在适配层抽取最小公共字段；否则会丢失工具特有证据。

## 8. 效率与成本

### 复杂度

开放空间扫描的朴素成本近似：

```text
O(assets × endpoints × rules × retries)
```

这会在 10x/100x 资产增长时爆炸。结构性优化顺序应是：

1. 授权求交和去重先于主动探测；
2. 被动发现先于主动发现；
3. 指纹/技术栈过滤先于模板展开；
4. 变更驱动增量扫描先于全量重扫；
5. 候选优先级和验证预算先于并发扩张；
6. 原始响应流式落盘并限制大小，不一次加载内存。

### Hot path

主要瓶颈是网络 I/O、浏览器/DAST、模板展开、漏洞 DB 刷新和 LLM 调用，不是 JSON 适配代码。

### 立即值得做

- 全局/每目标速率、超时、最大响应、最大跳转和预算；
- target/rule 去重、结果缓存和 incremental scan；
- 所有外部调用有界重试与熔断；
- 记录 request count、p95/p99、artifact bytes、CPU/内存峰值和 LLM token/cost。

### 需要测量后再做

- Kubernetes/secureCodeBox 扩展；
- 多 Agent 并行；
- 图数据库/GUAC；
- 大规模缓存与分布式队列。

### 暂不值得做

- 自研端口扫描器、HTTP 引擎、漏洞规则 DSL、SBOM 或签名系统；
- 为了扫描速度引入 ZMap/masscan；
- 在没有第二个真实消费者前创建插件框架。

## 9. 当前决策

- 采用：薄控制面 + 成熟工具适配 + 独立验证 + 不可变证据。
- 首个样例：Juice Shop / httpx / Nuclei / 独立安全重放。
- 延后：secureCodeBox、DefectDojo、Greenbone、Dependency-Track、Joern、Prowler。
- 只研究：CAI、PentAGI、Strix、PentestGPT、CyberSecEval、SecRL。
- 暂停：Nettacker 默认集成、ZMap、masscan。

一句话：让 Agent 负责提出和编排，让策略决定能不能做，让验证器决定事实能不能成立。
