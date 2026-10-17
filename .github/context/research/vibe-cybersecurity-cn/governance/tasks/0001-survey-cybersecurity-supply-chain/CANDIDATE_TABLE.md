# 开源网络安全供应链候选表

检索截面：`2026-08-13`。本表由 `supply-chain-candidates.json` 生成，请勿手工编辑。

评分是本项目的选型判断，不是上游官方声明，也不代表已完成本地能力验证。

| 状态 | 候选 | 类别 | 角色 | 接口 / 输出 | 网络副作用 | 许可 | 分数 | 主要门禁 |
|---|---|---|---|---|---|---|---:|---|
| mvp | [CISA Known Exploited Vulnerabilities](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | intelligence-standards | 已知在野利用优先级信号 | JSON, CSV / KEV catalog | data-only | 美国政府公开数据；使用时保留来源与 catalog 条款 | 24/25 | 只覆盖已收录 CVE；时效与资产映射 |
| mvp | [Grype](https://github.com/anchore/grype) | software-supply-chain | 镜像、文件系统与 SBOM 已知漏洞扫描 | CLI, Go library / JSON, CycloneDX, SARIF, table | none | Apache-2.0 | 24/25 | 数据库差异；包识别误差；同类工具结果不一致 |
| mvp | [OSV-Scanner](https://github.com/google/osv-scanner) | code-cloud-analysis | lockfile、SBOM、镜像的开源依赖漏洞与可达性分析 | CLI, Go API, offline DB / JSON, SARIF, HTML | none | Apache-2.0 | 24/25 | 生态覆盖差异；guided remediation 可执行包管理器脚本；数据库新鲜度 |
| mvp | [OSV.dev](https://osv.dev/) | intelligence-standards | 开源生态版本区间和别名规范化数据 | REST API, database dump, OSV schema / OSV JSON | data-only | 公开漏洞数据库与 API；逐数据源归因/许可需保留 | 24/25 | 生态覆盖差异；上游记录可能更正；别名与范围冲突 |
| mvp | [OWASP CycloneDX](https://github.com/CycloneDX/specification) | intelligence-standards | SBOM、VEX、漏洞与服务物料标准 | JSON/XML/Protobuf schemas, CycloneDX APIs / CycloneDX BOM, VEX | data-only | Apache-2.0 | 24/25 | 生成器扩展字段差异；格式转换可能丢字段；BOM 敏感性 |
| mvp | [Semgrep Community Edition](https://github.com/semgrep/semgrep) | code-cloud-analysis | 代码模式、缺陷变体与安全规则扫描 | CLI, rules DSL, CI / JSON, SARIF, JUnit | none | LGPL-2.1；规则库另有 Semgrep Rules License | 24/25 | 跨文件能力天花板；规则许可独立；社区规则误报需校准 |
| mvp | [Sigstore Cosign](https://github.com/sigstore/cosign) | software-supply-chain | 容器、blob 和 attestation 签名验证 | CLI, OCI registry, Sigstore bundle / JSON verification result, signature bundle, attestation | none | Apache-2.0 | 24/25 | 信任策略必须先定义；禁用 check-claims=false 绕过；离线根新鲜度 |
| mvp | [Syft](https://github.com/anchore/syft) | software-supply-chain | 镜像、文件系统和归档的 SBOM 生成与格式转换 | CLI, Go library / CycloneDX, SPDX, Syft JSON | none | Apache-2.0 | 24/25 | SBOM 不保证完整；不同格式字段损失；大型镜像资源成本 |
| mvp | [Trivy](https://github.com/aquasecurity/trivy) | code-cloud-analysis | 仓库、镜像、Kubernetes 的漏洞、秘密、错误配置与 SBOM 扫描 | CLI, server, CI, operator / JSON, SARIF, CycloneDX, SPDX | none | Apache-2.0 | 24/25 | 2026-03 官方披露 release/tag 供应链入侵，必须证明安全版本与签名；数据库新鲜度；多扫描器语义混合；第三方 SBOM 兼容精度 |
| mvp | [Gitleaks](https://github.com/gitleaks/gitleaks) | code-cloud-analysis | Git 历史和文件秘密检测 | CLI, pre-commit, Docker / JSON, CSV, JUnit, SARIF | none | MIT | 23/25 | 扫描结果本身高度敏感；假阳性；不得自动尝试凭据 |
| mvp | [httpx](https://github.com/projectdiscovery/httpx) | asset-discovery | 授权 HTTP 服务探测、指纹与响应采样 | CLI, stdin/stdout / JSONL, CSV, 可选请求响应 | active-low | MIT | 23/25 | 默认速率需下调；响应可能含秘密；重定向可能越界 |
| mvp | [Nuclei](https://github.com/projectdiscovery/nuclei) | dynamic-validation | 模板驱动的候选漏洞检测与可重复验证 | CLI, YAML DSL, stdin/stdout / JSONL, 请求响应证据, Markdown | active-medium | MIT | 23/25 | 模板风险不均；默认 RPS 偏高；某些模板产生副作用；响应可能含秘密 |
| mvp | [OWASP Juice Shop](https://github.com/juice-shop/juice-shop) | benchmarks-labs | 现代 Web 漏洞本地靶场与工具回归样本 | Docker, Node.js app, challenge API/scoreboard / 应用日志, challenge progress, Prometheus metrics | active-medium | MIT | 23/25 | 挑战集合与真实生产分布不同；容器必须隔离；某些用例可能破坏状态 |
| mvp | [Subfinder](https://github.com/projectdiscovery/subfinder) | asset-discovery | 被动子域候选发现 | CLI, stdin/stdout / JSONL, 文本 | passive | MIT | 23/25 | 来源配额与漂移；结果需范围求交和归属确认 |
| mvp | [FIRST EPSS](https://www.first.org/epss/) | intelligence-standards | 未来 30 天利用概率与百分位排序信号 | API, daily CSV, historical repository / CSV, JSON API | data-only | 公开免费使用，建议归因；非开源训练数据/运行管线 | 22/25 | 模型切换导致时序断点；底层遥测不可公开；不能用于非 CVE 候选 |
| mvp | [NIST National Vulnerability Database](https://nvd.nist.gov/) | intelligence-standards | CVE、CPE、CVSS 与适用性元数据 | CVE API 2.0, CPE API, JSON feeds / JSON API, JSON feeds | data-only | 美国政府公开数据；遵守 API 条款与归因 | 22/25 | API 配额与可用性；CPE 误匹配；记录丰富度不一 |
| mvp | [Nuclei Templates](https://github.com/projectdiscovery/nuclei-templates) | dynamic-validation | Nuclei 官方与社区检测规则供应链 | YAML/JavaScript/code templates, Git / 模板元数据, stats JSON | data-only | MIT | 22/25 | 社区规则质量差异；code/headless 模板扩大权限；payload 不全受签名摘要覆盖 |
| mvp | [Katana](https://github.com/projectdiscovery/katana) | asset-discovery | 授权 Web 端点和攻击面爬取 | CLI, stdin/stdout, headless / JSONL, URL/endpoint | active-low | MIT | 19/25 | 爬虫状态爆炸；外链越界；表单可能产生副作用 |
| pilot | [Checkov](https://github.com/bridgecrewio/checkov) | code-cloud-analysis | IaC、CI 配置、镜像与 SCA 策略扫描 | CLI, Python policies, CI / JSON, SARIF, JUnit XML, CycloneDX | none | Apache-2.0 | 22/25 | 与 Trivy 重叠；策略数量导致噪声；在线集成边界 |
| pilot | [in-toto Attestation Framework](https://github.com/in-toto/attestation) | software-supply-chain | 执行材料、产物与过程声明的可验证元数据规范 | DSSE/in-toto spec, Go/Python/Rust/Java bindings / attestation envelope, predicate | data-only | 按规范仓库固定版本复核 | 21/25 | 规范仍演进；predicate 设计成本；需要可信签名主体 |
| pilot | [Nmap](https://nmap.org/) | asset-discovery | 服务、版本、操作系统与 NSE 结构化探测 | CLI, NSE, XML DTD / XML, 结构化 NSE XML | active-medium | Nmap Public Source License (NPSL)；商业嵌入/再分发需法律或 OEM 审查 | 21/25 | NPSL 再分发限制；NSE 风险差异大；原始网络权限 |
| pilot | [OWASP Dependency-Track](https://github.com/DependencyTrack/dependency-track) | software-supply-chain | 持续 SBOM/VEX 分析与组件风险运营 | REST API, CycloneDX, Web UI / 组件/漏洞 API, policy violations, VEX | none | Apache-2.0 | 21/25 | 服务部署成本；v4/v5 迁移边界；组件身份与 VEX 质量 |
| pilot | [OWASP WebGoat](https://github.com/WebGoat/WebGoat) | benchmarks-labs | 教学型 Web 漏洞靶场与工具校准 | Docker, Java app / lesson/progress state, 应用日志 | active-medium | 按固定版本 LICENSE 复核 | 21/25 | 刻意不安全；必须断网隔离；ground truth 提取需适配 |
| pilot | [OWASP ZAP](https://github.com/zaproxy/zaproxy) | dynamic-validation | Web/API 被动与主动 DAST、代理与自动化框架 | REST API, Automation Framework, daemon, Docker / JSON/XML reports, alerts, session | active-medium | Apache-2.0 | 21/25 | Java/add-on 运维；主动规则副作用；认证状态与爬虫复杂度 |
| pilot | [DefectDojo](https://github.com/DefectDojo/django-DefectDojo) | orchestration-operations | 发现导入、去重、分诊、SLA 与漏洞运营 | REST API, import/reimport, Docker Compose / Finding API, 去重状态, 报表 | none | BSD-3-Clause | 20/25 | 数据模型需映射；去重算法需校准；不应成为验证真相源 |
| pilot | [Joern](https://github.com/joernio/joern) | code-cloud-analysis | Code Property Graph、跨过程查询和漏洞路径研究 | CLI/REPL, server, query DB, Docker / CPG, query results, scan findings | none | Apache-2.0 | 20/25 | 学习与查询成本；语言覆盖差异；资源开销；高频发布 |
| pilot | [OpenSSF Scorecard](https://github.com/ossf/scorecard) | software-supply-chain | 候选上游项目安全健康信号 | CLI, REST API, GitHub Action / JSON, SARIF, score | passive | Apache-2.0 | 20/25 | 评分可被误读；API 时效；私有仓库权限 |
| pilot | [OWASP Amass](https://github.com/owasp-amass/amass) | asset-discovery | 攻击面与外部资产图谱发现 | CLI, Open Asset Model, Asset Database / 资产关系, OAM 数据, 结构化输出 | passive | Apache-2.0；部分子组件可能不同 | 20/25 | 外部来源可能陈旧；资产归属需人工/合同确认；v5 数据模型需适配 |
| pilot | [Prowler](https://github.com/prowler-cloud/prowler) | code-cloud-analysis | 多云安全与合规检查 | CLI, API/UI, cloud SDK / OCSF JSON, CSV, HTML | active-low | 按固定版本 LICENSE 复核 | 20/25 | 云凭据高价值；多 provider 差异；输出可能含资源敏感信息；许可待复核 |
| pilot | [secureCodeBox](https://github.com/secureCodeBox/secureCodeBox) | orchestration-operations | Kubernetes 扫描执行、解析、级联与后处理层 | Kubernetes CRD, Helm, scbctl, hooks / 统一 Finding, 原始扫描报告, S3 artifact | active-medium | Apache-2.0 | 20/25 | Kubernetes 运维成本；级联扫描可放大范围；hook 可改写 finding |
| pilot | [AutoPenBench](https://github.com/lucagioacchini/auto-pen-bench) | benchmarks-labs | 生成式 Agent 渗透测试 benchmark、里程碑和脆弱容器 | Python, Docker Compose, structured tools / JSON agent actions, flags, stage/command milestones | active-high | MIT | 19/25 | 高危脆弱镜像；root/SSH 工具面；任务分布有限；部署资源 |
| pilot | [Greenbone Community Edition](https://github.com/greenbone) | orchestration-operations | 网络漏洞扫描、feed、任务管理与结果运营套件 | GMP, OSP, gvm-tools, Web UI / GMP XML, 扫描任务/结果, feed 状态 | active-medium | 多组件开源许可，核心服务常见 GPL/AGPL；需逐组件复核 | 18/25 | 多服务运维；feed 与组件耦合；扫描时长和资源成本；许可复杂 |
| pilot | [Naabu](https://github.com/projectdiscovery/naabu) | asset-discovery | 授权端口发现 | CLI, Go library, metrics / JSONL, callback results, metrics | active-medium | MIT | 18/25 | 原始包权限；高速扫描风险；CDN/WAF 地址归属 |
| reference | [MITRE ATT&CK STIX Data](https://github.com/mitre-attack/attack-stix-data) | intelligence-standards | 攻击技术、战术与检测/行为映射知识库 | STIX 2.1 JSON, collection index / STIX bundles, index JSON | data-only | MITRE ATT&CK 使用许可与归因要求 | 21/25 | 映射需要证据；类别覆盖不完整；不等于检测覆盖 |
| reference | [SkillSpector](https://github.com/NVIDIA/SkillSpector) | code-cloud-analysis | AI agent skills 安全扫描器：检测恶意指令、提权、数据外泄风险（15.5k star） | CLI, 规则引擎 / 扫描报告, 高风险 skill 定位 | none | Apache-2.0 | 20/25 | 规则覆盖有限；规则更新节奏；本地验证未跑 |
| reference | [Garak](https://github.com/NVIDIA/garak) | code-cloud-analysis | LLM 漏洞扫描器：prompt 注入、越狱、幻觉探测（9.1k star） | CLI, Python API, 扫描报告 / JSON 报告, 探测详情 | active-low | Apache-2.0 | 19/25 | 扫描成本；插件质量不均；探测覆盖有限 |
| reference | [Hacking-Tools (yogsec)](https://github.com/yogsec/Hacking-Tools) | intelligence-standards | 渗透测试与社工工具官方链接分类清单（参考索引） | README Markdown / 工具清单与官方仓库链接 | data-only | MIT | 19/25 | 链接可能失效或指向已改名仓库；含 StackScan/WebVerse Pro 赞助位；未逐工具审计 |
| reference | [Strix](https://github.com/usestrix/strix) | agent-harness | 应用安全 Agent、动态验证和修复闭环研究样本 | CLI, headless mode, CI, Agent skills / 本地 run 目录, 漏洞与 PoC, 报告 | active-high | Apache-2.0 | 19/25 | 高风险自动利用；多 Agent 所有权面；云/本地双形态；尚未本地复跑 |
| reference | [VulnClaw](https://github.com/Netw0rkNoob/VulnClaw) | agent-harness | AI 渗透测试 Agent：LLM + MCP 工具链 + Skill 参考资料，自然语言驱动信息收集→漏洞发现→利用→报告全流程（3.1k star） | CLI, REPL, TUI, Web UI, MCP / 结构化报告, Python PoC, 证据与子代理日志 | active-high | MIT | 19/25 | 高自主执行风险；traffic 模块未评估；上游导入 skill 未逐文件审计 |
| reference | [Blackstorm Security Research (ERS/MAS)](https://www.blackstormsecurity.com/research/) | intelligence-standards | 逆向工程与恶意软件分析研究 PDF 系列（Exploiting Reversing 01-09 / Malware Analysis Series 01-10） | PDF, RSS / 19 份 PDF 研究资料 | data-only | 官网声明 free-to-read；无显式开源许可证，存档仅供内部研究 | 18/25 | 无显式开源许可；资料质量未逐篇评估；不进入自动执行面 |
| reference | [OpenVAS Scanner](https://github.com/greenbone/openvas-scanner) | dynamic-validation | 网络漏洞测试执行引擎 | OSP, Greenbone stack / VT results, OSP/GMP records | active-medium | GPL 系列与组件例外需按固定版本复核 | 18/25 | 必须配套多组件；feed 状态影响结果；资源成本高 |
| reference | [CyberSecEval](https://github.com/meta-llama/PurpleLlama/tree/main/CybersecurityBenchmarks) | benchmarks-labs | LLM 网络安全风险、能力与自主攻击操作评测资料 | Python benchmark harness, datasets / benchmark results | active-high | PurpleLlama 自定义许可；数据子集可能有独立条款，需逐项复核 | 17/25 | 自定义许可；子模块数据条款；部分 offensive 测试高风险 |
| reference | [ExCyTIn-Bench / SecRL](https://github.com/microsoft/SecRL) | benchmarks-labs | 威胁调查与日志问答 Agent 评测 | Python, MySQL benchmark / evaluation logs, scores | none | MIT | 17/25 | 领域偏威胁调查；LLM judge 偏差；MySQL 运行成本 |
| reference | [GUAC](https://github.com/guacsec/guac) | software-supply-chain | 软件供应链元数据聚合、身份归一与图查询 | GraphQL, REST, collectors / 供应链图, GraphQL results | none | Apache-2.0 | 17/25 | 仍在活跃开发；身份归一边界情况；服务与存储成本；当前 YAGNI |
| reference | [PentAGI](https://github.com/vxcontrol/pentagi) | agent-harness | 自主渗透 Agent、沙箱和可恢复流程架构样本 | Web UI, GraphQL, Docker Compose / Flow 状态, 任务/子任务记录, 工具结果 | active-high | MIT 主项目；NOTICE/EULA 与云 SDK 需逐组件复核 | 17/25 | 高动作风险；部署复杂；混合服务条款；尚未做权限负例 |
| reference | [pwntools](https://github.com/Gallopsled/pwntools) | dynamic-validation | CTF 与 exploit 开发框架：汇编、shellcode、交互与调试（13.7k star） | Python API, CLI 工具 / exploit 脚本, 进程交互日志 | active-high | NOASSERTION（MIT 为主，需复核） | 17/25 | 许可复核；双用途工具滥用风险；与 Solidity 栈不同生态 |
| reference | [SpiderFoot](https://github.com/smicallef/spiderfoot) | intelligence-standards | OSINT 自动化：威胁情报与攻击面信息收集（21.6k star） | CLI, Web UI, 插件 API / OSINT 报告, 关联图数据 | passive | MIT | 17/25 | 数据源配额漂移；主动扫描模块越界风险 |
| reference | [Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | agent-harness | 817 个结构化网络安全 skills for AI agents，映射 6 个框架（32k star） | Markdown skills, 技能目录 / 技能文档 | none | Apache-2.0 | 16/25 | 第三方未官方背书；内容质量需抽样审计；体量大 |
| reference | [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) | benchmarks-labs | MITRE ATT&CK 映射的攻击行为检测测试集（12.5k star） | YAML 原子测试, 检测验证 / 测试日志, 检测覆盖率 | active-high | MIT | 16/25 | 动作副作用；与 S0 领域远 |
| reference | [Cybersecurity AI (CAI)](https://github.com/aliasrobotics/CAI) | agent-harness | 安全 Agent 架构、工具面与 HITL 研究样本 | CLI, Python SDK, MCP / 运行日志, Agent trace | active-high | MIT | 16/25 | 工具权限面过宽；需验证 guardrail 是否为运行时强制；尚未本地复跑 |
| reference | [PentestGPT](https://github.com/GreyDGL/PentestGPT) | agent-harness | 自动渗透 Agent 研究与 XBOW benchmark 适配样本 | CLI, Docker, benchmark runner / 会话状态, benchmark 结果, 遥测可选 | active-high | MIT | 16/25 | 宽 shell 能力；benchmark 外推风险；外部模型依赖 |
| reference | [dirsearch](https://github.com/maurosoria/dirsearch) | asset-discovery | Web 路径与目录扫描器（14.7k star） | CLI, 字典配置, JSON 输出 / 扫描结果列表, 响应状态证据 | active-low | NOASSERTION | 15/25 | 许可未断言；扫描噪声；与 S0 领域远 |
| reference | [PortSwigger Web Security Academy](https://portswigger.net/web-security) | benchmarks-labs | Web 漏洞知识、交互实验与验证思路资料 | Web labs / - | active-medium | 免费公开学习资源；不是可 vendoring 的开源软件 | 15/25 | 非开源依赖；平台条款；不适合大规模自动 Agent 运行 |
| reference | [Tsunami Security Scanner](https://github.com/google/tsunami-security-scanner) | asset-discovery | Google 通用网络扫描器，可插拔检测插件（8.6k star） | CLI, 插件 API / JSON 报告, 扫描日志 | active-medium | Apache-2.0 | 15/25 | 部署成本；插件生态；与 S0 无直接关系 |
| reference | [fscan](https://github.com/shadow1ng/fscan) | asset-discovery | 内网综合扫描：端口、服务、漏洞与弱口令探测（14.5k star） | CLI, JSON 输出 / 扫描结果, 漏洞探测记录 | active-high | MIT | 14/25 | 爆破模块副作用；二进制分发包信任；与 S0 无直接关系 |
| reference | [HexStrike AI](https://github.com/0x4m4/hexstrike-ai) | agent-harness | MCP 服务器驱动的 AI 渗透测试代理（11.5k star） | MCP, LLM Agent / 工具调用记录, 渗透任务输出 | active-high | MIT | 14/25 | MCP 工具权限面；模型依赖；自主执行风险 |
| reference | [reconFTW](https://github.com/six2dez/reconftw) | asset-discovery | 自动化域名侦察流水线：子域、端口、指纹、漏洞聚合（8k star） | CLI, 模块化流水线 / 侦察报告, 资产清单 | active-low | MIT | 14/25 | 依赖工具多；更新快导致漂移；主动探测需授权 |
| reference | [Shannon](https://github.com/KeygraphHQ/shannon) | agent-harness | AI 驱动的 Web 应用与 API 渗透测试 Agent（47.5k star，2026-09-02 截面） | CLI, Web UI / 扫描报告, 请求响应证据 | active-high | AGPL-3.0 | 13/25 | AGPL 传染性；自主请求面未审计；默认速率不可控 |
| reference | [Sn1per](https://github.com/1N3/Sn1per) | asset-discovery | 自动化渗透测试与攻击面管理平台（11.2k star） | CLI, Web UI, Docker / 扫描报告, 资产清单 | active-high | NOASSERTION（需逐文件复核） | 13/25 | 许可不明确；模板副作用不均；重量级依赖 |
| reference | [Nishang](https://github.com/samratashok/nishang) | dynamic-validation | Offensive PowerShell 后渗透脚本集（10k star） | PowerShell 脚本 / 脚本执行记录 | active-high | NOASSERTION（需逐文件复核） | 11/25 | 许可未断言；高对抗性；与 S0 领域无关 |
| hold | [OWASP Nettacker](https://github.com/OWASP/Nettacker) | agent-harness | 模块化自动渗透、资产发现和扫描管理研究样本 | CLI, REST API, Web UI, Docker / JSON, CSV, HTML, 数据库记录 | active-high | 按固定版本 LICENSE 复核 | 15/25 | 包含凭据爆破与规避能力；模块风险分级缺少本项目验证；许可待固定版本复核 |
| hold | [ZMap](https://github.com/zmap/zmap) | asset-discovery | 互联网尺度单包网络测量研究工具 | CLI / CSV/结构化字段 | active-high | Apache-2.0 | 12/25 | 互联网尺度影响；滥用与封禁风险；不符合默认授权模型 |
| hold | [masscan](https://github.com/robertdavidgraham/masscan) | asset-discovery | 超高速 TCP 端口扫描研究工具 | CLI / 多种扫描输出 | active-high | AGPL-3.0 | 10/25 | 高发包速率；AGPL 影响；默认需求无互联网级扫描 |

## 汇总

- 总候选：63
- 状态：mvp=18，pilot=15，reference=27，hold=3
- 类别：agent-harness=9，asset-discovery=13，benchmarks-labs=7，code-cloud-analysis=9，dynamic-validation=6，intelligence-standards=9，orchestration-operations=3，software-supply-chain=7

## 状态语义

- `mvp`：允许进入本地隔离纵向样例；仍需固定版本和真实复跑。
- `pilot`：价值明确，但部署、许可、动作风险或运维成本需要先校准。
- `reference`：仅用于架构、方法、数据或评测研究，不进入默认执行工具面。
- `hold`：当前阻塞未闭合，不进入实施计划。
