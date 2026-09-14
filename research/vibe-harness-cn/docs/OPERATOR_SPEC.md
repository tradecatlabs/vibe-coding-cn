# Problem-Solving Operator Specification

本规范定义 Harness 可交换的问题求解思维模型、原子算子和组合方法。设计原则只有一句：

> 公共契约严格约束机器形状和安全边界，不替作者决定方法内容。

字段级机器真相源是
[`contracts/problem-solving-operator-pack.schema.json`](../contracts/problem-solving-operator-pack.schema.json)。
本文解释哪些约束属于公共 Core Contract，哪些只能由特定 Profile、评测或运行时策略加严。

## 1. 分层

```text
Operator Pack
├── Core Contract             跨 Harness 的最小交换格式
├── Conformance Profile       某类库、组织或场景的额外准入规则
├── Evaluation                方法是否有效、稳定、值得晋升
└── Harness Runtime Policy    权限、预算、工具、执行和结果裁决
```

- Core Contract 回答“机器能否稳定解析”。
- Profile 回答“是否符合某个明确场景的准入要求”。
- Evaluation 回答“方法是否真的有效”。
- Runtime Policy 回答“这次是否允许执行”。

四层不得互相冒充。尤其不能因为当前参考库有五十六个领域、411 个来源条目和固定写法，就把这些
本地事实写成所有 Harness 必须遵守的公共标准。

## 2. Core Contract

### 2.1 必需结构

Pack 必须包含：

- `api_version`：解析哪个契约版本。
- `kind`：固定为 `OperatorPack`。
- `metadata`：至少包含稳定 `id`、语义 `version` 和开放的 `domain` 标识。
- `entries`：条目数组，可以为空。

每个条目必须包含：

- `id`、`version`：稳定机器身份与语义版本。
- `kind`：`MentalModelSpec`、`OperatorSpec` 或 `MethodSpec`。
- `origin`：稳定来源类别；推荐 `source` 或 `derived`，其中 `source` 还必须有 `source_key`。
- `name`、`domain`、`status`：最小发现与生命周期字段。
- `semantics`：与 `kind` 对应的结构对象；允许在 `draft` 阶段为空。

Core 只校验已出现字段的类型和结构，不强制：

- 领域必须来自固定枚举；
- 中英文名称必须成对出现；
- 必须填写摘要、核心问题、适用/不适用场景；
- 必须有固定数量的步骤、结果、证据、失败或恢复项；
- 必须使用某种 prompt、模型、tool、skill 或 workflow；
- 方法已经有效、安全或可投入生产。

### 2.2 三种条目

| `kind` | 含义 | Core 结构 |
|---|---|---|
| `MentalModelSpec` | 提供观察、解释或提问视角 | `semantics` 可包含 `questions`、`interpretation_rules`、`limitations` |
| `OperatorSpec` | 描述一次问题求解动作 | `semantics` 可包含前置、输入、过程、效果、结果、证据、失败与恢复 |
| `MethodSpec` | 组合指令、Mental Model、Operator 或其他 Method | `semantics.steps` 中每步只能选择 `instruction`、`use`、`apply_model` 之一 |

`MentalModelSpec` 不能声明 `effect` 等动作字段。`OperatorSpec` 和 `MethodSpec` 可以在草稿期省略
内容字段，但在进入实际执行前，应由目标 Profile 或 Harness policy 要求足够完整的执行语义。

### 2.3 开放词汇

`domain` 和 effect/outcome 等可扩展词汇只要求稳定标识符格式，不由 Core 封闭枚举。以下值是
推荐的公共词汇，不是穷尽集合：

- effect state：`world_state`、`knowledge_state`、`governance_state`；
- outcome：`succeeded`、`failed`、`inconclusive`、`not_applicable`、`blocked`、
  `budget_exhausted`、`cancelled`；
- lifecycle：`draft`、`experimental`、`verified`、`deprecated`、`retired`。

生命周期值保持封闭，是因为它直接参与装载与晋升判断；扩展生命周期应通过新契约版本或 Profile
映射完成，不能让两个 Harness 对同一状态各自解释。

## 3. 推荐内容，不作 Core 硬门槛

成熟条目通常应该提供：

- `summary`、`core_question`、`operation`、`agent_use`；
- `applicability.when` 与 `applicability.not_when`；
- `source_refs` 与可追溯来源；
- Operator 的 preconditions、inputs、procedure、effect、outcomes、evidence、failure、recovery；
- Method 的 steps、stop conditions、success conditions、evidence 和 failure modes；
- 风险、权限 owner、结果 owner 与敏感值处理声明。

这些内容通过作者指南、lint、Profile、review 和 eval 渐进加严。Core 不用“字段齐全”冒充“方法正确”。

## 4. 扩展规则

所有稳定对象都拒绝未知同级字段，防止 `summmary` 之类拼写错误静默通过。公共规范尚未覆盖的内容
放入 `extensions` 对象：

```json
{
  "extensions": {
    "example.org": {
      "selector_hint": "cheap-first"
    }
  }
}
```

扩展键应该使用组织控制的命名空间。扩展不得：

- 改写标准字段含义；
- 授权工具、批准高风险动作或自证 outcome；
- 成为 Core conformance 的隐藏前提；
- 内联凭据、完整私有 prompt、客户数据或不受控工具结果。

多个真实消费者反复需要同一扩展时，再提议将其晋升为标准字段；一次性需求不扩大公共契约。

## 5. 安全不变量

