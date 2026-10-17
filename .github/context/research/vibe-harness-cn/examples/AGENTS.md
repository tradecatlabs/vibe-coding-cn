# examples 目录

`examples/` 保存协议的可运行参考消费方，用来证明契约能被具体 Harness 实现；它不是元 Harness 的中央运行时。

```text
examples/
├── AGENTS.md
└── reference_harness/
    ├── AGENTS.md
    ├── README.md
    ├── reference_harness.py
    ├── bindings/instruction-packet.json
    └── requests/definition-first.json
```

上游是 `contracts/` 与 `operators/`；下游只有本地示例和 `tests/`。参考实现不得调用模型、执行工具、
访问网络或持有生产状态；新增真实 Harness 适配器时应进入对应 Harness 仓库，而不是继续扩张本目录。
