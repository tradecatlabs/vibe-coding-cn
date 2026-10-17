# Task-Level Acceptance
- 所有数学事实写入只经过唯一 owner，重复执行和并发执行不产生重复或半提交记录
- 证据产物必须位于可信根、真实存在、现场哈希匹配，并由注册 verifier 生成独立性
- 统一 CLI 能完成 run/resume/verify/status，故障注入后可幂等恢复
- 确定性 SymPy 和 Lean 两条真实垂直链均生成可重算证据并通过解库准入
- 攻击性负例覆盖伪 locator、伪 hash、路径逃逸、symlink、自我验证、超时、预算和状态漂移
- 成熟度审计只在全部 required gate 新鲜通过时输出 100/100
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 6
- 当前可立即执行叶子节点: TP-01

# Validation Plan
- python3 scripts/test_trusted_evidence.py
- python3 scripts/test_research_store.py
- python3 scripts/test_vibe_mathing_runtime.py
- python3 scripts/test_vibe_mathing_pipeline.py
- python3 scripts/test_lean_pipeline.py
- make check
- python3 scripts/pipeline_maturity_audit.py --strict
- python3 governance/tools/validate_governance_package.py --project-root . --strict
- TP-01 | Verify: python3 scripts/test_trusted_evidence.py | Gate: 所有证据 locator 位于可信根、真实存在、现场哈希匹配，独立性由 verifier registry 派生
- TP-02 | Verify: python3 scripts/test_research_store.py | Gate: 重复/并发写不重复，失败不留下半提交，Solution View 只能由当前有效 Result 重算
- TP-03 | Verify: python3 scripts/test_vibe_mathing_runtime.py | Gate: 非法状态转换、预算耗尽、超时、取消和恢复漂移全部 fail-closed
- TP-04 | Verify: python3 scripts/test_vibe_mathing_pipeline.py | Gate: 单命令完成 Problem→Attempt→artifact→Result→receipt→Solution，重复运行幂等且失效后退出解库
- TP-05 | Verify: python3 scripts/test_lean_pipeline.py | Gate: 真实 Lean build 通过、无 sorry/admit/unsafe、#print axioms 可审计、版本固定、statement faithfulness 独立记录
- TP-06 | Verify: make check && python3 scripts/pipeline_maturity_audit.py --strict | Gate: 所有 required commands 新鲜通过、任务状态一致、文档无漂移、攻击性负例和回滚入口齐全

# Review Gate
- 任何 caller-supplied independent/PASS/digest 可直接晋升均 BLOCK
- 任何 artifact 路径逃逸、hash 未现场重算或 verifier 未注册均 BLOCK
- 任何中断恢复造成重复记录、半提交或重复副作用均 BLOCK
- 任何 Lean fixture 含 sorry/admit/unsafe、未固定版本或缺 axiom audit 均 BLOCK
- 任何 100/100 不是从 required command 现场执行派生均 BLOCK

# Runtime Verification Gate
- [x] 每个 tool/action 结果都有可回指证据或明确未执行原因。
- [x] 高风险动作没有由 worker/agent 自我批准；审批状态可追踪。
- [x] compaction / resume 后目标、计划、修改文件、审批状态和验证项未丢失。
- [x] verifier / 自审已检查关键发现是否有证据支持。
- [x] closeout 明确 coverage gaps、failed packets 和 unresolved questions。
- [x] TP-01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：pre-fix RED;post-fix GREEN;counterfactual
- [x] TP-02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：concurrency test;partial failure test;idempotency test
- [x] TP-03: 输出格式 `按 outputs/acceptance 汇报`；证据要求：state transition tests;timeout/output/retry tests;resume tests
- [x] TP-04: 输出格式 `按 outputs/acceptance 汇报`；证据要求：CLI-level E2E output;record/artifact digests;idempotency proof
- [x] TP-05: 输出格式 `按 outputs/acceptance 汇报`；证据要求：lean --version;lake build output;escape scan;#print axioms output
- [x] TP-06: 输出格式 `按 outputs/acceptance 汇报`；证据要求：fresh command outputs;maturity JSON/Markdown;document drift audit;rollback path

# Ship Readiness
- 所有 TP 状态 Done 且 TODO/STATUS/ACCEPTANCE 一致
- make check 与 pipeline_maturity_audit.py --strict 新鲜通过
- governance strict/health 与 git diff --check 通过
- 剩余 unknowns 不影响单机生产闭环声明，并明确外部 reviewer provenance 边界

# Task Package Acceptance
## TP-01
- 标题: 可信证据根与不可伪造回执
- 验收标准:
  - 伪 locator/hash/path/symlink/self-review 全部被拒绝
  - 合法 receipt 可被 Result validator 消费
- Verify: python3 scripts/test_trusted_evidence.py
- Gate: 所有证据 locator 位于可信根、真实存在、现场哈希匹配，独立性由 verifier registry 派生
- 输出物: trusted evidence module；verifier registry contract；攻击性负例

## TP-02
- 标题: 原子研究存储与唯一写入器
- 验收标准:
  - 唯一 ID 与幂等键稳定
  - 并发 writer 测试通过
  - 崩溃前后记录一致
- Verify: python3 scripts/test_research_store.py
- Gate: 重复/并发写不重复，失败不留下半提交，Solution View 只能由当前有效 Result 重算
- 输出物: research store module；file locking；atomic rewrite；store tests

## TP-03
- 标题: 可恢复运行状态机与统一 CLI
- 验收标准:
  - run/resume/verify/status 可重跑
  - 中断后从 checkpoint 恢复
  - 完成状态从 validator 结果派生
- Verify: python3 scripts/test_vibe_mathing_runtime.py
- Gate: 非法状态转换、预算耗尽、超时、取消和恢复漂移全部 fail-closed
- 输出物: runtime state schema；CLI；checkpoint/trace；runtime tests

## TP-04
- 标题: 确定性 SymPy 垂直闭环
- 验收标准:
  - happy path 进入解库
  - 有限证据不进入
  - invalidation 自动移出
  - 故障恢复不重复
- Verify: python3 scripts/test_vibe_mathing_pipeline.py
- Gate: 单命令完成 Problem→Attempt→artifact→Result→receipt→Solution，重复运行幂等且失效后退出解库
- 输出物: deterministic adapter；fixture；E2E tests

## TP-05
- 标题: 固定 Lean/Mathlib 形式化闭环
- 验收标准:
  - kernel receipt 绑定真实输出
  - axiom audit receipt 独立存在
  - 删除任一证据后不准入
- Verify: python3 scripts/test_lean_pipeline.py
- Gate: 真实 Lean build 通过、无 sorry/admit/unsafe、#print axioms 可审计、版本固定、statement faithfulness 独立记录
- 输出物: Lean fixture；formalization adapter；verification receipts；Lean E2E test

## TP-06
- 标题: 生产成熟度审计、CI、文档与最终审查
- 验收标准:
  - audit 输出 100/100
  - 恢复任一旧漏洞后 audit 非零
  - make check 与 governance strict/health PASS
- Verify: make check && python3 scripts/pipeline_maturity_audit.py --strict
- Gate: 所有 required commands 新鲜通过、任务状态一致、文档无漂移、攻击性负例和回滚入口齐全
- 输出物: maturity audit；CI gate；review；docs；closeout evidence

# Anti-Goals
- 不覆盖既有数学事实、0002 任务资产或用户的未提交改动
- 不得虚构证据、独立 reviewer 身份或外部签名
- 不引入分布式队列、数据库、多 Agent runtime 或任意命令执行器
- 不提交、不推送、不部署；版本控制交付需用户另行授权
