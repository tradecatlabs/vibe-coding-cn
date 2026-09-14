---
id: GOV-CHANGELOG
type: changelog
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-09-07
review_cycle: P90D
---

# 治理包变更记录

- 发布公共 Point–Line–Face–Body v0.1 标准，将 PLFB 固定为唯一概念元模型根；PWTSJ 归入 F05，OSPS 归入 F04，Body 保持 reference-only。
- 固定 `Job succeeded ≠ Step accepted ≠ Obligation closed ≠ OutcomeNode closed ≠ Result admitted ≠ Project solved`，并明确概念模型不等于 runtime 已实现。
- 发布公开问题库的 candidate registry、CandidateObservation schema、ProblemContract v1 和 ResearchBundle 只读派生契约；明确来源状态不等于数学结论。
- 发布 41 个工具族的公开成熟度注册表与两列工具目录；缺少公开运行证据的族保持为调研分类，不引用内部盘点文件。
- 供应链新增固定的候选 Git reference 记录；抓取器拒绝未固定 clone、移动分支归档和不安全 TLS 绕过。

- 新增公开仓库发布边界和自包含机器门禁，拒绝私密研究路径、恢复快照、生成物、绝对用户路径、私有网络标识与凭据模式进入公开 Git 树。
- 初始化治理包。
- 记录 Problem → Attempt → Result → 派生解空间的项目操作模型与 ADR-0000。
- Result 采用 `outcome × evidence`，并以偏序能力集和追加失效账本替代单一证据等级。
- 新增 GATE-0002，阻止有限证据、自我审查和陈述失真进入完整解视图。
- 登记 problem-library、research、result-library 模块上下文和可移植/完整两级工具链。
- 发布项目级 `VIBE-MATHING-SPEC v0.1`，把研究闭环压缩为 R1 候选隔离、R2 验证准入、R3 证据守恒；九条候选要求收敛为操作层推论。
- 新增公共发布声明账本与 AI 发现资产的维护边界；它们是文档派生物，不是数学 Result 真相源。
- 登记 `vibemathing` 公共问题总库、具体问题 locator、网页版研究模板和 pointer-only 集成策略；远端目录不会绕过本地 ProblemContract 准入。
- 发布形式化方法与 Lean 定位地图，作为 skills、工具目录和 README 的方法层主线；不把教学目录、工具可运行或 Lean kernel check 写成数学 Result 证据。
- 增加公共 GEO 事实与引用入口、意图级 retrieval contract 和 Q11/Q12 引用与生命周期边界测试；所有 GEO 资产仍保持非数学证据边界。
- 新增公开全生命周期标准，明确 Project → Workflow → Task → Step → Job 与 ProblemContract → Attempt → Result 的正交关系，以及 Job/Step/Task/Project 不可越权的状态边界。
- 增加 Schema.org 实体元数据、GEO 检索路由/新鲜度规则和 README 架构总览；AI-citation 校验器现在同时检查结构化身份、稳定引用 URL 与非数学证据边界。
- 增加只读 citation renderer 与回归测试，使固定 retrieval intent 可在本地重复渲染，且不产生数学 Result。
- 增加静态无脚本架构图并加入公共内容校验，避免视觉资产引入外部内容或可执行载荷。
- 将 freshness/authority 纳入固定 GEO 意图、声明账本和实体卡，要求区分本地状态权威与带日期的外部快照。
- 增加只读 public status auditor 与回归测试，以文件摘要和空状态门禁支撑可复核的当前状态描述。
