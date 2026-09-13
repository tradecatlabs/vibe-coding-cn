# 问题库全景综述与资源路径图

本仓库把问题来源分为三层：

1. **raw**：本地来源证据和下载账本，Git ignored、不可人工编辑；
2. **derived**：由固定 inventory、解析器、schema 和 registry 派生的 CandidateObservation 快照；
3. **admitted/canonical**：经过来源审查、题面忠实性和 ProblemContract 校准后的研究输入。

## 可公开复用的能力

- `VIBEMATHING_PUBLIC_INDEX.md`：链接 Vibe Mathing 公共具体问题、问题总库和网页版研究模板；只读 pointer，不自动导入。
- `scripts/query_vibemathing_public.py`：以 timeout、响应上限和 namespace 绑定查询远端公开仓库元数据与 canonical catalog。
- `problem-library/templates/problem-contract.template.json`：创建 draft ProblemContract 的复制起点。
- `scripts/fetch_problem_library.py`：重建 Wikipedia 与 UnsolvedMath 来源记录。
- `scripts/fetch_erdosproblems.py`：将 Erdős Problems 页面纳入统一来源记录，并保存编号、标签、奖金与书目对账证据。
- `scripts/fetch_candidates.py`：隔离抓取候选来源；失败、超时、响应大小和并发写入均有明确语义。
- `scripts/build_candidate_observations.py`：绑定 raw artifact、解析器摘要、schema、registry 和 admission=false。
- `scripts/validate_candidate_problem_library.py`：校验 snapshot 输入、路径安全、artifact digest、parser 绑定、来源状态映射和候选隔离。
- `scripts/query_problem_library.py`：默认只查 admitted；候选必须显式 `--collection candidates|all`。

## 当前公开数据边界

公开 Git 不携带动态网页、论坛/API正文、PDF、压缩包、候选 raw、CandidateObservation 快照或空 canonical records。
这些内容只能在本地按来源许可和 registry 策略重建。canonical ProblemContract 当前仍是空库；这不等于来源库为空。

## 来源与许可

已准入来源记录由现有问题库 schema 管理；候选来源的角色、许可、允许用途和状态映射集中在
`problem-library/registry/candidate-sources.json`。许可不明确的来源不自动进入公开分发、训练或 embedding。
来源状态始终是来源元数据，不是数学结论。

## ProblemContract 边界

`problem-library/schema/canonical-problem.schema.json` 是 ProblemContract v1 的机器契约，冻结：

- 精确陈述、定义域、量词、定义、假设和允许公理；
- 固定 acceptance policy；
- 允许的方法、adapter、最大尝试次数、timeout、重试、内存/线程和输出预算；
- `lifecycle=draft|active|withdrawn`。

它不保存 `open|solved|refuted` 的解题状态。研究结果由 Result、有效 evidence 和派生 Solution View 决定。
只有 `active` ProblemContract 可以创建 Attempt。

## 资源图

```text
problem-library/
├── raw/                         # ignored；来源证据
├── derived/candidate-observations/ # ignored；版本化候选快照
├── registry/candidate-sources.json
├── registry/vibemathing-public-source.v1.json # 外部问题库/网页版模板 locator
├── templates/                   # draft ProblemContract copy template
├── schema/                      # source / candidate / ProblemContract schema
├── records/                    # 来源记录与空 canonical 输入
└── indexes/                    # 由校验器重建的索引
```

公开仓只发布可重建代码和契约；任何新增来源都必须先补 license、discovery、稳定 locator、parser、超时/失败语义和 admission 审计。
