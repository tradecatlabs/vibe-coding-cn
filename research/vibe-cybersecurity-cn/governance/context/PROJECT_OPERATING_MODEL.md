---
id: GOV-PROJECT-OPERATING-MODEL
type: context
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-14
review_cycle: P90D
---

# Project Operating Model

本文件是项目级人类入口和代理入口的共享操作模型。它只记录项目当前应该如何被理解、修改、验证和交付；不替代代码、契约、ADR、任务包、README 或 AGENTS。

## 项目一句话定义

`vibe-cybersecurity-cn` 是一个在明确授权与运行时策略内，让 Agent 规划安全任务、编排成熟工具、验证候选并沉淀证据的薄型安全证据控制面。

## 业务模型

- 核心用户：需要自动化攻击面管理、漏洞验证、代码与供应链审计的安全研究者和工程团队。
- 核心对象：`CyberTask`、`ScopeGrant`、`TaskPlan`、`ToolRun`、`Observation`、`CandidateFinding`、`ValidationRun`、`Evidence`、`Finding`。
- 当前实战领域：S0，公开协议源码 + 本地/fork 只读审计；默认对象为 DeFi/Web3 开源协议仓库，
  默认动作是 clone、固定 commit、编译、Slither/Foundry 分析、本地 PoC 和 fork 只读状态分析。
- 关键流程：安全目标 -> 动作分级（只读研究默认放行；主动交互必须绑定真实授权来源，fail closed）-> 任务规划 -> 工具运行 -> 候选发现 -> 独立验证 -> 证据准入 -> 实证视图。
- 不属于本项目的范围：对无真实授权来源目标的主动交互测试（无授权）、无界自主利用、凭据攻击、持久化、数据获取，以及把扫描器告警直接包装成实证漏洞。
- 全局定位：网络安全完整景观见 `context/CYBERSECURITY_LANDSCAPE.md`；IAM、EDR、SIEM、GRC、DFIR 和恢复平台默认是集成对象，不由本项目重建。

## 技术模型

- 主要运行形态：当前为 Git 管理的研究、治理和机器候选目录；生产运行时尚未实现。
- 核心模块：授权策略、任务编排、工具适配、证据账本、验证准入；扫描能力优先复用成熟工具。
- 数据事实源：领域坐标系位于 `governance/context/CYBERSECURITY_LANDSCAPE.md`；供应链研究位于 `governance/tasks/0001-survey-cybersecurity-supply-chain/`；准入决策位于 `governance/tasks/0002-prepare-supply-chain-admission/`；未来运行数据必须以结构化契约保存。
- 外部依赖：候选开源工具、规则库、漏洞情报和评测靶场；全部需要固定版本、许可审查和隔离执行。
- 主要验证入口：候选目录校验器与治理 strict/health；生产行为验证尚未启用。

## 工具链模型

工具链边界以 `context/TOOLCHAIN_MODEL.md` 为准。这里仅记录最短摘要：

- 构建：当前无业务构建。
- 测试：`python3 governance/tasks/0001-survey-cybersecurity-supply-chain/validate_candidates.py`。
- 类型检查：当前无业务类型检查。
- 格式 / lint：治理包 strict validator。
- 发布 / 回滚：尚未定义；当前全部产物为文档与 JSON，可通过普通变更回退。

## 目录和真相源地图

