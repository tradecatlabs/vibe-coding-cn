# Acceptance Checklist

# Global Standards
- [x] 原始 75 项 exact coverage 通过，计数和集合都可复算。
- [x] 7 个派生 Method 独立计数且引用全部可解析。
- [x] 三类 Spec Schema 和关键负例通过。
- [x] 未新增不必要依赖、服务、运行时或抽象。
- [ ] 文档、治理、review 和最终 verification 有新鲜证据。

# Task Package Checklists
## TP-01
- [x] 创建 Schema、catalog、source inventory。
- [x] Verify: JSON 语法、Schema 自检、75 项清单计数。
- [x] Gate: 结构能区分三类 Spec，清单与用户表格逐项一致。

## TP-02
- [x] 创建七个领域 pack。
- [x] Verify: source ID exact-set、总数、唯一性和派生 Method 引用。
- [x] Gate: `source_coverage=75/75`、`derived_methods=7/7`、`total=82`。

## TP-03
- [x] 实现并接入 operator library validator。
- [x] 增加 canonical 正例与八类关键负例。
- [x] Verify: self-test 和 unittest。
- [x] Gate: 正例 PASS、负例全部 BLOCK、既有 manifest 无回归。

## TP-04
- [x] 更新 README/AGENTS、PRD/HARNESS_MODEL、ADR 和治理上下文。
- [x] Verify: governance strict/health 和链接/术语扫描。
- [x] Gate: 真相源无文档漂移。

## TP-05
- [ ] 完成 review、sampling、closeout 和本地 Git 交付（review/sampling 已完成；closeout 被全局 retrospective registry 阻断）。
- [ ] Verify: principle scan、全部项目 gates、task verification strict。
- [ ] Gate: clean HEAD 的 required evidence 全部 PASS。
