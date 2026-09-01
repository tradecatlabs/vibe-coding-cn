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

## Follow-up Validation: 工程范畴边界优化

- 基线：`f5906e4 docs: formalize engineering category model`。
- 变更范围：仅 `README.md`；修正“六个核心词”的数量口径，补充工程范畴记号 $\mathcal{E}_{H,\Gamma}$、生成/执行/契约满足三层表，以及独立验证的可执行判据。
- 静态结果：固定版本 `markdownlint-cli@0.48.0` 检查 `README.md`、`explain.md`、`DEBUG.md` 通过。
- 结构结果：`git diff --check` 通过；代码围栏 `28` 个且配对；数学块 `28` 个且配对。
- 约束结果：零宽字符、折叠标签、手工锚点和禁用的“不是……而是……”句式均无匹配。
- 链接结果：`README.md` 的本地入口 `explain.md` 存在。
- 结论：本轮边界优化未引入可复现的文档结构或链接缺陷；当前剩余未知项仍是 GitHub 网页端实际数学渲染效果。

## Follow-up Validation: 验证语义严谨化

- 基线：864c8d8 docs: tighten category model semantics。
- 变更范围：仅 README.md；补充来源独立性谓词 $\mathsf{Ind}$ 与验证标记定义，限定部分映射的复合成功域，区分契约满足关系与工程层级，并同步文章结构说明、结论路径和记号表。
- 静态结果：固定版本 markdownlint-cli@0.48.0 检查 README.md、explain.md、DEBUG.md 通过。
- 结构结果：git diff --check 通过；代码围栏 28 个且配对；数学块分隔符 30 个且配对。
- 约束结果：未发现折叠标签、手工锚点、禁用的“不是……而是……”句式或零宽字符。
- 链接结果：README.md 的本地入口 explain.md 存在。
- 结论：验证独立性、偏映射适用域和章节口径已获得文档内明确表达；剩余未知项仍是 GitHub 网页端实际数学渲染效果。

## Follow-up Validation: 对偶与契约层次优化

- 基线：46abd06 docs: formalize verification semantics。
- 变更范围：仅 README.md；补充对偶范畴的对象/同态集合定义，明确对偶不推出逆态射，区分任务级契约 $\Gamma$ 与单步契约 $\Gamma_f$。
- 静态结果：固定版本 markdownlint-cli@0.48.0 检查 README.md、explain.md、DEBUG.md 通过。
- 结构结果：git diff --check 通过；代码围栏 28 个且配对；数学块分隔符 32 个且配对。
- 约束结果：未发现折叠标签、手工锚点、禁用的“不是……而是……”句式或零宽字符。
- 链接结果：README.md 的本地入口 explain.md 存在。
- 结论：对偶的形式含义、逆向工作的适用边界和任务/步骤契约层次已明确；剩余未知项仍是 GitHub 网页端实际数学渲染效果。

## Follow-up Debug: GitHub 数学宏兼容性

- RED：GitHub 页面显示 The following macros are not allowed: operatorname，相关数学块降级为原始文本。
- 根因：README.md 的公式和行内公式使用了 GitHub 渲染器拒绝的 \operatorname 宏。
- 修复：将 Ob、Hom、Pre、Post、Fail、Verified、Ind 的运算符排版统一为 \mathrm{...}；未改变公式的数学关系。
- 验证：operatorname 匹配数为 0；32 个数学分隔符和 28 个代码围栏均成对；固定版本 Markdown lint、调试记录校验和差异检查通过。
- 回归：README.md 保留本地入口 explain.md，折叠标签、手工锚点和零宽字符扫描均无匹配。
- 结论：源码层已移除截图中触发 GitHub 降级的宏；待 GitHub 页面重新渲染后确认视觉结果。

## Follow-up Debug: GitHub 行内公式分隔符

- RED：GitHub HTML 只将行内公式起始分隔符前有空格的内容转换为 math-renderer；紧跟中文标点的公式仍保留为原始文本。
- 根因：README.md 使用了中文逗号加美元符号、中文顿号加美元符号等无空格起始形式，触发 GitHub 行内数学解析边界。
- 修复：为所有行内公式起始分隔符补充前置空格，连续变量统一使用带空格的分隔形式。
- 验证：未发现中文字符或中文标点直接连接美元符号的位置；所有行内公式起始分隔符前均为空格；固定版本 Markdown lint、调试记录校验和差异检查通过。
- 结论：本地源码已满足 GitHub 行内数学解析的边界条件；推送后继续检查 GitHub 页面是否为每个公式生成 math-renderer。

## Follow-up Debug: 复合下标行内公式

- RED：推送后的 GitHub HTML 仍有 2 个行内公式未生成 math-renderer，原文中的下标被解析成 HTML 强调标记。
- 根因：复合下标公式 \mathcal{E}_{H,\Gamma} 放在行内美元分隔符中，触发 Markdown 下划线解析冲突。
- 修复：将该记号移入独立数学块，保留 \mathcal{E}_{H,\Gamma} 的原始数学表达。
- 本地验证：数学分隔符 34 个且配对；行内公式 93 组；未发现不满足 GitHub 起始边界的行内公式；Markdown lint、调试记录校验和差异检查通过。
- 结论：当前待推送改动已消除已知的 2 个复杂行内公式解析冲突。

## Follow-up Validation: 远端 GitHub HTML 烟测

- 基线：提交 `af9f655`。
- 结果：源码行内公式 93 组，GitHub 页面 `math-renderer` 节点 93 个，`operatorname` 错误字符串 0 个。
- 结论：已知宏、中文标点起始边界和复合下标冲突均已消除；GitHub HTML 已为每组行内公式生成渲染节点。
