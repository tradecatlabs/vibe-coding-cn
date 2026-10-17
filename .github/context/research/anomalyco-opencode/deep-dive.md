# anomalyco/opencode 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`anomalyco/opencode`。
- 证据来源：本目录 `raw/` 下的官方 README、源码、spec 和测试。
- 观察日期：2026-09-08。

## L2 结论

OpenCode 的 v2 设计把配置看成一组可重放、可更新的输入，而不是启动时一次性读取的常量。provider/model、agents、permissions、plugins 和 catalog 都有独立语义，同时通过 reload 生命周期重新组合。这个设计对本仓的启示是：配置备份、迁移和回滚必须记录“哪些层参与、哪些对象受影响”，不能只复制一个文件就声称安全。

## 源码和规格证据

- `raw/repository/packages/core/src/config.ts`：配置读取、合并和变换入口。
- `raw/repository/packages/core/src/provider.ts`、`model.ts`：提供商与模型目录。
- `raw/repository/packages/core/src/permission.ts`、`policy.ts`：权限和策略。
- `raw/repository/packages/core/src/plugin.ts`、`skill.ts`：插件和技能发现/生命周期。
- `raw/repository/packages/core/src/session.ts`、`snapshot.ts`：会话与状态快照。
- `raw/repository/packages/cli/`、`packages/tui/`、`packages/app/`：多种用户入口。
- `raw/repository/specs/v2/config.md`：v2 字段的 keep/remove/redesign 决策。
- `raw/repository/specs/v2/catalog-config-plugin-lifecycle.md`：配置变换、插件激活和全量 reload 的生命周期选项。

## 关键机制

### plan/build 是权限化的工作模式

README 中的 `plan` agent 默认偏只读，`build` agent 面向完整开发。这个区分把“先理解”与“允许副作用”分开，适合迁移为本仓研究和修改任务的前置检查。

### 权限是有序策略

v2 spec 讨论用有序的 allow/deny 规则替换零散的启用/禁用字段。可解释的规则顺序和资源匹配，比多个布尔开关更适合审计、覆盖和回滚。

### 插件改变配置后需要一致重载

spec 明确讨论插件 transform 可能改变任意配置字段，因此不能只刷新一个局部 catalog。这个机制提醒本仓：新增研究域后，README、metadata、AI 引用和 raw 事实都是依赖索引，不能只更新其中一个。

### 设计文档保留未决项

v2 spec 同时记录保留、删除、重设计和未决方案。这比把试验性设计伪装成稳定文档更诚实，也适合本仓 research 的事实/判断分层。

## 可迁移模式

- 将配置变更拆成发现、备份、写入、重载、验证和回滚。
- 为每个配置对象记录 owner、来源、风险和生效范围。
- 允许只读规划先输出影响面，再执行有副作用动作。
- 未稳定的上游设计放在 research，不直接下沉为强制教程。

## 不可迁移条件

- OpenCode 的 v2 spec 仍可能变化，不能当作已发布兼容契约。
- 本仓配置文件少，不需要复制完整 reload scheduler 或 catalog runtime。
- provider 凭据永远不能写入研究 raw、配置示例或日志。

## 验证计划

建立一个配置迁移 dry-run：输入旧配置和目标配置，输出变更对象、备份位置、权限影响、验证命令和恢复命令；dry-run 不写用户目录。成功信号是可审查 diff 与明确回滚；失败信号是无法指出某个配置字段由哪个层提供。
