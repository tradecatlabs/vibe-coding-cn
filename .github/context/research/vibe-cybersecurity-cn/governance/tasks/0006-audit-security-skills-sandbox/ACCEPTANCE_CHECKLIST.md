# Acceptance Checklist

## Global Standards

- [x] 外部内容按不可信数据处理；全部命中经人工核对。
- [x] 沙盒隔离、只读分析、未执行仓库脚本。
- [x] 审计报告逐仓库结论有证据。
- [x] 网络副作用仅浅克隆公开仓库。

## Task Package Checklists

### TP-01

- [x] 14/14 仓库浅克隆成功。
- Verify: `.sandbox/skill-audit/` 目录齐全。
- Gate: 拉取失败项已记录（无）。

### TP-02

- [x] 统计、恶意模式、嵌入指令、许可、二进制全扫描。
- Verify: `AUDIT_DATA.json` 与人工核对记录。
- Gate: 高危命中逐条核对，无真实投毒。

### TP-03

- [x] 报告含逐仓库结论、风险分级、使用护栏。
- Verify: `SKILL_AUDIT_REPORT.md`。
- Gate: 结论绑定证据与人工核对。

### TP-04

- [x] 治理同步与 closeout 完成。
- Verify: task docs + governance strict/health。
- Gate: 无占位、死链或过度声明。
