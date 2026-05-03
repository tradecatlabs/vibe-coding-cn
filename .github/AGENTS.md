# .github/ Agent 指南

本目录承载 GitHub 平台自动化与协作配置。

说明：本目录不放 `README.md`，避免 GitHub 仓库首页误展示平台配置说明；目录规则只保留在 `AGENTS.md`。

## 约束

- 修改 `workflows/` 前必须确认对应本地命令或验证方式。
- 修改 Issue / PR 模板时保持字段简洁、可执行、可审查。
- 修改安全政策时同步公开联系邮箱口径。
- 不提交任何密钥、Token、cookie、私有证书或本地账号信息。

## 验证

```bash
make test
```
