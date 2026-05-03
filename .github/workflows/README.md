# .github/workflows

GitHub Actions 工作流目录。

## 当前工作流

- `ci.yml` - Markdown lint、本地链接、docs 结构、目录治理、metadata、AI citation 和外链检查。

## 维护规则

- 优先复用 `Makefile` 和 `scripts/` 中已有门禁。
- 外链检查排除规则放在 `.lychee.toml`。
- action 版本升级后必须观察远端 CI 结果。
