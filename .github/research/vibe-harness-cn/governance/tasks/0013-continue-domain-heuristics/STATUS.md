# Task Status
- Overall Status: `In Progress`

# Next Executable Leaves
- TP-05 | Wave 5 | Depends On: TP-04 | Gate: 前置步骤已完成: materialize-library

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | 六个领域研究、来源链接、迁移边界和停止理由已写入研究报告与证据矩阵 | - | - |
| TP-01.01 | TP-01 | 2 | - | No | Done | 法律：争点、权威层级、先例、证明标准和规则事实适用已入矩阵与 pack | - | - |
| TP-01.02 | TP-01 | 2 | - | No | Done | 伦理：利益相关者、比例、权利、公平、监督和责任检查已入矩阵与 pack | - | - |
| TP-01.03 | TP-01 | 2 | - | No | Done | 教育：目标、先备诊断、提取、支架、反馈和迁移边界已入矩阵与 pack | - | - |
| TP-01.04 | TP-01 | 2 | - | No | Done | 语言：语料、最小对比、句法语义语用、篇章和歧义程序已入矩阵与 pack | - | - |
| TP-01.05 | TP-01 | 2 | - | No | Done | 历史：出处、语境、交叉印证、视角和反事实边界已入矩阵与 pack | - | - |
| TP-01.06 | TP-01 | 2 | - | No | Done | 社会科学：构念、抽样、质性编码、混合方法和制度情境已入矩阵与 pack | - | - |
| TP-02 | ROOT | 1 | TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06 | No | Done | 六个领域均完成 add/crosswalk/gap 去重审计，没有把同义动作重复入库 | - | - |
| TP-03 | ROOT | 1 | TP-02 | No | Done | 新增 30 source、6 derived；引用、功能主类和治理 owner 已登记 | - | - |
| TP-04 | ROOT | 1 | TP-03 | No | Done | catalog、inventory、packs、taxonomy、研究/架构/治理文档已同步到 256/32/288 | - | - |
| TP-05 | ROOT | 1 | TP-04 | No | In Progress | 当前 clean HEAD 上项目四门禁、治理 strict/health/principle、任务级 verification 均通过 | 外部独立审查尚未提供 | 独立 reviewer receipt 或明确人工验收后重跑 closeout |

# Blockers
- 任务内容已落库；本地确定性验证已完成，最终 closeout 仍需独立 reviewer receipt。

# Runtime State
- Active workflow state: 以 `TASK_PACKAGE_SET.json` / `TASK_EXECUTION_WAVE_PACKET.json` 为准。
- Approval state: 未记录即视为未授权。
- Resume rule: 继续任务前重新读取当前 packet、Recent Evidence、Blockers、Runtime State。
- Stop condition: 找不到支撑问题求解语义的权威来源
- Stop condition: 只能通过修改公共 Core 才能表达条目
- Stop condition: 条目与既有 source 重复或无法写出证据/失败契约
- Stop condition: required gate 失败且无新的修复证据
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
