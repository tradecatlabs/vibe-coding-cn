# Debug Record

## Bug

- 标题：浅克隆上游强制更新后同步失败
- 症状：Codex 官方分支前进后，`fetch --depth 1` 显示 forced update，随后 `merge --ff-only FETCH_HEAD` 报 `refusing to merge unrelated histories`。
- 首次发现位置 / 时间：2026-08-14，首次重跑 `bash scripts/sync_upstreams.sh`。

## Environment

- 仓库 / 模块：Harness Harness / `scripts/sync_upstreams.sh`
- 运行环境：Linux、bash、git；`research/upstreams/codex` 为 depth=1 浅克隆。
- 依赖 / 版本：系统 Git；官方 origin `https://github.com/openai/codex.git`。
- 配置差异：OpenCode 与 Claude Code 当次未前进；只有 Codex 在两次同步间更新了 `main`。

## Reproduction

1. 在 Codex `main` 的 depth=1 checkout 停留于 `781445f7c6928eda08fe8dc160a6003d2f3a184b`。
2. 官方 `main` 更新到 `990218bbbd5cb4bb5aafd646c56461dfb2f95d17`。
3. 执行 `bash scripts/sync_upstreams.sh`；fetch 成功，merge 以“不相关历史”失败。

## Observations

- O1: checkout 工作树为空，排除未提交文件阻塞；本地分支显示 `ahead 1, behind 1`。
- O2: 两个 tip 都被 Git 标为 `grafted`，`merge-base HEAD origin/main` 无输出，`rev-list --left-right --count` 为 `1 1`。
- O3: fetch 明确把远端引用从 `781445f` 更新到 `990218b`；失败发生在浅历史不足后的 ancestry 判定，不是 clone、网络或 origin 校验阶段。

## Hypotheses

### H1: depth=1 fetch 截断了可证明的 fast-forward 祖先链（ROOT HYPOTHESIS）
- Supports: 两个相邻观测 tip 都显示 `grafted`，且工作树干净、origin 正确。
- Conflicts: fetch 输出把引用变化显示为 forced update，也可能是真实历史改写。
- Test: 只对 Codex checkout 执行一次 `git fetch --deepen=1 origin main`，再检查旧 HEAD 是否成为 `origin/main` 的祖先。

### H2: 官方 Codex `main` 发生真实非 fast-forward 改写
- Supports: fetch 输出包含 `forced update`，浅仓库当前无法建立 merge base。
- Conflicts: 新旧 commit 时间和编号连续，符合普通前进也会被 depth=1 误判的特征。
- Test: deepen 后仍无 merge base，或旧 HEAD 明确不是新 tip 祖先，则支持该假设。

### H3: 本地 checkout 含用户 commit 或工作树修改
- Supports: `ahead 1, behind 1` 表面上可能表示本地分叉。
- Conflicts: `status --porcelain` 为空，本地 HEAD 正是上一版 lock 记录的官方 revision。
- Test: 比较本地 HEAD 与旧 lock，并检查工作树；任一不符才支持该假设。

## Experiments

### E1
- Hypothesis: H1
- Change: 仅深化 Codex 浅历史一层，不改脚本和工作树。
- Expected: 若是浅边界误判，`merge-base --is-ancestor HEAD origin/main` 将返回 0；若是真实改写则仍失败。
- Result: `git fetch --deepen=1 origin main` 后，`merge-base --is-ancestor HEAD origin/main` 返回 0，merge base 为旧 HEAD `781445f`。
- Verdict: confirmed
- Revert: 无需回滚工作树；深化的 Git 历史只增加研究缓存对象。

## Root Cause

- depth=1 checkout 每次再执行 `fetch --depth 1` 时只保留新旧 tip 的浅边界，Git 无法看到二者之间的父边，因而把普通前进显示成 forced update，并拒绝 `ff-only` merge。

## Fix

- 在 origin、分支和干净工作树检查后，先按 depth fetch；若无法证明 `HEAD` 是 `FETCH_HEAD` 的祖先，则按 32、64、128…有界深化历史，证明成功后才 `merge --ff-only`。
- 达到 `UPSTREAM_MAX_DEEPEN`、仓库已非 shallow 仍无祖先关系或工作树有改动时保持 fail closed；不使用 reset、强制 checkout 或覆盖。
- 新增纯本地 Git 回归测试，同时覆盖普通前进、脏工作树拒绝和真实远端历史改写拒绝。

## Regression Evidence

- 回归证据契约：Required
- 契约文件：REGRESSION_EVIDENCE.json
- 测试：`bash tests/test_sync_upstreams.sh`
- 结果：RED 失败、GREEN 通过、移除修复后的 counterfactual 再次失败；owner validator PASS。
- 备注：测试只使用 `mktemp` 下的本地 bare repository，不访问网络，不改变真实上游 checkout。

## Failed Nodes

-

## First Invalid Node

-

## Upstream Lineage

-

## Downstream Blast Radius

-

## Lowest Common Refinement Ancestor

-

## Repair Boundary

-

## Frozen Nodes

-

## Invalidated Nodes

-

## Reverification Required

-
