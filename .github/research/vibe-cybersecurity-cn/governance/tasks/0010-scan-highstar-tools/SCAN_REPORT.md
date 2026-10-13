# GitHub 高 star 渗透/安全工具扫描报告

扫描时间：2026-09-02。方式：`gh api search/repositories`（认证，按 stars 排序，每查询 top 8-12）。
结果仅作供应链候选；任何工具进入执行面前必须单独固定版本、核验许可、逐件审计。

## 查询覆盖（12 组）

| # | 查询 | 代表结果（top 3，star） |
|---|---|---|
| 1 | penetration testing | strix 60k / reverse-skill 33.8k / awesome-pentest 27k |
| 2 | offensive security | hexstrike-ai 11.5k / nishang 10k / my-arsenal-of-aws-security-tools 9.5k |
| 3 | red team | promptfoo 24.7k / atomic-red-team 12.5k / Red-Teaming-Toolkit 10.7k |
| 4 | hacking ethical | h4cker 29k / hacker-roadmap 15.6k / Ethical-Hacking-Resources 6.1k |
| 5 | vulnerability scanner | nuclei 31k / SkillSpector 15.6k / fscan 14.5k |
| 6 | 渗透测试（UTF-8） | Penetration_Testing_POC 7.5k / Pentest_Note 4.1k / AppInfoScanner 3.6k |
| 7 | web security scanner | dirsearch 14.7k / WhatWeb 6.8k / WebHackersWeapons 5k |
| 8 | cybersecurity | sherlock 90.8k / strix 60k / ImHex 54.6k |
| 9 | exploit framework | pwntools 13.7k / routersploit 13.2k / PowerSploit 13.1k |
| 10 | AI security agent | Anthropic-Cybersecurity-Skills 32k / SkillSpector 15.6k / hexstrike-ai 11.5k |
| 11 | SAST security | terrascan 5.2k / bearer 2.7k / nodejsscan 2.6k |
| 12 | （补充）cybersecurity 全类 | x64dbg 49.4k / shannon 47.5k / maigret 37.2k |

## 新增 14 条候选（disposition: reference）

| id | 仓库 | star | 许可 | 与本项目关系 |
|---|---|---|---|---|
| shannon | KeygraphHQ/shannon | 47.5k | AGPL-3.0 | AI Web 渗透 Agent 行为研究 |
| anthropic-cyber-skills | mukul975/Anthropic-Cybersecurity-Skills | 32k | Apache-2.0 | skills 供应链交叉对照 |
| nvidia-skillspector | NVIDIA/SkillSpector | 15.6k | Apache-2.0 | 护住 vendored skills 更新面 |
| hexstrike-ai | 0x4m4/hexstrike-ai | 11.5k | MIT | MCP 渗透代理工具面设计 |
| fscan | shadow1ng/fscan | 14.5k | MIT | 内网扫描（S2 候选） |
| sn1per | 1N3/Sn1per | 11.2k | 未断言 | 攻击面管理全流程样例 |
| nishang | samratashok/nishang | 10k | 未断言 | PowerShell 后渗透模式参考 |
| tsunami | google/tsunami-security-scanner | 8.6k | Apache-2.0 | 企业扫描器架构参考 |
| garak | NVIDIA/garak | 9.1k | Apache-2.0 | Agent 模型层安全基线 |
| atomic-red-team | redcanaryco/atomic-red-team | 12.5k | MIT | ATT&CK 行为库 |
| spiderfoot | smicallef/spiderfoot | 21.6k | MIT | OSINT 编排主干候选 |
| reconftw | six2dez/reconftw | 8k | MIT | 侦察流水线范式 |
| pwntools | Gallopsled/pwntools | 13.7k | 需复核 | PoC 开发基础设施 |
| dirsearch | maurosoria/dirsearch | 14.7k | 未断言 | Web 路径扫描 |

## 已存在候选（本轮扫描命中但无需新增）

nuclei、grype、osv-scanner、trivy、gitleaks、httpx、subfinder、nmap、katana、
pentagi、strix（60k，0001 已收录）——说明 0001 候选表对主流覆盖良好。

## 风险标注

- `reverse-skill`（33.8k star）名称可疑，疑似刷星/投毒类，未纳入；如需引用须先鉴定。
- `L1B3RT4S`（21.3k star）为 jailbreak prompt 集合，未纳入。
- 中文搜索命中政治敏感仓库，不纳入；仅记录数据。
- 所有 AI 渗透 Agent（shannon/hexstrike/pentagi 等）属于主动交互面，纳入仅作研究，
  进入执行面必须绑定 ScopeGrant 三通道授权。
