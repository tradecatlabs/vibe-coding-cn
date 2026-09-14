# Changelog

## 2026-09-09 — Project #2 Top-146 赏金问题仓库快照

- 从 GitHub Project #2 View 3 fresh-read 234 条 Award record，按 `USD Equivalent DESC`、`Title ASC` 排序，并按 Repository URL 去重，发布前 146 个唯一问题仓库的 JSON 与人类可读索引。
- 保留原币种、名义金额、USD 折算、FX 日期、来源状态、Award 状态、支付未知状态和 Award ID；同一仓库的多个 Award record 不相加。
- 明确严格 `USD Equivalent > 100` 的唯一仓库数量与 Top 146 边界不同；为满足 146 个仓库目标，快照透明保留 USD 100.00 边界行。
- 同步 README、英文 README、公共问题索引、GEO、LLM 检索摘要、实体卡和公共声明；Project、仓库、Issue、PR、CI、checkpoint 与赏金字段仍不是 Evidence、Result 或 Solution。
- 明确 `secp256k1` 是独立密码学复杂性审计问题，不属于六个千禧年问题。

## 2026-09-07 — 公共 README、AI 发现与 GEO 维护面

- 在 README 首屏和公共问题索引中增加 GitHub Project #1、公共 ProblemContract 问题库、单问题模板、公开仓库列表以及六个未闭合千禧年问题与 secp256k1 关键问题仓库的直达索引；所有链接保持 pointer-only，不把仓库活动解释为数学证据或已解决声明。
- 确立 Point–Line–Face–Body（PLFB）为唯一概念元模型根：PWTSJ 归入 F05 过程面，OSPS 归入 F04 结果空间面；公开 Face/Body、跨面绑定和状态非传播边界。
- 同步 README/GEO/AI citation/Schema.org/codemeta/架构图与公共声明；明确本次仅发布概念标准，不宣称 PLFB registry、Body runtime、OSPS orchestrator、通用 PWTSJ scheduler 或统一 Observation Ledger 已实现。
- 重构中英文 README 首屏，统一项目实体、公共 URL、当前空 ledger 状态、快速开始和证据边界。
- 新增 `llms.txt`、AI 引用资产、术语契约、双语回答矩阵和不承诺排名的 GEO 评估协议/机器报告模板。
- 新增公共声明账本、贡献/安全边界文档以及 README/GEO 事实和链接校验。
- 接入 `vibemathing` 公共具体问题索引、ProblemContract 总库 locator、网页版研究模板入口、只读 API/catalog 查询器和本地 draft ProblemContract 模板；远端条目不会自动准入。
- 发布 `FORMAL-METHODS-MAP.md`：以“规格与语义 → 演绎验证 → 模型检查 → 抽象解释 → SAT/SMT/符号推理（含符号执行） → 精化/综合”为方法层主线，并把 Lean 准确放在依赖类型理论型演绎验证分支。
- 新增 `GEO.md` 与 `retrieval-contract.v1.json`，提供意图级答案、最近一手引用目标、别名和不可推断边界；GEO 仍是文档准确性维护，不是数学证据或排名承诺。
- 将 Project → Workflow → Task → Step → Job 五级生命周期模型与 ProblemContract → Attempt → Result 数学事实链分离，并同步到公开标准、上下文、README 和 GEO Q12。
- 增加 Schema.org 软件实体元数据、README Mermaid 架构总览、GEO 检索路由表与 freshness/authority 规则，并让校验器检查身份、引用 URL 和非数学证据边界的一致性。
- 新增只读 `query_ai_citation.py` 与回归测试，可从固定 retrieval contract 渲染双语答案和稳定引用 URL，不接触网络或研究记录。
- 增加静态、可访问、无外链脚本的双层架构图 `assets/architecture.svg`，并由公共检查器验证其内容边界。
- 将 freshness/authority 纳入第十三个 GEO 固定意图、双语答案矩阵、声明账本、实体卡与引用渲染器，明确本地状态权威和外部快照重核规则。
- 新增只读 `audit_public_status.py` 与回归测试，以受限文件读取和 SHA-256 摘要机械核对公开 ledger/index 状态，不产生数学 Result。
- 公共文档仍不声称解决任何开放数学问题；GEO 评估只衡量理解和引用准确性，不是数学证据。

## 2026-09-01 — 公开候选契约、研究 bundle 与工具边界

