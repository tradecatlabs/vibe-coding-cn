# Project Codex Guide

本目录只保存 Vibe Mathing 的项目级 Codex 配置。它不反向修改用户级 `$CODEX_HOME/skills`，也不直接激活 `vendor/upstream/` 中的第三方 skills。

## 目录结构

```text
.codex/
├── AGENTS.md
└── skills/
    ├── vibe-mathing-router/
    ├── math-discovery/
    ├── math-derivation/
    ├── math-computation/
    ├── math-proof/
    └── math-formalization/
```

## 依赖方向

```text
vibe-mathing-router
  -> exactly one owner skill

math-discovery -> math-derivation | math-proof
math-derivation -> math-computation | math-proof
math-computation -> evidence only
math-proof -> math-formalization when available
math-formalization -> Lean kernel evidence

CandidateObservation -> math-discovery only
surveyed/source_locked tool -> no runtime route
```

每个 skill 必须包含 `SKILL.md`、`VERSION`、`CHANGELOG.md` 和来源/压力测试参考。禁止把上游安装器、全局配置写入器、旧 MCP 名称或隐含私有 workspace 直接复制进 active skill。

问题库候选只能产生 discovery shortlist，始终 `research_eligible=false`；没有 active ProblemContract 时不得启动研究计算、证明、形式化或 Result 晋升。工具族的公开能力边界见 `governance/control-plane/math-tool-maturity.v1.json` 与 `governance/tools/MATH_TOOL_CATALOG.md`。
