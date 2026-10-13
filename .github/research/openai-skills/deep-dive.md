# openai/skills 深度研究

## 研究级别

- 当前级别：L2 迁移结构研究。
- 研究对象：`openai/skills`。
- 证据来源：本目录 `raw/` 下的官方 README、根目录快照和浅层仓库工作树。
- 观察日期：2026-09-08。

## L2 结论

这个仓库展示了一个技能 catalog 的早期形态：把系统技能、精选技能和实验性技能放进统一目录，再由 Codex 提供发现与安装入口。它的关键研究意义不在某一个技能，而在于“技能目录是能力分发面”。官方随后将当前示例迁移到插件仓库，说明 catalog、manifest、安装和生命周期应被视为同一条供应链。

## 源码证据

- `raw/repository/skills/.system/`：随 Codex 提供的系统技能。
- `raw/repository/skills/.curated/`：由目录维护者精选的技能。
- `raw/repository/skills/.curated/gh-fix-ci/`：面向具体工程动作的技能样本。
- `raw/repository/skills/.curated/security-best-practices/`：把专业知识封装成可加载能力的样本。
- `raw/github-readme.raw.md.txt`：官方弃用声明和迁移到 Plugins 的说明。

## 关键机制

### 分层而非平铺

`.system` 和 `.curated` 表明技能不应只有一个平面列表。成熟度、信任级别和安装方式不同，目录和入口应能表达这种差异。

### 能力包而非单条提示词

技能目录可以同时承载说明、脚本、资源和验证材料。这个结构比把长提示词复制到每次对话更容易复用，也更容易审查权限和副作用。

### 目录生命周期必须可迁移

仓库被标记 deprecated 但技能概念没有消失，而是迁移到 Plugins。这说明技能内容、发现入口和分发载体不是同一个对象，迁移时必须单独处理三者。

## 可迁移模式

- 本仓 skill 入口写清任务触发条件，不要求 Agent 预加载全部技能。
- 高风险技能把命令、权限、回滚和验证写成显式边界。
- skill 的稳定事实与项目特有配置分开，避免把外部目录直接当本仓规则。
- 对失效或迁移中的上游对象保留来源和结论，但不继续推荐旧入口。

## 验证计划

1. 抽样检查 `.github/skills/auto-tmux`、`.github/skills/auto-skill` 和一个业务 skill。
2. 为每个样本记录触发、输入、输出、依赖、权限、失败和回滚。
3. 运行本仓 skill 目录校验和最小示例。
4. 若缺少验证命令，先补文档或脚本，再把该 skill 提升为默认入口。

## 风险和边界

- raw 仓库是外部事实缓存，不代表本仓认可其中每条指令。
- 许可证信息当前未在 GitHub license 接口中提供，不能从“官方仓库”推断单个技能均可自由复制。
- deprecated 状态会改变推荐结论；引用本研究时必须同时读取 `openai/plugins` 的当前材料。

## 下沉建议

将“技能能力包最小契约”沉淀到本仓 `.github/skills/AGENTS.md` 或现有 owner skill；不要新增一个只复述外部目录的长期教程。
