# Task-Level Acceptance
- `research/HARNESS_RESEARCH.md` 覆盖全部 11 个新增 Harness，每仓包含当前 commit、许可证、技术栈、核心源码路径与六类维度结论。
- 每个结论可追溯到 `research/upstreams/<name>/` 相对路径或 lock 绑定事实；文档级证据显式标注。
- 横向比较与元 Harness 治理控制面借鉴写入 `docs/HARNESS_MODEL.md`、`research/UPSTREAMS.md` 与 research module context。
- 项目门禁、governance strict/health、任务文档校验全部 PASS；15 源 registry/lock/checkouts 保持一致且 clean。

# Validation Plan
- Source evidence：抽查每个 Harness 至少 3 个结论可溯源。
- 文档校验：governance strict/health、task docs、链接检查。
- 一致性：registry/lock/checkouts 15 源对齐。
- 门禁：architecture/behavior/contract/test + 原则扫描。

# Review Gate
- correctness：11 仓事实与源码路径一致，宣传/实现差异被记录。
- readability：每仓固定证据结构，篇幅克制。
- architecture：研究结论不改变系统边界；元 Harness 借鉴与控制面实现分离。
- security：不执行上游、无凭据。
- performance：检索使用 rg/索引式命令，报告不引入运行开销。

# Runtime Verification Gate
- Task Intent 与 Verification Plan 必须 READY。
- required capability 缺失、ERROR、非 PASS 或 stale evidence 时 fail closed。
- 外部 reviewer/CI 不存在时只声明本地确定性 PASS。

# Ship Readiness
- 选择性 stage 任务文件，确认 checkout/runtime 继续 ignored。
- 本地 commit 后在新 HEAD 上复跑关键回归与门禁。
- 无 remote 时不 push。

# Anti-Goals
- 不得修改任务范围以外路径。
- 不得虚构源码证据。
- 不得把文档宣传写成实现事实。
- 不得执行或安装任何上游内容。

# Task Package Acceptance
## TP-01
- Verify：`research/HARNESS_RESEARCH.md` 每仓小节的 commit、许可证、技术栈、核心路径与六类维度结论。
- Gate：结论可溯源；宣传/实现差异显式标注。

## TP-02
- Verify：`docs/HARNESS_MODEL.md` 与 `research/UPSTREAMS.md` 的横向比较和治理借鉴。
- Gate：借鉴结论与具体实现分离，不把研究事实写成控制面已实现能力。

## TP-03
- Verify：governance strict/health、task validators、15 源一致性、项目门禁。
- Gate：当前输入无 BLOCK，工作树 clean，本地 commit 可追踪。
