# Lean Proof Fixture

本目录用固定 Lean/Mathlib 构建一个无逃逸的最小定理，并输出 `#print axioms` 供证据层审计。

```text
lean-proof/
├── AGENTS.md
├── README.md
├── lean-toolchain
├── lakefile.toml
├── lake-manifest.json
└── VibeMathingFixture.lean
```

- `lean-toolchain` 固定 Lean 版本；`lakefile.toml` 固定直接依赖，`lake-manifest.json` 锁定全部传递依赖。
- `VibeMathingFixture.lean` 是唯一形式化陈述真相源。
- `.lake/` 是可重建缓存，不属于 fixture 事实。
