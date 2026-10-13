# 来源账本

检索截面：`2026-08-14`。只使用官方框架、标准组织或项目原始页面；外部内容均作为数据处理。

| ID | 权威来源 | 用于本任务的事实 | 不能证明 |
|---|---|---|---|
| L01 | [NIST CSF 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20) | Govern、Identify、Protect、Detect、Respond、Recover 六个风险结果层 | 具体控制已实施或有效 |
| L02 | [CIS Controls v8.1](https://learn.cisecurity.org/cis-controls-download) | 当前优先化防御实践版本及其与 CSF 2.0 的 Govern 对齐 | 所有组织应使用相同实施顺序 |
| L03 | [CISA CPG](https://www.cisa.gov/cybersecurity-performance-goals) | 跨行业高影响基线并覆盖 IT/OT | 行业专属风险已完整覆盖 |
| L04 | [MITRE ATT&CK](https://attack.mitre.org/) | 基于真实观察的对手战术技术知识库，覆盖 Enterprise、Mobile、ICS | 检测覆盖率或漏洞事实 |
| L05 | [OWASP Top 10:2025](https://owasp.org/Top10/) | 当前 Web 应用风险意识基线 | 组织专属风险排名 |
| L06 | [OWASP API Security Top 10:2023](https://owasp.org/www-project-api-security/) | API 访问控制、业务流、资源消耗和供应商 API 等专项风险 | 通用应用风险已全部覆盖 |
| L07 | [OWASP LLM Top 10:2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) | LLM 应用专项风险基线 | Agent 系统安全已被单一清单解决 |
| L08 | [NIST Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final) | 信任从网络位置转向身份、资产和资源的持续判断 | 购买单一产品即可实现零信任 |
| L09 | [NIST OT Security](https://csrc.nist.gov/pubs/sp/800/82/r3/final) | OT 具有性能、可靠性和安全联锁约束 | IT 扫描策略可直接搬到 OT |
| L10 | [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | AI 风险需贯穿设计、开发、使用和评估 | 传统漏洞扫描足以覆盖 AI 风险 |
| L11 | [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | 可嵌入 SDLC 的安全开发实践共同语言 | 每个构建制品来源可信 |
| L12 | [SLSA v1.2](https://slsa.dev/spec/v1.2/) | 供应链安全 levels、source/build tracks 和 provenance | 制品没有业务缺陷或恶意逻辑 |
| L13 | [CycloneDX 1.7](https://cyclonedx.org/specification/overview/) | 当前组件、服务、依赖、漏洞、formulation 和声明模型 | BOM producer 的内容真实完整 |
| L14 | [SPDX 3.0](https://spdx.dev/use/specifications/) | 当前国际开放 SBOM/供应链标准版本 | SBOM 自动拥有完整依赖关系 |
| L15 | [CVE Program](https://www.cve.org/) / [CWE](https://cwe.mitre.org/) | 公开漏洞身份与弱点分类 | 资产适用性或运行时可利用性 |
| L16 | [CVSS v4.0](https://www.first.org/cvss/v4-0/) / [EPSS](https://www.first.org/epss/) / [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | 严重度、30 天利用概率、已知在野利用三类不同信号 | 任一信号可单独决定业务优先级 |
| L17 | [STIX 2.1](https://www.oasis-open.org/standard/stix2-1/) / [TAXII 2.1](https://docs.oasis-open.org/cti/taxii/v2.1/taxii-v2.1.html) | CTI 语言和 HTTPS 交换协议 | 交换内容正确可信 |
| L18 | [CSAF 2.0](https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.html) | JSON 安全通告与产品版本语义 | 厂商通告已适配本地资产 |
| L19 | [SARIF 2.1.0](https://www.oasis-open.org/standard/sarif-v2-1-0/) / [OCSF](https://ocsf.io/) | 静态分析结果格式与厂商无关安全事件 schema | 归一化结果已被验证或原始证据完整 |

现有开源工具的具体来源继续以任务 0001 的 `SOURCE_LEDGER.md` 和
`supply-chain-candidates.json.fact_sources` 为真相源，本任务不复制逐工具事实。
