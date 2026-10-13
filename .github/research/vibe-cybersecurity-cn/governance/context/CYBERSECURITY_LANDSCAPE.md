---
id: GOV-CYBERSECURITY-LANDSCAPE
type: context
status: current
owner: security-architecture
created: 2026-08-14
last_reviewed: 2026-08-14
review_cycle: P90D
---

# 网络安全全局景观

本文是项目的长期坐标系，不是产品采购清单，也不是扫描授权。框架与标准截面为
`2026-08-14`；动态版本以官方来源为准。

## 一句话看懂

网络安全不是“找漏洞”，而是持续回答五个问题：

1. 什么业务不能出事；
2. 哪些人、数据、系统和供应链支撑它；
3. 对手或错误如何破坏它；
4. 哪些控制能够预防、发现、响应和恢复；
5. 什么证据足以证明风险真实存在、控制真实有效。

```text
业务使命 / 风险偏好 / 法律与行业约束
                  │
                  ▼
       资产面 × 攻击行为 × 暴露条件
                  │
      ┌────────── Govern ──────────┐
      │ Identify Protect Detect    │
      │ Respond  Recover           │
      └────────────┬───────────────┘
                   ▼
 Observation -> Candidate -> Validation -> Evidence -> Finding
                  │                                      │
                  └──── Remediation <- Verification <────┘
                               ↺ 持续改进
```

NIST CSF 2.0 的六个 Function 是并行且持续的风险结果，不是一次性流水线；MITRE ATT&CK 是
对手行为语言。二者互补，不能互相替代。

## 一、资产面：到底在保护什么

| 资产域 | 典型对象 | 主要风险 | 成熟能力类别 |
|---|---|---|---|
| 业务与治理 | 核心流程、资金、声誉、法规承诺 | 风险无人负责、控制与业务脱节 | GRC、风险量化、合规、第三方风险 |
| 身份 | 员工、客户、服务账号、密钥、会话 | 账号接管、越权、权限蔓延 | IAM、MFA、PAM、IGA、ITDR、Secrets |
| 终端与工作负载 | PC、服务器、VM、容器、函数 | 恶意执行、持久化、提权 | EPP、EDR/XDR、CWPP、补丁与加固 |
| 网络与边缘 | DNS、域名、IP、端口、网关、邮件 | 暴露、横向移动、C2、流量滥用 | ASM、Firewall、WAF、NDR、IDS/IPS、SASE |
| 应用与 API | Web、移动端、API、微服务、业务流 | 访问控制、注入、业务逻辑滥用 | SAST、DAST、IAST、API Security、RASP |
| 云与 SaaS | 账号、租户、IAM、存储、Kubernetes | 错配、过权、跨租户和供应商依赖 | CSPM、CNAPP、CIEM、KSPM、SSPM |
| 代码与软件供应链 | 源码、依赖、构建器、制品、部署流水线 | 恶意依赖、构建篡改、来源不明 | SCA、SBOM、签名、provenance、policy-as-code |
| 数据与密码资产 | 数据库、对象存储、备份、证书、密钥 | 泄露、篡改、不可用、密码失效 | DSPM、DLP、KMS/HSM、加密、备份恢复 |
| 第三方与外包 | SaaS、MSP、开源维护者、合作伙伴 | 信任传导、集中故障、不可见变更 | TPRM、合同控制、持续监测、供应链证明 |
| OT / ICS / IoT | PLC、SCADA、楼宇、医疗与边缘设备 | 安全事故、停产、物理影响 | OT 资产发现、分区、被动监测、安全联锁 |
| AI 与 Agent | 模型、数据、prompt、RAG、工具、MCP | 注入、越权工具调用、数据投毒、失控成本 | AI red teaming、guardrail、eval、模型与数据治理 |

资产的核心不是 IP，而是稳定身份、所有权、业务重要度和授权关系。公网可见只说明
"能观察"，不说明"属于谁"或"允许主动交互"。公开代码与链上公开数据即研究输入：
阅读、静态分析与只读 fork 默认允许（见 `context/AUTHORIZATION_BOUNDARIES.md`）；
主动交互仍必须绑定真实授权来源。

## 二、威胁面：风险从哪里来

### 威胁来源

- 外部攻击者：犯罪团伙、国家行为者、机会主义扫描者和供应链攻击者。
- 内部与受信第三方：恶意人员、被接管账号、过宽权限和错误操作。
- 工程与运营失误：缺陷、错误配置、证书过期、备份失效和变更漂移。
- 系统性依赖：云、身份提供商、开源组件或集中控制面的共同故障。

