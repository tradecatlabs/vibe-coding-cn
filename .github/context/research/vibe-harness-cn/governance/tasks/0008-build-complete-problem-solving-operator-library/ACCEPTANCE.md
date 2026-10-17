# Task-Level Acceptance
- `operators/source-inventory.json` 精确列出原始 75 项，七个 domain count 分别为 3/10/12/12/12/12/14。
- 七个 pack 对 inventory 精确覆盖 75/75，并额外包含 7 个明确标记 `derived` 的领域 Method；总数 82。
- 每个条目保存中英文名、核心问题、操作模式、Agent 用法、适用/禁用边界、来源和类型化语义。
- Schema 区分 MentalModelSpec、OperatorSpec、MethodSpec；类型混淆和缺字段失败关闭。
- validator 检查目录路径、Schema、ID、source key、计数、exact set、引用和关键安全不变量。
- README/AGENTS、PRD、HARNESS_MODEL、ADR、操作模型、拓扑、工具链和 module context 与实现一致。

# Validation Plan
- Positive：验证 canonical `operators/catalog.json`，报告 75/75、7/7、82。
- Negative：缺 source item、重复 ID、坏 Method 引用、MentalModel 伪装 effect、MentalModel 被当动作、Method 循环、算子自授权和路径逃逸均返回非零。
- Regression：`validate_harness.py --self-test` 同时覆盖既有 Harness manifest 和新 Operator Library。
- Project：governance strict/health、principle scan、architecture/behavior/contract/security/test gates。
- Evidence：结构化 stdout、gate artifacts、REVIEW 与任务级 verification results。

# Review Gate
- Correctness：逐项核对用户清单与 source inventory，不能只看总数。
- Architecture：Catalog/Library/Binding/Harness owner 不混淆，Schema 不塞入 manifest。
- Security/Reliability：路径不能逃逸；定义不能授予权限；错误明确非零退出。
- Performance：单次验证 O(files + entries + refs)，无网络、模型或全库上下文注入。
- Ponytail：不新增服务、数据库、框架、SDK 或未使用抽象。
- Documentation：新模块、命令、Schema 和真相源有 owner 文档。

# Runtime Verification Gate
- `VERIFICATION_PLAN.json` READY；architecture、behavior、contract、test 为 REQUIRED。
- security 虽由计划判定 NOT_APPLICABLE，仍手动运行项目 security gate 作为额外检查。
- 所有 required result 必须绑定最终 clean HEAD 的 input/policy digest。

# Ship Readiness
- 任务文档 closeout、sampling、review、治理和项目 gates 全部通过。
- 选择性 stage 本任务文件；不混入 ignored runtime 或其他 Agent 改动。
- 无 remote 时只创建本地 commit，并明确未 push/PR/CI。

# Task Package Acceptance
## TP-01
- Schema、catalog 和 source inventory 结构稳定且可解析。
- 原始 75 项名称/ID 清单有独立计数和来源登记。

## TP-02
- 七个 pack 的 source entries 精确覆盖 inventory，无重复、无遗漏、无额外冒充项。
- 7 个派生 Method 引用真实存在的 source entries。

## TP-03
- canonical library PASS；八类关键负例 BLOCK。
- 既有 Harness manifest self-test 继续 PASS。

## TP-04
- 新模块和工具链被 README/AGENTS、领域/需求文档和 governance 正确描述。

## TP-05
- review 无 BLOCK/WARN；最终 required gates 与任务级 verification PASS。

# Anti-Goals
- 不得用同义词、摘要 Method 或数量声明代替任一原始条目
- 不得把纯思维视角伪装成拥有现实世界 effects 的 Operator
- 不得实现 selector、planner、业务 Binding 或在线 registry
- 不得虚构证据
- 不得越权补全未确认信息
