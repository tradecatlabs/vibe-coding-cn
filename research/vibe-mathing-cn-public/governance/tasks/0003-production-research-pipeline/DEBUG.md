# Debug Record

## Bug

- 标题：伪造证据摘要可错误晋升解库
- 症状：不存在的 artifact、调用者自填的 SHA-256 与 `independent=true` 可让伪 Result 进入 Solution View。
- 首次发现位置 / 时间：`scripts/validate_research_spaces.py::accepted_independent_capabilities`，2026-08-13。

## Environment

- 仓库 / 模块：`vibe-mathing-cn` / research-space validator
- 运行环境：WSL Ubuntu，Python 3.12，单机文件系统
- 依赖 / 版本：Python stdlib、jsonschema；与网络和模型无关
- 配置差异：无；默认仓库状态可稳定复现

## Reproduction

1. 构造 generator 为 `candidate-generator` 的 Attempt。
2. 构造 proof Result，附两个指向不存在文件的 accept 证据，并自填 `independent=true` 与 64 位伪摘要。
3. 调用 `qualifies_as_solution`；修复前错误返回 `True`。

## Observations

- O1: 现有实现只检查摘要字段是字符串，从不读取 locator。
- O2: 独立性完全相信调用者布尔值，只比较 verifier 字符串不等于 generator。
- O3: 没有受信 artifact 根、verifier registry、现场 hash 或 symlink/path traversal 校验。

## Hypotheses

### H1: 证据摘要被当成证据本身（ROOT HYPOTHESIS）
- Supports: `accepted_independent_capabilities` 不进行任何 I/O 或 registry 查询。
- Conflicts: 无。
- Test: 用不存在 locator 和伪摘要运行固定回归测试，预期修复前错误晋升。

### H2: Result schema 足以阻止伪造
- Supports: schema 约束摘要格式和字段完整性。
- Conflicts: schema 无法证明文件存在、摘要匹配或签发者可信。
- Test: 伪记录能通过字段形状要求但仍被旧业务逻辑接受。

### H3: verifier 名称不同即可证明独立
- Supports: 旧实现只做字符串不等比较。
- Conflicts: 调用者可以任意填写两个名称。
- Test: 任意 `forged-verifier` 在旧实现中被接受。

## Experiments

### E1
- Hypothesis: H1。
- Change: 只新增固定回归测试，不改产品代码。
- Expected: 测试因伪 Result 错误晋升而 RED。
- Result: 标准化 RED 1/1 失败；GREEN 1/1 通过；移除修复后的 counterfactual 1/1 以相同指纹失败。
- Verdict: confirmed
- Revert: 测试不修改业务状态，无需回滚。

## Root Cause

- 信任边界落在 Result 的调用者自报字段，而不是由受信 verifier registry 和真实 artifact 派生；结构校验错误承担了真实性校验职责。

## Fix

- 在 TP-01 引入唯一可信证据解析入口：限制根目录、拒绝 symlink/逃逸、重算 SHA-256、校验 registry capability，并从 generator/verifier trust domain 派生独立性。

## Regression Evidence

- 回归证据契约：Required
- 契约文件：REGRESSION_EVIDENCE.json
- 测试：`scripts/test_trusted_evidence.py`
- 结果：`REGRESSION_EVIDENCE.json` 已绑定标准化 RED / GREEN / counterfactual 三阶段记录。
- 备注：原始 `regression-red.json` 保留首次发现证据；标准化记录用于 owner validator。更广的路径、摘要、symlink、自验证攻击矩阵由独立契约测试补充。

## Failed Nodes

- Result evidence admission
- Solution View derivation
-

## First Invalid Node

- `accepted_independent_capabilities`
-

## Upstream Lineage

- caller-supplied Result evidence fields
-

## Downstream Blast Radius

- `qualifies_as_solution` → `derive_solution_ids` → `solutions.json`
-

## Lowest Common Refinement Ancestor

- trusted evidence resolver
-

## Repair Boundary

- evidence path/digest/issuer/capability/independence validation；不改数学 outcome 规则。
-

## Frozen Nodes

- Problem、Attempt、Result 三对象模型
- outcome × evidence 二维语义
- append-only invalidation 规则
-

## Invalidated Nodes

- caller-supplied `independent` 的信任语义
- 未经现场校验的 `sha256` 与 `locator`
-

## Reverification Required

- research-space schema/cross-reference tests
- trusted evidence attack matrix
- Solution View rebuild
-

## Follow-up: 非交互 shell 找不到 Lean

- Observation：提交后直接运行 `python3 scripts/test_lean_pipeline.py` 报 `FileNotFoundError: lean`；`~/.elan/bin/lean` 与 `lake` 均真实存在，但当前非交互 shell 的 `PATH` 不包含 `~/.elan/bin`。
- Hypotheses：H4（ROOT）为 adapter 错把 shell PATH 当成安装事实；H5 为 Lean 未安装；H6 为固定 toolchain 损坏。
- Experiment：只在命令环境加入 `~/.elan/bin`，原命令立即通过，排除 H5/H6，确认 H4。
- Root Cause：工具发现边界只使用裸命令名，没有兼容 elan 官方默认安装目录。
- Fix：adapter 先用 `shutil.which`，再检查可执行的 `~/.elan/bin/lake`，所有 Lean 命令通过 `lake env lean` 绑定 fixture toolchain，仍缺失时输出明确错误；测试主动移除该 PATH 项后运行真实 Lean 链。
- Regression Evidence：`python3 scripts/test_lean_pipeline.py` 在当前不含 elan PATH 的 shell 中通过；随后重跑完整成熟度审计。

## Follow-up: CI 冷缓存构建日志超过预算

- Observation：GitHub Actions `31721149936` 的可移植 job 通过，生产 job 在 `lean-e2e` 以 85/100 失败；首个无效节点为 `lake build`，错误是输出超过 2 MiB 预算。
- Hypotheses：H7（ROOT）为冷缓存构建进度日志超过证据预算；H8 为 Lean 编译失败；H9 为 CI 超时。
- Experiment：CI 在 51 秒内因输出预算终止而非超时；Lake 5.0.0 帮助明确提供 `--quiet`，本地 `lake build -q` 成功且 stdout/stderr 均为 0 字节，支持 H7 并反对 H8/H9。
- First experiment：使用 Lake 官方 `--quiet` 模式消除非证据信息并锁定回执命令；本地通过，但 GitHub Actions `31721732429` 仍以相同 `SIGXFSZ` 指纹失败，因此否决“日志量是唯一根因”。
- Root Cause：`execute_bounded` 使用进程级 `RLIMIT_FSIZE` 限制日志临时文件，但该限制继承给子进程并同时限制 Lean 写入 `.olean/.a` 等业务构建产物；本地热缓存不重写大型产物，两个 CI 冷构建稳定复现。
- Fix：删除 `RLIMIT_FSIZE`，改用 stdout/stderr pipe 流式计数；任一通道超过预算或超时就终止整个进程组，但不限制业务文件。保留 Lake `--quiet` 以减少非证据信息。
- Counterfactual：runtime 回归让子进程在 100-byte 日志预算下写入 4096-byte 业务文件；旧实现会因文件限制失败，新实现必须成功，同时原有 1000-byte stdout/100-byte budget 负例仍失败。
- Reverification Required：runtime 回归、无 elan PATH 的 Lean E2E、成熟度审计 100/100、新 GitHub Actions production-loop。