### 行为链

ATT&CK 用真实观察组织对手从侦察、资源准备、初始访问，到执行、维持访问、权限与
凭据获取、发现、横向移动、收集、命令控制、外传和影响的行为。项目只保存版本化
映射，不把 ATT&CK 覆盖率当作检测有效率或漏洞证据。

### 不要混为一谈

| 概念 | 含义 | 不能推出 |
|---|---|---|
| Weakness / CWE | 缺陷或弱点类型 | 当前系统一定存在该缺陷 |
| Vulnerability / CVE | 被公开识别的具体漏洞 | 当前资产版本一定受影响或可利用 |
| Exposure | 可到达、错配或不必要暴露 | 一定存在软件漏洞 |
| CandidateFinding | 工具或规则提出的候选 | 已经是事实 |
| ConfirmedFinding | 有效授权或只读研究边界内由独立证据支持的结论 | 已遭入侵 |
| Incident | 已发生或高度可信的恶意活动 | 根因一定是已知 CVE |

## 三、防御面：组织需要哪些能力

| NIST CSF 2.0 Function | 人话解释 | 关键能力 |
|---|---|---|
| Govern | 决定谁负责、接受多大风险、供应商怎么管 | 风险治理、政策、角色、审计、供应链风险 |
| Identify | 知道有什么、重要性、暴露和依赖 | 资产清单、ASM/CAASM、漏洞与配置、SBOM、风险分析 |
| Protect | 降低事件发生概率和破坏面 | 身份、最小权限、加固、修补、加密、安全开发、备份 |
| Detect | 尽快看见异常和攻击 | 日志、SIEM、EDR/XDR、NDR、云检测、威胁情报 |
| Respond | 控制损失并清除威胁 | 分诊、隔离、SOAR、IR、取证、沟通与披露 |
| Recover | 恢复业务并防止复发 | 灾备、恢复验证、连续性、复盘和控制改进 |

成熟安全栈通常还会按市场能力拆成：GRC、ASM/CAASM、VM、AppSec、CNAPP、IAM/PAM、
EDR/XDR、NDR、SIEM/SOAR、DSPM/DLP、邮件安全、威胁情报、DFIR、备份恢复、OT Security
和 AI Security。分类会变化，责任边界比产品名字更重要。

## 四、工程与证据面：系统之间怎么说同一种话

| 层级 | 代表框架或标准 | 主要用途 | 证据上限 |
|---|---|---|---|
| 风险结果 | NIST CSF 2.0、CIS Controls v8.1、CISA CPG | 目标、优先级和基线控制 | 不证明控制已实施或有效 |
| 对手行为 | MITRE ATT&CK、CAPEC | 威胁建模、检测与验证假设 | 不证明特定漏洞存在 |
| 应用风险 | OWASP Top 10:2025、API Top 10:2023、LLM Top 10:2025 | 领域风险意识和测试覆盖 | 不是组织专属风险排名 |
| 弱点与漏洞身份 | CWE、CVE | 弱点分类和公开漏洞关联 | CVE ID 不是适用性或可利用性证明 |
| 优先级 | CVSS v4.0、EPSS、CISA KEV | 严重度、利用概率和在野利用信号 | 不能替代资产上下文与业务影响 |
| 安全开发 | NIST SSDF、SLSA | 安全 SDLC、源码/构建完整性与来源 | 来源可信不等于内容无漏洞 |
| 组件透明度 | CycloneDX 1.7、SPDX 3.0、VEX | 组件、依赖、许可证和适用性声明 | producer 不可信时结构也不可信 |
| 情报与通告交换 | STIX/TAXII 2.1、CSAF 2.0 | CTI、观察、关系和厂商通告互操作 | 交换成功不等于情报正确 |
| 工具结果交换 | SARIF 2.1.0、OCSF、工具原生 JSON | 静态发现、遥测和告警互操作 | 归一化不能制造缺失的原始证据 |
| 制品证明 | in-toto、Sigstore/Cosign | 声明、签名、身份和完整性 | 签名不证明安全性或业务正确性 |

所有外部数据都有生产者、版本、观察时间、置信度和失效条件。项目必须保留原始产物，
统一 envelope 只抽取公共字段，不能抹平工具特有证据。

## 五、本项目在全局景观中的位置

