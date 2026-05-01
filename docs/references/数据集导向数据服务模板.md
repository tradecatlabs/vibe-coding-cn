# 数据集导向数据服务模板

> 这份文档定义一套可复用的**数据采集服务通用架构模板**：以后新建数据服务，或把外部源码重构纳入本仓库时，优先按这套模板落地。

## 1) 一句话

- **以 dataset 为边界、以 schema/data contract 为先、以 runtime/registry/config 为共享控制面、以 collect/backfill/repair/validate 为实现单元。**

## 2) 适用范围

### 适合

- 行情事实采集服务
- 另类事件采集服务
- 周期轮询快照服务
- 原子事件流 + 时间桶聚合并存的数据服务
- 需要长期运行、补数、巡检、血缘、质量治理的数据产品服务

### 不适合直接照抄

- 纯 API 网关
- 纯 Web 应用
- 纯交易执行服务
- 一次性脚本工具
- 不产出稳定 dataset 的临时任务

> 判断规则：**如果服务的核心交付物是“稳定数据集”，而不是“页面”或“接口”，就优先用这套模板。**

## 3) 设计目标

- 让 **dataset** 成为开发、调度、部署、运维、血缘、权限、生命周期管理的统一边界
- 让 **schema / contract** 成为稳定真相源，而不是让采集代码反过来定义数据模型
- 让 **控制面**（config / registry / service_entry / runtime）统一收口，避免每个数据集各自长脚本
- 让 **legacy 兼容层** 明确可识别、可退役，而不是长期混在主链里

## 4) 核心原则

### 4.1 Dataset First

- 顶层先按 dataset 划分，而不是先按 `collector/ parser/ writer/ task` 划分
- 一个 dataset 对应一个清晰的数据交付对象
- 代码、存储、血缘、权限都围绕 dataset 收口

### 4.2 Schema / Contract First

- 先定义目标落表、字段语义、主键/幂等键、时间列、分区策略、刷新粒度
- 再写采集、解析、写入、校验、回补逻辑
- 不允许“先把代码跑起来，后面再猜表结构”

### 4.3 Layered Modeling

- 原子层和聚合层分开
- 事件流和时间桶分开
- 运行状态和资源存在性分开
- active / backfill_only / reserved 分开

### 4.4 Shared Control Plane

- `config.py`：统一配置入口
- `registry.py`：统一 dataset 真相矩阵
- `service_entry.py`：统一内部服务入口
- `runtime/*`：统一执行面
- 业务代码不允许自己重新发明第二套控制面

### 4.5 Legacy Is Explicit

- 过渡期允许保留 legacy 壳
- 但 legacy 壳只能做兼容转发
- 新逻辑不得回流 legacy 路径

## 5) 标准目录模板

```text
<service-root>/
├── README.md
├── AGENTS.md
├── pyproject.toml                 # 单工程时使用；多壳过渡期可暂时保留多个
├── scripts/
│   ├── start.sh                   # 薄壳：统一转发到 service_entry
│   ├── verify.sh                  # 服务级快速校验（可选）
│   └── check_legacy_shells.sh     # legacy 回流静态门禁（迁移期建议强制）
├── src/<service_name>/
│   ├── __init__.py
│   ├── config.py                  # 统一配置入口
│   ├── registry.py                # dataset 真相矩阵
│   ├── service_entry.py           # 统一内部入口：plan/start/stop/status/restart
│   ├── common/                    # 公共工具：env、io、time、symbols、shared utils
│   ├── runtime/                   # 统一执行层
│   │   ├── stack_runner.py
│   │   ├── process_utils.py
│   │   ├── <group>_runner.py
│   │   └── <group>_worker.py
│   ├── writers/                   # 统一写入层（可选，按需要抽）
│   ├── validators/                # 统一校验层（可选，按需要抽）
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
│           └── <future_dataset>/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
└── legacy/ or old-shells/         # 可选：迁移期显式归档
```

## 6) dataset 目录的标准职责

每个 dataset 目录不是“一个表一个文件”，而是**一个数据集一个实现单元**。

推荐最小结构：

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

### 每个文件干什么

