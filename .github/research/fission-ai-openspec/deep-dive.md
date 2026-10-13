# Fission-AI/OpenSpec 深度研究

## 研究级别

- 当前级别：L2 变更规格与工具适配研究。
- 研究对象：Fission-AI/OpenSpec。
- 证据来源：本目录 raw/ 下的 README、openspec/、schemas/、.github/skills/ 和 src/。
- 观察日期：2026-09-08。

## L2 结论

OpenSpec 的核心结构是“变更是一级对象”：explore 用于低风险探索，propose 创建 proposal、specs、design 和 tasks，apply 执行，verify 验证，archive 归档并同步稳定规格。这个模型比把所有知识都写入一个永久 README 更适合持续变化的项目。

## 关键机制

### 变更目录承载临时状态

openspec/changes/ 保存进行中的变更，openspec/specs/ 保存稳定规格，archive 保存完成的历史。临时过程和长期真相分开，降低正文污染。

### Skill 与 CLI 分离

.github/skills/ 提供 Agent 可加载的动作，src/commands/ 提供 CLI，schemas/ 提供结构约束。能力、执行入口和数据契约各自有边界。

### Brownfield 优先

官方 README 明确强调既有项目和跨工具使用，说明规格系统不能假定绿地项目；它必须先理解当前结构，再提出局部变更。

### 可验证场景

需求以 requirement/scenario 组织，能直接转化为检查条件。对本仓而言，研究文章也可以用“事实 -> 判断 -> 迁移 -> 验证”形成可反驳链。

## 可迁移模式

- 对可能反复修改的研究主题保留 proposal 和当前稳定结论的差别。
- 将 deep-dive 视为验证资产，将 README 视为当前判断层。
- 为每个迁移动作写成功信号、失败信号和停止条件。
- 采用单对象单目录，横向比较放到综合文档。

## 迁移边界

- 本仓目前没有必要增加 openspec/ 运行时目录。
- 只在研究过程确实复杂、会产生临时状态时使用 proposal 资产。
- 文档任务仍以现有 AGENTS、Makefile 和质量门禁为准。

## L3 验证任务

1. 为一个跨 3 个目录的研究更新写短版变更提案。
2. 观察 proposal 是否减少重复修改和索引漂移。
3. 若提案只增加记录负担而没有降低风险，则合并为现有任务/研究模板。
