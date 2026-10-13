# operators/taxonomy 目录

`taxonomy/` 保存算子内容的分类视图，不复制算子语义，也不承担运行时 selector、planner 或权限决策。

```text
taxonomy/
├── AGENTS.md
└── problem-solving-methodology.json  # 母领域 × 八类功能的双轴交叉索引
```

`source_domain` 表示方法从哪里来；`functional_class` 表示它主要改变问题空间的哪一部分。算子包是
语义真相源，`source-inventory.json` 是来源覆盖真相源，本目录只提供可审计的分类映射和解析规则。
映射可以是项目推断，不能被解释为母学科官方分类；若映射与条目扩展同时存在，显式 override 只用于
分类审计，不改变 Core Contract。

修改分类轴、默认映射或解析规则时，必须同步更新 `operators/README.md`、`operators/AGENTS.md`、
`docs/OPERATOR_SPEC.md` 和对应治理 ADR，并运行算子库与治理 strict 校验。
