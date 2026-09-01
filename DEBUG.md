# Debug Record

## Bug

- 标题：minimal README 重构后的文档一致性调试
- 症状：用户要求开始 debug，但未提供具体报错或失败现象；需要确认最近一次 `README.md` 预备知识扩展是否引入可复现问题。
- 首次发现位置 / 时间：`minimal` 分支，2026-09-01；目标提交 `21f6273`。

## Environment

- 仓库 / 模块：`/home/lenovo/.projects/vibe-coding-cn-minimal` / `README.md` 与 `explain.md`
- 运行环境：WSL Ubuntu；Git 分支 `minimal`
- 依赖 / 版本：`markdownlint-cli@0.48.0`，通过 `npx --yes` 临时运行
- 配置差异：当前极简分支没有 `Makefile`、测试脚本或 CI 文件，使用仓库主分支的 lint 配置进行文档检查。

## Reproduction

1. 在 `minimal` 分支读取当前 `README.md`、`explain.md` 和最近提交。
2. 运行 `npx --yes markdownlint-cli@0.48.0 --config /home/lenovo/.projects/vibe-coding-cn/.github/lint_config.json README.md`。
3. 检查 `README.md` 的本地链接、折叠标签、手工锚点、禁用句式和 `$$` 数学块配对。
4. 运行 `git diff --check`，确认当前工作树不存在空白错误。

## Observations

- O1：最近提交为 `21f6273 docs: enrich category theory preliminaries`；执行调试前工作树干净，远端 `origin/minimal` 已同步。
- O2：Markdown lint 命令退出码为 `0`，没有输出诊断信息。
- O3：`README.md` 中的本地链接目标 `explain.md` 存在；当前文档只发现该本地文档链接和一个完整仓库外部链接。
- O4：没有发现 `<details>`、`<summary>`、手工 `<a id>`、`点击展开/收起` 或“不是……而是……”结构；`$$` 行共 `22` 个，数量为偶数。
- O5：`git diff --check` 退出码为 `0`，当前变更没有空白错误。

## Hypotheses

### H1: README 的近期扩展应先通过静态结构层的确定性验证（ROOT HYPOTHESIS）
- Supports：本次变更新增了较长的类比段落、代码块和数学块，结构风险集中在新增区域。
- Conflicts：当前没有具体渲染或 CI 报错，缺陷尚未被观察到。
- Test：运行固定版本 Markdown lint、`git diff --check`，并统计 `$$` 分隔符数量，确认结构是否完整。

### H2：`README.md` 到 `explain.md` 的本地跳转失效
- Supports：最近把 `explain.md` 的详细内容纳入预备知识，同时保留了附录链接。
- Conflicts：工作树中存在 `explain.md`，README 链接目标为同级路径。
- Test：解析 README 链接并检查本地目标文件存在。

### H3：此前清理过的折叠标签、手工锚点或禁用句式重新进入 README
- Supports：当前分支历史上曾使用过这些结构，新增内容可能带回旧模式。
- Conflicts：本次新增内容按纯 Markdown 线性结构编写。
- Test：扫描 `<details>`、`<summary>`、`<a id>`、折叠提示和“不是……而是……”模式。

## Experiments

### E1
- Hypothesis: H1
- Change: 无；仅运行固定版本 lint、空白检查和数学分隔符统计。
- Expected: 若结构有效，所有检查退出码为 `0`，数学分隔符数量为偶数。
- Result: Markdown lint 退出码 `0`；`git diff --check` 退出码 `0`；`$$` 数量为 `22`。
- Verdict: confirmed
- Revert: 无需回滚；实验未修改仓库文件。

### E2
- Hypothesis: H2
- Change: 无；检查 `explain.md` 是否存在并列出 README 中的 Markdown 链接。
- Expected: `explain.md` 存在，README 的本地链接目标可解析。
- Result: 输出 `local-link: explain.md exists`；链接目标为 `explain.md`，检查退出码 `0`。
- Verdict: rejected
- Revert: 无需回滚；实验未修改仓库文件。

### E3
- Hypothesis: H3
- Change: 无；扫描折叠标签、手工锚点、折叠提示和禁用句式。
- Expected: 扫描无匹配结果。
- Result: 所有扫描均无输出。
- Verdict: rejected
- Revert: 无需回滚；实验未修改仓库文件。

## Root Cause

- 当前没有确认的产品或文档缺陷。调试请求未提供具体失败样本，现有可复现实验也没有失败；最近一次 README 扩展在已执行的静态门禁范围内保持通过。

## Fix

- 没有生产修复。保留本调试记录作为本轮审计证据；若后续出现具体 GitHub 渲染、链接或 CI 报错，应以该报错建立新的 RED 实验，不沿用本次“未发现失败”的结论。

## Regression Evidence

- 回归证据契约：Optional
- 契约文件：本轮未创建；没有确认的 bugfix 或 regression test。
- 测试：固定版本 Markdown lint、`git diff --check`、本地链接存在性、禁用结构扫描、数学分隔符配对。
- 结果：全部退出码为 `0`；没有新增生产修复需要回归证明。
- 备注：当前结论限定在 WSL 本地静态检查；GitHub 网页端实际渲染未在本轮复现。

## Failed Nodes

- 无。

## First Invalid Node

- 无；未发现失败节点。

## Upstream Lineage

- 用户的 debug 请求 → 目标提交 `21f6273` → README 结构与链接检查。

## Downstream Blast Radius

- 无；本轮实验未修改 README 或 explain 内容。

## Lowest Common Refinement Ancestor

- `README.md` 文档一致性静态检查。

## Repair Boundary

- 无需修复；如出现新报错，仅修改导致该报错的最小文档范围。

## Frozen Nodes

- `README.md`、`explain.md` 当前内容；本轮实验只读。

## Invalidated Nodes

- 无。

## Reverification Required

- 若后续修改 README、explain 或收到 GitHub/CI 具体错误，必须重新运行 lint、链接检查和对应的最小复现；本轮结论不能覆盖后续变更。

## Follow-up Validation: README 深度优化

- 基线：`c92eaed chore: record minimal README debug audit`。
- 变更范围：仅 `README.md`；补充工程态射契约、形式边界、`T_H` / `V_\Gamma` 记号和生成域术语边界，清除公式中的零宽字符。
- 静态结果：固定版本 `markdownlint-cli@0.48.0` 检查 `README.md`、`explain.md`、`DEBUG.md` 通过。
- 结构结果：`git diff --check` 通过；代码围栏 `28` 个且配对；数学块分隔符 `22` 个且配对。
- 约束结果：未发现折叠标签、手工锚点或禁用的“不是……而是……”句式。
- 链接结果：`README.md` 的本地入口 `explain.md` 存在。
- 结论：当前深度优化没有引入可复现的文档结构缺陷；GitHub 网页端渲染仍属于本轮未直接复现的外部环境项。
