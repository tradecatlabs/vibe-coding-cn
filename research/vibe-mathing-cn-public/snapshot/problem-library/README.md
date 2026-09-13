# 本地数学问题库

问题库把外部来源观察、候选发现和稳定研究输入严格分层。公开 Git 只发布可重建代码、schema、registry 与文档；动态网页、原始响应和派生数据留在本地。

Vibe Mathing 的公开具体问题、问题总库和网页版研究模板见 [`VIBEMATHING_PUBLIC_INDEX.md`](VIBEMATHING_PUBLIC_INDEX.md)。该页只保存外部公开入口和快照说明，不把远端仓库自动导入本地 canonical ledger。

Project #2 View 3 的高赏金问题仓库快照见 [`BOUNTY_PROJECT_2_TOP146.md`](BOUNTY_PROJECT_2_TOP146.md)，机器版本见 [`registry/bounty-project-2-top146.v1.json`](registry/bounty-project-2-top146.v1.json)。它们是带日期的 pointer-only 运营索引，不是 canonical Problem、Evidence、Result 或 Solution。

在顶层生命周期中，问题库提供 Project 所引用的 `ProblemContract` 输入；它不直接创建 Workflow、Task、Step、Job、Attempt 或 Result。五级编排与数学事实链的边界见 [`RESEARCH-LIFECYCLE-MODEL-v0.1.md`](../governance/standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md)。

## 来源层级

已准入来源记录由抓取器统一为 `records/problems.jsonl`：

- [Wikipedia: List of unsolved problems in mathematics](https://en.wikipedia.org/wiki/List_of_unsolved_problems_in_mathematics)
- [UnsolvedMath: Mathematics Problem Archive](https://www.unsolvedmath.com/problems)
- [Erdős Problems](https://www.erdosproblems.com/)

候选来源由 `registry/candidate-sources.json` 登记；`registry/vibemathing-public-source.v1.json` 登记外部具体问题总库、网页版模板和 pointer-only 集成策略。候选只进入 discovery，不是研究问题，也不创建 Attempt、Result 或 Solution。

## 数据边界

- `raw/` 是来源证据缓存，Git ignored、不可人工编辑；包含响应、下载账本和失败记录。
- `derived/candidate-observations/` 是由 inventory、解析器、schema 和 registry 摘要派生的版本化本地快照，Git ignored。
- `records/problems.jsonl` 是已准入的来源观察，允许来源状态、重复和不完整陈述；它不是 canonical Problem。
- `records/canonical-problems.jsonl` 是 ProblemContract v1 的输入记录，目前保持为空；空库不表示来源库为空。
- 来源的 `open`、`answered`、`resolved`、`solved` 只保留为来源元数据，不能当作数学结论。

“完整”只表示某一抓取批次覆盖了来源自身声明的范围，不表示数学上完备，也不表示题面已被独立证明。

## 许可与归属

- Wikipedia 记录按来源许可保留页面版本、来源链接和归属。
- UnsolvedMath 的公开页面未提供可识别的再分发许可；只在本地保存必要目录事实和短摘要，详情以原站为准。
- ErdősProblems 的使用边界按站点 `robots.txt` 的 Content-Signal 及其页面归属执行；不把来源内容用于 AI 训练，不复制论坛内容。
- 候选来源的 `license.review`、`allowed_uses` 和 `attribution` 以 registry 为准。许可未闭合的来源不自动公开正文、不进入训练或 embedding。

## ProblemContract

`schema/canonical-problem.schema.json` 冻结：

- 精确 statement、domain、quantifiers、definitions、assumptions、allowed_axioms；
- 固定 `acceptance.policy`；
- 允许的方法与 adapter、`max_attempts`、timeout、重试、内存/线程和输出预算；
- `lifecycle=draft|active|withdrawn`。

ProblemContract 不保存 `open|solved|refuted` 的解题状态。Result 与有效 evidence 决定研究结论；只有 `active` 契约可以创建 Attempt。

## 重建与查询

```bash
# 三来源统一重建（使用本地缓存；Erdős 入口负责协调）
python3 scripts/fetch_erdosproblems.py all

# 旧两来源入口
python3 scripts/fetch_problem_library.py
python3 scripts/fetch_problem_library.py --refresh

# 候选只在本地生成，不写入 admitted records
python3 scripts/fetch_candidates.py --only theoremdb
python3 scripts/build_candidate_observations.py
python3 scripts/validate_candidate_problem_library.py --verify-raw
python3 scripts/audit_candidate_admission.py --source theoremdb

# 默认只查 admitted；候选必须显式选择
python3 scripts/query_problem_library.py --collection admitted --source unsolvedmath --limit 20
python3 scripts/query_problem_library.py --collection candidates --source theoremdb --limit 20
python3 scripts/query_problem_library.py --collection all --text Riemann --json
```

抓取和构建必须有 timeout、限速、响应大小上限、单 writer 和明确失败语义。候选 snapshot 的每条记录绑定 raw artifact、parser digest、schema、registry 和 `research_eligible=false`；输入摘要变化必须生成新的 snapshot。

## 结构化字段

来源记录的 `source_native_id` 不能默认当作全局主键；同一题在不同来源的翻译、改写或数学等价关系需要人工审查。Erdős 记录的站点编号只是来源字段，不能替代本地内容身份。

CandidateObservation 的 `source_status_class` 只允许 `open_claimed`、`closed_claimed`、`under_review` 或 `unknown`。它描述来源声称，不描述本项目的 `Result.outcome`。

## 验证

```bash
python3 scripts/validate_portable_problem_library.py
python3 scripts/test_validate_candidate_problem_library.py
python3 scripts/test_fetch_candidates.py
python3 scripts/test_query_problem_library.py
# 拥有 ignored raw 与 manifest 时再运行：
python3 scripts/validate_problem_library.py
python3 scripts/test_problem_library.py
```

新增来源前必须补充许可审查、discovery 证据、稳定 locator、解析器、失败/超时规则和 admission 策略；结构漂移一律 fail-closed。
