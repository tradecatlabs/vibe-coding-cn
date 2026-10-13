# Task-Level Acceptance

- `skills/` 落地 13 个 skill（11 Web3 + 2 合约审计），文件完整。
- `SKILLS_MANIFEST.json` 记录来源、commit、许可、审计引用。
- 未安装任何内容到全局 skills 目录。
- AGENTS/README 使用规则同步。

# Validation Plan

```bash
find skills -type f | wc -l          # 文件完整性
python3 -c "import json; json.load(open('skills/SKILLS_MANIFEST.json'))"
python3 <CODEX_SKILLS>/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0007-vendor-project-skills --phase closeout
python3 governance/tools/validate_governance_package.py --project-root . --strict
```

# Review Gate

- `PASS`：来源固定、许可记录、未装全局、文件完整。
- `WARN`：skill 内容质量未逐篇复核，使用前需抽查。
- `BLOCK`：发现未审计内容混入或 manifest 与文件不一致。

# Runtime Verification Gate

本任务不运行 skill 内容；运行时验证为 `vendoring-only`。

# Task Package Acceptance

- TP-01：范围仅审计通过项。
- TP-02：13 skill + manifest。
- TP-03：入口文档同步。
- TP-04：closeout 通过。

# Ship Readiness

只交付本地 vendored 目录与文档；不安装、不部署、不 push。

# Anti-Goals

- 不复制高敏感仓库（claude-pentest/communitytools/nc.exe）。
- 不执行 skill 内脚本。
