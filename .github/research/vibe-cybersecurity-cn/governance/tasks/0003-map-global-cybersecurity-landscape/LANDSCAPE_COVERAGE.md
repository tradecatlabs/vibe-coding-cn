# 现有候选在全局景观中的覆盖

本表把任务 0001 的 46 项研究候选放回能力景观。计数来自既有机器目录，`8 + 4 + 7 + 7 + 6 + 3 + 6 + 5 = 46`。
这里表示“研究候选覆盖”，不表示安装、准入、启用或生产能力。

| 0001 类别 | 数量 | 候选 | 景观位置 | 结论 |
|---|---:|---|---|---|
| asset-discovery | 8 | Amass、Subfinder、httpx、Naabu、Nmap、Katana、ZMap、masscan | Identify / ASM / 网络与应用暴露 | 覆盖广；高速主动发现继续 hold |
| dynamic-validation | 4 | Nuclei、Nuclei Templates、OWASP ZAP、OpenVAS Scanner | Identify + 验证 / VM / DAST | 是候选生成与异构验证核心，不拥有实证结论 |
| code-cloud-analysis | 7 | Semgrep、Joern、Trivy、Checkov、Gitleaks、Prowler、OSV-Scanner | AppSec / Cloud / Secrets / SCA | 代码与云配置覆盖较好，运行时云检测仍缺 |
| software-supply-chain | 7 | Syft、Grype、Dependency-Track、GUAC、Cosign、in-toto、Scorecard | SBOM / SCA / provenance / 持续运营 | 透明度和完整性覆盖好，不证明可利用性 |
| intelligence-standards | 6 | CISA KEV、EPSS、NVD、OSV.dev、ATT&CK STIX、CycloneDX | 漏洞优先级、行为和互操作 | 是 enrichment，不是本地资产事实 |
| orchestration-operations | 3 | secureCodeBox、DefectDojo、Greenbone CE | 编排、漏洞运营、网络 VM | 候选下游和扩展层，不进入首个切片核心 |
| benchmarks-labs | 6 | Juice Shop、WebGoat、PortSwigger Academy、AutoPenBench、CyberSecEval、SecRL | ground truth / 教学 / Agent eval | 用于校准，不能外推真实生产覆盖率 |
| agent-harness | 5 | CAI、PentAGI、Strix、PentestGPT、Nettacker | Agent 编排参考 | 吸收机制，不整体复制；高风险能力不得默认启用 |

## 覆盖热区

- 强：外部资产发现、Web 动态候选、代码/SCA/SBOM、漏洞 enrichment、制品完整性和实验基线。
- 中：云配置、漏洞运营、异构验证和任务编排；尚未形成真实运行证据。
- 弱或空白：身份、终端、网络遥测、数据安全、事件响应/取证、恢复、邮件/人员、OT/IoT、移动端和 AI/Agent 专项控制。

## 空白处理原则

| 空白 | 默认动作 | 触发扩展条件 |
|---|---|---|
| IAM/PAM/ITDR | 对接，不自研 | 出现身份资产和授权验证场景 |
| EDR/XDR/NDR/SIEM | 消费/导出遥测，不自研传感器 | 需要运行时攻击验证或事件关联 |
| DSPM/DLP | 只接数据分类和风险上下文 | 出现明确数据资产消费者 |
| DFIR/SOAR | 导出 case/evidence | 实证 finding 进入响应流程 |
| Backup/Recovery | 记录验证结果，不实现备份系统 | 需要 Recover 控制验证 |
| OT/ICS/IoT | 默认不主动扫描 | 有专属 ScopeGrant、安全联锁和被动采集方案 |
| AI/Agent Security | 先做本项目工具调用和 prompt injection 负例 | Agent runtime 进入实现阶段 |

## 当前最短路径

不要为了填满景观而继续加工具。当前最有价值的下一切片仍是：

```text
本地 Juice Shop
  -> 固定 ScopeGrant
  -> 固定 Nuclei engine/template 产生 CandidateFinding
  -> 独立安全 HTTP predicate 验证
  -> 版本和摘要绑定 Evidence
  -> 派生 ConfirmedFinding
```

它能够验证产品边界；增加一个新的 SIEM、EDR 或 AI Agent 候选不能。

