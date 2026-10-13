# continuedev/continue 深度研究

## 研究级别

- 当前级别：L2 生命周期、上下文和入口架构研究。
- 研究对象：continuedev/continue。
- 证据来源：本目录 raw/ 下的 README、.continue、core、extensions、packages 和 eval。
- 观察日期：2026-09-08。

## L2 结论

Continue 的源码把 core、IDE extensions、CLI、packages 和 binary 分开，同时在 .continue/ 中保存 agents、checks、prompts 和 rules。仓库停止维护这一事实本身也是研究证据：架构研究需要同时判断技术价值和继续采用风险。

## 关键机制

### 配置与检查是显式资产

.continue/agents 中包含破坏性变更、依赖安全、错误消息和输入校验等审查角色；这类角色可以转化为本仓的审查问题库。

### 上下文和工具分层

core/context、core/tools、core/config 和 core/indexing 说明 coding agent 的主要复杂度集中在上下文来源、工具能力、配置和索引，而不仅是 UI。

### 维护状态改变结论

README 的只读说明意味着公开源码和架构仍可研究，但安装、升级和安全判断不能按活跃项目处理。

## 可迁移模式

- 把文档、配置、命令和 API 的陈旧引用纳入变更审查。
- 将检查角色整理成可复用审计问题，而不是复制整个 agent。
- 研究目录记录生命周期状态、最后观察版本和推荐等级。

## 迁移边界

- 不运行已停止维护的安装流程。
- 不从其依赖或配置推导本仓当前技术栈。
- 不把 IDE 特有行为写进通用 Vibe Coding 教程。

## L3 验证任务

1. 抽取一个 breaking-change 检查项，映射到本仓索引门禁。
2. 抽取一个 error-message 检查项，映射到文档报错处理规范。
3. 将本研究域标注为历史/只读对标，并持续观察是否出现继任项目。
