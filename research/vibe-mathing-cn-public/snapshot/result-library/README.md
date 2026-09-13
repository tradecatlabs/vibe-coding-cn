# 成果空间与解库视图

`result-library/` 保存经过结构化表达的研究成果。完整解不是独立人工录入的数据，而是从满足晋升条件的 `Result` 派生出的视图。它消费 `Job` 产生的候选和验证回执，但 `Job`、`Step`、`Task` 或 `Workflow` 的完成状态都不能替代 `Result` 的数学准入。

## 目录结构

```text
result-library/
├── AGENTS.md
├── README.md
├── schema/
│   └── result.schema.json
├── records/
│   └── results.jsonl
└── indexes/
    └── solutions.json
```

## 派生规则

一个结果只有同时满足以下条件才进入 `solutions.json`：

1. `kind=proof` 且 `outcome=established`，或 `kind=counterexample` 且 `outcome=refuted`；
2. 当前有效证据包含独立的直接验证：proof 为 `human_review` 或 `kernel_check + axiom_escape_audit`；counterexample 为 `counterexample_check | human_review` 或 `kernel_check + axiom_escape_audit`；
3. 当前有效证据包含独立且接受的 `statement_faithfulness`；
4. 以上证据绑定可复查 locator 与 SHA-256，且没有被账本中的后续记录失效；
5. Result 与 Attempt 引用同一个 Problem，证据 verifier 不等于候选 generator。

`outcome` 表示数学结果，`evidence` 表示验证能力集合；`refuted` 不是证据等级。证据能力构成偏序，不使用 `numeric < symbolic < human < kernel` 的伪全序。

`prior_art_review` 可记录归因和新颖性审查，但当前不作为“数学上已证明/已反驳”的准入替代物。它不能替代直接验证，直接验证也不能自动证明新颖性。

`solutions.json` 必须由校验器重算并核对，不接受绕过 `results.jsonl` 的手工答案。

按 Problem 导出时，`ResearchBundle.disposition` 从当前有效 Solution View 派生为 `solved|refuted|open`。若同一 Problem 同时存在通过准入的 proof 与 counterexample，研究空间校验和 `export-bundle` 都会非零失败；系统不会任选一侧，也不会把冲突伪装成 open。

## 验证

```bash
python3 scripts/validate_research_spaces.py
python3 scripts/validate_research_spaces.py --write-index
```
