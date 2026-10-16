# .github/workflows

GitHub Actions 工作流目录。

## 当前工作流

- `ci.yml` - 在 `main` 的 push / pull_request 上执行 Markdown lint、本地链接、docs 结构、目录治理、metadata、AI citation 和外链检查。
- `welcome.yml` - 在 Issue / PR opened 时欢迎首次贡献者；`actions/first-interaction@v3` 的输入使用
  `repo_token`、`issue_message`、`pr_message`，令牌由 GitHub Actions 原生 secret 注入。
