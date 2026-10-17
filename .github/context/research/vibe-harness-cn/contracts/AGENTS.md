# contracts 目录

`contracts/` 是受管 harness 声明结构的单一真相源。Schema 只表达跨实现稳定的治理边界，
不得塞入某个模型供应商或 agent 框架的私有运行状态。

```text
contracts/
├── AGENTS.md
├── harness-manifest.schema.json          # Harness v1alpha1 结构契约
├── operator-runtime.schema.json          # Binding、RunRequest 与 RunRecord 互操作信封
├── problem-solving-operator-pack.schema.json # 思维模型、原子算子与组合方法契约
└── examples/
    ├── minimal-coding-harness.json        # 最小有效 Harness 声明
    ├── minimal-operator-pack.json         # 最小宽松 Core Operator Pack
    ├── minimal-operator-binding.json      # 最小 Harness 本地 Binding
    ├── minimal-operator-run-request.json  # 最小运行请求
    └── minimal-operator-run-record.json   # 最小摘要化运行记录
```

上游是 `docs/HARNESS_MODEL.md`、PSOA PRD 与 ADR；下游是 `operators/`、参考 Harness 和验证脚本。
Operator Pack Core 只约束稳定字段形状、类型判别、显式扩展和不可省略的安全边界；内容完整度由
Profile、review 与 eval 加严。Runtime Core 只约束 Binding/请求/记录的稳定信封，开放 problem 与
extensions，不规定选择算法或具体执行器。字段变化必须同步正例、负例与版本策略，破坏性变化不得静默复用旧 `api_version`。

存在性：三份 Schema、正例和负例由当前准入验证直接消费；最低阶梯是成熟 JSON Schema 加薄策略，
验证入口为 `uv run --locked --script scripts/validate_harness.py --self-test`。第二个真实 Harness 出现前不提取 Binding SDK。
