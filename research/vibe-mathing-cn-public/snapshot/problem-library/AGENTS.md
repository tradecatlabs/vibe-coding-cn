# Problem Library Agent Guide

本目录分离来源观察、候选发现和稳定研究输入。`raw/` 是不可编辑、可重建的来源证据；`derived/` 是带输入摘要的候选派生层；只有 `records/canonical-problems.jsonl` 中的 ProblemContract 才能进入研究生命周期。

## 目录结构

```text
problem-library/
├── README.md
├── RESEARCH_CANDIDATES.md       # 候选来源范围与许可边界
├── OVERVIEW.md                  # 公开能力与资源路径图
├── VIBEMATHING_PUBLIC_INDEX.md  # 外部具体问题库与网页版模板入口
├── BOUNTY_PROJECT_2_TOP146.md   # Project #2 View 3 的带日期赏金仓库快照
├── templates/                   # 可复制的 draft ProblemContract 模板
├── schema/
│   ├── problem.schema.json
│   ├── canonical-problem.schema.json
│   ├── candidate-source.schema.json
│   └── candidate-observation.schema.json
├── registry/candidate-sources.json
├── registry/bounty-project-2-top146.v1.json
├── registry/vibemathing-public-source.v1.json
├── raw/                         # Git ignored：来源响应、inventory、失败账本
├── derived/candidate-observations/ # Git ignored：CandidateObservation snapshot
└── records/
    ├── problems.jsonl           # 已准入来源观察（本地生成）
    └── canonical-problems.jsonl # ProblemContract 输入，目前为空
```

## 边界与不变量

- 来源数据、raw 快照、manifest、索引和候选 snapshot 只在本地重建，不进入公开 Git。
- `raw/` 不是知识编辑区；刷新只能通过抓取器完成，不能用手工空记录掩盖失败。
- CandidateObservation 必须是 `collection=candidate`、`admission.state=candidate`、`research_eligible=false`。
- `answered`、`resolved`、`solved` 和 `open` 是来源状态，不是数学 Result；候选不能直接创建 Attempt、Result、Solution 或 canonical Problem。
- 默认查询 collection 是 `admitted`；查询候选必须显式使用 `--collection candidates` 或 `--collection all`。
- 候选记录必须绑定 registry 的 parser、source status map、license、raw artifact 路径和 digest；snapshot 必须绑定 inventory、parser、schema 和 registry digest。
- artifact、latest pointer 和 snapshot output 路径必须是仓库相对路径且不能逃逸允许的 raw/derived 根目录。
- Git 来源必须先进入 `vendor/sources.lock.json` 的固定 reference；禁止抓取器执行未固定的 clone 或 branch archive。
- 来源记录不能直接作为 canonical Problem。ProblemContract 必须冻结陈述、定义域、量词、定义、假设、允许公理、固定准入策略和有界执行预算。
- `lifecycle` 只表示 ProblemContract 是否可研究：`draft → active → withdrawn`；不恢复解题 `status` 双真相。
- 顶层 `Project → Workflow → Task → Step → Job` 是编排层语言；问题库只提供 Project 引用的契约输入，不直接生成 Job、Attempt 或数学 Result。

## 维护命令

```bash
python3 scripts/fetch_erdosproblems.py all
python3 scripts/fetch_candidates.py --only theoremdb
python3 scripts/build_candidate_observations.py
python3 scripts/validate_candidate_problem_library.py [--verify-raw]
python3 scripts/audit_candidate_admission.py --source theoremdb
python3 scripts/query_problem_library.py --collection admitted --limit 10
python3 scripts/query_problem_library.py --collection candidates --limit 10
python3 scripts/query_vibemathing_public.py --catalog
python3 scripts/query_vibemathing_public.py --kind concrete --limit 20
python3 scripts/validate_problem_library.py
python3 scripts/test_problem_library.py
```

所有网络请求和外部命令都必须有 timeout、限速、响应/输出上限、停止条件和非零失败语义。并行 agent 不得同时重建同一 `records/manifest/indexes` 真相源；重建后必须重新运行校验。
