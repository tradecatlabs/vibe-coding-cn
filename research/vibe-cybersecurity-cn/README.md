# vibe-cybersecurity-cn

面向明确授权场景的 Agent 网络安全自动化研究与工程项目。

项目目标是把安全任务编译为受策略约束的执行计划，复用成熟开源工具产生观察与候选，
再通过独立验证和可追溯证据派生可信安全结论。

当前阶段：全局景观、供应链调研完成；Web3/EVM 本地靶场纵向闭环已跑通
（候选生成 -> 独立复现 -> 证据归档），5 项核心工具正式准入（9 门禁），
验证控制面已升级为强制门禁（git 输入摘要绑定）。公开协议源码审计与只读 fork
默认放行；对链上或网络资产的主动交互必须绑定真实授权来源（自有资产、
赏金规则或书面授权）。

当前实战领域固定为 **S0：公开协议源码 + 本地/fork 只读审计**。默认工作面是
DeFi/Web3 开源协议仓库：clone、固定 commit、编译、Slither/Foundry 分析、
本地 PoC 与 fork 只读状态分析；不发真实交易，不主动扫描线上目标。

## 当前核心链路

```text
CyberTask
  -> ScopeGrant
  -> TaskPlan
  -> ToolRun
  -> Observation
  -> CandidateFinding
  -> ValidationRun
  -> Evidence
  -> ConfirmedFinding view
```

## 研究入口

- [项目操作模型](governance/context/PROJECT_OPERATING_MODEL.md)
- [授权边界（什么动作需要授权）](governance/context/AUTHORIZATION_BOUNDARIES.md)
- [网络安全全局景观](governance/context/CYBERSECURITY_LANDSCAPE.md)
- [安全证据控制面决策](governance/decisions/adr/ADR-0001-security-evidence-control-plane.md)
- [开源供应链候选表](governance/tasks/0001-survey-cybersecurity-supply-chain/CANDIDATE_TABLE.md)
- [首轮综合分析](governance/tasks/0001-survey-cybersecurity-supply-chain/SYNTHESIS.md)
- [来源账本](governance/tasks/0001-survey-cybersecurity-supply-chain/SOURCE_LEDGER.md)
- [供应链准入候选表](governance/tasks/0002-prepare-supply-chain-admission/ADMISSION_CANDIDATE_TABLE.md)
- [供应链准入政策](governance/tasks/0002-prepare-supply-chain-admission/ADMISSION_POLICY.md)
- [现有候选覆盖与空白](governance/tasks/0003-map-global-cybersecurity-landscape/LANDSCAPE_COVERAGE.md)
- [Web3/EVM 供应链候选表](governance/tasks/0004-web3-vertical-proof/WEB3_CANDIDATE_TABLE.md)
- [Web3 本地靶场与证据闭环](web3-lab/README.md)
- [Web3 靶场证据账本](web3-lab/evidence/findings-2026-08-14.json)
- [Web3 工具链准入表](governance/tasks/0005-admit-web3-toolchain/ADMISSION_TABLE.md)
- [项目级 Skills 供应链清单](skills/SKILLS_MANIFEST.json)
- [供应链审计：Hacking-Tools 清单 + Blackstorm 研究资料](governance/tasks/0009-supply-chain-yogsec-blackstorm/AUDIT_REPORT.md)
- [实战就绪度评估（差距与里程碑）](governance/context/COMBAT_READINESS.md)

## 安全边界

- S0 是当前默认执行范围：公开源码、本地环境、只读 fork；不需要注册、不需要额外授权。
- 公开协议源码、仓库与链上公开数据即研究输入；fork 主网区块只读分析默认允许。
- 发交易、状态修改、利用验证与主动扫描等主动交互必须绑定真实授权来源，fail closed；
  目标可达或"有响应"不构成授权。
- 授权来源三通道：自有资产声明、赏金项目规则、书面授权。
- 授权、范围、速率、动作等级和停止条件由运行时策略执行，不能依赖模型自律。
- 工具输出默认只是候选证据；未经独立验证不得晋升为实证漏洞。
