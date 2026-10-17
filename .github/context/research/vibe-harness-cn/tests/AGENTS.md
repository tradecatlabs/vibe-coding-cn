# tests 目录

`tests/` 保存行为回归输入，重点证明门禁会拒绝危险或不完整声明，而不只证明 happy path。

```text
tests/
├── AGENTS.md
├── __init__.py                              # 允许按模块路径运行标准库 unittest
├── test_sync_upstreams.sh                    # 验证 15 源精确登记、浅克隆同步与防覆盖
├── test_reference_operator_harness.py        # 验证 Runtime 闭环和失败关闭
├── test_verify_project.py                    # gate runner 的架构/回滚回归测试
└── fixtures/
    ├── invalid-missing-stop-condition.json                 # Harness 缺停止条件负例
    └── invalid-operator-runtime-missing-binding-id.json    # Runtime 缺 Binding 负例
```

测试依赖 `contracts/`、`operators/` 和 `scripts/`；测试数据不得包含真实凭据、私有客户数据或完整生产
prompt。manifest/Runtime 文件负例、Core Pack 宽松正例与 Reference Profile 内存负例由
`validate_harness.py --self-test` 执行，项目 gate 回归使用标准库 `unittest`；Git 同步回归使用 bash
与临时本地仓库，不增加测试框架依赖或网络依赖。
