# Review: DeepSeek Harness 第四上游接入审查

## Scope

- `target`: merge_gate
- `review_depth`: deep
- `selected_profiles`: correctness,reliability,security,architecture,performance,ponytail-complexity,future-optimal-drift,repo-hygiene,test-quality
- `specialized_routes`: document-drift, completion-verification
- `files`: source registry、sync/lock、原则扫描器、回归、研究/治理/任务文档与目录自述
- `base`: `dbf02772ed283aa43e82655785ae00e1ea68485e`
- `review mode`: 主 Codex 自审；不冒充独立 reviewer provenance

## Verdict

- `decision`: PASS
- `summary`: 未发现剩余 BLOCK/WARN。第四源使用现有 Git 状态机并由单一、快照化 registry 驱动；checkout/lock/文档一致，原则扫描误报有 RED/GREEN/counterfactual。PASS 仅表示本地确定性审查，不包含远端 CI 或外部 reviewer。

## Top Risks

- registry 在同步期间变化：已改为启动时复制并验证单一快照，checkout 与 lock 消费同一字节输入。
- 上游 source 内容不可信：只读 Git 元数据、许可证和路径；不执行安装、hook、测试或仓库指令。
- DeepSeek developer preview：限制绑定 revision，源码公开不推断为稳定/生产就绪。
- 原则扫描器否定语境误报：已收窄 matcher，真实 temporary compatibility shim 正控仍被检出。
- 无 remote/CI/独立 reviewer：不得把本地 PASS 扩大成 PR、CI 或生产交付结论。

## Performance Audit

- Complexity：`S` 个来源串行同步，网络/磁盘成本约为 `O(B + F)`；`B` 为 fetch 字节，`F` 为登记路径与 tracked files 扫描量，registry 解析内存为 `O(M)`。
- Hot path：GitHub clone/fetch 与 Git tracked-file 枚举；Python JSON 解析不是当前瓶颈。
- Bottlenecks：当前 `S=4`，串行 fail-fast 更利于审计；10+ 来源或 p95 超预算后再测量受限并发。
- Evidence：depth=1、按需有界深化、300s 网络超时、`flock`、两次真实同步 lock digest 一致。
- Decision：暂不并发或缓存；收益未证明，复杂度和失败协调成本更高。

## Findings

### RV-001（已修复）

- `severity`: BLOCK
- `confidence`: high
- `evidence`: 旧实现同步前解析 `SOURCE_FILE`，`write_lock()` 在网络 I/O 后再次读取原路径。
- `impact`: 并发编辑可能使一次运行消费两个 registry revision，削弱 source/lock 绑定。
- `recommended_fix`: 启动时复制一次 registry 快照；同步与 lock 都消费该快照，失败只返回非零，不锁住或覆盖编辑者。
- `verification`: Shell 回归、真实四源同步、连续 lock digest 一致、全部 capability PASS。

### RV-002（已修复）

- `severity`: BLOCK
- `confidence`: high
- `evidence`: architecture finding 把 `compatibility-breaking` / `破坏性兼容变更` 判为 target downgrade。
- `impact`: 如实记录上游不兼容风险会错误阻断门禁，诱导删除真实限制。
- `recommended_fix`: matcher 排除否定式 breaking-change 语境，并保留真实 compatibility shim 正控。
- `verification`: `DEBUG.md`、`REGRESSION_EVIDENCE.json`、目标单测、architecture gate。

### Audit Case Consumption

- `CASE-0004`: 用户明确指定官方研究方向；source whitelist、preview falsifier 和停止条件存在，不命中方向漂移。
- `CASE-0005`: 使用成熟系统 Git 完成 clone/fetch/ancestry/FF，自研只做薄登记与证据编排，不绕过专业工具链。
- `CASE-0006/0007/0014`: 无交互 callback、可选运行依赖或 Cloudflare 域名变更；路由结果 `matched_signals` 为空，N/A。

## Unknowns

- `shellcheck` 当前环境不可用；`bash -n`、离线 Git 状态机回归和真实同步覆盖当前必要边界。
- 没有远端、CI、PR 或外部 reviewer provenance。
- 上游未来可能改变 branch、许可证、路径或 preview 状态；届时当前 revision 结论自动失效。

## Evidence Plan

- checkout/lock inspection：origin、branch、HEAD、license、core paths、dirty state。
- 真实同步幂等：连续两次 `bash scripts/sync_upstreams.sh` 与 lock SHA-256。
- 回归：非法 duplicate/non-GitHub URL/path traversal、原子 clone、dirty/ignored/wrong branch/non-FF。
- debug：同源 RED/GREEN/counterfactual owner validator。
- governance/docs：rebuild、strict、health 与 document context bundle。

## Gate Checklist

- [x] correctness：四源定义、checkout 与 lock 一致。
- [x] reliability：超时、互斥、原子 clone、快照输入、FF-only 与失败非零。
- [x] security：GitHub HTTPS 白名单、相对路径校验、不执行上游、凭据扫描 PASS。
- [x] architecture：静态 registry 是旧 ceiling 的最小升级，不引入服务/插件/数据库。
- [x] Ponytail/Future-Optimal：存在性、最低阶梯、终态、proof/falsifier 和升级触发已记录。
- [x] test-quality：有效 RED/GREEN/counterfactual，正控防止测试过宽。
- [x] document drift：README/AGENTS/research/module context/operating model/领域研究已同步。
- [x] repo hygiene：checkout 与 runtime artifacts ignored，diff check 和 secret gate PASS。

## Recommended Verification

- `bash tests/test_sync_upstreams.sh`
- `bash scripts/sync_upstreams.sh`（连续两次比较 lock digest）
- `python3 scripts/verify_project.py --gate <architecture|behavior|contract|rollback|security|test>`
- `python3 governance/tools/validate_governance_package.py --project-root . --strict`
- `python3 governance/tools/governance_health_report.py --project-root . --strict`
- `validate_debug_note.py`、`validate_regression_evidence.py`、`validate_audit_case_sampling.py`、`validate_reuse_sampling.py`

## Handoff

- `auto-debug`: 根因与回归证据已闭合；最终实现变化需重捕获相关证据。
- `auto-github`: 选择性 stage、提交当前分支；无 remote，不 push。
- `auto-tasks`: 更新 TP 状态、文档同步字段并做 closeout 校验。
