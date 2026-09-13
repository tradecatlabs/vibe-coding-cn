# Audit Case Sampling Decision

- Source: problem-library
- Fixed Problem: Wikipedia 章节容器定位错误，以及 UnsolvedMath 公开源 ID/URL 一对多冲突导致的唯一键假设失败。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: external_source_contract_assumption
- Trigger Signals: 外部目录结构变化；来源 ID 重复；目录声明总数与唯一身份数不一致。
- Evidence: `RETROSPECTIVE.md`、`COMPLETION_EXEMPLAR.md`、`manifest.json`；可执行回归入口见 `README.md`。
- No-Case Reason: 当前只有本项目一次来源适配实例；“完成事实必须从原始证据重算”已由全局 CASE-0008 覆盖，项目特有的 DOM 与 ID 冲突已由原始快照回归门禁固化。待第二个项目出现同类来源身份冲突后，再提炼跨项目案例，避免基于单例扩张全局案例库。
