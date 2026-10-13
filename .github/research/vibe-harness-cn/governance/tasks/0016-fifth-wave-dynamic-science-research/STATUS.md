# Task Status
- Overall Status: `In Progress`

# Next Executable Leaves
- TP-05 | Wave 5 | Depends On: TP-04 | Gate: 前置步骤已完成: materialize-library；等待独立 reviewer receipt

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | 六个动态科学领域的权威来源、问题求解程序、边界和停止理由已写入研究报告与证据矩阵 | - | - |
| TP-01.01 | TP-01 | 2 | - | No | Done | 随机状态转移、鞅/界限、停止时刻和耦合比较已入矩阵与 pack | - | - |
| TP-01.02 | TP-01 | 2 | - | No | Done | 适定性、相空间、稳定性、分岔和敏感性已入矩阵与 pack | - | - |
| TP-01.03 | TP-01 | 2 | - | No | Done | 作用量、Euler-Lagrange、守恒、Hamilton 表示和扰动检查已入矩阵与 pack | - | - |
| TP-01.04 | TP-01 | 2 | - | No | Done | 控制体守恒、无量纲相似、主导平衡、边界条件和降阶检查已入矩阵与 pack | - | - |
| TP-01.05 | TP-01 | 2 | - | No | Done | 速率律、机理候选、速率控制、稳态近似和参数敏感性已入矩阵与 pack，保持只读高风险边界 | - | - |
| TP-01.06 | TP-01 | 2 | - | No | Done | 电化学平衡、界面动力学、传质限制和信号交叉检查已入矩阵与 pack，保持只读高风险边界 | - | - |
| TP-02 | ROOT | 1 | TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06 | No | Done | 六个领域均完成 add/crosswalk/gap 去重审计，没有把同义动作重复入库 | - | - |
| TP-03 | ROOT | 1 | TP-02 | No | Done | 新增 30 source、6 derived；引用、功能主类和治理 owner 已登记 | - | - |
| TP-04 | ROOT | 1 | TP-03 | No | Done | catalog、inventory、packs、taxonomy、研究/架构/治理文档已同步到 346/50/396 | - | - |
| TP-05 | ROOT | 1 | TP-04 | No | In Progress | 待在最终 clean HEAD 上重跑 required gates 并补独立 reviewer receipt | 外部独立审查尚未提供 | 独立 reviewer receipt 或明确人工验收后重跑 closeout |

# Blockers
- 等待最终 clean HEAD 的验证结果与外部独立 reviewer receipt；任务保持 In Progress。

# Runtime State
- Active workflow state: 以 `TASK_PACKAGE_SET.json` / `TASK_EXECUTION_WAVE_PACKET.json` 为准。
- Approval state: 未记录即视为未授权。
- Resume rule: 继续任务前重新读取当前 packet、Recent Evidence、Blockers、Runtime State。
- Stop condition: 找不到支撑问题求解语义的权威来源
- Stop condition: 只能修改公共 Core 才能表达
- Stop condition: 候选与既有条目重复或无法写证据/失败契约
- Stop condition: 需要凭据、部署、现实操作授权、远端写入或破坏性操作
- TP-01.01: status=Done; verifier_context=自审
- TP-01.02: status=Done; verifier_context=自审
- TP-01.03: status=Done; verifier_context=自审
- TP-01.04: status=Done; verifier_context=自审
- TP-01.05: status=Done; verifier_context=自审
- TP-01.06: status=Done; verifier_context=自审
- TP-02: status=Done; verifier_context=自审
- TP-03: status=Done; verifier_context=自审
- TP-04: status=Done; verifier_context=自审
- TP-05: status=In Progress; verifier_context=自审后等待独立审查
