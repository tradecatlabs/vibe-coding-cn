# SymPy Counterexample Fixture

本目录保存可通过统一 CLI 注册和运行的确定性 Problem Contract；它证明系统闭环，不进入真实开放问题库。

```text
sympy-counterexample/
├── AGENTS.md
├── README.md
└── problem.json
```

- `problem.json` 是固定全称命题；adapter 用精确有理数 `1/2` 生成并复算反例。
- 修改陈述必须同步 `pipeline.py` 的 Problem Contract、faithfulness policy 与 E2E 测试。
