---
id: LESSON-0002
type: record
status: current
owner: engineering
created: 2026-08-14
last_reviewed: 2026-08-14
source: governance/tasks/0002-sync-official-harness-sources/DEBUG.md
related_gates: []
---

# LESSON-0002 上游源码研究必须绑定官方 revision 与可见性证据

## 背景

用户明确要求从 GitHub 获取 OpenCode、Codex 与 Claude Code。实际核验发现前两者公开核心源码，
Claude Code 官方仓库当前只公开插件、hooks、示例和分发资料；同时浅克隆会让普通分支前进
暂时表现为 forced update。

## 决策或结论

- 源码研究必须固定官方 origin、登记分支与 commit，不能用本机安装状态、fork 或项目名称代替来源事实。
- 许可证、核心路径与负面可见性结论都必须绑定当前 revision；上游变化后旧结论自动失效。
- 浅克隆无法证明 ancestry 时只能有界深化后再 fast-forward；不得用 reset 或删除重克隆掩盖状态。

## 证据

- `research/upstreams.lock.json`
- `research/UPSTREAMS.md`
- `governance/tasks/0002-sync-official-harness-sources/DEBUG.md`
- `tests/test_sync_upstreams.sh`

## 影响范围

适用于外部仓库、SDK、模型工具链或参考实现的源码研究、对比、审计和供应链输入固定。

## 后续动作

- [x] 用同步脚本、revision lock、源码可见性 assessment commit 和本地 Git 回归机械化该规则。

## 失效条件

当上游提供签名、SBOM、机器可读许可证和官方源码可见性 manifest，并能由成熟工具完整验证时，
可替换当前部分人工登记；官方来源与 revision 绑定原则仍然有效。