- 发布 ProblemContract v1、CandidateObservation schema/registry、候选 snapshot 校验和默认 admitted 查询边界。
- 发布只读 ResearchBundle、failed-route append-only schema、SMT/SymPy 有界 fixture 与文献 provider registry。
- 发布 41 个工具族的公开成熟度 registry、严格两列工具目录和正例/反例/错误/timeout canary 契约；不携带内部运行报告。
- 供应链来源只接受固定 commit/reference；抓取器拒绝未固定 Git clone、移动分支归档和 TLS 验证绕过，并为外部命令设置 timeout。
- 公开仓继续保持 canonical Problem、Attempt、Result 和 Solution View 业务记录为空；候选不等于已解决问题。

## 2026-08-13 — 单机可信研究闭环 100/100

- 新增受信 verifier registry、不可覆盖证据回执、现场摘要重算和 append-only 失效语义。
- 新增 `flock + WAL + fsync + os.replace` 原子研究存储、可恢复运行状态机与统一 CLI。
- 新增 SymPy 反例和固定 Lean/Mathlib 两条端到端闭环，以及攻击矩阵、故障恢复、成熟度审计和 CI 门禁。
- 100/100 限定为单机、单 Agent、可信研究闭环；Git 交付、外部 reviewer 签发和分布式高可用仍是独立边界。
- Lean adapter 兼容 elan 官方默认目录，即使非交互 shell 未配置 `~/.elan/bin` 也能确定性发现工具链。
- Lean 冷缓存构建使用 Lake 官方 quiet 模式，保留 2 MiB 输出预算而不让进度日志误触发资源门禁。
- 子进程输出预算改为只流式约束 stdout/stderr，不再错误限制 Lean 等工具写入业务构建产物。

## 2026-08-13 — VIBE-MATHING-SPEC v0.1

- 发布三条项目基本法则：候选隔离、验证准入、证据守恒。
- Result 证据能力新增 `axiom_escape_audit` 与 `prior_art_review`。
- kernel 直接验证只有与独立公理/逃逸审计组合时才满足完整解准入。

## 2026-08-13 - 供应链审计快照

- 增加经过隔离、范围受限的第三方材料精简快照；快照不自动激活，也不整体发布。
- 扩展供应链脚本，以来源、目标、lockfile 三方 inventory 和树摘要提供幂等同步与漂移检查。

## 2026-08-13 - 问题空间到解空间基础框架

- 新增 canonical Problem、Attempt、Result 三个最小机器契约与空真相源。
- 结果状态采用 `outcome × evidence` 二维模型；证据使用能力偏序和可失效追加账本。
- 新增研究空间、成果空间和由 Result 派生的解库索引；有限证据、自我审查和陈述失真不能晋升完整解。
- 新增最小治理包、项目操作模型、架构决策和数学成果晋升 Gate。
- 新增 `make check` / `make check-full` 与 GitHub Actions CI；可移植 CI 不依赖本地电子书、原始网页或上游缓存。

## 2026-08-13 - 数学电子书文献库

- 新增 `literature/` 的 Work/Edition/File/Relation 目录模型和 JSON Schema。
- 将《数学大辞典（第二版）》移动到 ISBN 对象路径，分类为 MSC2020 `00A20` 综合数学辞典。
- 新增文件摘要、ISBN、引用完整性离线校验；电子书二进制明确排除 Git。

## 2026-08-13 - 本地数学问题库

- 新增 `problem-library/`，保存 Wikipedia 与 UnsolvedMath 的原始目录快照、统一问题记录和倒排索引。
- 新增幂等抓取、离线校验与查询脚本；UnsolvedMath 完整性绑定站点声明总数和分页哈希。
- 明确 Wikipedia CC BY-SA 归属以及 UnsolvedMath 未知许可下的“目录字段/短摘要、不镜像详情正文”边界。

## 0.1.0 - 2026-08-13

- 初始化 Vibe Mathing 中文数学研究工作台。
- 新增 6 个项目级 active skills：路由、发现、推导、计算、证明和形式化。
- 拉取并锁定 RW、Wentor、K-Dense 三个上游供应链仓库。
- 保存 Annals 三个证明相关 skill 的精简审计快照。
- 新增供应链同步、项目结构校验和 SymPy 数学 smoke 脚本。
- 建立 `conjecture` 到 `kernel-checked` 的证据状态边界。