内容宽松不等于执行宽松：

- Pack 是数据，不是可执行代码；装载定义不能自动触发工具或模型调用。
- Operator 可以声明风险和所需 capability，不能授予自身权限。
- 省略 `governance` 表示“由 Harness 使用默认策略裁决”，不表示允许。
- `permission_decision` 若出现只能是 `harness_policy`；`outcome_decision` 若出现只能是 `verifier`；
  `sensitive_values` 若出现只能是 `reference_only`。
- 本地文件引用必须留在声明的库/项目范围内。
- `use` 与 `apply_model` 的引用类型、全局引用解析和 Method 无环性由装载 catalog 的 Profile 检查。
- `verified` 只是生命周期声明；真实晋升必须有版本绑定的 conformance、eval 和 review 证据。

## 6. 母领域与功能分类

参考库把“方法从哪里来”和“方法在问题求解中做什么”拆成两条轴：

- `source_domain` 是开放词汇，表示数学、计算机科学、统计、工程等母领域出处；它不是运行时能力等级。
- `functional_class` 是本项目的八类工作性视图：`representation`、`decomposition`、`transformation`、
  `search`、`construction`、`verification-falsification`、`diagnosis-revision`、`control-metacognition`。
- 分类保存在 [`operators/taxonomy/problem-solving-methodology.json`](../operators/taxonomy/problem-solving-methodology.json)，
  可用 `extensions.vibe-harness-cn` 表达，不改变 Core 字段含义，也不授予权限。
- 一个条目只选一个主功能类，可附交叉类；没有显式映射时按来源域默认值解析。映射是项目推断，不能冒充母学科官方分类。

## 7. Reference Library Profile

本仓库 `operators/catalog.json` 声明
`vibe-harness-cn/reference-library-v1` Profile。它在 Core 之上额外要求：

- 五十六个 pack 对独立 inventory 精确覆盖 411 个 source 条目；
- 57 个 derived 条目全部为 `MethodSpec`；
- pack、domain、来源、名称、计数和 ID 与 inventory/catalog 一致；
- entry ID、source key、来源引用全局唯一或可解析；
- Method 步骤连续、引用类型正确且图无环；
- 当前参考内容填写完整的说明、适用性、governance 和对应 kind 的语义字段；
- 路径不逃逸，权限、结果和敏感值 owner 不被内容作者改写。

这是 Vibe Harness CN 参考库的发布规则，不是第三方 Operator Pack 的公共入场券。

## 8. Operator Runtime Core

[`contracts/operator-runtime.schema.json`](../contracts/operator-runtime.schema.json) 固定三个跨 Harness
可交换对象：

| 对象 | 固定什么 | 不固定什么 |
|---|---|---|
| `OperatorBinding` | 所属 Harness、支持的 Operator 契约/Profile、执行模式、效果范围和策略上限 | prompt 模板、SDK、模型、工具或 workflow 实现 |
| `OperatorRunRequest` | Binding 引用、开放 problem 状态、选择条件、预算和所需效果范围 | 领域问题字段、选择算法或 Planner |
| `OperatorRunRecord` | 选中项、候选摘要、物化/验证结果、claim scope 和 provenance 摘要 | 完整 prompt、工具参数/结果、业务状态或方法有效性结论 |

Runtime Core 沿用“结构严格、语义宽松”：稳定对象拒绝未知同级字段，私有内容进入 `extensions`；
`problem` 保持开放。Binding 只能缩小 Harness policy，不能授权自身；Executor 只提供物化产物和候选
证据，Verifier 必须从原始输入重算后给出 verdict。`instruction_materialization_only` 明确表示通过
只覆盖指令物化，不覆盖真实问题求解。

`examples/reference_harness/` 是第一个协议消费样例，不是中央 Runtime。它固定无模型、无工具、
无外部写入，用确定性 `O(n)` 目录扫描和 `max_steps` 展开证明三种 Spec 可装载；第二个独立 Harness
Binding 与真实效果评估仍是互操作 MVP 的剩余门禁。

## 9. 验证入口

校验单个 Core Pack：

```bash
uv run --locked --script scripts/validate_harness.py \
  --operator-pack contracts/examples/minimal-operator-pack.json
```

校验本仓库 Reference Library Profile：

```bash
uv run --locked --script scripts/validate_harness.py \
  --operator-library operators/catalog.json
```

校验 Runtime Core 对象：

```bash
uv run --locked --script scripts/validate_harness.py --operator-runtime \
  contracts/examples/minimal-operator-binding.json \
  contracts/examples/minimal-operator-run-request.json \
  contracts/examples/minimal-operator-run-record.json
```

运行参考 Harness 行为回归：

```bash
python3 -m unittest tests.test_reference_operator_harness
```

运行正反例回归：

```bash
uv run --locked --script scripts/validate_harness.py --self-test
```

## 10. 契约演进

- 放宽可选内容不会破坏既有消费者，现有 `v1alpha1` pack 可继续使用。
- 删除/重命名必需字段、改变字段类型或改变既有词汇含义属于破坏性变化，必须升级 `api_version`。
- Profile 独立版本化；升级 Profile 不能静默改变 Core Contract。
- 新 Profile 只有在出现明确消费方、准入目标和验证样本后才创建。

当前实现不证明 Operator 有效，也不提供通用 planner、生产 Binding 或真实模型/工具执行。它提供
可交换格式、参考库离线准入证据，以及一个无副作用的 Selector/Binding/Materialize/Verify/Trace
协议证明。
