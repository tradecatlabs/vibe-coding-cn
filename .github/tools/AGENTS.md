# .github/tools/ Agent 指南

本目录维护辅助工具、外部工具入口和工具配置。

## 职责

- `.github/tools/config/`：工具与开发环境配置基线。
- `.github/tools/prompts-library/`：提示词 Excel、Markdown、JSONL 转换工具。
- `.github/tools/chat-vault/`：AI 聊天记录保存工具。
- `.github/tools/external/`：第三方工具、外部仓库和 Git submodule。
- `faqi-catalog.md`：法器重要性只读浏览表，仅含“品级、名称、解释”三列；解释合并登记的范围与分级依据，完整登记归`.github/metadata/faqi.json`，原资源字段仍归资源YAML。

## 约束

- 不把大型第三方源码直接复制进主仓库；新增外部仓库默认使用 submodule。
- 不在工具配置中提交真实密钥、Token 或个人凭证。
- 修改工具行为时，同步更新对应 README、AGENTS 和根目录命令说明。
- 外部源码目录除非任务明确要求，否则不要顺手格式化或批量替换。
- 法器清单不手改；按`make sync-faqi-catalog`生成，随后`make check-faqi-catalog`与`make test-faqi-catalog`验证，不搬移源码或执行被审程序。
- 来源初审与重要性分类彼此独立；重要性分级也不证明完整包语义、运行/效果、许可或独立身份；文件/入口/副本/版本/产品关系分别核，不按名称或目录计独立法器。
