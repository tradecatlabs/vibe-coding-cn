# 来源账本

本账本说明来源能够证明什么、不能证明什么。完整逐候选 URL 位于
`supply-chain-candidates.json` 的 `fact_sources`；这里保留架构判断所依赖的关键原始来源。

## A. Agent 与自动化框架

| ID | 原始来源 | 可确认事实 | 证据边界 |
|---|---|---|---|
| S01 | [CAI 官方仓库](https://github.com/aliasrobotics/CAI)、[技术报告](https://arxiv.org/abs/2504.06017) | 安全专用 Agent、工具、MCP、guardrail、HITL 和研究定位 | 不能证明 guardrail 覆盖全部绕过，也不能证明真实漏洞发现率 |
| S02 | [PentAGI 官方仓库](https://github.com/vxcontrol/pentagi)、[Flow 文档](https://github.com/vxcontrol/pentagi/blob/main/backend/docs/flow_execution.md) | Docker 隔离、工具集、自治 flow、任务/子任务和控制接口 | 主项目、云 SDK、NOTICE/EULA 与依赖许可需逐组件复核 |
| S03 | [Strix 官方仓库](https://github.com/usestrix/strix) | headless CLI、本地 run、动态验证、PoC、CI 与 Agent skills | “真实 PoC/低误报”是项目声明，尚未由本项目独立复跑 |
| S04 | [PentestGPT 官方仓库](https://github.com/GreyDGL/PentestGPT)、[USENIX 论文](https://www.usenix.org/conference/usenixsecurity24/presentation/deng) | Docker-first Agent、benchmark runner、会话与研究血缘 | benchmark 表现不能直接外推开放生产环境 |
| S05 | [OWASP Nettacker 官方仓库](https://github.com/OWASP/Nettacker) | CLI/API/UI、模块化 recon/scan/bruteforce、JSON/CSV/HTML | 模块能力面包含爆破和规避；必须按模块风险而非项目名授权 |

## B. 执行与漏洞运营

| ID | 原始来源 | 可确认事实 | 证据边界 |
|---|---|---|---|
| S06 | [secureCodeBox 系统边界](https://www.securecodebox.io/docs/architecture/system_scope_and_context/)、[hooks](https://www.securecodebox.io/docs/how-tos/hooks/)、[级联扫描](https://www.securecodebox.io/docs/hooks/cascading-scans) | 它负责 Kubernetes 扫描执行、parser、S3 artifact 和 hooks，扫描能力来自第三方工具 | 不拥有本项目授权、证据真实性或实证准入；级联可放大范围 |
| S07 | [DefectDojo 官方仓库](https://github.com/DefectDojo/django-DefectDojo)、[API](https://docs.defectdojo.com/automation/api/api-v2-docs/)、[去重](https://docs.defectdojo.com/triage_findings/finding_deduplication/about_deduplication/) | BSD-3-Clause、REST API、200+ 导入、去重、分诊和漏洞运营 | 运营记录不是原始证据；去重不等于独立验证 |
| S08 | [Greenbone 架构](https://greenbone.github.io/docs/latest/architecture.html)、[官方组织](https://github.com/greenbone) | OpenVAS scanner、GMP/OSP、gvmd、GSA、Community Feed 的多服务体系 | 各组件许可、feed 新鲜度和部署成本必须分开审计 |

## C. 资产发现与动态验证

| ID | 原始来源 | 可确认事实 | 证据边界 |
|---|---|---|---|
| S09 | [OWASP Amass](https://github.com/owasp-amass/amass)、[Open Asset Model](https://github.com/owasp-amass/open-asset-model) | 外部攻击面收集、资产关系和 OAM | 来源观察不能证明组织所有权或测试授权 |
| S10 | [ProjectDiscovery 开源工具](https://docs.projectdiscovery.io/opensource)、[Subfinder](https://github.com/projectdiscovery/subfinder)、[httpx](https://docs.projectdiscovery.io/opensource/httpx/usage)、[Naabu](https://github.com/projectdiscovery/naabu)、[Katana](https://github.com/projectdiscovery/katana) | 被动子域、HTTP 探测、端口扫描、爬虫、JSONL 与限速能力 | 默认速率和功能面不能直接作为本项目安全默认值 |
| S11 | [Nmap XML](https://nmap.org/book/output-formats-xml-output.html)、[NPSL](https://nmap.org/npsl/) | 稳定 XML/DTD、NSE 结构化输出和自定义许可 | NPSL 对商业嵌入/再分发有重要限制；NSE 风险不统一 |
| S12 | [ZMap](https://github.com/zmap/zmap)、[masscan](https://github.com/robertdavidgraham/masscan) | 互联网尺度或超高速端口测量能力 | 速度不是当前需求；默认动作风险与授权模型冲突 |
| S13 | [Nuclei 运行参数](https://docs.projectdiscovery.io/opensource/nuclei/running)、[模板签名](https://docs.projectdiscovery.io/templates/reference/template-signing)、[模板仓库](https://github.com/projectdiscovery/nuclei-templates) | JSONL、请求响应证据、限速、协议类型、官方模板签名与 code 模板约束 | 非 code 模板签名可选；payload 不全部进入签名摘要；模板命中仍是候选 |
| S14 | [OWASP ZAP Automation Framework](https://www.zaproxy.org/docs/automate/automation-framework/)、[ZAP 仓库](https://github.com/zaproxy/zaproxy) | API、daemon、Automation plan、passive/active DAST | alert 不自动证明业务影响，active scan 可产生副作用 |

## D. 代码、云与软件供应链

| ID | 原始来源 | 可确认事实 | 证据边界 |
|---|---|---|---|
| S15 | [Semgrep CE](https://github.com/semgrep/semgrep)、[社区规则](https://github.com/semgrep/semgrep-rules) | CE 引擎 LGPL-2.1、30+ 语言、规则 DSL；社区规则具有独立 Rules License | CE 官方明确说明安全分析局限于函数/文件边界，规则许可和质量需分开审计 |
| S16 | [Joern](https://github.com/joernio/joern)、[CPG 规范](https://cpg.joern.io/) | Code Property Graph、跨语言解析、query DB 和 server | 静态路径不能单独证明运行时可利用性 |
| S17 | [Trivy](https://github.com/aquasecurity/trivy)、[仓库扫描文档](https://trivy.dev/docs/latest/guide/target/repository/) | 仓库/镜像/K8s 的 vuln、secret、misconfig、license 与多标准输出 | 多扫描器结果依赖 DB、目标类型和自定义属性，不能视为统一真理 |
| S18 | [Trivy 官方供应链通告](https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23)、[安全 releases](https://github.com/aquasecurity/trivy/releases) | 2026-03 恶意 release/tag/Action 事件；后续不可变 release、checksum、Sigstore bundle 与 SBOM 可用 | 说明“官方 tag”本身不是稳定信任根；采用时必须固定安全 artifact 并验证签名/摘要 |
| S19 | [Checkov](https://github.com/bridgecrewio/checkov)、[Gitleaks](https://github.com/gitleaks/gitleaks)、[Prowler](https://github.com/prowler-cloud/prowler) | IaC/CI policy、秘密检测、云配置与 JSON/SARIF/OCSF 输出 | 云扫描需要高价值凭据；秘密扫描结果本身是敏感数据 |
| S20 | [OSV-Scanner](https://github.com/google/osv-scanner)、[输出文档](https://google.github.io/osv-scanner/output/) | lockfile/SBOM/image、offline DB、JSON/SARIF、部分 call analysis | guided remediation 可能运行包管理器及不可信脚本，默认不得自治执行 |
| S21 | [Syft](https://github.com/anchore/syft)、[Grype](https://github.com/anchore/grype) | SBOM 生成、CycloneDX/SPDX、镜像/文件系统漏洞扫描 | SBOM 完整性和漏洞适用性取决于生态、构建和 DB |
| S22 | [Dependency-Track](https://github.com/DependencyTrack/dependency-track)、[REST API](https://docs.dependencytrack.org/integrations/rest-api/) | API-first、CycloneDX SBOM/VEX、持续组件风险运营 | 组件风险平台不能替代应用可达性与漏洞验证 |
| S23 | [GUAC](https://github.com/guacsec/guac) | 供应链安全元数据聚合、GraphQL/REST 和多格式输入 | 官方明确仍在活跃开发且身份 heuristic 存在边界情况 |
| S24 | [Cosign](https://github.com/sigstore/cosign)、[验证文档](https://docs.sigstore.dev/cosign/verifying/verify/)、[in-toto](https://github.com/in-toto/attestation) | artifact/attestation 签名、digest/identity/issuer 和过程声明格式 | 签名证明来源与完整性，不证明内容安全；`check-claims=false` 会缩小保证 |
| S25 | [OpenSSF Scorecard](https://github.com/ossf/scorecard) | 开源项目安全健康启发式指标和 JSON/SARIF | 分数不是具体 release 无恶意或无漏洞的证明 |

## E. 漏洞情报与标准

| ID | 原始来源 | 可确认事实 | 证据边界 |
|---|---|---|---|
| S26 | [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | CISA 维护已知在野利用漏洞，并提供 JSON/CSV | 收录不证明当前资产受影响；未收录不证明未被利用 |
| S27 | [FIRST EPSS 数据](https://www.first.org/epss/data.html)、[FAQ](https://www.first.org/epss/faq) | 每日 CSV/API、30 天利用概率、模型版本；数据免费使用并建议归因 | 底层训练遥测和运营管线不公开；概率不是当前利用证据 |
| S28 | [NVD CVE API](https://nvd.nist.gov/developers/vulnerabilities)、[feeds](https://nvd.nist.gov/vuln/data-feeds) | CVE/CPE API 2.0、JSON feeds、分页与增量字段 | CPE/CVSS 可能不完整或误匹配，不应成为唯一事实源 |
| S29 | [OSV.dev](https://osv.dev/)、[OSV 仓库](https://github.com/google/osv.dev) | 开源生态漏洞 schema、版本区间、别名和 API/数据库 | 上游记录会更正；可达性和实际构建条件不由 OSV 单独证明 |
| S30 | [MITRE ATT&CK STIX](https://github.com/mitre-attack/attack-stix-data)、[数据模型](https://mitre-attack.github.io/attack-data-model/) | STIX 2.1 collections、版本化攻击知识和使用许可 | ATT&CK 映射不是漏洞证据或完整检测覆盖证明 |
| S31 | [CycloneDX specification](https://github.com/CycloneDX/specification) | SBOM/VEX 等机器 schema 与格式 | 标准化结构不能保证 producer 的真实性和完整性 |

## F. 靶场与评测

| ID | 原始来源 | 可确认事实 | 证据边界 |
|---|---|---|---|
| S32 | [OWASP Juice Shop](https://github.com/juice-shop/juice-shop)、[WebGoat](https://owasp.org/www-project-webgoat/) | 刻意脆弱应用、Docker/本地运行和教学/工具校准用途 | 必须隔离；漏洞分布不能代表真实生产分布 |
| S33 | [PortSwigger Academy](https://portswigger.net/web-security) | 免费公开 Web 安全知识和交互实验 | 不是开源可 vendoring 依赖，也不应被自动化滥扫 |
| S34 | [AutoPenBench](https://github.com/lucagioacchini/auto-pen-bench)、[论文](https://arxiv.org/abs/2410.03225) | Docker 脆弱机、flags、命令/阶段 milestone 和结构化 Agent 工具 | benchmark 成功不外推开放环境；环境包含 root/SSH 高风险能力 |
| S35 | [CyberSecEval](https://github.com/meta-llama/PurpleLlama/blob/main/CybersecurityBenchmarks/README.md)、[论文](https://arxiv.org/abs/2408.01605) | 多类 LLM 网络安全风险/能力评测，含 autonomous offensive tests | 自定义许可和子数据条款需逐项核验 |
| S36 | [Microsoft SecRL](https://github.com/microsoft/SecRL) | 威胁调查 benchmark、MySQL 数据和 evaluation logs | 偏防御调查，不验证本项目主动漏洞闭环 |

## G. 当前覆盖缺口

- 尚未对任何 `mvp/pilot` 下载、安装或固定版本本地复跑。
- 许可证文本只完成候选级初筛；混合组件和商业嵌入必须由固定版本清单再审查。
- 未建立统一的实证漏洞 ground truth 数据集；首轮只选择 Juice Shop 做本地垂直样例。
- 未测量不同扫描器的真实误报率、漏报率、p95 延迟、资源峰值和证据完整率。
- 未验证现有 Agent 项目的 runtime guardrail、prompt injection 防护和越权负例。

因此本账本证明“候选事实可回溯，采用判断有明确依据与限制”，不证明候选已经生产可用。

