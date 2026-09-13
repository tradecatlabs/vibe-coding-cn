# Acceptance Checklist

# Global Standards
- [x] VIBE-MATHING-SPEC v0.1 的 R1/R2/R3 全部机械执行
- [x] 所有完成状态由 owner 从输入、产物和 validator 结果重算，不接受调用者自报
- [x] 高风险失败 fail-closed 且返回非零状态，保留可操作错误和恢复入口
- [x] 性能保持 O(P+A+R+E) 线性扫描；外部进程有明确 timeout、输出上限和预算
- [x] 文档、schema、脚本、CI、ADR/Gate/module context 同步

# Task Package Checklists
## TP-01
- 标题: 可信证据根与不可伪造回执
- 验收项:
  - [x] 伪 locator/hash/path/symlink/self-review 全部被拒绝
  - [x] 合法 receipt 可被 Result validator 消费
- Verify: python3 scripts/test_trusted_evidence.py
- Gate: 所有证据 locator 位于可信根、真实存在、现场哈希匹配，独立性由 verifier registry 派生
- 输出物:
  - [x] trusted evidence module
  - [x] verifier registry contract
  - [x] 攻击性负例
- 标准清单:
  - [x] Verify: python3 scripts/test_trusted_evidence.py
  - [x] Gate: 所有证据 locator 位于可信根、真实存在、现场哈希匹配，独立性由 verifier registry 派生
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: 原子研究存储与唯一写入器
- 验收项:
  - [x] 唯一 ID 与幂等键稳定
  - [x] 并发 writer 测试通过
  - [x] 崩溃前后记录一致
- Verify: python3 scripts/test_research_store.py
- Gate: 重复/并发写不重复，失败不留下半提交，Solution View 只能由当前有效 Result 重算
- 输出物:
  - [x] research store module
  - [x] file locking
  - [x] atomic rewrite
  - [x] store tests
- 标准清单:
  - [x] Verify: python3 scripts/test_research_store.py
  - [x] Gate: 重复/并发写不重复，失败不留下半提交，Solution View 只能由当前有效 Result 重算
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: 可恢复运行状态机与统一 CLI
- 验收项:
  - [x] run/resume/verify/status 可重跑
  - [x] 中断后从 checkpoint 恢复
  - [x] 完成状态从 validator 结果派生
- Verify: python3 scripts/test_vibe_mathing_runtime.py
- Gate: 非法状态转换、预算耗尽、超时、取消和恢复漂移全部 fail-closed
- 输出物:
  - [x] runtime state schema
  - [x] CLI
  - [x] checkpoint/trace
  - [x] runtime tests
- 标准清单:
  - [x] Verify: python3 scripts/test_vibe_mathing_runtime.py
  - [x] Gate: 非法状态转换、预算耗尽、超时、取消和恢复漂移全部 fail-closed
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-04
- 标题: 确定性 SymPy 垂直闭环
- 验收项:
  - [x] happy path 进入解库
  - [x] 有限证据不进入
  - [x] invalidation 自动移出
  - [x] 故障恢复不重复
- Verify: python3 scripts/test_vibe_mathing_pipeline.py
- Gate: 单命令完成 Problem→Attempt→artifact→Result→receipt→Solution，重复运行幂等且失效后退出解库
- 输出物:
  - [x] deterministic adapter
  - [x] fixture
  - [x] E2E tests
- 标准清单:
  - [x] Verify: python3 scripts/test_vibe_mathing_pipeline.py
  - [x] Gate: 单命令完成 Problem→Attempt→artifact→Result→receipt→Solution，重复运行幂等且失效后退出解库
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-05
- 标题: 固定 Lean/Mathlib 形式化闭环
- 验收项:
  - [x] kernel receipt 绑定真实输出
  - [x] axiom audit receipt 独立存在
  - [x] 删除任一证据后不准入
- Verify: python3 scripts/test_lean_pipeline.py
- Gate: 真实 Lean build 通过、无 sorry/admit/unsafe、#print axioms 可审计、版本固定、statement faithfulness 独立记录
- 输出物:
  - [x] Lean fixture
  - [x] formalization adapter
  - [x] verification receipts
  - [x] Lean E2E test
- 标准清单:
  - [x] Verify: python3 scripts/test_lean_pipeline.py
  - [x] Gate: 真实 Lean build 通过、无 sorry/admit/unsafe、#print axioms 可审计、版本固定、statement faithfulness 独立记录
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-06
- 标题: 生产成熟度审计、CI、文档与最终审查
- 验收项:
  - [x] audit 输出 100/100
  - [x] 恢复任一旧漏洞后 audit 非零
  - [x] make check 与 governance strict/health PASS
- Verify: make check && python3 scripts/pipeline_maturity_audit.py --strict
- Gate: 所有 required commands 新鲜通过、任务状态一致、文档无漂移、攻击性负例和回滚入口齐全
- 输出物:
  - [x] maturity audit
  - [x] CI gate
  - [x] review
  - [x] docs
  - [x] closeout evidence
- 标准清单:
  - [x] Verify: make check && python3 scripts/pipeline_maturity_audit.py --strict
  - [x] Gate: 所有 required commands 新鲜通过、任务状态一致、文档无漂移、攻击性负例和回滚入口齐全
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
