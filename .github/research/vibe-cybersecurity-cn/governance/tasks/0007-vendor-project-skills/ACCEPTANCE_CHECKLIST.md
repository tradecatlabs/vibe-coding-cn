# Acceptance Checklist

## Global Standards

- [x] 来源固定 commit，许可记录。
- [x] 未安装全局；内容视为数据。
- [x] 无未审计内容混入。

## Task Package Checklists

### TP-01

- [x] 范围=0006 审计通过且 Web3 匹配。
- Verify: `SKILL_AUDIT_REPORT.md` 建议项。
- Gate: 高敏感仓库不纳入。

### TP-02

- [x] 13 skill 落地 + manifest。
- Verify: `find skills -type f` + JSON 解析。
- Gate: commit/许可/审计引用齐全。

### TP-03

- [x] AGENTS/README 使用规则同步。
- Verify: 文档包含授权求交规则。
- Gate: 全局 skills 零改动。

### TP-04

- [x] closeout 与治理校验通过。
- Verify: task docs + governance strict。
- Gate: 无占位或死链。
