# Verification Fixtures Agent Guide

本目录保存可重复、无外部业务数据的验证样例；fixture 只证明工具链和信任边界，不进入真实问题库。

## 目录结构

```text
fixtures/
├── AGENTS.md
├── lean-proof/                # 固定 Lean/Mathlib 的最小 kernel 垂直链
├── smt-lra/                   # 有界 SMT/LRA adapter 与攻击样例
└── sympy-counterexample/      # 可经 CLI 注册的确定性反例 Problem
```

## 边界

- 上游：官方 Lean、Mathlib 固定版本。
- 下游：`scripts/vibe_mathing/lean.py`、`scripts/vibe_mathing/smt.py` 及对应测试。
- 禁止 `sorry`、`admit`、`unsafe`；变更定理陈述时必须同步陈述忠实性契约和 axiom audit。
- fixture 不得引用本机绝对路径、凭据、私有材料或网络动态内容；fixture PASS 不得创建 Problem、Attempt、Result 或 Solution。
