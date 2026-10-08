<a id="reference-engineering-practice-7-dataset-first-数据服务结构"></a>
# Dataset First 数据服务结构

适合长期运行、补数、巡检、血缘、质量治理的数据产品服务。

判断规则：

> 如果服务的核心交付物是“稳定数据集”，而不是页面、接口或一次性脚本，就优先使用 Dataset First。

<a id="reference-engineering-practice-一句话"></a>
##### 一句话

以 dataset 为边界，以 schema/data contract 为先，以 runtime/registry/config 为共享控制面，以 collect/backfill/repair/validate 为实现单元。

<a id="reference-engineering-practice-适合"></a>
##### 适合

- 行情事实采集服务。
- 另类事件采集服务。
- 周期轮询快照服务。
- 原子事件流 + 时间桶聚合并存的数据服务。
- 需要长期运行、补数、巡检、血缘、质量治理的数据服务。

<a id="reference-engineering-practice-不适合直接照抄"></a>
##### 不适合直接照抄

- 纯 API 网关。
- 纯 Web 应用。
- 纯交易执行服务。
- 一次性脚本工具。
- 不产出稳定 dataset 的临时任务。

<a id="reference-engineering-practice-核心原则"></a>
##### 核心原则

1. Dataset First：顶层先按 dataset 划分，而不是按 `collector/parser/writer/task` 划分。
2. Contract First：先定义目标落表、字段语义、主键、时间列、分区策略和刷新粒度。
3. Layered Modeling：原子层、聚合层、事件流、时间桶、运行状态分开建模。
4. Shared Control Plane：`config.py`、`registry.py`、`service_entry.py`、`runtime/*` 统一收口。
5. Legacy Is Explicit：迁移期 legacy 壳只能兼容转发，新逻辑不得回流旧路径。

<a id="reference-engineering-practice-标准目录"></a>
##### 标准目录

```text
service-root/
├── README.md
├── AGENTS.md
├── pyproject.toml
├── scripts/
│   ├── start.sh
│   ├── verify.sh
│   └── check_legacy_shells.sh
├── src/<service_name>/
│   ├── __init__.py
│   ├── config.py
│   ├── registry.py
│   ├── service_entry.py
│   ├── common/
│   ├── runtime/
│   │   ├── stack_runner.py
│   │   ├── process_utils.py
│   │   ├── <group>_runner.py
│   │   └── <group>_worker.py
│   ├── writers/
│   ├── validators/
│   └── datasets/
│       ├── <dataset_a>/
│       │   ├── contract.py
│       │   ├── collect.py
│       │   ├── backfill.py
│       │   ├── repair.py
│       │   ├── writer.py
│       │   ├── validate.py
│       │   └── README.md
│       ├── <dataset_b>/
│       └── _reserved/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
└── legacy/ or old-shells/
```

<a id="reference-engineering-practice-dataset-最小结构"></a>
##### Dataset 最小结构

```text
<dataset>/
├── contract.py
├── collect.py
├── backfill.py
├── repair.py
├── writer.py
├── validate.py
└── README.md
```

职责边界：

- `contract.py`：定义 dataset key、resource_id、物理表、主键、幂等键、时间语义、字段语义。
- `collect.py`：实时采集或轮询采集主逻辑。
- `backfill.py`：历史补数、文件回填、分页补齐。
- `repair.py`：缺口修复、异常恢复、局部重算。
- `writer.py`：统一落库、批量写入、去重、冲突处理。
- `validate.py`：数据质量检查、行数、字段、时间连续性校验。
- `README.md`：说明该 dataset 的输入、输出、约束与边界。

如果某个 dataset 没有 `repair` 或 `backfill`，必须在 registry 中显式标记为不支持。

<a id="reference-engineering-practice-registry-真相矩阵"></a>
##### Registry 真相矩阵

`registry.py` 至少应定义：

```text
dataset_key
resource_id
runtime_status        # active | backfill_only | reserved | disabled
physical_table
group                 # lf | hf | events | snapshots
source_kind           # ws | rest | zip | scrape | file | api
collect_supported
backfill_supported
repair_supported
default_enabled
owner
```

推荐额外字段：

```text
symbol_scope
refresh_granularity
retention_policy
partition_key
schema_version
sensitivity
```

Registry 的作用：

- 它是 dataset 清单的单一真相源。
- 文档、运行、血缘、权限、门禁都应从 registry 派生。
- 没有 registry，就会回到“数据集藏在脚本里”的旧问题。

<a id="reference-engineering-practice-dataset-命名"></a>
##### Dataset 命名

推荐格式：

```text
<market>_<instrument>_<topic>_<granularity?>_<layer?>
```

示例：

- `spot_trades`
- `futures_um_trades`
- `futures_um_book_ticker`
- `futures_um_book_depth`
- `candles_1m`
- `futures_metrics_5m`
- `futures_um_metrics_atomic`

命名要求：

- 名字必须表达数据是什么，而不是代码怎么实现。
- `_reserved/` 只用于预留未来命名空间，不用于临时文件。
- 事件流、快照、时间桶、派生结果要在命名或 contract 中显式表达。

<a id="reference-engineering-practice-service-entry-与-runtime"></a>
##### Service Entry 与 Runtime

`service_entry.py` 统一入口只做：

- `plan`
- `start`
- `stop`
- `status`
- `restart`

它不直接写业务逻辑，只负责读取 config、读取 registry、调用 runtime runner、输出运行真相。

`runtime/` 负责：

- 进程编排。
- 模式分组。
- PID、日志、健康状态。
- cold-start、restart、stop 行为一致性。

业务代码不允许各自实现第二套守护逻辑。

<a id="reference-engineering-practice-数据模型分层"></a>
##### 数据模型分层

推荐区分：

```text
atomic            # 原子事件/原子明细
snapshot          # 单次轮询快照
bucketed          # 时间桶聚合结果
derived           # 从事实层再派生的结果
reserved          # 预留但未启用
```

事件流模型适合 trades、orderbook updates、tick events、message stream，重点是顺序、幂等、去重、水位线。

时间桶 / 快照模型适合 candles、metrics、periodic snapshots、polling APIs，重点是覆盖、补齐、时间边界一致性。

<a id="reference-engineering-practice-新建数据服务流程"></a>
##### 新建数据服务流程

1. 先定 dataset 清单：哪些 active、哪些 backfill_only、哪些 reserved。
2. 先写 contract：字段、主键、时间列、分区策略、资源 ID、schema version。
3. 再建 registry、config、service_entry、runtime。
4. 逐个实现 dataset：`contract -> writer -> collect -> backfill -> validate -> repair`。
5. 最后补 README、AGENTS、verify/CI、资源目录、血缘映射、smoke。

<a id="reference-engineering-practice-外部源码接入流程"></a>
##### 外部源码接入流程

1. 先盘点外部源码实际产出的数据对象，不先搬代码。
2. 把原项目脚本反向映射为 dataset。
3. 将 API client、auth、rate limiter、storage client、retry/backoff 抽到 `common/`、`runtime/` 或 `writers/`。
4. 将 legacy 壳显式隔离，只允许兼容转发，不允许承载新逻辑。
