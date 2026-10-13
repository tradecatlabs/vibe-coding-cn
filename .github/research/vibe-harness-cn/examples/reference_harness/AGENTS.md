# reference_harness 目录

本目录是一份最小、无副作用的 Operator Runtime 协议证明。

```text
reference_harness/
├── AGENTS.md                         # 本地职责与边界
├── README.md                         # 运行方式和声明范围
├── reference_harness.py              # Select/Bind/Materialize/Verify/Trace
├── bindings/instruction-packet.json  # Harness 本地 Binding 与策略上限
└── requests/definition-first.json    # 可重跑请求
```

- `reference_harness.py` 只把静态算子物化为 instruction packet，不解决原问题、不执行任何 instruction。
- `bindings/` 由这个 Harness 本地拥有；它只能缩小能力，不能覆盖算子或上层 Harness policy。
- `requests/` 只放公开、无敏感信息的演示输入；运行记录仅保留摘要和元数据。
- 生产能力、远端状态、模型和工具接入均不属于本目录。
