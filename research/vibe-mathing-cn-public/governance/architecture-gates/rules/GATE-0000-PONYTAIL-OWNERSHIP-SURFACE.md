---
id: GATE-0000
type: gate
status: active
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-13
review_cycle: P90D
severity: BLOCK
detectability: agent+script+manual
source: STD-PONYTAIL-LADDER
---

# 新增所有权面必须证明存在必要性

## 阻止条件

新增或扩展依赖、抽象、配置、文件、目录、流程、脚本、skill 或治理规则，但没有说明当前需求、最低工程阶梯、跳过范围、天花板、升级路径和最小验证方式。

## 原因

无证明的所有权面会增加维护、review、测试、迁移和长期理解成本，并让代理在后续任务中继续围绕错误结构扩张。

## 检查方式

- Script：`python3 governance/tools/scan_principle_gates.py --repo . --git-mode working --strict`。
- Agent review：使用 `auto-review` 的 `ponytail-complexity` profile。
- 人工审查：检查新增对象是否有当前消费者、owner、验证方式和删除/升级触发。

## 可操作错误提示

你新增了一个所有权对象，但没有证明它现在应该存在。请先尝试删除、合并、内联、使用标准/平台/项目原生能力，或补充存在性理由、最低阶梯选择、跳过范围、天花板和最小验证。

## 最小修复

- 删除或合并不必要对象；或
- 替换为标准库、平台原生、项目既有能力；或
- 补充当前存在性理由、owner、验证方式、天花板和升级触发条件。
