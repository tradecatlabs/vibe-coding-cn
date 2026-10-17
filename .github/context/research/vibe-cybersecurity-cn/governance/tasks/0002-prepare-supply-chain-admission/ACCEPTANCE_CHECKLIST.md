# Acceptance Checklist

# Global Standards

- [x] 研究事实与准入决策分离。
- [x] 所有候选不授予运行权，版本和摘要不猜测。
- [x] 准入状态不能绕过固定版本和八门禁。
- [x] 主动网络能力后置且绑定隔离配置。
- [x] 没有下载、安装、联网或扫描。

# Task Package Checklists

## TP-01

- [x] 生命周期、门禁、波次和失效条件明确。
- Verify: 审阅 `ADMISSION_POLICY.md` 的状态机和八门禁。
- Gate: 供应链目录不持有运行授权，状态不得越级。

## TP-02

- [x] 18 个研究 MVP 全量映射，其他 28 项未进入准入队列。
- [x] W0=6、W1=5、W2=4、W3=3。
- Verify: `python3 validate_admission_candidates.py`。
- Gate: 准入集合必须等于研究 MVP 集合，active-high 必须拒绝。

## TP-03

- [x] 标准库校验器与生成表存在。
- [x] 研究 snapshot、覆盖集合、风险、状态、pin 和 checks 被机械验证。
- Verify: `python3 -m unittest test_validate_admission_candidates.py`。
- Gate: 删除门禁、无证据 PASS、伪 digest、默认运行权和血缘漂移必须 fail closed。

## TP-04

- [x] 目录架构文档和长期项目真相源同步。
- [x] 任务 closeout、治理 strict/health 和原则门禁纳入最终校验。
- [x] 主要任务复用采样完成；项目 overlay 不重复晋升为全局 SOP。
- Verify: task closeout、governance strict/health、principle gate 命令。
- Gate: 候选表准备完成不得包装成真实 artifact 已纳入。
