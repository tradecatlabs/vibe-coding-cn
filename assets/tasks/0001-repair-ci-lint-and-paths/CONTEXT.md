# CONTEXT — 迁移后 lint/路径问题图谱

## 现状追溯（Live Evidence）

### 1) CI markdownlint 配置缺失（硬失败）

- CI 命令（来自 `.github/workflows/ci.yml`）：  
  `markdownlint --config .github/lint_config.json '**/*.md'`
- 现场输出（本机复现）：

```text
Cannot read or parse config file '.github/lint_config.json': ENOENT: no such file or directory, open '.github/lint_config.json'
```

### 2) 本地 `make lint` 与 CI 不一致（假通过）

- `Makefile` 当前 lint 命令：`markdownlint **/*.md`
- 在 `/bin/sh -> dash` 下，`**/*.md` 只会匹配“单层目录的 md”，不会递归覆盖 `assets/**`。
- 结果：`make lint` 可能返回 0，但 CI 会真正 lint 全仓并失败。

### 3) 关键“操作指引”仍引用旧路径

- `assets/config/.codex/README.md` 仍要求复制 `config/.codex/...`（实际路径已迁到 `assets/config/.codex/...`）。
- `assets/skills/skills-skills/references/*.md` 示例仍写 `./skills/...`（实际应为 `./assets/skills/...`）。

### 4) 忽略规则偏差导致工作区污染

- `.gitignore` 仍忽略 `backups/gz/`（旧位置），但当前备份落在 `assets/repo/backups/gz/`。
- 现场信号：`git status` 出现 `?? assets/repo/backups/gz/`。

## 约束矩阵（从仓库 AGENTS.md/资产规范提取）

| 约束 | 来源 | 含义 |
|---|---|---|
| 不自动修改 `.github/workflows/*.yml` | 根 `AGENTS.md` | 优先“补配置/改命令”而不是改 CI 工作流 |
| 不删除或覆盖 `assets/repo/backups/gz/` 存档 | 根 `AGENTS.md` | 不清理现有 `.tar.gz`，只能通过 ignore/流程避免污染 |
| `assets/repo/` 第三方镜像少改动 | `assets/AGENTS.md` | 仅在影响入口/指引时做最小修改 |

## 风险量化表

| 风险点 | 严重程度 | 触发信号 (Signal) | 缓解方案 (Mitigation) |
| :--- | :--- | :--- | :--- |
| 通过“放宽 lint 配置”掩盖真实问题 | Medium | CI 绿但文档质量下降、后续难以收敛 | 配置要“最小放宽”，并在 PLAN 中记录哪些规则被禁用及原因 |
| 为了 lint 大规模重排文档引入链接/引用破坏 | High | lychee/link-checker 或手工打开出现断链 | 优先改配置与关键入口文档；如果必须改文档，限定范围并每步做 link/rg 校验 |
| 继续生成备份产物污染工作区 | Medium | `git status` 持续出现 `assets/repo/backups/gz/` | `.gitignore` 增加 `assets/repo/backups/gz/`，并在脚本说明中明确输出位置 |

## 假设与证伪（执行 Agent 必跑）

| 假设 | 默认假设 | 证伪命令 |
|---|---|---|
| CI 失败主因是缺 `.github/lint_config.json` | 是 | `ls -la .github/lint_config.json` |
| 修复 `.github/lint_config.json` 后仍会有 lint 违规 | 是（已见多条） | `markdownlint --config .github/lint_config.json '**/*.md'` |
| `make lint` 未覆盖 `assets/**` | 是 | `make -n lint` + 对比 `markdownlint '**/*.md'` 的输出范围 |

