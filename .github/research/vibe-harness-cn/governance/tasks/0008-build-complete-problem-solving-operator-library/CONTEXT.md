# Repo Evidence
- 当前 HEAD：`e0d5cc5`；工作树在任务开始时 clean。
- PRD v0.2 已确认 `Operator Library ⊂ Harness`，但 Schema、内容库和 validator 尚未实现。
- 现有 `contracts/` 只有 Harness manifest；现有验证入口为带锁定 `jsonschema` 的 `scripts/validate_harness.py`。
- `operators/` 尚不存在；创建后必须有目录级 README/AGENTS 和治理 module context。

# Constraints Matrix
| 约束 | 执行口径 |
|---|---|
| 完整性 | 原始 75 项必须由独立 inventory 精确约束，缺一项或多一项均失败 |
| 类型语义 | MentalModel/Operator/Method 使用条件分支 Schema，不用同一自由文本结构糊平 |
| 依赖 | 复用现有 `jsonschema` 和 `uv` lock，不新增框架或服务 |
| 安全 | 定义不能授予权限；敏感输入只允许引用；路径必须限制在 library root |
| 来源 | 用户提供的框架只作为 reference/provenance；不执行外部内容 |
| Git | 不 reset/clean/stash/强推；选择性 stage；无 remote 不 push |

# Change Boundary
- 可改：`operators/`、相关 `contracts/`、`scripts/`、`tests/`、README/AGENTS、docs 与 governance。
- 禁改：`research/upstreams.sources.json`、`research/upstreams.lock.json`、第三方 checkout 和既有 Harness manifest 语义。
- Side effects：新增版本化数据与本地校验入口；无网络、数据库、模型调用或生产写入。

# Risk Matrix
| 风险 | 级别 | 缓解 |
|---|---|---|
| 漏掉用户条目 | High impact | 独立 source inventory + exact-set validator + 75/75 测试 |
| 泛化模板导致内容空洞 | Medium | 每项保存核心问题、操作模式、AI 用法、适用/禁用边界和证据 |
| 类型混淆 | Medium | `oneOf` 条件 Schema + 伪装 MentalModel 负例 |
| 引用/路径漂移 | Medium | 相对路径约束、ID 唯一、引用解析、catalog 计数复算 |
| 过度平台化 | Medium | 只做离线数据、Schema、薄 validator；selector/runtime 延后 |

# Assumptions and Falsification
- 假设：用户说的“全部”指会话中明确列名的 75 项，并要求全部结构化；七个领域总结序列作为派生 Method 单列。
- Proof point：validator 报告 `source_coverage=75/75`、`derived_methods=7/7`、`total=82`。
- Falsifier：任一原始名称无法映射到唯一 ID，或必须把纯视角伪造成带执行效果的 Operator 才能入库。

# Critical Ambiguities
- 无阻塞歧义。STRIPS/PDDL、HTN、TEVV、BPMN/CMMN、DMN、PROV、Essence 等是架构来源，不计入 75 个用户原始方法条目。
- 若用户后续提供新的明确清单，以新增 inventory 版本处理，不回写本次 75 项基线。

# Debug Evidence Contract
- 调试模式: Optional
- 回归证据契约: Optional
- 本任务是新功能与契约实现，不是已知 bug 修复；通过正例和结构/完整性/引用负例建立初始行为基线。

# Task Package Context Map
## TP-01
- 输入：PRD v0.2、用户原始表格、现有 Harness manifest Schema 模式。
- 边界：只确定最小 JSON 结构和独立覆盖清单。

## TP-02
- 输入：TP-01 Schema/inventory。
- 边界：逐项建模七个领域，不扩写领域百科。

## TP-03
- 输入：catalog、packs、Schema。
- 边界：薄校验器只做本项目稳定不变量，不实现 planner。

## TP-04
- 输入：真实实现路径和命令。
- 边界：更新 owner 文档，不复制字段级 Schema。

## TP-05
- 输入：最终 diff 和门禁结果。
- 边界：本地主 Codex 自审不冒充外部 reviewer。
