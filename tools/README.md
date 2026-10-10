# tools

本目录存放辅助工具、转换器、外部工具镜像和工具配置。

## 当前结构

- `tools/prompts-library/`：提示词 Excel ↔ Markdown 互转工具。
- `tools/chat-vault/`：AI 聊天记录保存工具。
- `tools/external/`：外部仓库、第三方工具与 submodule。
- `tools/config/`：Codex 等工具配置。
- [faqi-catalog.md](faqi-catalog.md)：法器来源限定初审及外部资源分流的只读清单；来源与判定归[metadata/faqi.json](../metadata/faqi.json)，类型归唯一本体，原资源字段仍归资源YAML。

## 法器清单维护

```bash
make sync-faqi-catalog
make check-faqi-catalog
make test-faqi-catalog
```

不搬移源码、Skill或配置；按程序指令内容、方法/规约、模型、载体、地址及运行实际所指分离。
脚本、Lua或嵌入shell的配置可具有程序所指，不因所在目录或后缀一律排除；纯配置、Skill说明与软件实现不强行合并。
清单只证明所列固定来源的初审记录，不证明独立产品数、运行正确、许可证、可用性或效果，法器不套功法品级。
当前清单纳入10项；Chat Vault、MC Player Transfer、XHS ZIP→PDF、HTML工具五项及my-nvim共9项按用户范围明确排除，并保留逐项来源证据和重审条件；不表示它们不是软件。
新增来源/内容变化先核身份与版本；视图仅由维护脚本生成，不把临时报告或个人目录作为长期数据源。
