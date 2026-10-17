# auto-skill维护规则

本Skill只整理Skill指令、模板和资料，不保留自研生成、校验、导入或更新封装。

## 文件职责

- `SKILL.md`：当前触发、边界、流程、示例与验收。
- `assets/template-minimal.md`、`assets/template-complete.md`：既有模板参考，不是已实现能力。
- `references/index.md`、`references/README.md`：参考导航与来源。
- `references/skill-spec.md`、`quality-checklist.md`、`anti-patterns.md`：结构、内容与误用检查。
- `references/skill-seekers.md`：固定上游工具的可选使用边界，不是自动安装入口。

## 约束

- 原6个本地辅助脚本已按用户要求退役；不得在文档里继续给出可执行旧命令或恢复兼容壳。
- 先增强已有Skill，不为模板、计数或未证明的未来需求增加对象。
- 使用普通文件工具和平台原生发现；不新增管理框架或包装程序。
- 固定上游和独立初始化器保留，使用前另核对来源、依赖、授权及副作用，不运行上游来补造证据。
- 不虚构资料、模型行为、抽取范围、许可或效果；缺证据明确范围。
- 修改后核对当前两Skill可发现、导航有效与相关项目契约；最终完整测试按根AGENTS执行。
