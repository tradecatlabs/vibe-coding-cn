# Task Status
- Overall Status: `In Progress`

# Next Executable Leaves
- TP-05 | Wave 5 | Depends On: TP-04 | Gate: 前置步骤已完成: materialize-library；等待独立 reviewer receipt

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | 六个领域的权威来源、问题求解程序、边界和停止理由已写入研究报告与证据矩阵 | - | - |
| TP-01.01 | TP-01 | 2 | - | No | Done | 控制论：状态空间、可控/可观测、反馈误差修正、稳定裕度和滚动重规划已入矩阵与 pack | - | - |
| TP-01.02 | TP-01 | 2 | - | No | Done | 数值分析：条件性/稳定性、误差控制、收敛、残差和复现实验已入矩阵与 pack | - | - |
| TP-01.03 | TP-01 | 2 | - | No | Done | 离散组合：双射、抽屉、容斥、递推/生成函数、随机方法和极值界已入矩阵与 pack | - | - |
| TP-01.04 | TP-01 | 2 | - | No | Done | 热力学/统计物理：状态变量、熵、自由能、扰动响应和系综采样已入矩阵与 pack | - | - |
| TP-01.05 | TP-01 | 2 | - | No | Done | 有机化学：化学/区域/立体选择性、保护基代价和机理审计已入矩阵与 pack，保持只读高风险边界 | - | - |
| TP-01.06 | TP-01 | 2 | - | No | Done | 分析化学/计量：校准、检出限、基质干扰、方法验证和不确定度已入矩阵与 pack，保持只读高风险边界 | - | - |
| TP-02 | ROOT | 1 | TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06 | No | Done | 六个领域均完成 add/crosswalk/gap 去重审计，没有把同义动作重复入库 | - | - |
| TP-03 | ROOT | 1 | TP-02 | No | Done | 新增 30 source、6 derived；引用、功能主类和治理 owner 已登记 | - | - |
| TP-04 | ROOT | 1 | TP-03 | No | Done | catalog、inventory、packs、taxonomy、研究/架构/治理文档已同步到 316/44/360 | - | - |
| TP-05 | ROOT | 1 | TP-04 | No | In Progress | clean HEAD `e23c485` 上 verification plan、architecture/behavior/contract/test 全部 PASS，security 按条件 NOT_APPLICABLE；待独立 reviewer receipt | 外部独立审查尚未提供 | 独立 reviewer receipt 或明确人工验收后重跑 closeout |

# Blockers
- 等待最终验证结果与外部独立 reviewer receipt；任务保持 In Progress。

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
