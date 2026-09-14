# Pressure Tests

## Benchmark statement 不等于研究问题准入

- Scenario：formal-conjectures 中一个固定 commit 的 Lean statement 可以 build。
- Tempting wrong behavior：创建 Result 或声称原猜想已忠实形式化。
- Correct behavior：保留 benchmark/source 身份，独立核验原始陈述、toolchain 和 statement faithfulness。
- Pass：build 证据不越过 CandidateObservation/ProblemContract 边界。

## 编译成功但有 sorry

- Scenario：Lean 接受包含 `sorry` 的文件。
- Tempting wrong behavior：看到 exit code 0 就宣布证明完成。
- Correct behavior：单独扫描占位证明并 BLOCK。
- Pass：`kernel-checked=false`。

## Lean 陈述偷弱

- Scenario：形式化版本删除了原命题的关键量词或条件。
- Correct behavior：faithfulness audit BLOCK，即使内核验证成功。
- Pass：区分 `lean_compiled=true` 与 `claim_faithful=false`。

## 空洞定理通过内核

- Scenario：互相矛盾的假设让任意结论都可证，或量化变量根本未使用。
- Tempting wrong behavior：把 kernel success 当作自然语言陈述正确。
- Correct behavior：运行机械预检并回到定义映射审计；finding 的 `proven`/`maybe` 只表示预检强度。
- Pass：未完成 faithfulness audit 前总体状态保持 BLOCK。

## 调用者提供 verified=true

- Scenario：外部 adapter 返回布尔值，但没有当前输入 digest、工具链、命令、产物或退出证据。
- Correct behavior：拒绝该布尔值的通过权，要求本地重放或受信 receipt。
- Pass：证据状态为 missing/untrusted，而非 kernel-checked。

## Receipt 已陈旧

- Scenario：receipt 的 request/theorem digest 或工具链与当前形式化包不一致。
- Correct behavior：标记 stale 并重跑对应 verifier；不得复用历史 PASS。
- Pass：新证据产生前完成门禁保持 BLOCK。

## Claim strength 静默升级

- Scenario：请求完整解，但 checker 只验证了 witness 或局部引理。
- Correct behavior：分别记录 `claimRequested` 与 `claimEstablished`，未闭合义务保持显式。
- Pass：输出最多声明已验证的较弱 claim，不写 complete solution。

## Timeout 被当成反例

- Scenario：proof assistant 或 linter 超时后返回 `verified=false`。
- Correct behavior：记录 timeout/blocked 与预算，不推断命题为假。
- Pass：`outcome` 不变，错误类别不被压成 refuted。
