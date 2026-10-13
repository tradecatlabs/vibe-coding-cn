# openai/skills 研究分析

## 本轮结论

`openai/skills` 的研究价值已经从“当前技能目录”变成“技能目录迁移到插件分发体系的历史样本”。官方 README 明确写出仓库已 deprecated，并把当前 Codex skill 与 plugin 示例指向 `openai/plugins`。因此，本仓只保留它作为迁移对照，不把它推荐为现行安装入口。

## 本地证据

- `raw/github-readme.raw.md.txt`：官方 README 的弃用声明、迁移目标和安装说明。
- `raw/github-root-contents.raw.json`：仓库根目录包含 `.github/skills/`。
- `raw/repository/skills/.system/`：系统技能目录。
- `raw/repository/skills/.curated/`：精选技能目录。
- `raw/sources.yml`：拉取时间、命令和文件状态。

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `openai/skills` |
| 核心问题 | 把可复用 Agent 能力集中目录化，并让 Codex 能按需发现与安装 |
| 核心机制 | `.system`、`.curated`、`.experimental` 分层，技能以目录和 `SKILL.md` 承载 |
| 迁移信号 | 官方 README 将现行示例和 skill-only plugin 构建方式转向 `openai/plugins` |
| 可迁移做法 | 技能分层、目录发现、安装前说明、技能与运行时规则分离 |
| 不可迁移条件 | 不把已 deprecated 的目录继续当作当前官方目录；不复制外部技能内容进本仓 |
| 下一步试用动作 | 对本仓 3 个高频 skill 增加触发条件、输入输出、风险和验证字段 |

## 改良迭代

| 改良目标 | 本仓版本 | 验证指标 |
|:---|:---|:---|
| 技能发现 | `.github/skills/README.md` 给出按任务选择的入口 | 新用户能从任务找到一个明确 skill |
| 技能边界 | 每个 `SKILL.md` 写触发条件、输入、输出和禁用场景 | Agent 不需读取全仓即可判断是否加载 |
| 迁移治理 | 当前插件参考 `.github/research/openai-plugins`，历史目录只做来源说明 | 文档不再把 deprecated 仓库当现行方案 |
| 质量控制 | skill 产出绑定脚本、测试或检查命令 | 技能结果有可复现证据而非口头保证 |

## 可迁移清单

- 用系统、精选、实验性等层级表达技能成熟度。
- 让技能目录只承载能力，具体项目规则仍由项目级 `AGENTS.md` 管理。
- 在安装前展示来源、权限、依赖和验证方式。
- 以插件或技能 manifest 作为机器可读发现入口。

## 不可迁移清单

- 不把 `openai/skills` 作为当前 Codex 安装入口。
- 不直接复制外部 `SKILL.md` 并默认在本仓执行。
- 不因目录存在就跳过许可证、来源和副作用审查。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 对照 3 个本仓 skill 补齐元数据 | 触发、输入输出和验证路径完整 | 仍只能靠阅读全文猜用途 |
| 检查旧技能引用 | 当前文档指向 `openai/plugins` 或本仓 skill | 把 deprecated 目录写成最新安装方式 |
| 试装一个本仓 skill | 安装后能被 Agent 发现且有回滚路径 | 安装产生未审查命令或隐式权限 |

## 沉淀判断

“技能是可分发能力包，而不是提示词堆”可以下沉到 `.github/skills/AGENTS.md`；“技能目录已经迁移到插件体系”只保留在本研究域和 `openai/plugins` 研究域，避免把动态迁移事实写成稳定规则。
