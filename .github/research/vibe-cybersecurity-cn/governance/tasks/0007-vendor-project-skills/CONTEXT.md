# Repo Evidence

- 0006 审计通过 14 仓库；Web3 方向优先项为 web3-bug-bounty-hunting-ai-skills
  与 Anthropic-Cybersecurity-Skills（Foundry/合约审计 skill）。
- 沙盒保留完整克隆；本任务从沙盒复制选定 skill，固定 commit：
  web3 41238d8、Anthropic 4c0b700。

# Constraints Matrix

| 约束 | 强制决策 |
|---|---|
| 不装全局 | skills 只放项目内，manifest 声明 scope |
| 来源固定 | manifest 记录 commit，升级须重审计 |
| 内容不可信 | 使用规则要求授权求交 |
| 许可合规 | MIT/Apache-2.0 记录在 manifest |

# Change Boundary

新增 `skills/` 目录与 0007 任务包；更新 AGENTS/README；不触碰全局 skills。

# Risk Matrix

| 风险 | 影响 | 控制 |
|---|---|---|
| 内容过时 | skill 失效 | 固定 commit + 升级流程 |
| 误用攻击内容 | 越权动作 | 使用规则 + 授权求交 |
| manifest 漂移 | 来源不可溯 | 校验器核对 commit |

# Assumptions and Falsification

- 假设：13 个 skill 覆盖当前 Web3 审计主流程；推翻条件：真实任务暴露缺口则扩展。
- 假设：项目级存放满足"不要全局"；推翻条件：用户改需求则调整。

# Critical Ambiguities

- 无重大歧义；纳入范围以 Web3 审计方向为准。

# Debug Evidence Contract

- 调试模式: `Optional`
- 本任务不是缺陷修复任务。

# Task Package Context Map

- TP-01：0006 审计报告
- TP-02：`skills/`、`SKILLS_MANIFEST.json`
- TP-03：`AGENTS.md`、`README.md`
- TP-04：`STATUS.md`
