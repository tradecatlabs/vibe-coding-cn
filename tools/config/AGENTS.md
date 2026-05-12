# tools/config/ Agent 指南

本目录维护工具和开发环境配置基线。

## 约束

- 配置文件必须是可公开审查的模板或基线，不得包含真实密钥。
- 本机专用配置应放在用户本地目录，不直接提交到仓库。
- 修改 Codex 配置时，同步更新 `tools/config/.codex/README.md` 和相关 getting-started 文档。
- 公开默认配置不得包含本机 `projects` 信任路径；高权限配置必须显式标注风险并通过独立 profile 安装。
- 一键安装脚本必须先备份用户现有配置，并提供恢复脚本。

## 验证

```bash
make test
```
