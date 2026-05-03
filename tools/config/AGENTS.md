# tools/config/ Agent 指南

本目录维护工具和开发环境配置基线。

## 约束

- 配置文件必须是可公开审查的模板或基线，不得包含真实密钥。
- 本机专用配置应放在用户本地目录，不直接提交到仓库。
- 修改 Codex 配置时，同步更新 `tools/config/.codex/README.md` 和相关 getting-started 文档。

## 验证

```bash
make test
```
