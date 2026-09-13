# SMT/LRA bounded fixture

这是无业务数据的合成 fixture，用于测试 `scripts/vibe_mathing/smt.py` 的有限 SAT/UNSAT、精确 witness、timeout 和错误回执边界。

- `case.json` 固定一个 QF_LRA 风格的有限输入和预期结果。
- `AGENTS.md` 规定 adapter、输出预算和不得晋升 Result 的边界。
- 测试只使用本地合成输入，不访问网络、不写 `research/` 或 `result-library/`。

运行：

```bash
python3 scripts/test_smt_pipeline.py
```

fixture 通过只表示 adapter 的 bounded 行为可复现；它不证明任意线性实数命题，也不构成数学 Result。
