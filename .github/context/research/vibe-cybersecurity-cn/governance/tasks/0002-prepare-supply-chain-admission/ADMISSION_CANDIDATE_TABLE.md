# 网络安全供应链准入候选表

快照：`2026-08-13`。本表由 `admission-candidates.json` 与 0001 研究目录联合生成，禁止手工修改。

`准入候选` 不等于已安装、已纳入或已启用。当前所有候选默认禁用；版本、摘要和门禁未闭合前不得进入执行面。

| 波次 | 候选 | 类型 | 计划职责 | 风险配置 | 网络副作用 | 门禁 | 固定版本 | 状态 | 主要阻塞 |
|---|---|---|---|---|---|---:|---|---|---|
| W0 | [OWASP CycloneDX](https://github.com/CycloneDX/specification) | schema | 跨工具 SBOM/VEX 交换格式 | schema-data | data-only | 0/8 | 待固定 | admission-candidate | schema 版本未固定；内部证据 envelope 尚未落地 |
| W0 | [Sigstore Cosign](https://github.com/sigstore/cosign) | executable | 工具与证据制品签名验证 | local-readonly | none | 0/8 | 待固定 | admission-candidate | 信任策略未定义；bootstrap 校验路径未验证 |
| W0 | [CISA Known Exploited Vulnerabilities](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | data | 在野利用优先级信号 | schema-data | data-only | 0/8 | 待固定 | admission-candidate | 快照下载和 freshness 策略未实现 |
| W0 | [FIRST EPSS](https://www.first.org/epss/) | data | CVE 利用概率排序信号 | schema-data | data-only | 0/8 | 待固定 | admission-candidate | 模型切换和历史断点策略未定义 |
| W0 | [NIST National Vulnerability Database](https://nvd.nist.gov/) | data | CVE/CPE/CVSS 元数据补全 | schema-data | data-only | 0/8 | 待固定 | admission-candidate | 缓存、配额和过期失败语义未实现 |
| W0 | [OSV.dev](https://osv.dev/) | data | 开源生态漏洞版本区间数据 | schema-data | data-only | 0/8 | 待固定 | admission-candidate | 快照更新和冲突解析策略未实现 |
| W1 | [Syft](https://github.com/anchore/syft) | executable | 本地制品 SBOM 生成 | local-readonly | none | 0/8 | 待固定 | admission-candidate | 固定版本和 golden SBOM 尚未验证 |
| W1 | [Grype](https://github.com/anchore/grype) | executable | 基于 SBOM 的异构漏洞匹配 | local-readonly | none | 0/8 | 待固定 | admission-candidate | 数据库差异和误匹配基线未建立 |
| W1 | [Gitleaks](https://github.com/gitleaks/gitleaks) | executable | 源码与 Git 历史秘密候选检测 | local-readonly | none | 0/8 | 待固定 | admission-candidate | 脱敏 golden test 尚未建立 |
| W1 | [Semgrep Community Edition](https://github.com/semgrep/semgrep) | executable | 可解释源码安全规则扫描 | local-readonly | none | 0/8 | 待固定 | admission-candidate | 规则子集、许可和 benchmark 未冻结 |
| W1 | [OSV-Scanner](https://github.com/google/osv-scanner) | executable | lockfile/SBOM 开源依赖扫描 | local-readonly | none | 0/8 | 待固定 | admission-candidate | 离线数据库和自动修复拒绝负例未验证 |
| W2 | [OWASP Juice Shop](https://github.com/juice-shop/juice-shop) | container | 本地已知漏洞 ground truth | lab-active | active-medium | 0/8 | 待固定 | admission-candidate | 镜像 digest、隔离网络和 ground truth manifest 未固定 |
| W2 | [httpx](https://github.com/projectdiscovery/httpx) | executable | 靶场 HTTP 存活与响应观察 | lab-active | active-low | 0/8 | 待固定 | admission-candidate | 安全默认配置和越界负例未验证 |
| W2 | [Nuclei Templates](https://github.com/projectdiscovery/nuclei-templates) | rules | 固定的低副作用 HTTP 检测规则子集 | lab-active | data-only | 0/8 | 待固定 | admission-candidate | 模板 allowlist、payload 摘要补强和回归样本未建立 |
| W2 | [Nuclei](https://github.com/projectdiscovery/nuclei) | executable | 靶场候选漏洞生成器 | lab-active | active-medium | 0/8 | 待固定 | admission-candidate | 独立 HTTP verifier、越界负例和证据 envelope 未实现 |
| W3 | [Trivy](https://github.com/aquasecurity/trivy) | executable | 仓库与镜像综合安全基线 | local-readonly | none | 0/8 | 待固定 | admission-candidate | 2026 供应链事件后的安全 artifact 路径尚未本地证明 |
| W3 | [Subfinder](https://github.com/projectdiscovery/subfinder) | executable | 授权资产的被动子域候选发现 | authorized-passive | passive | 0/8 | 待固定 | admission-candidate | 数据源凭据和归属验证策略未实现 |
| W3 | [Katana](https://github.com/projectdiscovery/katana) | executable | 授权 Web 端点候选发现 | authorized-active | active-low | 0/8 | 待固定 | admission-candidate | 外链越界、状态爆炸和表单副作用负例未验证 |

## 波次

- `W0`（6）：标准、信任根和情报数据
- `W1`（5）：本地只读代码与制品分析
- `W2`（4）：隔离 Web 靶场候选—验证闭环
- `W3`（3）：扩大能力面前的高约束候选

## 汇总

- 准入候选：18
- 已正式纳入：0
- 类型：container=1，data=4，executable=11，rules=1，schema=1

## 门禁含义

除研究来源外，每项需要完成 8 个正式门禁：许可、不可变版本、完整性、安全审查、接口契约、隔离策略、行为测试和回滚测试。
