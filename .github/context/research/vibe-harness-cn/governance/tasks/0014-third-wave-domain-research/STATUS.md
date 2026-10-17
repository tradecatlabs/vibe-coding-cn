# Task Status
- Overall Status: `In Progress`

## Next Executable Leaves
- TP-05 | Wave 5 | Depends On: TP-04 | Gate: 前置步骤已完成: materialize-library；等待独立 reviewer receipt

## Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | 六个领域的权威来源、问题求解程序、边界和停止理由已写入研究报告与证据矩阵 | - | - |
| TP-01.01 | TP-01 | 2 | - | No | Done | 形式逻辑：规格、语法语义、反模型、子目标和内核检查已入矩阵与 pack | - | - |
| TP-01.02 | TP-01 | 2 | - | No | Done | 认识论：观察、解释、辅助假设、欠定性和区分证据已入矩阵与 pack | - | - |
| TP-01.03 | TP-01 | 2 | - | No | Done | 地学：观测误差、地层、地图剖面、质量平衡和地面真值已入矩阵与 pack | - | - |
| TP-01.04 | TP-01 | 2 | - | No | Done | 天文：观测模型、背景、尺度、光变/光谱拟合和独立确认已入矩阵与 pack | - | - |
| TP-01.05 | TP-01 | 2 | - | No | Done | 材料：加工结构性能、计量、微观结构、数据质量和校准已入矩阵与 pack | - | - |
| TP-01.06 | TP-01 | 2 | - | No | Done | 信息知识：信息需求、查询扩展、来源权威、检索指标和元数据公平性已入矩阵与 pack | - | - |
| TP-02 | ROOT | 1 | TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06 | No | Done | 六个领域均完成 add/crosswalk/gap 去重审计，没有把同义动作重复入库 | - | - |
| TP-03 | ROOT | 1 | TP-02 | No | Done | 新增 30 source、6 derived；引用、功能主类和治理 owner 已登记 | - | - |
| TP-04 | ROOT | 1 | TP-03 | No | Done | catalog、inventory、packs、taxonomy、研究/架构/治理文档已同步到 286/38/324 | - | - |
| TP-05 | ROOT | 1 | TP-04 | No | In Progress | 本地静态校验已完成，待最终 clean HEAD 和独立 reviewer receipt | 外部独立审查尚未提供 | 独立 reviewer receipt 或明确人工验收后重跑 closeout |

## Blockers
- 无

## Runtime State
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
