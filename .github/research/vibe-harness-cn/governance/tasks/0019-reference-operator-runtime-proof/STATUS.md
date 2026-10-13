# Task Status
- Overall Status: `In Progress`

# Next Executable Leaves
- TP-05 | Wave 5 | Depends On: TP-04 | Gate: clean-HEAD 任务级验证已通过；等待外部独立 reviewer receipt

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | Runtime Core、三类样例、正反例和统一 CLI 已落地；self-test PASS | - | - |
| TP-02 | ROOT | 1 | TP-01 | No | Done | 参考 Harness 已完成确定性 Select/Bind/Materialize/Verify/Trace，claim scope 被限制为 instruction materialization | - | - |
| TP-03 | ROOT | 1 | TP-02 | No | Done | 9 个 unittest 覆盖三种 Spec、选择、预算、策略、引用、篡改、CLI 与 Runtime record conformance | - | - |
| TP-04 | ROOT | 1 | TP-03 | No | Done | README/AGENTS、Operator Spec、PRD、Harness Model、ADR、QA、module context 与操作模型已同步 | - | - |
| TP-05 | ROOT | 1 | TP-04 | No | In Progress | 本地提交完成；clean-HEAD 任务级 verification 的四个 required gate 均通过，security 为 NOT_APPLICABLE | 外部独立审查尚未提供 | 外部 reviewer 提供绑定最终 HEAD 的独立 receipt |

# Blockers
- 本地实现与确定性门禁无阻塞；任务最终关闭需要外部独立 reviewer receipt。

# Runtime State
- Active workflow state: 以 `TASK_PACKAGE_SET.json` / `TASK_EXECUTION_WAVE_PACKET.json` 为准。
- Approval state: 未记录即视为未授权。
- Resume rule: 继续任务前重新读取当前 packet、Recent Evidence、Blockers、Runtime State。
- Stop condition: 需求需要真实模型、工具、远端服务或生产凭据
- Stop condition: 实现开始演化成通用 Planner、中央 runtime 或插件框架
- Stop condition: 现有目录内容无法提供确定性选择或展开所需的稳定字段
- Stop condition: Schema 必须收紧内容语义才可表达第一版闭环
- TP-01: status=Done; verifier_context=Runtime Core self-test 与契约门禁
- TP-02: status=Done; verifier_context=参考 Harness 正常闭环与摘要重算
- TP-03: status=Done; verifier_context=9 个行为/失败关闭回归
- TP-04: status=Done; verifier_context=document-drift 自审与 governance strict/health
- TP-05: status=In Progress; verifier_context=clean-HEAD 确定性验证已通过，等待外部独立审查
