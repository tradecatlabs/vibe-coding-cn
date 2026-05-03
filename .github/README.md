# .github

GitHub 平台配置目录，集中管理 CI、Issue 模板、PR 模板、安全政策、赞助配置和 Wiki 说明。

## 目录

- `workflows/` - GitHub Actions 工作流。
- `ISSUE_TEMPLATE/` - Issue 表单和模板。
- `PULL_REQUEST_TEMPLATE.md` - PR 描述模板。
- `SECURITY.md` - 安全报告入口。
- `WIKI.md` - Wiki 使用说明。
- `labeler.yml` - PR 自动标签规则。
- `lint_config.json` - Markdown lint 配置。

## 维护规则

- CI 变更必须能用本地命令复现核心检查。
- 外链检查规则集中放在 `.lychee.toml`。
- 不在此目录保存密钥、Token 或本地账号信息。
