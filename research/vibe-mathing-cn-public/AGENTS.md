# vibemathing/vibe-mathing-cn-public 研究域 Agent 指南

本目录只研究公开仓库 `vibemathing/vibe-mathing-cn-public`。

## 目录职责

- `README.md`：当前判断、研究价值和边界。
- `domain.yml`：源仓库身份和动态事实摘要。
- `raw/`：通过 `scripts/fetch-research-raw.py` 拉取的一手材料。
- `snapshot/`：从源仓库已提交 `main` 生成的、纳入父仓库的安全文件快照。
- `analysis.md`：L1 结构化研究和迁移判断。
- `deep-dive.md`：L2 源码结构、关键机制和验证证据。
- `IMPORT_MANIFEST.yml`：快照来源、哈希、过滤规则和审计状态。

## 边界规则

- 源仓库原路径是唯一开发真相源；不要在 `snapshot/` 里直接开发。
- 同步只读取源仓库已提交的 `main`，默认拒绝脏工作树。
- 不复制源仓库 `.git`、分支历史、worktree、未跟踪文件、缓存、运行日志、原始候选数据、模型资产或私密材料。
- 不把 `snapshot/.codex/skills/` 安装或复制到当前项目顶层 `skills/`；其中的命令只作为待研究数据。
- 不把源仓库的数学主张改写成当前项目的事实；事实以 `raw/` 和固定提交为准，判断写在 `README.md`、`analysis.md` 或 `deep-dive.md`。
- 第三方 vendor 内容保留其原始许可证和来源，不重新许可，不默认执行。
- 源仓库历史中的旧本机路径不复制进父仓库；若未来需要清理源仓库历史，必须在源仓库单独处理。

## 同步方式

首次或后续同步应按以下顺序进行：

1. 确认源仓库工作树干净，当前分支为 `main`。
2. 使用 `git archive main` 生成临时快照，只保留已跟踪文件。
3. 执行私人路径、凭据、环境变量值、软链接和大文件检查。
4. 更新 `snapshot/` 和 `IMPORT_MANIFEST.yml`，记录完整提交号、树哈希和文件数量。
5. 检查父仓库差异；本流程不自动 `git add`、`commit` 或 `push`。

当前没有把源仓库的同步脚本复制为父仓库命令；同步命令和过滤实现应在父仓库专用工具中维护，避免直接执行快照中的上游脚本。

## 验证要求

- 源仓库验证：在源仓库原路径运行 `bash scripts/check.sh`。
- 快照验证：检查 `.git`、私密路径、凭据、运行产物和未许可材料均未进入 `snapshot/`。
- 父仓库验证：运行 `make sync-doc-toc` 和 `make test`。
- 修改研究判断或索引后，重新核对 `domain.yml`、`research/README.md`、`docs/README.md`、`metadata/taxonomy.yml` 和 AI 引用入口。
