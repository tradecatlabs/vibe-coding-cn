# SMT/LRA Fixture Agent Guide

本目录保存 SymPy 命题 SAT 与 QF-LRA theory solver 的固定反例样例，只证明有限 solver、精确 witness 与证据回执连接正确。

## 文件

```text
smt-lra/
├── AGENTS.md   # 能力天花板与维护规则
└── case.json   # 固定陈述、精确有理数 witness 与线性约束
```

## 边界

- 只允许命题逻辑与无量词线性实数算术；不得加入非线性、位向量、数组、字符串或量词后仍沿用当前 verifier 名称。
- fixture 的 SAT 结论只闭合本例的精确反例，不代表一般证明或完整搜索。
- 变更陈述、witness 或约束时必须同步 verifier output policy 与 statement-faithfulness 测试。
