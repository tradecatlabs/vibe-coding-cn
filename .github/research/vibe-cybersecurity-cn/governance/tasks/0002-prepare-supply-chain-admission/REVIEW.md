# Review

- Date: `2026-08-13`
- Target: 网络安全供应链准入候选表
- Provenance: 主 Agent 自审，无外部独立 reviewer provenance
- Verdict: `PASS` for candidate-table preparation; `BLOCK` for real admission

## Findings Resolved

### RESOLVED-01 — 八门禁可被目录自身缩减

- Evidence: 初版从 `admission-candidates.json.check_keys` 派生必填门禁，修改者可同时删除 key 和各候选 check。
- Impact: 可能在缺安全审查时伪造“全部通过”。
- Fix: 校验器固定 `REQUIRED_CHECK_KEYS`，JSON 必须逐项完全一致；新增删除门禁负例。
- Verification: `test_required_check_keys_cannot_be_deleted`。

### RESOLVED-02 — 通过状态缺少证据引用

- Evidence: 初版 check 可以写 `pass` 而无需指向 artifact。
- Impact: 状态自报不能证明许可、安全、接口或回滚门禁真实通过。
- Fix: 新增 `evidence_refs`；除 research_source 外，每个 `pass` 必须绑定安全相对引用。
- Verification: `test_passed_gate_requires_evidence`。

### RESOLVED-03 — 供应链目录越权拥有 enabled 状态

- Evidence: 初版生命周期包含 `enabled`。
- Impact: 供应链 maintainer 可能被误解为能批准具体网络动作。
- Fix: 删除 `enabled`；具体运行权只归 `ScopeGrant`、运行时策略和预算。
- Verification: 状态枚举与政策文档检查。

### RESOLVED-04 — 研究血缘路径绑定模块 ROOT

- Evidence: 隔离测试目录替换 `ADMISSION_PATH` 后，校验器仍读取真实 0001 目录。
- Impact: 迁移与负例测试可能读取错误真相源。
- Fix: 相对 `ADMISSION_PATH.parent` 解析固定 `source_catalog`。
- Verification: `test_active_high_research_candidate_is_rejected` 从 RED 转 GREEN；详见 `DEBUG.md`。

## Passed Checks

- 18 项全量覆盖且只覆盖 0001 研究 MVP。
- active-high 和非 MVP 无法进入本轮准入队列。
- 候选不授予运行权，具体 pin/digest 未猜测。
- `admitted` 必须要求 verified pin、SHA-256 和全部门禁证据。
- profile 与网络副作用必须匹配。
- 表格由研究事实与准入 overlay 联合确定性生成。
- 实现只用 Python 标准库；时间复杂度 `O(n log n)`、空间 `O(n)`，`n=18`，不是 hot path。

## Unknowns / BLOCK Before Admission

- 固定版本、制品摘要、签名和 SBOM 尚未选择或验证。
- 许可证仍需按具体 artifact 审查。
- 行为、隔离、回滚和安全负例尚未实际执行。
- 当前审查为实现者自审，不能替代未来真实 artifact 的独立准入审查。

## Gate

候选表准备完成可以交付；任何工具的 `verified`、`admitted` 或可运行声明继续 BLOCK，直到真实证据引用和 owner 门禁全部闭合。
