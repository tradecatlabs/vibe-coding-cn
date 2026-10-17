# Verification Gate Debug Record

## Bug

- 标题：architecture 与 rollback capability 在有效项目状态上误报 BLOCK。
- 症状：`python3 scripts/verify_project.py --gate architecture` 和 `--gate rollback` 均非零退出。
- 首次发现位置 / 时间：2026-08-14，项目 Verification Policy 首次接入时。

## Environment

- 仓库 / 模块：Harness Harness，`scripts/verify_project.py`。
- 运行环境：Linux，Python 3.12，项目本地离线 gate。
- 依赖 / 版本：标准库；被编排的 manifest validator 使用锁定 `jsonschema==4.25.1`。
- 配置差异：无 CI/远端；项目初始为非 Git 目录，准备建立本地 revision 以捕获证据。

## Reproduction

1. 运行 `python3 scripts/verify_project.py --gate architecture`。
2. 运行 `python3 scripts/verify_project.py --gate rollback`。
3. 两条命令均写出 `BLOCK` artifact 并以 1 退出。

## Observations

- O1: 原始原则扫描 JSON 的 `scanned_files` 是 18 个路径的数组，`finding_count` 为 0，decision 为 PASS。
- O2: architecture gate 把 `payload["scanned_files"]` 列表直接与整数 `len(PRINCIPLE_FILES)` 比较。
- O3: manifest Schema 的 `lifecycle.rollback` 明确定义为非空字符串；有效样例也是字符串。
- O4: rollback gate 却要求该字段为包含 `trigger/action` 的对象，假设与正式契约冲突。

## Hypotheses

### H1: gate runner 与 owner 契约不一致（ROOT HYPOTHESIS）

- Supports: O1-O4 直接显示错误判断与 Schema/扫描器输出类型不一致。
- Conflicts: 暂无；底层扫描与 manifest self-test 均独立 PASS。
- Test: 只把扫描判断改为 `len(scanned_files)`，rollback 判断改为非空字符串，再原样运行回归测试。

### H2: 治理包存在真实原则 finding

- Supports: architecture gate 失败可能来自原则扫描。
- Conflicts: 独立执行扫描器返回 `finding_count=0`。
- Test: 保存并检查 scanner 原始 JSON；已被 O1 否定。

### H3: 有效 manifest 缺少可执行回滚信息

- Supports: rollback gate 报告缺 `trigger/action`。
- Conflicts: Schema、样例与领域文档当前契约都选择字符串回滚说明，且 Schema self-test PASS。
- Test: 读取 Schema 与样例类型；已被 O3/O4 否定。

## Experiments

### E1

- Hypothesis: H1
- Change: 不改实现；独立运行 scanner 并打印 `lifecycle` Schema/样例。
- Expected: scanner PASS 且 rollback 是非空字符串，证明失败来自 gate 假设而非被测对象。
- Result: scanner `finding_count=0`、18 文件；Schema `$ref` 指向 `non_empty_string`，样例为字符串。
- Verdict: confirmed
- Revert: 无状态变更。

## Root Cause

- gate runner 没有按 owner 输出契约检查数据：对 scanner 列表做了列表/整数比较，并为 rollback 自行发明了对象结构。

## Fix

- architecture gate 验证 `scanned_files` 是列表且其长度与显式 scope 一致。
- rollback gate 遵循 manifest Schema，只验证非空操作说明；不放宽 Schema、不降低风险 profile。

## Regression Evidence

- 回归证据契约：Required
- 契约文件：`REGRESSION_EVIDENCE.json`
- 测试：`python3 -m unittest discover -s tests -p test_verify_project.py`
- 结果：RED 两项失败；修复后 GREEN 通过；回放未修复脚本后 counterfactual 再次两项失败。
- 备注：counterfactual 将使用未修复脚本字节回放，不使用破坏性 Git 操作。

## Failed Nodes

- `architecture`、`rollback` verification capabilities。

## First Invalid Node

- `scripts/verify_project.py` 的 artifact 类型判断。

## Upstream Lineage

- Verification Policy -> capability registry -> generic-command adapter -> gate runner。

## Downstream Blast Radius

- high-risk Task Verification Plan 和 task closeout 会被错误 BLOCK；manifest validator 本身不受影响。

## Lowest Common Refinement Ancestor

- 项目 gate runner。

## Repair Boundary

- `scripts/verify_project.py` 两个判断与直接回归测试。

## Frozen Nodes

- manifest Schema、有效样例、风险 profile、底层治理 scanner。

## Invalidated Nodes

- architecture/rollback 旧 artifact 与引用它们的验证结果。

## Reverification Required

- architecture、rollback、标准库回归测试，以及最终全部 required capability。
