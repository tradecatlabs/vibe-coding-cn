---
id: GOV-PROJECT-TOPOLOGY
type: index
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-13
review_cycle: P90D
---

# Project Topology

## 项目结构

| 路径 | 职责 | 禁止事项 | 主要验证 |
|---|---|---|---|
| `problem-library/` | 来源问题与 canonical Problem | 来源记录直接冒充规范化问题 | portable/full problem validation |
| `literature/` | Work/Edition/File 文献目录 | 上传本地电子书或推断未知权利 | portable/full literature validation |
| `research/` | Attempt 研究活动 | 把 lifecycle 完成当问题解决 | research spaces validation |
| `result-library/` | Result 真相源与解库派生视图 | 手写无 Result 支撑的解 | research spaces validation + negative tests |
| `.codex/skills/` | 项目 active 研究方法 | 直接激活未经审计上游 skill | project validation |
| `governance/standards/FORMAL-METHODS-MAP.md` | 规格、验证范式与 Lean 的方法层地图 | 将 Lean 等同于全部形式化方法 | governance strict/health + skill boundary checks |
| `governance/standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md` | Project → Workflow → Task → Step → Job 顶层生命周期语言 | 将 Job 成功等同于数学问题解决 | governance strict/health + public boundary checks |
| `vendor/` | 上游版本、许可、快照与缓存 | 让 upstream 参与 active discovery | supply-chain validation |
| `scripts/` | 抓取、查询和验证胶水 | 吞错或伪造成功 | `make check` / `make check-full` |
| `governance/` | 项目记忆、标准、ADR、Gate 和任务证据 | 替代局部 README/AGENTS | governance strict/health |
| `.github/workflows/` | 公开仓库 CI | 写权限、抓取或秘密依赖 | GitHub Actions + `make check` |

## 依赖方向

```text
external sources ──> source problem records ──> canonical Problem
literature catalog ────────────────────────────────┐
active skills ─────────────────────────────────────┤
method-layer map ──────────────────────────────────┤
Project → Workflow → Task → Step → Job ────────────┤
canonical Problem ──> Attempt ──> candidate Result ──> solutions.json
                                          │
                                   trusted verification gate
```

`solutions.json` 是只读派生视图。失败、局部结果与有限证据保留在 Attempt/Result 中，但不会进入完整解视图；Result 的数学状态由 `outcome × evidence` 表达。
