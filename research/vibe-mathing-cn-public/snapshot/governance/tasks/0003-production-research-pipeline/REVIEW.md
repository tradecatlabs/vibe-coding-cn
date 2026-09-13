# Review: Vibe Mathing 单机生产闭环

## Verdict

- decision: PASS
- target: release_gate
- depth: deep
- scope: 单机、单 Agent、可恢复、可审计研究闭环；不含外部 reviewer attestation 实际签发、分布式高可用或任意开放问题必然求解。
- provenance: 确定性命令与 owner validators 已通过；本文件不冒充平台或外部独立 reviewer 身份。

## Findings

### 已修复：伪造 invalidation 可撤销真实证据

- severity: BLOCK → FIXED
- evidence: 原实现先按调用者 `invalidates` 删除证据，再验证回执。
- impact: 不存在或未注册的失效记录可能把合法结果移出 Solution View。
- fix: 只有回执、输出 policy、独立性均通过的 `reject` 证据才有撤销权，且只能撤销同 capability 的更早证据。
- verification: `python3 scripts/test_research_spaces.py`，含伪 invalidation 与跨 capability invalidation 负例。

### 已修复：唯一 writer 可写入断链记录

- severity: BLOCK → FIXED
- evidence: Store 早期只运行单表 JSON Schema。
- impact: 直接调用 Store 可写入引用不存在 Problem 的 Attempt/Result。
- fix: 每次事务在同一 `flock` 临界区内对最终三表快照执行跨记录完整性验证。
- verification: `python3 scripts/test_research_store.py`，断链 Attempt 必须拒绝。

### 已修复：README 快速开始缺 Problem 注册入口

- severity: WARN → FIXED
- evidence: `run` 要求 canonical Problem，但示例未创建它。
- impact: 新用户照抄命令会立即失败。
- fix: 增加受 schema/完整性门保护的 `register-problem --file`，并提供可版本化 SymPy fixture。
- verification: CLI E2E 连续注册两次分别返回 `created=true/false`。

### 已修复：历史 accepted run 在 Result 失效后仍可被重复 run 返回

- severity: BLOCK → FIXED
- evidence: 运行状态记录历史执行结果，Result 失效后原实现会在终态快速返回，调用方可能把历史 `accepted` 误读为当前仍有效。
- impact: Solution View 已正确移除 Result，但重复 `run` 仍可能向上层输出误导性成功。
- fix: 终态 `accepted` 快速返回前强制重算 Solution View；Result 已失效时非零失败并指明失效结果，历史 run state 保持不可篡改。
- verification: `python3 scripts/test_vibe_mathing_pipeline.py` 覆盖失效、二次失效幂等及失效后重复 run fail-closed。

### 已修复：日志预算通过 RLIMIT_FSIZE 误伤业务构建产物

- severity: BLOCK → FIXED
- evidence: GitHub Actions `31721149936` 与 `31721732429` 均在冷缓存 Lean 构建中被 `SIGXFSZ` 终止；本地热缓存无法复现大型 `.olean/.a` 重写。
- impact: 2 MiB 日志安全预算错误限制了子进程写入的全部文件，使真实 Lean 冷构建稳定失败。
- fix: `execute_bounded` 改为通过 pipe 在宿主侧流式计数 stdout/stderr，超限或超时终止整个进程组，但不限制业务文件；Lake 保留官方 quiet 模式减少噪声。
- verification: runtime 反事实在 100-byte 日志预算下成功写入 4096-byte 业务文件，同时超量 stdout 仍 fail-closed；Lean E2E 与成熟度审计本地 100/100。

## Security / Reliability

- locator 限定 `research/artifacts/`，拒绝绝对路径、`..`、symlink、缺失文件和现场 SHA-256 漂移。
- verifier capability、trust domain 与 output policy 从 registry 派生；caller 自报 `independent`、PASS、hash 无通过权。
- receipt、verifier 输出与 Result evidence 只允许创建或 append-only 失效，内容漂移拒绝覆盖。
- JSONL 写入采用单机 `flock + WAL + fsync + os.replace`；WAL target/temporary 使用白名单并在读写前恢复。
- 同一 run 有进程锁；状态有 schema、合法转换、checkpoint、retry/timeout/output budget 与预算外紧急取消。
- Lean 固定 v4.33.0、Mathlib commit `db584cd6…`、完整 manifest；零 `sorry/admit/unsafe`，`#print axioms` 为零依赖。

## Architecture / Ponytail

- 目标终态保持三对象和一个派生视图：Problem / Attempt / Result → Solution View。
- 新增包只承担证据、存储、runtime 和 adapter 胶水；没有自研 CAS、proof kernel、数据库、队列、Web 服务或多 Agent 平台。
- `RuntimeErrorBase` 的存在性由统一 runtime 失败语义与专项测试证明；principle scan 的 ownership-surface WARN 已有最小边界和验证路径，不需要再造异常层级。
- JSONL 全量重写是有意受限的单机实现；达到可测写入瓶颈才迁移 SQLite/PostgreSQL。

## Performance / Cost

- 证据验证：O(E + artifact bytes)，单文件流式 SHA-256，空间 O(1)（JSON 输出解析除外）。
- JSONL 写入：O(n) 时间与 O(n) 内存；当前 truth records 为空、主要热路径是研究验证而非高频写入，暂不引入数据库。
- runtime 子进程：有硬 timeout、输出文件大小限制和有限 retry；无无界并发。
- Lean 首次安装约 548 MiB，Mathlib cache 8690 文件；CI 独立 30 分钟 job，普通 `make check` 不承担该网络成本。
- 升级触发：JSONL p95 写入或恢复超预算、记录达到 10x/100x 规模、或出现多主机 writer 需求时，用 benchmark 决定迁移。

## Evidence

- `MATURITY_AUDIT.json`: 100/100，所有 required commands 退出码 0，使用单调时钟。
- `REGRESSION_EVIDENCE.json`: owner validator 证明 RED / GREEN / counterfactual。
- `make check`: PASS。
- Lean：固定 Mathlib fixture 的 bounded kernel build PASS；`two_add_two` does not depend on any axioms。
- governance strict / health：PASS；task decompose validator：PASS；`git diff --check`：PASS。

## Remaining Boundaries

- 外部专家/平台 reviewer attestation 尚无实际签发渠道；实现提供 fail-closed 信任模型，不自签外部身份。
- 真实开放问题仍可能长期 `undetermined`；100/100 只证明闭环可靠，不证明搜索完备或必然求解。
- 当前 CI 配置已落盘但未推送，远端 GitHub Actions 尚未运行；本任务未获 commit/push 授权。
- owner task closeout 还要求项目 Verification Plan、Completion Exemplar handoff 和外部签名 retrospective；这些不影响本仓库所定义的单机产品成熟度 100/100，但在补齐前任务状态必须保持 `In Progress`。

## Rollback

- 代码/CI/文档使用普通 Git revert；禁止 reset/clean/checkout/stash 覆盖用户改动。
- 运行中断先完成 WAL；无法证明目标摘要时 fail-closed 并保留 journal。
- 数学结论失效只追加受信 invalidation 并重算 Solution View，不覆盖历史。
