# Task-Level Acceptance
- Harness、Agent、Workflow 和元 harness 的边界可从长期文档查证。
- manifest 契约覆盖指令、上下文、工具、权限、循环、验证、观测、环境与生命周期。
- 有效样例 PASS；结构缺失和高风险免审批均被确定性 BLOCK。
- 治理 context bundle、strict validator 和 health report 没有未解释的阻塞问题。

# Validation Plan
1. 用 `validate_task_intent.py` 证明意图、风险与验收映射 READY。
2. 用 `uv run --locked --script scripts/validate_harness.py --self-test` 证明正例和多类负例的反事实敏感性。
3. 用项目 Verification Policy 编译 `VERIFICATION_PLAN.json`，执行六个 required capability。
4. 用 owner strict validator 重新执行 gate，并校验当前 Git tree、policy 与 artifact digest。
5. 用 auto-review 的 agent-harness、security、contract、Ponytail、future-optimal、test-quality 和 document-drift lens 自审。

# Review Gate
- Correctness：Schema 和策略没有已知假通过路径，错误定位可操作。
- Readability：领域语义、契约和实现职责分离，路径与入口明确。
- Architecture：控制面不拥有业务状态；没有统一 runtime/DB/UI 等投机对象。
- Security：权限默认拒绝，高风险审批、secret、内容信任和脱敏有结构化边界。
- Performance：validator 为 O(n)，当前无 I/O 或并发 hot path；不做无证据优化。

# Runtime Verification Gate
- 本轮没有受管 Harness 生产 runtime；线上 trace 和真实 eval 明确为 NOT COVERED。
- 本地 `architecture/behavior/contract/rollback/security/test` required gate 必须全部新鲜 PASS。
- 本地 validator 只证明确定性 conformance，不提供独立 reviewer provenance 或生产晋升权。
- 首个真实 harness 接入前，项目只能声明为本地控制面 bootstrap。

# Ship Readiness
- 交付形态：本地项目文件，不发布、不部署、不 push。
- 回滚：删除/恢复本轮新增文件；Schema 破坏性演进必须升级 `api_version`。
- 观察项：第二类 harness 是否触发 falsifier；validator 错误路径和接入字段缺口。

# Task Package Acceptance
## TP-01 研究并定义 Harness 领域模型
- `docs/HARNESS_MODEL.md` 包含定义、loop、控制面能力、候选路径、风险、效率和路线图。

## TP-02 落地 manifest 契约与 validator
- Schema 自身有效；正例 PASS；结构与策略负例 BLOCK；命令可重跑且错误非零退出。

## TP-03 建立项目治理与架构记忆
- 架构 context bundle PASS；ADR、QA、module context 与目录文档同步。

## TP-04 执行验证与风险审查
- 新鲜命令证据完整；所有实质 BLOCK 修复或明确保留为未完成项。

# Anti-Goals
- 不把研究汇报夸大为生产级元 harness。
- 不把 manifest 合规夸大为 agent 效果、安全或上线通过。
- 不新增没有当前消费方的 runtime、数据库、UI、队列或插件系统。
- 不虚构 Git、CI、线上、独立 reviewer 或部署证据。
