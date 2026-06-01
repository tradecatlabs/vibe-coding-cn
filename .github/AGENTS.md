# .github/ Agent 指南

本目录承载 GitHub 平台自动化与协作配置。

说明：本目录不放 `README.md`，避免 GitHub 仓库首页误展示平台配置说明；目录规则只保留在 `AGENTS.md`。

## 结构

```text
.github/
├── AGENTS.md                 # GitHub 平台配置目录规则
├── CODEOWNERS                # 路径级 owner 评审基线
├── FUNDING.yml               # GitHub Sponsors / 赞助入口
├── ISSUE_TEMPLATE/           # Issue 模板和配置
├── PULL_REQUEST_TEMPLATE.md  # PR 模板
├── SECURITY.md               # 安全漏洞报告策略
├── WIKI.md                   # GitHub Wiki 独立仓库说明
├── labeler.yml               # PR 标签规则
├── lint_config.json          # markdownlint 配置
└── workflows/                # GitHub Actions 工作流
```

## 约束

- 修改 `CODEOWNERS` 会影响 GitHub 的 owner review 触发范围，必须同步检查关键路径是否仍有明确 owner。
- 修改 `workflows/` 前必须确认对应本地命令或验证方式。
- 修改 Issue / PR 模板时保持字段简洁、可执行、可审查。
- 修改安全政策时同步公开联系邮箱口径。
- 不提交任何密钥、Token、cookie、私有证书或本地账号信息。

## 职责边界

- `CODEOWNERS` 是路径级审查入口，不替代分支保护、必需检查和人工维护者判断。
- `lint_config.json` 只定义 Markdown lint 规则，不承载业务文档标准。
- `workflows/` 只放 GitHub Actions 编排；本地可复现命令应优先放在 `Makefile` 或 `scripts/`。
- Issue / PR 模板只收集协作上下文，不承载长期项目知识；长期规则应回到 `AGENTS.md`、`docs/` 或治理文档。

## 验证

```bash
make test
```
