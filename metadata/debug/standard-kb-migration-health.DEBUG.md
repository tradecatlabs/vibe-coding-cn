# Debug Record

## Bug

- 标题：标准知识库迁移后仓库健康度排查
- 症状：迁移后本地校验通过，但需要确认远端 CI、链接、子模块、旧路径和目录结构是否真实一致。
- 首次发现位置 / 时间：2026-05-02，迁移提交 `628a3bc` 与根目录降噪提交 `5caada8` 之后。

## Environment

- 仓库 / 模块：`tukuaiai/vibe-coding-cn`
- 当前分支：`develop`
- 当前 HEAD：`5caada8 chore: move ai citation pack under metadata`
- GitHub 默认分支：`develop`
- 远端分支：`develop`、`master`；未发现 `main`。
- 关键配置：`.github/workflows/ci.yml` 当前监听 `main`。

## Reproduction

1. 在 `develop` 执行本地仓库校验。
2. 查询 GitHub Actions 最近运行记录。
3. 查询仓库默认分支与远端分支。
4. 对照 `.github/workflows/ci.yml` 的触发条件。

## Observations

- O1：`make lint` 通过。
- O2：本地 Markdown 相对链接检查通过，范围为排除 `.history/`、`.github/wiki/`、`tools/external/`、`tools/chat-vault/`、`scripts/backups/gz/` 后的 263 个 Markdown 文件。
- O3：`git diff --check` 通过。
- O4：`git submodule status --recursive` 正常返回 `.tmux`、`Skill_Seekers-development`、`claude-official-skills`、`tmux` 及嵌套 `configs_repo`。
- O5：`find . -xtype l -print` 未发现断软链接。
- O6：旧路径扫描只命中 `CHANGELOG.md` 与 `metadata/redirects.yml`，属于迁移记录和重定向映射，不是活跃引用。
- O7：GitHub 默认分支是 `develop`。
- O8：远端存在 `develop` 与 `master`，没有 `main`。
- O9：`.github/workflows/ci.yml` 只监听 `push.branches: [ main ]` 和 `pull_request.branches: [ main ]`。
- O10：最近 `develop` 相关远端检查只有 `Labeler`，没有 `CI`。
- O11：历史 CI 最近记录来自 2026-02 的 `main` push，且 `markdown-lint` 失败；这不是当前 `develop` 迁移提交的验证结果。
- O12：修复 CI 触发分支后，`develop` 的 push / PR 均触发了 CI。
- O13：CI 的 `link-checker` 成功，`markdown-lint` 失败，失败原因是 Node.js 16 解析最新版 `markdownlint-cli` 依赖 `string-width` 中的正则 `/v` flag 报 `SyntaxError: Invalid regular expression flags`。

## Hypotheses

### H1: 迁移导致 Markdown 链接断裂

- Supports：大规模从 `assets/documents/` 移动到 `docs/`，容易留下旧相对路径。
- Conflicts：本地链接检查通过；旧路径扫描没有发现活跃旧路径引用。
- Test：运行本地 Markdown 相对链接检查。
- Verdict：rejected。

### H2: 迁移导致 submodule 或软链接断裂

- Supports：`assets/repos/` 拆分到 `tools/external/`，同时 Skills 中存在跨目录软链接。
- Conflicts：`git submodule status --recursive` 正常；`find . -xtype l -print` 无输出。
- Test：运行 submodule 状态检查与断软链接扫描。
- Verdict：rejected。

### H3: 远端 CI 没有覆盖当前默认分支

- Supports：GitHub 默认分支是 `develop`，远端没有 `main`，但 CI 只监听 `main`；最近 `develop` 只跑了 Labeler。
- Conflicts：无。
- Test：查询 `gh repo view --json defaultBranchRef`、`git ls-remote --heads origin master main develop`、`gh run list --workflow CI`、`.github/workflows/ci.yml`。
- Verdict：confirmed。

### H4: CI Node 版本过旧导致 markdownlint 运行时崩溃

- Supports：CI 日志显示 Node 16 环境下 `string-width/index.js` 的 `/v` 正则 flag 语法错误；本地 Node 环境运行 `make lint` 通过。
- Conflicts：无。
- Test：修复 CI 触发后查看失败日志。
- Verdict：confirmed。

## Experiments

### E1

- Hypothesis：H1 迁移导致 Markdown 链接断裂。
- Change：无生产改动，只运行链接检查脚本。
- Expected：如存在断链，输出缺失目标。
- Result：`OK local links checked: 263 files`。
- Verdict：rejected。
- Revert：无需。

### E2

- Hypothesis：H2 迁移导致 submodule 或软链接断裂。
- Change：无生产改动，只运行状态检查。
- Expected：如存在问题，`git submodule status` 出现异常或 `find . -xtype l` 输出断链。
- Result：submodule 正常；断软链接无输出。
- Verdict：rejected。
- Revert：无需。

### E3

- Hypothesis：H3 远端 CI 没有覆盖当前默认分支。
- Change：无生产改动，只查询远端和 workflow。
- Expected：如果成立，默认分支与 CI 触发分支不一致。
- Result：默认分支为 `develop`，远端无 `main`，CI 只监听 `main`。
- Verdict：confirmed。
- Revert：无需。

### E4

- Hypothesis：H4 CI Node 版本过旧导致 markdownlint 运行时崩溃。
- Change：查看 GitHub Actions 失败日志。
- Expected：如果成立，失败发生在工具启动阶段，而不是 Markdown 规则输出阶段。
- Result：`markdown-lint` job 在解析依赖时抛出 `SyntaxError: Invalid regular expression flags`；`link-checker` job 成功。
- Verdict：confirmed。
- Revert：无需。

## Root Cause

- 当前迁移后的本地结构健康，但远端质量门禁存在两层问题：
  1. 仓库默认分支是 `develop`，仍保留 `master`，不存在 `main`，而 CI workflow 原先只监听 `main`，导致当前默认开发流不会触发 `markdown-lint` 和 `link-checker`。
  2. CI 使用 Node.js 16 安装最新版 `markdownlint-cli`，其依赖已使用 Node 16 不支持的正则 `/v` flag，导致 `markdown-lint` 在工具启动阶段崩溃。

## Fix

- 已把 `.github/workflows/ci.yml` 触发分支改为当前真实分支策略：
  - `push.branches: [ develop, master ]`
  - `pull_request.branches: [ develop, master ]`
- 已同步更新 `AGENTS.md` 中 CI 触发规则，避免 Agent 继续相信 `main` 是主线。
- 已给 CI 增加 `workflow_dispatch`，方便手动验证迁移大改。
- 已把 CI Node.js 从 16 升级到 22，并同步 README / AGENTS 的 Node.js 环境要求。

## Regression Evidence

- 本地测试：`make lint` 通过。
- 本地链接：263 个 Markdown 文件相对链接检查通过。
- Git 检查：`git diff --check` 通过。
- 子模块检查：`git submodule status --recursive` 正常。
- 远端检查：`develop` 最新提交只有 Labeler，没有 CI；CI 分支触发条件与默认分支不一致。
- 修复后本地复测：`make lint`、本地 Markdown 相对链接检查、`git diff --check`、断软链接检查、submodule 状态检查均通过。
- 修复后需要再次 push 触发远端 CI，确认 `markdown-lint` 不再因 Node 16 崩溃。
