# 数学开放问题候选来源登记

> 本文件只登记来源范围、许可审查和解析策略，不是准入决定，也不携带候选原始数据。
> Vibe Mathing 的外部具体问题仓库与问题总库入口见 [`VIBEMATHING_PUBLIC_INDEX.md`](VIBEMATHING_PUBLIC_INDEX.md)。
> `problem-library/registry/candidate-sources.json` 是机器可读真相源；公开仓不发布 raw candidate
> 快照、派生 CandidateObservation 或来源网页正文。

## 隔离规则

- CandidateObservation 永远是 `collection=candidate`、`admission.state=candidate`、`research_eligible=false`。
- 来源的 `open`、`answered`、`resolved`、`solved` 等词只保留为 `source_status_raw` 及其保守映射，不能转成数学 Result。
- 候选默认不进入查询；使用 `scripts/query_problem_library.py` 时必须显式指定 `--collection candidates` 或 `--collection all`。
- 候选不能直接创建 Attempt、Result、Solution 或 canonical Problem；准入需要单独的来源、题面、定义域、量词、许可与陈述忠实性审查。
- PDF、压缩包、论坛/API、Git repository 和动态网页分别记录其 artifact locator；不能以文本相等自动合并翻译、改写或数学等价题面。

## 来源分组

注册表包含 39 个候选来源，覆盖以下公开发现路径：

- 结构化/专题目录：TheoremDB、OpenLogicProblems、TOPP、OpenQuantumProblems、UCSD Erdős Graphs、AIM、Clay。
- 社区/API 与索引：MathOverflow、Math StackExchange、Polymath、OEIS、Wikipedia、arXiv、PlanetMath、UnsolvedProblems.org、PrimePages。
- 文献/文档入口：Kourovka、Kirby/K3、Scottish Book、Green、Kyoto low-dimensional topology 等 PDF 或列表入口。
- 研究数据与交叉索引：FM:OP、vibemathed，以及其他列在 registry 中的发现源。

来源是否允许 `redistribution` 由 registry 的 license object 决定；许可证待审来源只允许受限本地 reference/query，不能自动公开其正文或训练/embedding。

## 受限 Git 来源

`teorth/erdosproblems` 与 `google-deepmind/formal-conjectures` 只作为 `vendor/sources.lock.json` 的
reference-only 固定来源。候选抓取器不得在目标目录不存在时执行未固定的 `git clone`；刷新必须先更新
lockfile、commit、许可证摘要和审计记录。固定 commit 不等于安装、可执行或数学准入。

## 可重建入口

```bash
# 隔离抓取（raw 与 inventory 只在本地生成）
python3 scripts/fetch_candidates.py --only theoremdb

# 从 inventory + 解析器生成 versioned CandidateObservation
python3 scripts/build_candidate_observations.py
python3 scripts/validate_candidate_problem_library.py --verify-raw
python3 scripts/audit_candidate_admission.py --source theoremdb

# 查询时显式声明 collection
python3 scripts/query_problem_library.py --collection candidates --source theoremdb --limit 20
```

抓取器默认单 writer、限速、网络 timeout、响应大小上限和非零失败；发现来源不可达时必须保留失败账本，不得以空记录伪装成功。公开提交前运行 `scripts/validate_public_boundary.py`，确认 raw、session、凭据和本机路径没有进入 Git。
