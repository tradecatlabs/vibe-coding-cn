# Reference Operator Harness

这是共享 Operator Runtime 契约的最小消费方。它以确定性规则从 468 条目录中选择一个算子，读取
Harness 本地 Binding，将算子展开为 instruction packet，再由独立验证阶段重算选择、展开结果和摘要。

```bash
uv run --locked --script scripts/validate_harness.py --operator-runtime \
  examples/reference_harness/requests/definition-first.json \
  examples/reference_harness/bindings/instruction-packet.json
python3 examples/reference_harness/reference_harness.py \
  --request examples/reference_harness/requests/definition-first.json \
  --binding examples/reference_harness/bindings/instruction-packet.json
```

输出是 `OperatorRunBundle`：`record` 可按公共 Runtime Core 交换，`instruction_packet` 是该参考 Harness
的本地产物。`completed/accepted` 仅说明指令物化符合契约，绝不表示问题已解决或方法有效。

实现固定为 `effect_scope=none`、无模型、无工具、无外部写入。Selector 对目录做一次 `O(n)` 扫描；
Method 递归展开受 `max_steps` 约束，未知引用、循环、策略不匹配和摘要篡改都失败关闭。
参考运行模块只重复检查执行所需的安全不变量；完整字段形状由前置 Core 校验器负责，避免在两个实现中复制 Schema。
