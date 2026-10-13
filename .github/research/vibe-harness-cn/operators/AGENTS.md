# operators 目录

`operators/` 是 Harness 内问题求解能力的供应商中立内容库；它保存方法语义，不执行方法。

```text
operators/
├── AGENTS.md                  # 本模块架构与维护规则
├── README.md                  # 内容、类型、边界和验证入口
├── catalog.json               # Reference Library Profile、pack 注册、声明计数与全库不变量
├── source-inventory.json      # 用户扩展 411 项的独立验收清单与来源索引
├── taxonomy/                  # 母领域来源与八类功能的双轴分类视图
└── packs/                     # 五十六个领域内容包，共 411 个 source + 57 个 derived 条目
```

## 依赖与职责

```text
用户清单与参考来源 -> source-inventory.json
contracts/problem-solving-operator-pack.schema.json -> packs/*.json
source-inventory.json + catalog.json + packs/*.json -> validate_operator_library.py
operators/ -> 未来具体 Harness 的本地 Library/Binding
```

- `source-inventory.json` 独立于 pack，防止作者通过同步删除清单和内容来掩盖漏项。
- `catalog.json` 显式声明本仓库 Reference Library Profile，并登记本地 pack、计数和不变量；不保存运行态选择或执行结果。
- `packs/` 保存 `MentalModelSpec`、`OperatorSpec`、`MethodSpec`；来源项必须有 `source_key`，派生项
  必须明确标记 `derived`。
- `taxonomy/` 只保存 source domain 与 functional class 的交叉索引；母领域是方法出处，八类功能是问题空间动作视角，二者不得混成一个分类轴。
- Core 字段结构由 `contracts/` 拥有；本仓库内容完整性和引用检查属于 Reference Profile，由
  `scripts/` 执行；本目录不得把五十六个领域或 411+57 计数提升为公共契约。
- 条目不能授权工具、批准自身结果、内联秘密或冒充外部标准的完整实现。

新增、删除或重分类原始条目时，必须同步 inventory、pack、声明计数、文档和负例，并执行：

```bash
uv run --locked --script scripts/validate_harness.py --self-test
```

破坏性语义变化必须升级条目版本；未完成真实 Harness Binding 和 eval 前，状态不得从
`experimental` 晋升为 `verified`。
