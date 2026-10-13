# Debug Record

## Bug

- 标题：原则扫描器误判 compatibility-breaking 上游事实
- 症状：`architecture` capability 把 DeepSeek 官方的 compatibility-breaking 风险声明判定为 Future-Optimal target downgrade，并返回 BLOCK。
- 首次发现位置 / 时间：2026-08-14，执行 `python3 scripts/verify_project.py --gate architecture`。

## Environment

- 仓库 / 模块：Harness Harness / `governance/tools/scan_principle_gates.py`。
- 运行环境：WSL2 Linux，Python 3.12.3。
- 依赖 / 版本：Python 标准库；当前 HEAD `dbf02772ed283aa43e82655785ae00e1ea68485e` 加工作树变更。
- 配置差异：DeepSeek Harness 接入后，revision lock 首次出现英文 `compatibility-breaking` 与中文 `破坏性兼容变更`。

## Reproduction

1. 在 `research/upstreams.lock.json` 保存 DeepSeek developer preview 的破坏性变化限制。
2. 运行 `python3 scripts/verify_project.py --gate architecture`。
3. 观察 `scan_future_optimal()` 在该行产生 `future-optimal-drift` BLOCK。

## Observations

- O1: gate finding 的 evidence 精确指向 DeepSeek limitation，而不是实现中的 shim、alias 或迁移分支。
- O2: `FUTURE_DRIFT_PATTERNS` 使用 `\bcompatibility\b` 和无上下文的 `兼容`，会命中“破坏性兼容变更”。
- O3: 新增的单元测试在未修复扫描器上以目标断言失败，failure rate 为 1.0；首次 package-import 捕获因命令错误作废并已覆盖。

## Hypotheses

### H1: （ROOT HYPOTHESIS）否定式 breaking-change 事实被过宽 drift 正则命中
- Supports: finding evidence 与正则逐字匹配；`compatibility-breaking` 语义上表示不兼容风险，不是兼容层。
- Conflicts: 尚无。
- Test: 单元测试同时输入英文 `compatibility-breaking` 与中文 `破坏性兼容变更`，预期零 finding，并用真实 `temporary compatibility shim` 保持正控命中。

### H2: revision lock 本来就应该携带完整 Future-Optimal 证据
- Supports: scanner 按单文件要求七类 marker，lock 当前没有。
- Conflicts: lock 是外部 revision 事实，不是实现方案；加入架构散文会污染机器元数据职责。
- Test: 若 drift matcher 对 breaking-change 事实返回空，缺 marker 不再影响结果；因此不应修改 lock schema 填充无关证据。

### H3: architecture capability 读取了陈旧 artifact
- Supports: gate 会写 runtime artifact。
- Conflicts: 本次命令重新执行 scanner，输出包含当前 lock 的精确行与文本。
- Test: 直接调用当前 `scan_future_optimal()` 复现同一 finding，排除 artifact stale。

## Experiments

### E1
- Hypothesis: H1
- Change: 仅新增一个正反控单元测试，production regex 未修改。
- Expected: breaking-change 事实断言失败，证明当前 matcher 有反事实敏感性。
- Result: exit 1；断言收到一个 `future-optimal-drift` BLOCK，failure rate 1.0。
- Verdict: confirmed
- Revert: 测试保留为回归资产。

### E2
- Hypothesis: H1
- Change: 英文模式排除 `compatibility-breaking`，中文模式排除 `破坏性兼容` / `兼容性破坏`。
- Expected: breaking-change 外部事实不再命中，真实 temporary compatibility shim 正控仍命中。
- Result: exit 0；目标单测通过，failure rate 0.0。
- Verdict: confirmed
- Revert: 不回退；进入 counterfactual 验证。

### E3
- Hypothesis: H1
- Change: 临时恢复两条旧正则并运行同一测试，随后立即恢复修复。
- Expected: 同一测试重新失败。
- Result: exit 1；failure rate 1.0；最终工作树已恢复修复版本。
- Verdict: confirmed
- Revert: 已恢复 E2 的 production regex，并再次运行目标测试通过。

## Root Cause

- `FUTURE_DRIFT_PATTERNS` 把表示“不保证兼容”的 breaking-change 外部事实当成“保留兼容层”信号；单文件 marker 规则随后把这一词法误报升级为 BLOCK。

## Fix

- 英文兼容模式排除 `compatibility-breaking`，中文兼容模式排除 `破坏性兼容` / `兼容性破坏`；保留 temporary compatibility shim 正控。
- 将新 source manifest 与当前任务计划纳入 architecture 显式扫描范围，并为 source registry 的存在性补透明证据，消除非目标 ownership WARN。

## Regression Evidence

- 回归证据契约：Required
- 契约文件：REGRESSION_EVIDENCE.json
- 测试：`tests/test_verify_project.py::ProjectGateRegressionTest.test_breaking_change_notice_is_not_compatibility_shim`。
- 结果：RED 100% 失败、GREEN 通过、counterfactual 100% 失败；owner validator PASS；architecture gate 复验 PASS。
- 备注：三个 run artifact 位于任务 runtime，并绑定 scanner/test 文件摘要；首次无效 package-import RED 已被有效 RED 覆盖。

## Failed Nodes

- `architecture` capability。

## First Invalid Node

- `scan_future_optimal()` 的 drift regex 分类。

## Upstream Lineage

- DeepSeek developer preview limitation -> source manifest -> revision lock -> principle scanner -> architecture gate。

## Downstream Blast Radius

- architecture BLOCK；test gate 的 gate-runner 回归也会受影响。同步、contract、rollback、security 行为不受影响。

## Lowest Common Refinement Ancestor

- `scan_future_optimal()` pattern 定义与对应单元测试。

## Repair Boundary

- `scan_future_optimal()` 的两条兼容性正则、对应回归测试和 architecture 显式扫描范围。

## Frozen Nodes

- 上游 source registry、同步状态机、lock 布局校验、Harness manifest 契约。

## Invalidated Nodes

- 旧 architecture artifact；未修复 matcher 的任何 PASS 声明。

## Reverification Required

- 单元 GREEN、counterfactual、architecture、test 及最终六个 capability 已全部重验通过。
