# Execution Checklist
[x] TP-01 | P0 | 可信证据根与不可伪造回执 | Verify: python3 scripts/test_trusted_evidence.py | Gate: 所有证据 locator 位于可信根、真实存在、现场哈希匹配，独立性由 verifier registry 派生 | Parallelizable: No
[x] TP-02 | P0 | 原子研究存储与唯一写入器 | Verify: python3 scripts/test_research_store.py | Gate: 重复/并发写不重复，失败不留下半提交，Solution View 只能由当前有效 Result 重算 | Parallelizable: No
[x] TP-03 | P0 | 可恢复运行状态机与统一 CLI | Verify: python3 scripts/test_vibe_mathing_runtime.py | Gate: 非法状态转换、预算耗尽、超时、取消和恢复漂移全部 fail-closed | Parallelizable: No
[x] TP-04 | P0 | 确定性 SymPy 垂直闭环 | Verify: python3 scripts/test_vibe_mathing_pipeline.py | Gate: 单命令完成 Problem→Attempt→artifact→Result→receipt→Solution，重复运行幂等且失效后退出解库 | Parallelizable: No
[x] TP-05 | P0 | 固定 Lean/Mathlib 形式化闭环 | Verify: python3 scripts/test_lean_pipeline.py | Gate: 真实 Lean build 通过、无 sorry/admit/unsafe、#print axioms 可审计、版本固定、statement faithfulness 独立记录 | Parallelizable: No
[x] TP-06 | P0 | 生产成熟度审计、CI、文档与最终审查 | Verify: make check && python3 scripts/pipeline_maturity_audit.py --strict | Gate: 所有 required commands 新鲜通过、任务状态一致、文档无漂移、攻击性负例和回滚入口齐全 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
