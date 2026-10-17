# Acceptance Checklist

# Global Standards
- [x] 需求与非目标边界明确。
- [x] Future-Optimal、Ponytail 和 Glue 原则有可追溯判断。
- [x] 所有规划能力明确标记为需求而非已实现事实。
- [x] 最终验证绑定当前输入且无 stale evidence。
- [x] 文档漂移、权限、性能和回滚经过自审。

# Task Package Checklists
## TP-01
- Verify: 检查 PRD 必需章节、FR/NFR/AC 编号和未决问题边界。
- Gate: 需求可供后续契约任务消费，且没有把规划写成已实现能力。
- [x] Problem Statement、用户、目标和成功信号完整。
- [x] 三类状态和核心对象 owner 明确。
- [x] FR、NFR、MVP、用户故事、验收场景、风险和路线图完整。
- [x] 待决策实现问题没有被伪装成已确认字段。

## TP-02
- Verify: 检查 ADR、module context、README/AGENTS、操作模型与拓扑导航。
- Gate: 长期真相源一致，现有 Harness manifest 与工具链保持不变。
- [x] ADR-0003 记录架构取舍、proof point、falsifier 和回滚。
- [x] docs/AGENTS 与根 AGENTS 反映新增文件和依赖方向。
- [x] README、HARNESS_MODEL、操作模型、拓扑和 context map 已同步。
- [x] docs module context 无占位符，职责与非职责完整。

## TP-03
- Verify: 运行任务、治理、原则、项目门禁与 Git 交付检查。
- Gate: 当前输入 required gate 全部 PASS，提交范围只包含本任务文件。
- [x] REVIEW.md 给出明确 PASS/WARN/BLOCK 与剩余风险。
- [x] REUSE_SAMPLING.json 通过 owner validator。
- [x] 任务文档 closeout、治理 strict/health、原则扫描通过。
- [x] Verification Plan required gates 全部产生新鲜 PASS。
- [x] 选择性本地提交且工作树最终 clean。
