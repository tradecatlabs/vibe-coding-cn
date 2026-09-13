# Audit Case Sampling

- decision: no-case
- source: 0003 production research pipeline final review and debug evidence
- fixed_problem: 修复伪证据晋升、伪失效撤销、断链写入、WAL 恢复、任务状态漂移，以及子进程日志预算误伤 Lean 业务构建产物
- evidence: REGRESSION_EVIDENCE.json; REVIEW.md; DEBUG.md; MATURITY_AUDIT.json; scripts/test_evidence_attacks.py; scripts/test_research_store.py; scripts/test_vibe_mathing_runtime.py
- no_case_reason: 本轮根因已完整命中全局 CASE-0008：关键事实必须由 owner 派生，且 stdout/stderr 必须在宿主侧硬限额；本次回归把该要求落实为“只限制日志通道，不用继承式 RLIMIT_FSIZE 限制业务文件”。任务状态漂移由 CASE-0003 覆盖，没有形成新的根因类别，重复建 case 会制造治理噪声
