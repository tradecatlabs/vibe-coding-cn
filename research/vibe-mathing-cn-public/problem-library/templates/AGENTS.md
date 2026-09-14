# ProblemContract 模板目录规则

- 这里只保存可公开复制的 draft 模板和说明，不保存真实问题、raw source、研究运行、凭据或 Result。
- `problem-contract.template.json` 必须保持 `lifecycle=draft`，不得伪装成已准入 ProblemContract。
- 模板字段必须与 `problem-library/schema/canonical-problem.schema.json` 保持一致；字段含义以 schema 为准。
- 修改模板后运行 `make check`，并确认 canonical Problem、Attempt、Result 和 Solution index 的空状态没有改变。
