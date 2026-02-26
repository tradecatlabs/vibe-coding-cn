# TODO — 可执行清单（按 P0→P2）

> 格式：`[ ] Px: <动作> | Verify: <验证手段> | Gate: <准入>`

## P0（必须先做，阻塞 CI/开发体验）

- [x] P0: 应用补丁（落地修复） | Verify: `git apply --check assets/tasks/0001-repair-ci-lint-and-paths/patches/0001-fix-ci-lint-and-paths.patch` | Gate: 输出 `OK`
- [x] P0: 应用补丁（执行） | Verify: `git apply assets/tasks/0001-repair-ci-lint-and-paths/patches/0001-fix-ci-lint-and-paths.patch` | Gate: ExitCode=0
- [x] P0: 创建 `.github/lint_config.json`（最小放宽，保证可落地） | Verify: `cat .github/lint_config.json` | Gate: 文件存在且 JSON 可解析
- [x] P0: 让 `markdownlint --config .github/lint_config.json '**/*.md'` 退出 0 | Verify: `markdownlint --config .github/lint_config.json '**/*.md'` | Gate: ExitCode=0
- [x] P0: 对齐本地 `make lint` 与 CI（同 config + 同 glob） | Verify: `make lint` | Gate: ExitCode=0 且覆盖 `assets/**`
- [x] P0: 修复 `assets/config/.codex/README.md` 复制路径 | Verify: `rg -n "cp -f config/\\.codex" assets/config/.codex/README.md || true` | Gate: 无匹配
- [x] P0: 修复 `assets/skills/skills-skills/references/*.md` 旧示例路径 | Verify: `rg -n "\\./skills/skills-skills" assets/skills/skills-skills/references -S || true` | Gate: 无匹配

## P1（清理迁移遗留，减少未来误操作）

- [ ] P1: 更新 `.gitignore` 忽略 `assets/repo/backups/gz/` | Verify: `rg -n "^assets/repo/backups/gz/" .gitignore` | Gate: 有匹配
- [ ] P1: 更新 `.gitignore` 中旧路径 `skills/skills-skills/...` | Verify: `rg -n "skills/skills-skills/scripts/\\.venv-skill-seekers" .gitignore || true` | Gate: 旧条目移除或替换为 `assets/skills/...`
- [ ] P1: 决定是否将 lint 范围排除 `assets/repo/**`（第三方镜像） | Verify: `markdownlint --config .github/lint_config.json '**/*.md'` | Gate: 无需改动第三方大量文件也能通过

## P2（可选增强）

- [ ] P2: 为 lint/CI 策略写入“为什么这样配置”的注释/说明文档 | Verify: `rg -n "lint_config" -S README.md AGENTS.md .github/workflows/ci.yml` | Gate: 维护者能读懂规则与边界
- [ ] P2: 增加一个最小 smoke 校验脚本（可选） | Verify: `bash -lc '<script>'` | Gate: 一键复验不漏项

## 可并行（Parallelizable）

- P0 的“文档路径修复”与“gitignore 更新”可并行。
- `lint_config.json` 与 `Makefile` 对齐需串行（先定 config 再对齐命令）。
