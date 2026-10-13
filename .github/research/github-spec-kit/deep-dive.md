# github/spec-kit 深度研究

## 研究级别

- 当前级别：L2 规格驱动流程研究。
- 研究对象：github/spec-kit。
- 证据来源：本目录 raw/ 下的官方 README、.specify、templates、extensions、integrations、workflows 和 tests。
- 观察日期：2026-09-08。

## L2 结论

Spec Kit 的主要工程价值在于中间产物，而不是 slash command。constitution 固定项目原则，specify 固定需求，plan 固定技术实现，tasks 固定执行颗粒度，implement 执行任务，converge 检查实现是否回到规格。extensions、presets、bundles 和 integrations 则把可选能力放在独立分发面。

## 关键机制

### 规格阶段有独立职责

项目原则解决长期边界，规格解决目标和行为，计划解决技术路径，任务解决执行顺序。分开后，Agent 不需要把所有上下文压进一次提示。

### 收敛是闭环的一部分

README 将 converge 放在实现之后，说明“代码能运行”不是规格完成的充分条件。实现、测试和原始需求需要再次对齐。

### 扩展面独立

extensions、presets、bundles 和 integrations 不直接改变核心阶段概念。这个结构能控制本仓未来增加模板或工具时的复杂度。

### 测试分层

仓库中同时存在 contract、integration、unit 和 workflow 测试，说明流程型工具也需要测试命令、模板渲染和真实集成的不同证据。

## 可迁移模式

- 将本仓复杂任务的最小产物链固定为问题定义、方案、任务、实现、验证。
- 用 capability map 判断是否需要递归拆分，而不是所有任务都走重流程。
- 对每个模板记录 owner、输入、输出、验证和失效条件。
- 把扩展能力当作可卸载对象，避免污染核心教程。

## 迁移边界

- 本仓不需要引入 Python CLI、uv 或 Spec Kit 的完整目录。
- 用户的简单文档修改可以绕过完整规格阶段，但仍要有链接和结构验证。
- 规格不能替代测试，也不能让 Agent 自己批准高风险变更。

## L3 验证任务

1. 为本仓选一个多模块任务写 capability map 和小型规格。
2. 让一项研究索引更新走“计划 -> 修改 -> 链接/结构验证 -> 收敛”闭环。
3. 评估新增模板是否降低了歧义，若没有则删除或合并。
