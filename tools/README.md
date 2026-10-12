# tools

本目录存放辅助工具、转换器、外部工具镜像和工具配置。

## 当前结构

- `tools/prompts-library/`：提示词 Excel ↔ Markdown 互转工具。
- `tools/chat-vault/`：AI 聊天记录保存工具。
- `tools/external/`：外部仓库、第三方工具与 submodule。
- `tools/config/`：Codex 等工具配置。
- [faqi-catalog.md](faqi-catalog.md)：法器重要性只读浏览表，仅展示“品级、名称、解释”三列；解释合并重要性范围和分级依据，完整登记归[metadata/faqi.json](../metadata/faqi.json)，原资源字段仍归资源YAML。

## 法器总表维护

```bash
make sync-faqi-catalog
make check-faqi-catalog
make test-faqi-catalog
```

表格由维护脚本生成原生Markdown语法；不要手改生成视图。不搬移源码、Skill或配置；按程序指令内容、方法/规约、模型、载体、地址及运行实际所指分离。
脚本、Lua或嵌入shell的配置可具有程序所指，不因所在目录或后缀一律排除；纯配置、Skill说明与软件实现不强行合并。
本表30项按Vibe Coding重要性暂分天4、地12、玄9、黄5；这与本体中的正式任务效果评级分轴，后者仍为未校准草案。依赖类别纳入范围与版本观测不证明具体实现的任务效果、许可证、可用性或来源绑定。
当前清单纳入10项；Chat Vault、MC Player Transfer、XHS ZIP→PDF、HTML工具五项及my-nvim共9项按用户范围明确排除，并保留逐项来源证据和重审条件；不表示它们不是软件。
新增来源/内容变化先核身份与版本；视图仅由维护脚本生成，不把临时报告或个人目录作为长期数据源。
