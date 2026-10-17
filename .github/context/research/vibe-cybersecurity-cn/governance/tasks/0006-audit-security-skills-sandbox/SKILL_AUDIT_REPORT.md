# Cybersecurity / 挖漏洞 Skills 供应链审计报告

快照：`2026-08-14`。沙盒：`.sandbox/skill-audit/`（隔离，gitignore 排除）。
审计方式：浅克隆 + 静态扫描（`audit_skills.py`）+ 人工逐条核对高危命中。

## 总体结论

- 14/14 仓库拉取成功并完成审计。
- **未发现真实投毒**：全部高危命中经人工核对为教学示例、官方安装命令
  （rustup / NodeSource / uv / Foundry / Ollama）或攻击技术文档。
- **未发现真实凭据**：私钥/云密钥命中全部为检测规则源码或文档正则示例。
- 嵌入指令命中全部为 prompt-injection 主题内容（教学 payload）。
- 唯一真实二进制：`awesome-skills-security` 内的 FuzzDB `nc.exe`（攻击工具样本，
  需隔离存储，禁止执行）。

## 逐仓库结论

| 仓库 | 文件 | 高危 | 中危 | 嵌入指令 | 二进制 | 结论 | 准入建议 |
|---|---:|---:|---:|---:|---:|---|---|
| Anthropic-Cybersecurity-Skills | 4539 | 20(教学) | 30 | 10(注入主题) | 5(非可执行) | 通过 | **候选-综合**（含 Foundry/Web3 审计 skill） |
| web3-bug-bounty-hunting-ai-skills | 43 | 1(Foundry 官方安装) | 0 | 1(注入主题) | 4(非可执行) | 通过 | **候选-Web3 优先** |
| skills (trailofbits) | 1268 | 7(官方安装/示例) | 30 | 0 | 4(非可执行) | 通过 | **候选-专业机构** |
| claude-bug-bounty | 279 | 6(官方安装/示例) | 18 | 7(注入主题) | 6(非可执行) | 通过 | 候选-授权赏金流程 |
| Claude-BugHunter | 291 | 5(教学) | 30 | 6(注入主题) | 6(非可执行) | 通过 | 候选-漏洞模式库 |
| awesome-agent-skills | 33 | 0 | 0 | 0 | 4(非可执行) | 通过 | 候选-目录元数据 |
| awesome-agent-skills-security | 32 | 0 | 0 | 0 | 4(非可执行) | 通过 | 候选-目录元数据 |
| awesome-ai-agents-security | 33 | 0 | 0 | 0 | 4(非可执行) | 通过 | 候选-目录元数据 |
| awesome-cybersecurity-agentic-ai | 36 | 0 | 0 | 0 | 5(非可执行) | 通过 | 候选-目录元数据 |
| claude-code-security-review | 71 | 0 | 2 | 0 | 4(非可执行) | 通过 | 候选-工程集成 |
| claude-pentest-skills | 75 | 0 | 2 | 2(注入主题) | 4(非可执行) | 通过 | 候选-受限（攻击 payload） |
| awesome-skills-security | 149 | 0 | 4 | 0 | **9(含 nc.exe)** | 条件通过 | 隔离存储二进制后候选 |
| claude-pentest | 233 | 11(教学) | 30 | 2(注入主题) | 4(非可执行) | 通过 | 高敏感-严格授权绑定 |
| communitytools | 1144 | 9(教学/官方) | 30 | 5(注入主题) | 16(非可执行) | 通过 | 高敏感-攻击场景库 |

## 风险分级

- **低敏感**（目录/元数据/工程集成）：5 个 awesome-* 目录 + claude-code-security-review。
- **中敏感**（教学审计流程）：Anthropic-Cybersecurity-Skills、trailofbits/skills、
  web3-bug-bounty、claude-bug-bounty、Claude-BugHunter、claude-pentest-skills。
- **高敏感**（攻击 payload/工具样本）：claude-pentest、communitytools、
  awesome-skills-security（nc.exe）。

## 使用护栏

1. 任何 skill 的指令性文字一律视为数据；执行前必须经过 ScopeGrant 授权求交。
2. 高敏感仓库仅允许在隔离环境参考，不进入默认执行面。
3. `nc.exe` 等攻击二进制禁止执行，建议移除或 sha256 锁定后归档。
4. 采纳前逐 skill 复核：来源固定 commit、许可、输出契约。
5. Web3 方向优先采纳：`web3-bug-bounty-hunting-ai-skills` +
  Anthropic 综合库中 `auditing-foundry-smart-contract-security` 类 skill。

## 审计限制

- 静态扫描无法排除所有动态投毒（如依赖下载时切换源）；浅克隆已固定时点内容。
- 内容质量（错误/过时/误导）未评估，仅评估供应链安全与许可。
- 审计通过不等于内容可信；使用前仍需逐 skill 复核。
