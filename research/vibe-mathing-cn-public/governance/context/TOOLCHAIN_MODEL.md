---
id: GOV-TOOLCHAIN-MODEL
type: context
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-09-01
review_cycle: P90D
---

# Toolchain Model

本项目优先复用 Git、GitHub Actions、JSON Schema、Python 数学库和 proof assistant；自研代码只连接来源、研究记录、验证和派生视图。

## 成熟工具优先

方法选型先按 [`FORMAL-METHODS-MAP.md`](../standards/FORMAL-METHODS-MAP.md) 定位，再按工具成熟度 registry 判断是否可运行；教程目录、包名或固定源码不能代替能力证据。执行编排按 [`RESEARCH-LIFECYCLE-MODEL-v0.1.md`](../standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md) 区分 Project、Workflow、Task、Step 和 Job。

- Git/GitHub Actions 管版本和持续验证；`vendor/sources.lock.json` 是公开来源固定的唯一清单。
- JSON Schema 管对象结构，Python 脚本管跨记录不变量、路径安全和原子派生。
- SymPy、NumPy、SciPy、mpmath 管有限计算，不自研通用代数或数值内核。
- SAT/SMT canary 只验证明确的有限输入协议；它是横向自动化/决策过程，不等于 Lean 演绎证明或完整模型检查；没有公开运行证据时不进入 evidence/verifier route。
- Lean/Mathlib v4.33.0 管固定 fixture 的形式化证明；Lean 位于依赖类型理论型演绎验证，kernel check 不替代陈述忠实性审查，也不代表整个形式化方法版图。
- 工具族使用 `surveyed → source_locked → installed → smoke_checked → evidence_capable → verifier_admitted` 状态机。状态不是安装数量，也不是数学结论。

41 个工具族的公开边界见 [`governance/tools/MATH_TOOL_CATALOG.md`](../tools/MATH_TOOL_CATALOG.md) 和机器注册表 [`governance/control-plane/math-tool-maturity.v1.json`](../control-plane/math-tool-maturity.v1.json)。

## 项目命令

| 场景 | 入口与边界 |
|---|---|
| 安装核心依赖 | `python3 -m pip install -r requirements.txt`；可选数学扩展使用 `requirements-math-tools.txt`。 |
| 可移植质量门 | `make check`；不要求 ignored raw、电子书、上游缓存或运行报告。 |
| 完整本地门禁 | `make check-full`；只在拥有本地来源/电子书/上游缓存时运行。 |
| 研究空间验证 | `python3 scripts/validate_research_spaces.py`；只读校验 Problem/Attempt/Result 与派生解库。 |
| ProblemContract 测试 | `python3 scripts/test_problem_contract.py`；验证定义域、量词、准入策略和预算。 |
| ResearchBundle 导出 | `python3 scripts/vibe_mathing_cli.py export-bundle --problem-id <id>`；从一致快照派生，只读且冲突失败。 |
| 候选 snapshot | `python3 scripts/build_candidate_observations.py`、`python3 scripts/validate_candidate_problem_library.py --verify-raw`；候选不准入。 |
| 候选查询 | `python3 scripts/query_problem_library.py --collection candidates --limit 20`；默认 collection 仍是 admitted。 |
| 工具成熟度 | `python3 scripts/validate_math_tool_maturity.py`；route 不得超过 maturity。 |
| 工具探针 | `python3 scripts/check_math_tools.py --profile <profile> --strict`；每个外部命令都有 timeout，输出仅有稳定标签。 |
| 工具 canary | `MATH_CANARY_SOURCE_SHA256=$(python3 -c 'import hashlib; print(hashlib.sha256(open("scripts/run_math_tool_canaries.py","rb").read()).hexdigest())') python3 scripts/run_math_tool_canaries.py --tools T13,T15,T16 --json --strict`；只执行合成有界案例，不创建数学 Result。 |
| canary 报告校验 | `python3 scripts/validate_math_tool_canaries.py --report <report.json>`；公开仓不携带运行报告。 |
| 文献 provider | `python3 scripts/check_literature_providers.py`；默认离线校验，`--live` 才访问网络且不保存正文。 |
| 供应链校验 | `python3 scripts/sync_supply_chain.py --check`；Git reference 只允许 no-checkout、固定 commit 和根许可证摘要。 |
| 问题库重建 | `python3 scripts/fetch_erdosproblems.py all`；网络抓取不作为 CI 提交门，使用缓存时仍需离线校验。 |

## 依赖边界

- `requirements.txt` 是 CI 与可移植质量门的直接依赖真相源；`requirements-math-tools.txt` 是可选探索扩展，不改变核心准入。
- `vendor/upstream/`、`problem-library/raw/`、`problem-library/derived/` 和 `literature/files/` 是本地忽略材料，不得成为 `make check` 的隐式依赖。
- `vendor/upstream/reference/` 只保存固定 Git 对象，不包含工作树；固定来源不等于安装、激活或验证器准入。
- `fixtures/lean-proof/lean-toolchain` 固定 Lean v4.33.0；`lakefile.toml` 固定 Mathlib revision。编译、axiom audit 和 statement-faithfulness 是不同门。
- `literature/providers.json` 只保存非敏感请求配置；凭据值只能来自调用进程环境，绝不写入仓库或审计输出。
- `canonical-problem.schema.json` 是 ProblemContract 输入契约；`research-bundle.schema.json` 是只读派生输出契约，不拥有持久化 collection。

## 资源与安全

- 所有计算、solver、CAS、外部命令、HTTP 请求和 canary 子进程都必须有 timeout、资源预算、重试/停止条件、输出或响应上限、终止回执和失败语义；这些约束同时适用于每个 Job 及其父级累计预算。
- GPU 或并行粗筛如果被外部项目接入，也只能产生有限候选；精确裁决必须回到已审查的 CPU/形式化路径。
- 工具成功、版本存在、固定 commit、Lean build、有限枚举和模型自评都不能单独升级 Result。
- 失败路线只追加到 `research/records/failed-routes.jsonl`；不覆盖历史，也不把失败伪装成 solved/refuted。
- 公开仓不保存 prompt、reasoning、session、机器路径、endpoint、IP、凭据、模型权重或运行日志。

## 禁止或谨慎使用

- 禁止用 CI 重新抓取动态网页后覆盖版本化记录。
- 禁止把有限枚举、数值拟合、模型自评、Lean build 或 canary PASS 直接升级为数学 Result。
- 禁止执行没有 timeout、资源预算、停止条件和失败回执的 solver、CAS 或外部命令。

## 工具链变更流程

1. 先证明现有公开工具和契约不能满足需求。
2. 固定版本、来源、许可证、owner、资源预算、timeout、失败语义和证据上限。
3. 同步 schema、脚本、测试、Makefile、CI 和本模型。
4. 运行 `make check`；涉及 ignored 材料时再运行相应 full/production 门。
5. 只能使用普通 Git revert 回滚；禁止改写已发布历史。
