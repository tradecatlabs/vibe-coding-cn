# Lean/Mathlib 最小验证样例

该 fixture 证明三件事：固定工具链可构建、定理无 `sorry/admit/unsafe`、`#print axioms` 输出可审计。它不证明任何开放数学问题，也不替代陈述忠实性审查。

项目 adapter 从 `PATH` 查找 `lean`，并兼容 elan 官方默认安装目录 `~/.elan/bin`；它从固定 `lake-manifest.json` 构造最小 `LEAN_PATH`，再以 `-j1` 和有界资源运行 Lean。缺少固定依赖缓存时 fail-closed。手工准备缓存时不要执行会移动依赖版本的 `lake update`。

```bash
lake exe cache get
lake --quiet build
lake env lean -j1 VibeMathingFixture.lean
lake env lean -j1 AxiomAudit.lean
```
