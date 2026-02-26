# ACCEPTANCE — 精密验收标准

## 原子断言（Atomic Assertions）

### A1. CI markdownlint 不再硬失败

- Verify：
  - `test -f .github/lint_config.json`
  - `markdownlint --config .github/lint_config.json '**/*.md'`
- Expected：
  - 不再出现 `Cannot read or parse config file '.github/lint_config.json': ENOENT`
  - 命令退出码为 0

### A2. 本地 `make lint` 与 CI 行为一致

- Verify：
  - `make lint`
  - `markdownlint --config .github/lint_config.json '**/*.md'`
- Expected：
  - 两者 lint 的覆盖范围一致（至少包含 `assets/documents/**`、`assets/skills/**` 等深层 Markdown）
  - 退出码一致（都为 0）

### A3. 关键入口指引不再引用旧路径（最小集）

- Verify：
  - `rg -n "cp -f config/\\.codex" assets/config/.codex/README.md`
  - `rg -n "\\./skills/skills-skills" assets/skills/skills-skills/references -S`
- Expected：
  - 上述 grep/rg 均无匹配（或仅在“明确标注为历史示例”的段落中出现，并有解释）

### A4. 忽略规则与新结构一致

- Verify：
  - `rg -n "^assets/repo/backups/gz/" .gitignore`（或等价忽略规则）
  - `git status --porcelain=v1`
- Expected：
  - `.gitignore` 能覆盖 `assets/repo/backups/gz/`
  - `git status` 不再因为该目录出现未跟踪噪音（除非用户明确想纳入版本控制）

## 边缘路径（Edge Cases，至少 3 个）

1. 在没有启用 `globstar` 的 `/bin/sh` 环境下执行 `make lint` 仍能递归 lint（通过“引用 glob 交给 markdownlint”解决）。
2. `assets/repo/` 下第三方镜像的 Markdown 仍然存在违规时，lint 策略不会逼迫去改第三方大量文件（通过 `ignorePatterns` 或限定 lint 范围解决，需在 PLAN 明确选择）。
3. 新增任意 `assets/documents/**.md` 后，`make lint` 必定能扫到（通过新增一个临时 md 文件自测，或用 `markdownlint --debug` 验证匹配）。

## 禁止性准则（Anti-Goals）

- 不以“删除大段内容/关闭整个 lint”来换 CI 绿。
- 不修改 `.github/workflows/*.yml`（除非证明仅靠配置文件无法修复，且得到明确授权）。