本项目不是 SIEM、EDR、IAM、扫描器或 GRC 的替代品。它位于 `Identify` 与安全验证的交叉
位置，为 `Protect/Detect/Respond` 提供可追溯事实。

```text
资产源 / CMDB / Cloud / Repo / SBOM / Threat Intel
                         │
CyberTask + ScopeGrant + Policy + Budget
                         │
                         ▼
              Security Evidence Control Plane
      plan -> adapter -> candidate -> independent validation
                         │
                         ▼
      append-only evidence -> confirmed finding -> export
                         │
          GRC / VM / SIEM / SOAR / Ticket / Human
```

### 直接建设

- `ScopeGrant`、规则求交、动作等级、预算、审批和停止条件；
- canonical asset、任务计划、工具适配器和结果 envelope；
- 候选与实证分离、独立验证、证据账本、失效和重验证；
- 基于业务重要度、可达性、KEV/EPSS 和证据质量的优先级；
- 审计、指标、人工门和向外部系统导出。

### 对接成熟系统

- 资产/CMDB、云账号、代码仓库、SBOM 和漏洞情报；
- SAST/DAST/SCA/ASM/CSPM 等发现器；
- IAM/PAM、EDR/XDR、NDR、SIEM/SOAR、GRC、工单和 DFIR；
- 本地靶场、评测集、签名、provenance 和制品仓库。

### 禁止默认自治

- 根据互联网观察自行扩大授权范围；
- 凭据猜测、爆破、钓鱼、持久化、规避检测或数据外传；
- 互联网尺度主动扫描、无界并发或无停止条件；
- 把扫描器告警、多数投票或模型判断直接写成实证漏洞；
- 未经审批修改生产系统、自动利用或删除生产数据。

## 六、现有供应链覆盖与真正空白

现有 46 项研究候选已覆盖：Agent 参考框架、资产发现、动态验证、代码/云分析、软件供应链、
漏洞情报/标准、编排运营和靶场评测。详细映射见
`governance/tasks/0003-map-global-cybersecurity-landscape/LANDSCAPE_COVERAGE.md`。

当前明显空白是身份安全、终端检测、网络检测、统一遥测、数据安全、事件响应/取证、恢复、
邮件/人员、OT/IoT 和 AI/Agent 专项控制。空白不等于现在就该加入供应链：首个纵向样例只需
证明授权、独立验证和证据晋升；其余能力应在出现真实消费者和验证路径后，以连接器方式引入。

## 七、衡量系统，而不是数工具

| 维度 | 建议指标 |
|---|---|
| 覆盖 | 已知资产率、授权资产率、近期开箱率、规则适用率 |
| 质量 | ground-truth precision/recall、候选确认率、重开率、证据完整率 |
| 新鲜度 | 资产、规则、漏洞情报和证据的 age / stale rate |
| 安全 | 越权动作数必须为 0、停止延迟、秘密泄漏数、策略拒绝率 |
| 效率 | p95/p99 任务时间、请求数、CPU/内存峰值、每个实证 finding 成本 |
| 结果 | 修复时间、复验通过率、重复漏洞率、风险下降量 |

开放空间朴素扫描成本近似 `O(A × E × R × V)`：资产、端点、规则和验证组合相乘。
优先做授权求交、去重、技术指纹过滤、变更驱动增量扫描和验证预算；不要用无界并发掩盖模型错误。

## 八、演进顺序

1. 本地靶场证明 `ScopeGrant -> Candidate -> Validation -> Evidence -> Finding`。
2. 接入只读代码、SBOM 和漏洞数据，校准证据质量。
3. 接入受限 Web/API 与资产发现，证明范围和停止控制。
4. 向 VM/GRC/SIEM/工单输出，不重建下游平台。
5. 只有真实需求出现后，再扩身份、云运行时、数据、OT 或 AI 专项能力。

核心判断：让成熟工具负责“看见”，让策略负责“能不能做”，让独立证据负责“能不能成立”。

## 权威基线

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [CIS Controls v8.1](https://learn.cisecurity.org/cis-controls-download)
- [CISA Cross-Sector Cybersecurity Performance Goals](https://www.cisa.gov/cybersecurity-performance-goals)
- [OWASP Top 10:2025](https://owasp.org/Top10/)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- [SLSA v1.2](https://slsa.dev/spec/v1.2/)
- [NIST Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [NIST Guide to Operational Technology Security](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
