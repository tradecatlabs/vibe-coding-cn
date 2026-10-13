# Meta Harness Bootstrap Review

## Verdict

- Decision: `WARN`
- Review depth: `deep`
- Target: 本地 bootstrap 与确定性 closeout，不是 merge/release/production gate。
- Provenance: 当前主 Codex 自审；不具备仓库外独立 reviewer provenance。

领域模型、manifest 契约、项目验证策略和 required gate 均已建立，当前无未处理实现级 BLOCK。
`WARN` 来自仍然存在的保证边界：本地仓库没有 remote、PR 或 CI，也没有外部 reviewer；项目
尚未接入真实 Harness runtime、版本化 eval dataset、生产 trace 和组织审批系统。

## Selected Profiles

- correctness
- contract
- security
- reliability
- agent-harness
- architecture
- test-quality
- ponytail-complexity
- future-optimal-drift
- document-drift
- repo-hygiene
- performance
- completion-verification

## Audit Cases Consumed

- `CASE-0003`：TODO/STATUS/closeout 必须描述同一完成事实。
- `CASE-0005`：结构校验复用 JSON Schema/jsonschema，自研 Python 只做跨字段项目策略。
- `CASE-0007`：PEP 723 直接依赖与 `uv` script lock 固定完整运行闭包。
- `CASE-0008`：Verification Plan、input digest 和 gate result 必须由 owner 重算，不能自报。
- `CASE-0006`：无交互回调、冷查询或在线请求路径，不适用。
- `CASE-0014`：无 Cloudflare Pages、DNS 或外部资源变更，不适用。

## Findings

### RESOLVED-001：工具契约曾是悬空 URI

- Severity: `BLOCK -> RESOLVED`
- Evidence: 首轮样例使用不存在的 `builtin://...` Schema，仅能证明 URI 非空。
- Risk: 工具可声称存在输入/输出/错误契约，但实际无法解析或验证，形成准入假绿。
- Fix: 改为内联 Draft 2020-12 JSON Schema；validator 校验子 Schema 自身有效，并要求
  输入 Schema 是 `object` 且 `additionalProperties=false`。
- Verification: `synthetic://invalid-tool-input-schema` 被 self-test 确定性拒绝。

### RESOLVED-002：条件式审批曾指向不可解析 policy URI

- Severity: `BLOCK -> RESOLVED`
- Evidence: 首轮 `conditional` 声明引用 `policy://...`，项目没有 registry/resolver。
- Risk: 高风险工具看似受策略保护，运行时却没有可验证的策略实体。
- Fix: `v1alpha1` 收缩为 `never/always`；写和特权工具使用 `always`，模型自批固定为 false。
- Verification: 高风险工具改成 `approval=never` 和模型自批均被 self-test 拒绝。

### RESOLVED-003：运行依赖最初只固定直接版本

- Severity: `WARN -> RESOLVED`
- Evidence: PEP 723 固定 `jsonschema==4.25.1`，但最初没有传递依赖锁。
- Risk: 开发环境与未来最小运行环境可能解析出不同依赖闭包。
- Fix: 使用 `uv lock --script` 生成 `scripts/validate_harness.py.lock`，正式入口使用 `--locked`。
- Verification: `uv lock --check --script scripts/validate_harness.py` PASS。

### RESOLVED-004：原则扫描的空范围假绿

- Severity: `WARN -> RESOLVED`
- Evidence: 初始非 Git 目录使用 `--git-mode working` 时返回零扫描范围但 decision PASS。
- Risk: 把“什么也没扫描”误当作没有原则问题。
- Fix: 项目 gate 固定显式文件 scope，并同时验证结果类型、数量和 `finding_count`。
- Verification: architecture capability 扫描 18 个真实文件并由 strict validator 重新执行。

### RESOLVED-005：gate runner 猜错 owner 输出结构

- Severity: `BLOCK -> RESOLVED`
- Evidence: architecture 把 `scanned_files` 列表与整数比较；rollback 为字符串契约却被要求是对象。
- Risk: 有效项目状态被错误 BLOCK，导致验证控制面无法可信地裁决 closeout。
- Fix: 消费 scanner 与 manifest Schema 的真实类型，不调整风险 profile 或被测契约。
- Verification: `DEBUG.md` 和 `REGRESSION_EVIDENCE.json` 记录 RED、GREEN、反事实重新 RED；
  owner validator 校验 subject/test/argv/digest 一致。

### WARN-001：没有远端、CI 或独立审查 provenance

- Severity: `WARN`
- Evidence: 本地 `main` 有 revision，但 `git remote -v` 为空；没有 PR/check/reviewer receipt。
- Impact: 本地 HEAD 可以绑定输入和回归证据，不能证明 reviewer 身份独立或远端状态。
- Minimum fix: 用户指定远端和交付流程后，对固定 review HEAD 运行 CI，并由外部 reviewer 签发 provenance。
- Verification: Git delivery evidence、CI checks 和外部 review receipt；本任务不伪造。

### WARN-002：尚未完成真实 Harness 与 eval 接入

- Severity: `WARN`
- Evidence: 当前是 candidate manifest、样例、conformance validator 和项目本地验证控制面。
- Impact: 不能证明真实工具执行、权限 enforcement、checkpoint/resume、trace 或任务效果。
- Minimum fix: 接入第一个真实 Harness，构建版本绑定 eval；第二类 Harness 用 falsifier 审查契约泛化。
- Verification: adapter/conformance/eval/trace artifact；当前明确 NOT COVERED。

### WARN-003：高风险复盘没有外部 reviewer

- Severity: `WARN`
- Evidence: 本任务风险为 high；当前实现者不能为自己的复盘签发独立可信 PASS。
- Impact: 可保存并验证 task-local draft，但不能写入 canonical retrospective state 或签发 handoff。
- Minimum fix: 由 owner trust policy 中登记的外部 reviewer 对固定 draft digest 审查和签名。
- Verification: detached review signature、review receipt 与 owner validator；当前不自批。

## Deterministic Evidence

```text
PASS  uv lock --check --script scripts/validate_harness.py
PASS  manifest self-test：正例 + 多类 EXPECTED-BLOCK 负例
PASS  gate regression：RED -> GREEN -> counterfactual RED
PASS  Task Intent owner validator
PASS  auto-tasks task docs validator
PASS  Verification Policy/Capability Registry strict validator
PASS  architecture/behavior/contract/rollback/security/test required gates
PASS  owner strict verification：计划重编译、input/policy digest、artifact digest、全 gate 重执行
PASS  governance context bundle、strict validator、health report
PASS  inline credential filename-only scan
```

## Performance And Cost

- manifest validator 时间/空间复杂度均为 `O(n)`，`n` 为 manifest 节点数。
- gate runner 顺序执行六类本地能力；当前数据规模下人类契约评审是 hot path，不是 Schema 计算。
- 立即值得做：锁定依赖、负例回归、owner-derived digest、结构化 artifact。
- 数据后再做：批量 registry 索引、并行 eval、trace 存储和缓存。
- 暂不值得做：数据库、队列、常驻服务和微优化。

## Unknowns

- 第一个真实受管 Harness 的仓库、runtime、模型与部署平台。
- eval 数据集、阈值、holdout 和外部可信晋升 owner。
- 真实审批系统、credential manager、sandbox 与 trace backend 的集成契约。
- 远端、CI、PR 和独立 reviewer 流程。

## Gate Conclusion

- 本地研究、项目骨架、manifest 契约和确定性 closeout：可交付。
- 正式 merge/release/production readiness：`NOT ESTABLISHED`。
- manifest lifecycle 只能是 `candidate`，作者和模型均无自我晋升权。
