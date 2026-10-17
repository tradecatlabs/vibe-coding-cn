---
id: GOV-PROJECT-TOPOLOGY
type: index
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-14
review_cycle: P90D
---

# Project Topology

## 项目结构

| 路径 | 职责 | 禁止事项 | 主要验证 |
|---|---|---|---|
| `governance/` | 项目工程治理包、上下文路由、标准、门禁和证据记录 | 不覆盖项目原有 README、AGENTS、CI 或模块文档 | `validate_governance_package.py --strict` |
| `governance/tasks/` | 任务树、任务包和执行状态 | 不把任务临时状态直接当成长期标准 | `validate_tasks_tree.py` |
| `governance/tasks/0001-survey-cybersecurity-supply-chain/` | 开源供应链候选、来源账本、综合分析和机器校验 | 不把候选表当成安装清单或生产批准 | `validate_candidates.py` |
| `governance/tasks/0002-prepare-supply-chain-admission/` | 把研究 MVP 编译为供应链准入队列、门禁和实施波次 | 不把准入候选当成已纳入或已启用 | `validate_admission_candidates.py` |
| `governance/tasks/0003-map-global-cybersecurity-landscape/` | 保存全局景观来源、候选覆盖映射、审查和 closeout 证据 | 不复制工具真相源，不把覆盖当成能力 | task docs closeout + governance strict |
| `governance/tasks/0004-web3-vertical-proof/` | Web3/EVM 聚焦供应链候选与本地靶场闭环任务包 | 不把靶场结论当生产审计结论 | `validate_web3_candidates.py` + task docs closeout |
| `governance/tasks/0005-admit-web3-toolchain/` | Web3 工具链 9 门禁准入与验证控制面升级任务包 | 不把 admitted 当运行授权 | `validate_web3_admission.py` + closeout 验证门禁 |
| `governance/tasks/0006-audit-security-skills-sandbox/` | 安全 skills 供应链审计沙盒任务包 | 不把未审计内容装进 Codex skills | `audit_skills.py` + task docs closeout |
| `governance/tasks/0007-vendor-project-skills/` | 项目级 skills vendored 落地任务包 | 不装全局、不运行仓库脚本 | `SKILLS_MANIFEST.json` + task docs closeout |
| `governance/context/COMBAT_READINESS.md` | 实战（授权协议 fork 级审计）就绪度真相源 | 不把评分当能力承诺 | governance strict + P30D 复查 |
| `governance/context/AUTHORIZATION_BOUNDARIES.md` | 授权边界真相源：动作分级、三通道授权来源与 ScopeGrant 草案 | 不把可达性当主动交互授权 | governance strict + P30D 复查 |
| `web3-lab/` | 本地 EVM 已知漏洞靶场与候选-验证-证据闭环（教学 ground truth） | 禁止用于真实协议；工具输出不直接当实证 | `validate_lab_evidence.py` + `forge test` |

## 依赖方向

治理包只提供项目记忆和执行护栏；`CYBERSECURITY_LANDSCAPE.md` 定义领域坐标；任务容器记录研究过程；长期有效经验再晋升到 context、standards、processes、architecture-gates 或 evidence。未来运行时只能依赖授权策略和结构化工具适配，不能反向让扫描器或 Agent 框架拥有项目事实与准入规则。
