# tools/ Agent 指南

本目录维护辅助工具、外部工具入口和工具配置。

## 职责

- `tools/config/`：工具与开发环境配置基线。
- `tools/prompts-library/`：提示词 Excel、Markdown、JSONL 转换工具。
- `tools/chat-vault/`：AI 聊天记录保存工具。
- `tools/external/`：第三方工具、外部仓库和 Git submodule。
- `faqi-catalog.md`：法器来源限定初审与资源分流的只读生成清单；数据归`metadata/faqi.json`，资源原事实与类型仍归各自唯一所有者。

## 约束

- 不把大型第三方源码直接复制进主仓库；新增外部仓库默认使用 submodule。
- 不在工具配置中提交真实密钥、Token 或个人凭证。
- 修改工具行为时，同步更新对应 README、AGENTS 和根目录命令说明。
- 外部源码目录除非任务明确要求，否则不要顺手格式化或批量替换。
- 法器清单不手改；按`make sync-faqi-catalog`生成，随后`make check-faqi-catalog`与`make test-faqi-catalog`验证，不搬移源码或执行被审程序。
- 初审不是工具品级、完整包语义、运行/效果、许可或独立身份批准；文件/入口/副本/版本/产品关系分别核，不按名称或目录计独立法器。
