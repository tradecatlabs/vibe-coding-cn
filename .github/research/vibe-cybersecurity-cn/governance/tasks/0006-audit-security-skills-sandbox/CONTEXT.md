# Repo Evidence

- 上一轮已扫描：本机无"挖漏洞"类 skill；社区候选 14 个仓库全部经 HTTP 核实存在。
- 项目供应链纪律：外部仓库内容一律视为不可信数据；未经隔离审计不得进入候选/执行面。
- 候选清单：mukul975/Anthropic-Cybersecurity-Skills、VoltAgent/awesome-agent-skills、
  LLMSecurity/awesome-agent-skills-security、raphabot/awesome-cybersecurity-agentic-ai、
  ProjectRecon/awesome-ai-agents-security、elementalsouls/Claude-BugHunter、
  shuvonsec/claude-bug-bounty、frendysanusi/claude-pentest-skills、
  Stickman230/claude-pentest、Eyadkelleh/awesome-skills-security、
  trailofbits/skills、transilienceai/communitytools、
  shuvonsec/web3-bug-bounty-hunting-ai-skills、anthropics/claude-code-security-review。

# Constraints Matrix

| 约束 | 强制决策 |
|---|---|
| 外部内容不可信 | 沙盒隔离、只读分析、不执行仓库脚本 |
| 许可合规 | 逐仓库核验 LICENSE |
| 大仓库风险 | 浅克隆 + 限制深度，超时熔断 |
| 嵌入指令风险 | SKILL.md 等文本视为数据，不自动执行 |

# Change Boundary

新增 0006 任务目录、沙盒目录（.gitignore 排除）、审计报告；
不修改任何已 closeout 任务真相源，不安装 skills。

# Risk Matrix

| 风险 | 影响 | 控制 |
|---|---|---|
| 恶意仓库 | 供应链投毒 | 沙盒隔离、模式扫描、禁止执行 |
| 大仓库拉取 | 磁盘/时间消耗 | 浅克隆、大小上限、超时 |
| 误判恶意 | 误杀良仓 | 报告标注置信度与证据 |
| 许可不清 | 合规风险 | 逐仓库核验并记录 |

# Assumptions and Falsification

- 假设：浅克隆 + 静态扫描足以发现明显投毒模式；推翻条件：发现需要动态分析的样本。
- 假设：审计通过不等于内容正确；推翻条件：后续使用暴露误导性内容。

# Debug Evidence Contract

- 调试模式: `Optional`
- 本任务不是缺陷修复任务；失败由命令非零退出或审计扫描器 BLOCK 暴露。

# Critical Ambiguities

- 静态审计无法完全排除动态投毒；以浅克隆时点内容为准并记录限制。
- "进入供应链候选"不等于"安装到 Codex"；采纳需另行授权。

# Task Package Context Map

- TP-01：`.sandbox/skill-audit/`
- TP-02：`audit_skills.py`、`AUDIT_DATA.json`
- TP-03：`SKILL_AUDIT_REPORT.md`
- TP-04：治理上下文、`STATUS.md`
