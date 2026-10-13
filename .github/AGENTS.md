# `.github/` Agent 指南

本目录既承载 GitHub 平台配置，也集中存放仓库的知识、工具和自动化内容。仓库首页仍由根目录 `README.md` 负责；本目录不放 `README.md`，避免覆盖 GitHub 的首页展示。

## 结构

```text
.github/
├── AGENTS.md                 # 本文件：目录职责、路径约定与平台边界
├── assets/                   # 静态资产、外部资源注册表与 AI 引用语料
├── docs/                     # 入门教程与功法正文
├── metadata/                 # 机器可读登记、分类、重定向和生成目录
├── prompts/                  # 提示词库入口
├── research/                 # 研究对象、来源事实和冻结材料
├── scripts/                  # 本地检查、目录生成与数据维护脚本
├── skills/                   # 可复用技能库
├── tools/                    # 工具、配置与外部依赖
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

## 路径约定

- 从仓库根目录引用迁入的目录时，使用 `.github/<目录>/...`，例如 `.github/docs/`、`.github/scripts/` 和 `.github/tools/`。
- 迁入目录内部的 Markdown 相对链接、包内相对路径和软链接保持相对关系；不要重复添加 `.github/`。
- 八个目录的职责与子目录规则由各自的 `AGENTS.md` 管理；本文件只规定共同边界和 GitHub 平台配置约定。
- `.github/workflows/`、`.github/ISSUE_TEMPLATE/`、`CODEOWNERS` 等 GitHub 识别的固定入口必须保留其平台要求的路径。

## 约束

- 修改 `CODEOWNERS` 会影响 GitHub 的 owner review 触发范围；必须确认根配置与迁入目录均由当前维护者覆盖。当前维护者为 `@tukuaiai` 和 `@tradecatlabs`。
- 修改 `workflows/` 前先确认对应本地命令和验证方式；只为保持现有检查在新路径下运行而更新路径，不借机改变 CI 触发条件或检查范围。
- 修改 Issue / PR 模板时保持字段简洁、可执行、可审查。
- 修改安全政策时同步公开联系邮箱口径。
- 不提交任何密钥、Token、cookie、私有证书或本地账号信息。
- 外部仓库仍由 `.github/tools/external/` 中的 submodule 指针固定；不得将本地缓存或运行产物混入来源快照。

## 职责边界

- `CODEOWNERS` 是路径级审查入口，不替代分支保护、必需检查和人工维护者判断；PR 作者不能用自己的账号完成自审。
- `lint_config.json` 只定义 Markdown lint 规则，不承载业务文档标准。
- `workflows/` 只放 GitHub Actions 编排；本地可复现命令由根 `Makefile` 调用 `.github/scripts/` 中的脚本。
- Issue / PR 模板只收集协作上下文，不承载长期项目知识；长期规则由根 `AGENTS.md`、`.github/docs/` 或治理文档维护。

## 验证

从仓库根目录执行：

```bash
make lint
make check-links
make check-directory-docs
```