- `contract.py`
  - 定义 dataset key、resource_id、物理表、主键/幂等键、时间语义、字段语义
- `collect.py`
  - 实时采集 / 轮询采集主逻辑
- `backfill.py`
  - 历史补数、文件回填、分页补齐
- `repair.py`
  - 缺口修复、异常恢复、局部重算
- `writer.py`
  - 统一落库 / 批量写入 / 去重 / 冲突处理
- `validate.py`
  - 数据质量检查、行数/字段/时间连续性校验
- `README.md`
  - 只说明这个 dataset 的输入、输出、约束与边界

> 如果某个 dataset 没有 `repair` 或 `backfill`，可以不实现，但必须在 registry 里显式标记为不支持，而不是偷偷缺省。

## 7) registry 统一真相矩阵

`registry.py` 至少应定义这些字段：

```text
dataset_key
resource_id
runtime_status        # active | backfill_only | reserved | disabled
physical_table
group                 # 例如 lf / hf / events / snapshots
source_kind           # ws / rest / zip / scrape / file / api
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

### 为什么 registry 必须存在

- 它是 dataset 清单的单一真相源
- 文档、运行、血缘、权限、门禁都应从这里派生
- 没有 registry，就会回到“代码里藏着很多隐式数据集”的旧问题

## 8) 命名规则

### 8.1 dataset 命名

推荐组合维度：

```text
<market>_<instrument>_<topic>_<granularity?>_<layer?>
```

例如：

- `spot_trades`
- `futures_um_trades`
- `futures_um_book_ticker`
- `futures_um_book_depth`
- `candles_1m`
- `futures_metrics_5m`
- `futures_um_metrics_atomic`

### 8.2 命名要求

- 名字必须表达**数据是什么**，不是代码怎么实现
- 尽量包含这些维度：
  - 市场类型：`spot` / `futures`
  - 合约类型：`um` / `cm`
  - 主题：`trades` / `book_ticker` / `book_depth` / `metrics`
  - 粒度：`1m` / `5m`
  - 层次：`atomic` / aggregate
- `_reserved/` 只用于预留未来命名空间，不用于临时垃圾存放

## 9) 统一控制面模板

### 9.1 service_entry

统一入口只做这几类动作：

- `plan`
- `start`
- `stop`
- `status`
- `restart`

它不直接写业务逻辑，只负责：

- 读取 config
- 读取 registry
- 调 runtime runner
- 输出当前运行真相

### 9.2 runtime

runtime 负责：

- 进程编排
- 模式分组（如 lf / hf / events / snapshots）
- PID / 日志 / 健康状态
- cold-start / restart / stop 行为一致性

业务代码不允许各自实现第二套守护逻辑。

## 10) 数据模型分层建议

推荐至少区分这几类：

```text
atomic            # 原子事件/原子明细
snapshot          # 单次轮询快照
bucketed          # 时间桶聚合结果
derived           # 从事实层再派生的结果
reserved          # 预留但未启用
```

### 两类典型模型

#### A. 事件流模型

适合：

- trades
- orderbook updates
- tick events
- message stream

特点：

- 高频
- append-only 倾向更强
- 更强调顺序、幂等、去重、水位线

#### B. 时间桶 / 快照模型

适合：

- candles_1m
- metrics_5m
- periodic snapshots
- polling APIs

特点：

- 按窗口/批次刷新
- 更强调覆盖、补齐、时间边界一致性

## 11) 从零新建服务的推荐流程

### Step 1：先定 dataset 清单

明确：

- 服务要产出哪些 dataset
- 每个 dataset 的物理表是什么
- 哪些是 active，哪些是 backfill_only，哪些是 reserved

### Step 2：先写 contract

每个 dataset 先写 `contract.py`，明确：

- 字段
- 主键/幂等键
- 时间列
- 分区策略
- 资源 ID
- schema version

### Step 3：再建 registry / config / service_entry / runtime

先把共享控制面搭起来，再实现具体 dataset。

### Step 4：逐个实现 dataset

每个 dataset 按：

```text
contract -> writer -> collect -> backfill -> validate -> repair
```

的顺序推进。

### Step 5：最后补文档与门禁

至少补：

- README
- AGENTS
- verify / CI
- 资源目录 / 血缘映射 / smoke

## 12) 从外部源码接入时的重构流程

很多外部源码不是按 dataset-first 设计的，通常是：

```text
collector/
parser/
writer/
scripts/
```

接入时不要直接原样搬进来。建议这样重构：

### Step 1：先做盘点，不先搬代码

盘点外部源码：

- 实际产出哪些数据对象
- 每个对象对应什么表/文件/消息
- 哪些逻辑是 collect，哪些是 backfill，哪些是 repair
- 哪些模块只是工具层

### Step 2：反向抽 dataset

把原项目里的功能点反向映射成 dataset：

```text
外部源码里的“多个脚本”
-> 抽象成若干 dataset
-> 为每个 dataset 建 contract / writer / collect / backfill
```

### Step 3：公共能力抽到 common/runtime/writers

例如：

- API client
- auth
- rate limiter
- symbol normalize
- storage client
- retry / backoff
- file downloader

这些不属于单一 dataset，应放共享层。

### Step 4：把 legacy 壳显式隔离

过渡期可以保留旧入口，但必须：

- 只做兼容转发
- 不再承载新逻辑
- 有门禁防止回流

## 13) 最低门禁模板

每个 dataset-first 服务至少要有这些门禁：

### 代码门禁

- `compileall` 覆盖服务新树
- 无语法错误
- 无关键路径未纳入版本控制

### 结构门禁

- 不允许新逻辑回流 legacy 壳
- 不允许第二套 start/status/restart 控制面
- registry 中的 dataset 必须与实际实现一致

### 运行门禁

- `stop -> start -> status -> restart -> status` 可通过
- 日志可证明真实执行源
- PID / log / run metadata 可追踪

### 数据门禁

- 每个 active dataset 至少有 contract + writer + collect/或 backfill
- 血缘 resource_id 与 registry 一致
- 质量检查最少覆盖：空写、重复写、时间边界、幂等

### 文档门禁

- README 更新
- AGENTS 更新
- 资源目录 / 当前真相文档更新

## 14) 反模式

以下情况不应接受：

- 顶层继续按 `collector/ parser/ writer` 组织，dataset 只是注释概念
- 没有 registry，dataset 清单散落在代码里
- 先写采集器，再倒推表结构
- runtime 到处复制，每个 dataset 都有自己一套守护脚本
- legacy 壳长期承担真实执行逻辑
- `_reserved` 被当成垃圾桶
- 同一 dataset 同时存在两套 writer / 两套 contract / 两套运行入口

## 15) 推荐的最小模板文件

如果以后你新建一个数据服务，最少应先建出这些文件：

```text
<service-root>/
├── README.md
├── AGENTS.md
├── scripts/start.sh
└── src/<service_name>/
    ├── config.py
    ├── registry.py
    ├── service_entry.py
    ├── runtime/
    │   ├── stack_runner.py
    │   └── process_utils.py
    └── datasets/
        ├── <dataset_a>/
        │   ├── contract.py
        │   ├── collect.py
        │   ├── writer.py
        │   └── README.md
        └── _reserved/
```

## 16) 仓库内参考实现

当前仓库里，最接近这套模板的落地参考是：

- `core/market/binance/src/binance/`
- `core/market/binance/src/binance/datasets/*`
- `core/market/binance/src/binance/registry.py`
- `core/market/binance/src/binance/service_entry.py`
- `core/market/binance/src/binance/runtime/*`

> 说明：这份模板不是说“以后每个服务都必须和 Binance 长得一模一样”，而是说：**以后凡是新的数据采集服务，都优先按这个方法组织，再根据数据源特性做局部裁剪。**

## 17) 一句话结论

- **这套模板可以作为你后续“数据采集服务”的通用源码架构模板。**
- 它的核心不是目录长什么样，而是：**先定义 dataset 与 contract，再围绕 dataset 实现 collect/backfill/repair/write/validate，并把 config/registry/runtime/service_entry 收敛成统一控制面。**
