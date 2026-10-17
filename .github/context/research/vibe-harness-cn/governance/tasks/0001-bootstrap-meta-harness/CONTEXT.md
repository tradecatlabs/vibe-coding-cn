# Repo Evidence
- 初始工作目录为空且不是 Git 仓库；为绑定 high-risk 验证输入，现已建立本地 `main` revision，
  仍没有远端、PR、CI 或外部 reviewer。
- `uv 0.9.5` 可用；validator 通过 PEP 723 与 uv script lock 固定完整依赖闭包。
- 一手资料来自 Anthropic、OpenAI、MCP、OpenTelemetry 与 NIST，引用见 `docs/HARNESS_MODEL.md`。

# Constraints Matrix
| Constraint | Source | Effect |
|---|---|---|
| 单 agent 串行执行 | 根会话规则 | 不创建或依赖原生子代理 |
| 控制面/数据面分离 | 目标架构 | 元 harness 不接管业务运行状态 |
| 默认拒绝与运行时审批 | 安全边界 | 高风险工具不能只靠 prompt 约束 |
| 存在性优先 | Ponytail | 首版不创建 UI、DB、队列、插件和统一 runtime |
| 成熟能力优先 | Glue Principle | 复用 JSON Schema、jsonschema、uv、MCP/OTel 概念 |

# Change Boundary
- 允许：根入口、`docs/`、`contracts/`、`scripts/`、`tests/`、`governance/`。
- 禁止：远端发布/push、凭据搜寻或持久化、业务 runtime 和供应商专用实现。
- 结构变化已同步根及各新增目录的 `AGENTS.md`、项目 topology 和 module context。

# Risk Matrix
| Risk | Level | Mitigation |
|---|---|---|
| 坏 manifest 被误判为合规 | High | Schema + 跨字段策略 + 结构/策略负例 |
| conformance 被误当成生产安全 | High | 文档和 QA 明确证据边界与 candidate lifecycle |
| 权限只存在 prompt 中 | High | default deny、tool risk、approval binding、secret policy |
| 过早平台化 | Medium | 首版 kill list 与第二真实实现升级触发 |
| Schema 绑定供应商 | Medium | 核心字段供应商中立，私有实现留给 adapter |

# Assumptions and Falsification
- 假设：首个受管对象是 coding harness；不对就说，Schema 核心仍须保持领域中立。
- Proof point：有效 manifest 通过，缺停止条件与高风险免审批被拒绝。
- Falsifier：第二类真实 harness 必须依赖自由文本特例表达关键边界。
- 假设被推翻时升级契约版本并更新 ADR，不在 validator 中堆供应商特例。

# Critical Ambiguities
- 无阻塞本轮启动切片的歧义。
- 非阻塞未知：首个真实受管 harness 的仓库、runtime 与部署平台尚未指定。

# Debug Evidence Contract
- 调试模式: Required
- 触发原因：Verification Policy 接入时发现 gate runner 误判。
- 回归证据契约: Required
- Owner evidence: `DEBUG.md` 与 `REGRESSION_EVIDENCE.json` 已通过 RED/GREEN/反事实校验。

# Task Package Context Map
## TP-01 研究并定义 Harness 领域模型
- 输入：用户定义、一手资料、agent harness 六问。
- 输出：领域边界、终态、候选路径、proof point、falsifier 和路线图。

## TP-02 落地 manifest 契约与 validator
- 输入：TP-01 稳定概念。
- 输出：JSON Schema、有效样例、负例与薄校验脚本。

## TP-03 建立项目治理与架构记忆
- 输入：TP-01 目标架构和项目目录变化。
- 输出：operating model、architecture standard、ADR、QA、topology、module context。

## TP-04 执行验证与风险审查
- 输入：TP-02/TP-03 全部产物。
- 输出：新鲜命令证据、审查 finding、文档漂移与剩余风险结论。
