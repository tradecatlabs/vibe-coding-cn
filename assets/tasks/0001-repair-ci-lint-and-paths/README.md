# 0001 — repair-ci-lint-and-paths

本任务把“路径迁移后审计发现的阻塞项”收敛为一组可执行修复：让 CI 可跑通、让本地 `make lint` 与 CI 一致、并清理会误导执行的旧路径指引。

## In Scope

- 修复 CI `markdown-lint` 阶段的硬错误（缺失 `.github/lint_config.json`）。
- 修复本地 `make lint` 的“假通过”（使其覆盖 `assets/**` 深层 Markdown，并与 CI 使用同一套 glob/配置）。
- 修复迁移后仍会误导执行的旧路径指引（以“仓库自有文档”为主，第三方镜像按最小原则处理）：
  - `assets/config/.codex/README.md` 的复制路径。
  - `assets/skills/skills-skills/references/*.md` 的示例路径（`skills/...` → `assets/skills/...`）。
- 修复忽略规则偏差（`.gitignore`）以匹配新结构：
  - 忽略 `assets/repo/backups/gz/`（避免审计/备份产物污染工作区）。
  - 更新旧路径忽略项 `skills/skills-skills/...` → `assets/skills/...`（如仍需要）。

## Out of Scope

- 不做“全仓 Markdown 大规模重排/格式化”（除非为让 lint 过关的最小改动）。
- 不对 `assets/repo/` 下第三方镜像/子模块做“顺手修文档/批量替换”，除非它直接影响本仓库的入口可运行性与操作指引。
- 不修改 `.github/workflows/*.yml`（优先通过补齐/修复配置文件与命令一致性解决）。

## 执行顺序（必须按此阅读/执行）

1. `CONTEXT.md`：现状证据、约束、风险与假设
2. `ACCEPTANCE.md`：验收标准（执行前先确认目标）
3. `PLAN.md`：方案对比、决策与回滚协议
4. `TODO.md`：按 P0→P2 执行，每步必须跑 Verify
5. `STATUS.md`：执行中持续记录证据与状态

