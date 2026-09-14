# Scripts

## 边界与来源

- `validate_public_boundary.py` / `test_validate_public_boundary.py`：验证公开 origin、禁止路径、符号链接、敏感内容模式和不可发布文件类型；未知输入 fail-closed。
- `check_public_readme.py`：校验中英文 README、`llms.txt`、公共元数据、声明账本、链接/锚点以及空 canonical ledger 状态。
- `audit_public_status.py` / `test_audit_public_status.py`：只读、带大小上限地统计三张 canonical ledger 和 `solutions.json`，输出 SHA-256 文件摘要；不写入、不准入 Result，`--expect-empty` 仅用于当前公开空状态门禁。
- `check_ai_citation_assets.py`：校验 AI 引用资产、双语回答矩阵、实体卡、Schema.org 元数据、GEO 评估协议/报告模板、证据引用和反操纵边界。
- `validate_plfb_metamodel.py` / `test_validate_plfb_metamodel.py`：校验公共 PLFB 概念 registry、F01–F13/B0–B4、唯一归属、PWTSJ/OSPS 定位和虚假 runtime 能力升级攻击；不保存业务实例。
- `query_ai_citation.py` / `test_query_ai_citation.py`：只读渲染固定 retrieval intent 和稳定 GitHub 引用 URL；拒绝路径逃逸，不访问网络或写入研究记录。
- `sync_supply_chain.py` / `test_sync_supply_chain.py`：按 lockfile 幂等同步固定 Git reference 和审计快照；拒绝移动分支归档、未固定 clone 与 TLS 验证绕过。外部命令有 timeout。
- `validate_project.py`：校验 active skill 结构、来源映射和禁止依赖。
- `smoke_math.py`：验证公开 SymPy/mpmath 计算切片。
- 方法选型总览见 `governance/standards/FORMAL-METHODS-MAP.md`；脚本能力和 maturity 标签不得被解释为完整形式化方法或数学证明。

## 问题库与候选

- `fetch_problem_library.py`：限速抓取公开问题目录，保存本地 raw 并重建 records/indexes。
- `validate_problem_library.py` / `test_problem_library.py`：在拥有 ignored raw 时校验来源覆盖、哈希、许可归属和索引一致性。
- `validate_portable_problem_library.py`：校验进入 Git 的问题 schema 与空 canonical 边界。
- `query_problem_library.py` / `test_query_problem_library.py`：查询问题集合；默认 `admitted`，候选必须显式 `--collection candidates|all`。
- `query_vibemathing_public.py` / `test_query_vibemathing_public.py`：只读查询 `vibemathing` 公共仓库元数据与 canonical catalog；不 clone、不执行远端代码、不写本地问题记录。
- `fetch_candidates.py` / `test_fetch_candidates.py`：从登记的候选来源获取本地原始输入；只接受固定来源，失败不伪造成功。
- `consolidate_candidates.py`：将允许的来源适配为候选输入；不创建 canonical Problem。
- `build_candidate_observations.py`：生成绑定 inventory、parser、schema、registry 和 raw artifact digest 的 snapshot。
- `validate_candidate_problem_library.py` / `test_validate_candidate_problem_library.py`：验证候选 schema、路径、latest pointer、artifact digest 和 `research_eligible=false`。
- `audit_candidate_admission.py`：只读审计候选准入条件；不写 SourceRecord、ProblemContract、Attempt、Result 或 Solution。

## 研究、证据与工具契约

- `validate_research_spaces.py`：校验 ProblemContract、Attempt/Result 引用、二维状态和完整解派生索引。
- `test_problem_contract.py` / `test_research_bundle.py`：测试 ProblemContract v1 和只读 ResearchBundle 的冲突/生命周期边界。
- `test_research_spaces.py`、`test_trusted_evidence.py`、`test_evidence_attacks.py`：用正例和攻击性反例校验解库晋升、伪 locator/hash、路径逃逸、symlink、自验证与越权能力。
- `validate_failed_routes.py` / `test_validate_failed_routes.py`：校验 append-only 失败路线账本。
- `vibe_mathing_cli.py`：统一 `register-problem/run/resume/verify/status/cancel/export-bundle` 单机入口；只接受受限 adapter。
- `test_research_store.py`：验证 JSONL 唯一 writer、并发幂等与 WAL 崩溃恢复。
- `test_vibe_mathing_runtime.py` / `test_vibe_mathing_pipeline.py`：验证状态转换、重试、timeout、输出预算和确定性 SymPy 垂直链。
- `test_lean_pipeline.py`：运行固定 Lean/Mathlib kernel、逃逸、公理和陈述忠实性链。
- `compute_plan.py`：为受限计算计划校验 timeout、预算、停止条件和允许的 adapter。

## 数学工具与文献

- `validate_math_tool_maturity.py` / `test_validate_math_tool_maturity.py`：校验 41-family registry，禁止 maturity 与 runtime route 越权。
- `check_math_tools.py` / `test_check_math_tools.py`：执行有界、稳定标签的现场探针；不输出主机、容器、endpoint 或凭据。
- `run_math_tool_canaries.py` / `test_run_math_tool_canaries.py`：运行合成正例、反例、错误和 timeout canary；不访问网络或研究记录。严格模式要求调用方显式绑定 `MATH_CANARY_SOURCE_SHA256`。
- `validate_math_tool_canaries.py` / `test_validate_math_tool_canaries.py`：校验显式 canary 报告及 runner digest；公开仓不携带内部报告。
- `check_literature_providers.py` / `test_literature_providers.py`：校验 provider registry；live 请求必须显式开启，凭据只来自环境，正文不落盘。
- `validate_portable_literature.py` / `validate_literature.py`：校验文献目录和本地二进制摘要边界。

## 质量门

- `pipeline_maturity_audit.py`：现场执行带 timeout、资源预算和终止回执的 required capabilities；严格模式只在全部通过时输出满分。
- `check.sh`：CI 与本地共用的可移植质量门；任一子检查失败即非零退出。

所有脚本只写本项目范围；网络、solver、CAS、Lean、Git 和其他外部命令必须有 timeout、资源/输出/响应上限、停止条件、终止回执与明确失败语义。
