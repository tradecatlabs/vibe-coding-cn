# ProblemContract 模板

[`problem-contract.template.json`](problem-contract.template.json) 是一个可复制的 `ProblemContract v1` 草稿模板。它使用 `problem:example-draft`、`example.invalid` 和 `lifecycle=draft`，**不是**本仓库的 canonical Problem，也不代表任何真实开放问题。

## 使用步骤

1. 复制模板到受控的本地草稿位置，不要直接把模板当作研究问题；
2. 替换 `problem_id`、题目、精确 statement、domain、quantifiers、definitions、assumptions、sources、acceptance 和 runtime constraints；
3. 对来源许可、题面忠实性、定义域、量词、允许公理和验收谓词完成单独审查；
4. 只有通过项目准入的 `lifecycle=active` 合同，才能作为 Attempt 的输入；
5. 研究过程产生的 Attempt、Evidence、Result 和 Solution 不写入模板目录。

公共问题总库与单问题网页版 Harness 的入口见 [`../VIBEMATHING_PUBLIC_INDEX.md`](../VIBEMATHING_PUBLIC_INDEX.md)。外部 catalog 不会自动写入本仓库的 [`../records/canonical-problems.jsonl`](../records/canonical-problems.jsonl)。

模板只解决“如何填写问题契约”；如果要启动完整网页版研究仓库，还需要使用公开的 [`vibemathing-problem-public-template`](https://github.com/vibemathing/vibe-mathing-problem-public-template)，并按其 `WEB_BOOTSTRAP.md` 和 `WEB_OUTPUT_CONTRACT.json` 执行。