| 事实类型 | 真相源 | 备注 |
|---|---|---|
| 项目操作模型 | `governance/context/PROJECT_OPERATING_MODEL.md` | 人类和代理的项目入口 |
| 授权边界 | `governance/context/AUTHORIZATION_BOUNDARIES.md` | 什么动作需要 ScopeGrant、三通道授权来源与字段契约草案 |
| 网络安全全局景观 | `governance/context/CYBERSECURITY_LANDSCAPE.md` | 资产、威胁、防御、证据和产品位置的长期坐标系 |
| 上下文路由 | `governance/context/CONTEXT-ROUTER.md` | 任务类型到最小上下文包 |
| 工程流程 | `governance/processes/DOCUMENT_DRIVEN_DEVELOPMENT.md` | 文档先行和文档回填规则 |
| 工具链边界 | `governance/context/TOOLCHAIN_MODEL.md` | 成熟工具、项目脚本和禁用做法 |
| 机器契约 | `governance/context/project_operating_model_contract.v1.yaml` | 脚本和 agent 可读取的契约 |
| 架构决策 | `governance/decisions/adr/` | 不可逆或高影响决策 |
| 任务证据 | `governance/tasks/` | 执行计划、状态、验收、closeout |
| 供应链候选 | `governance/tasks/0001-survey-cybersecurity-supply-chain/supply-chain-candidates.json` | 当前工具、资料、数据源与评测候选真相源 |
| 候选可读视图 | `governance/tasks/0001-survey-cybersecurity-supply-chain/CANDIDATE_TABLE.md` | 由校验器从 JSON 生成，不手工维护 |
| 供应链准入决策 | `governance/tasks/0002-prepare-supply-chain-admission/admission-candidates.json` | 只保存波次、状态、固定版本和门禁，不复制研究事实 |
| 准入可读视图 | `governance/tasks/0002-prepare-supply-chain-admission/ADMISSION_CANDIDATE_TABLE.md` | 联合研究目录和准入 overlay 生成 |
| 候选景观覆盖 | `governance/tasks/0003-map-global-cybersecurity-landscape/LANDSCAPE_COVERAGE.md` | 46 项研究候选到全局能力的时点映射 |
| Web3 供应链候选 | `governance/tasks/0004-web3-vertical-proof/web3-supply-chain-candidates.json` | EVM/Solidity 聚焦的候选真相源 |
| Web3 靶场证据 | `web3-lab/evidence/findings-*.json` | 本地靶场候选-验证-证据账本；`status: confirmed` 仅限本地复现 |
| Web3 工具准入 | `governance/tasks/0005-admit-web3-toolchain/web3-admission-candidates.json` | 5 项核心工具 admitted；主动交互运行权由 ScopeGrant 决定 |
| 实战就绪度 | `governance/context/COMBAT_READINESS.md` | 授权协议 fork 级审计的评分、差距清单与里程碑；P30D 复查 |
| 项目级 Skills 供应链 | `skills/SKILLS_MANIFEST.json` | 13 个 vendored skill，固定来源 commit 与许可 |

## 变更入口

非平凡工程变更开始前必须判断：

- 是否需要先更新本操作模型。
- 是否需要更新文档驱动开发流程。
- 是否需要更新工具链模型。
- 是否需要新增或更新 ADR、Gate、module context、contracts、catalog、README 或 AGENTS。

## 验证入口

```bash
python3 governance/tools/governance_context_bundle.py --project-root . --task-type docs
python3 governance/tools/validate_governance_package.py --project-root . --strict
python3 governance/tools/governance_health_report.py --project-root . --strict
```

## 最近一次 review

- 日期：2026-08-14
- 结论：产品定位已固定为安全证据控制面；Web3 工具链 5 项核心工具正式 admitted（9 门禁）；Echidna 属性基线覆盖 4 漏洞；验证控制面升级 enforce 并全绿；13 个 skills 已 vendored（0007）；实战就绪度评估 ≈47/100（0008）；授权边界收敛为合规宽松口径：公开源码审计与只读 fork 默认放行，主动交互绑定真实授权来源。
- 后续动作：围绕 S0 启动 M1 管线骨架（公开协议仓库 clone -> 固定 commit -> compile -> slither -> forge test/本地 PoC -> fork 只读分析）；链上主动交互按三通道授权来源导入 ScopeGrant，默认不进入当前执行面；评估 Solodit/DeFiHackLabs 等情报源接入；建立跨任务回归基线。
