# Source Map

- `wentor-research-plugins`：`lean-theorem-proving-guide` 的 Lean 4/Mathlib/内核验证方向。
- 上游示例中的 `lean_agent` API 未被采用，因为当前供应链与本机没有证明该 API 可安装或可运行。
- `leanprover-skills`：官方 `lean-proof` 的工作期占位、逐个错误修复与最终无 `sorry`/error 门禁；`scripts/check-validation` 提供测试结果新鲜度思路。固定 commit 的 `lean-proof/tests/example.yaml` 仍是占位样例，因此不把其仓库状态视为充分评测证据。
- `mathevidence`：`schemas/checker-receipt.schema.json` 的 request/bundle/theorem/axiom digest、checker/toolchain、claim strength、unresolved obligations、assurance mode 与 result status 不变量。上游处于 experimental preview，只作 schema donor，不是本项目证明权威或第二真相源。
- `itpeval`：Lean/Rocq/Isabelle/HOL Light 原生 adapter 和 timeout/error 捕获边界。其记录主要压成 `verified: bool`，因此只吸收 adapter 形状，不复用结果 schema。
- `atp-checkers`：除零、自然数截断、空洞假设、未用 binder、`sorry`/axiom 等机械预检，以及 `proven`/`maybe` confidence。其 `LIMITATIONS.md` 明确不能裁决形式化是否表达正确数学，因此 finding 只能辅助 faithfulness audit。
- Lean 与 Mathlib 本身作为后续正式工具链依赖，使用时以官方文档、锁定版本和真实编译输出为准。
