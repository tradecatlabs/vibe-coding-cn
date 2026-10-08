<a id="reference-engineering-practice"></a>

# 工程实践

> 项目架构、代码组织、开发经验、质量门禁与常见坑。

<a id="reference-engineering-practice-核心摘要"></a>
### 核心摘要

工程实践的核心目标是把“AI 可能写对”变成“系统必须可验证”：任务开始前写清目标、边界和验收标准；实现过程中用拼好码优先复用成熟方案；交付前用测试、CI、脚本、类型、schema、检查清单和代码审查形成硬门禁。

本文件适合作为开发者和 Agent 的工程约束手册：遇到架构设计、代码组织、质量门禁、常见坑、环境问题、Git 操作和项目维护时，优先在这里查规则和检查项。

<a id="reference-engineering-practice-顶部导航"></a>
### 顶部导航

| 主题 | 用途 |
|:---|:---|
| [项目架构模板](#1-项目架构模板) | 判断目录、模块、边界和职责是否清楚 |
| [代码组织](code-organization.md) | 检查命名、分层、依赖、状态和可维护性 |
| [开发经验](development-experience.md) | 沉淀任务推进、协作、复盘和交付经验 |
| [AI 编程质量门禁与常见坑](quality-gates-and-pitfalls.md) | 把验收标准转成测试、CI、脚本、类型、schema 或清单 |
| [底层程序逻辑设计与工程优化项](low-level-program-logic.md) | 用运行、并发、数据、性能和可观测模型约束实现 |

<a id="reference-engineering-practice-使用方式"></a>
### 使用方式

- 新项目从「项目架构模板」开始，先确定目录、边界、门禁和检查清单。
- 写代码前看「代码组织」与「开发经验」，统一命名、结构、职责和迭代方式。
- 做实现、重构或性能排查前看「底层程序逻辑设计与工程优化项」，用运行模型、并发模型、数据模型和性能模型约束方案。
- 使用 AI 编程时看「AI 编程质量门禁与常见坑」，把自然语言验收标准落到测试、CI、脚本、类型、schema 或检查清单。
- 遇到问题时优先按本文档中的门禁和常见坑排查，不要直接进入盲目重写。

<a id="reference-engineering-practice-目录"></a>
### 目录

- [1. 项目架构模板](#1-项目架构模板)
- [2. 代码组织](code-organization.md)
- [3. 开发经验](development-experience.md)
- [4. AI 编程质量门禁与常见坑](quality-gates-and-pitfalls.md)
- [5. 底层程序逻辑设计与工程优化项](low-level-program-logic.md)

<a id="reference-engineering-practice-1-项目架构模板"></a>

### 1. 项目架构模板

<a id="reference-engineering-practice-1-使用原则"></a>
#### 1. 使用原则

项目架构不是先追求“高级感”，而是先回答这些问题：

- 代码放哪里。
- 模块怎么分工。
- 数据怎么流动。
- 依赖怎么隔离。
- 如何测试、部署、回滚和维护。

默认顺序：

1. 先确定交付物：页面、API、数据集、CLI、服务还是组合系统。
2. 再确定边界：模块边界、数据边界、运行边界、外部依赖边界。
3. 再确定目录：目录只服务于边界，不反过来制造复杂度。
4. 最后补门禁：测试、lint、schema、配置示例、README、AGENTS。

<a id="reference-engineering-practice-2-快速选型"></a>
#### 2. 快速选型

| 项目类型 | 推荐模板 |
| --- | --- |
| Python 应用 / 服务 / 脚本工具 / 库项目 | 通用 Python 项目骨架 |
| Web API / 后端服务 | Python Web/API 项目结构 |
| 数据分析 / 量化 / 机器学习 | 数据科学项目结构 |
| 多服务 / 大型系统 | Monorepo 项目结构 |
| 中大型工程组织 / 平台工程 / 多产品线 | 企业级 Monorepo / Multi-repo 项目架构标准模板 |
| 前后端一体项目 | Full-Stack Web 应用结构 |
| 长期运行的数据采集服务 | Dataset First 数据服务结构 |

<a id="reference-engineering-practice-3-python-webapi-项目结构"></a>
#### 3. Python Web/API 项目结构

适合 Flask、FastAPI、RESTful API、Web 后端服务。

```text
project/
├── README.md
├── AGENTS.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .env.example
├── .gitignore
├── docs/
│   ├── api.md
│   ├── architecture.md
│   └── development.md
├── scripts/
│   ├── deploy.sh
│   ├── backup.sh
│   └── init_db.sh
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── src/
│   ├── main.py
│   ├── app.py
│   ├── config.py
│   ├── api/
│   │   ├── v1/
│   │   └── dependencies.py
│   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── data/
│   │   ├── repository/
│   │   └── migrations/
│   └── external/
│       ├── clients/
│       └── integrations/
├── data/                 # 不提交，或只提交 README/.gitkeep
└── logs/                 # 不提交，或只提交 README/.gitkeep
```

关键边界：

- `api/` 只处理协议、路由、参数校验和响应格式。
- `core/services/` 承载业务逻辑。
- `data/repository/` 隔离数据库访问。
- `external/` 隔离第三方 API、SDK 和平台依赖。
- `.env` 不提交，必须提供 `.env.example`。

<a id="reference-engineering-practice-4-数据科学-量化项目结构"></a>
#### 4. 数据科学 / 量化项目结构

适合量化交易、机器学习、数据分析、AI 研究。

```text
project/
├── README.md
├── AGENTS.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .env.example
├── .gitignore
├── docs/
│   ├── notebooks/
│   └── reports/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
├── scripts/
│   ├── collect_data.py
│   ├── train_model.py
│   ├── backtest.py
│   └── deploy_model.py
├── tests/
│   ├── test_data/
│   └── test_models/
├── configs/
│   ├── model.yaml
│   ├── database.yaml
│   └── trading.yaml
├── src/
│   ├── data/
│   │   ├── collectors/
│   │   ├── processors/
│   │   ├── features/
│   │   └── loaders.py
│   ├── models/
│   │   ├── strategies/
│   │   ├── backtest/
│   │   └── risk/
│   ├── core/
│   │   ├── config.py
│   │   ├── signals.py
│   │   └── portfolio.py
│   └── utils/
│       ├── logging.py
│       ├── database.py
│       └── api_client.py
├── data/                 # 不提交大数据文件
├── models/               # 不提交大模型/大 checkpoint
└── logs/
```

关键边界：

- Notebook 用于探索，不作为长期生产入口。
- `scripts/` 是薄入口，核心逻辑应在 `src/`。
- 数据、模型、日志默认不进 Git，除非是小型示例或 fixture。
- 回测、训练、采集、部署脚本必须能复现关键参数。

<a id="reference-engineering-practice-5-monorepo-项目结构"></a>
#### 5. Monorepo 项目结构

适合多服务架构、大型项目、团队协作。

```text
project-monorepo/
├── README.md
├── AGENTS.md
├── LICENSE
├── .gitignore
├── .gitmodules
├── docker-compose.yml
├── docs/
│   ├── architecture.md
│   └── deployment.md
├── scripts/
│   ├── build_all.sh
│   ├── test_all.sh
│   └── deploy.sh
├── services/
│   ├── user-service/
│   │   ├── Dockerfile
│   │   ├── pyproject.toml
│   │   ├── src/
│   │   └── tests/
│   ├── trading-service/
│   └── data-service/
├── packages/
│   ├── common/
│   └── contracts/
├── infrastructure/
│   ├── terraform/
│   ├── kubernetes/
│   └── nginx/
└── monitoring/
    ├── prometheus/
    ├── grafana/
    └── alertmanager/
```

关键边界：

- 每个 `services/*` 应能独立构建、测试和部署。
- 公共能力放 `packages/`，不要让服务之间互相直接 import 私有实现。
- `contracts/` 存 API schema、事件 schema、数据契约，作为跨服务真相源。
- 顶层脚本只做编排，不隐藏服务内部逻辑。

<a id="reference-engineering-practice-6-full-stack-web-应用结构"></a>
#### 6. Full-Stack Web 应用结构

适合 SPA、前后端分离项目、轻量产品原型。

```text
project/
├── README.md
├── AGENTS.md
├── LICENSE
├── .gitignore
├── docker-compose.yml
├── docs/
│   ├── architecture.md
│   └── deployment.md
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── store/
│       └── utils/
└── backend/
    ├── Dockerfile
    ├── pyproject.toml
    ├── src/
    │   ├── api/
    │   ├── core/
    │   └── models/
    └── tests/
```

关键边界：

- 前端状态管理不要直接绑定后端数据库结构。
- 后端 API contract 应有 schema 或类型定义。
- 前后端共享类型时，优先从 OpenAPI、JSON Schema 或生成工具派生。

<a id="reference-engineering-practice-8-架构设计原则"></a>
#### 8. 架构设计原则

<a id="reference-engineering-practice-关注点分离"></a>
##### 关注点分离

```text
API -> Service -> Repository -> Database / External System
```

上层可以调用下层，下层不能反向依赖上层。

<a id="reference-engineering-practice-可测试性"></a>
##### 可测试性

- 每个模块可独立测试。
- 外部依赖可 mock。
- 核心业务逻辑不依赖 CLI、HTTP、数据库连接对象。

<a id="reference-engineering-practice-可配置性"></a>
##### 可配置性

```text
环境变量 > 配置文件 > 默认值
```

配置与代码分离，敏感配置不得提交。

<a id="reference-engineering-practice-可维护性"></a>
##### 可维护性

- 文件名表达职责。
- 目录边界表达模块边界。
- 业务逻辑、平台适配、第三方依赖隔离。

<a id="reference-engineering-practice-版本控制友好"></a>
##### 版本控制友好

- `data/`、`logs/`、`models/` 默认加入 `.gitignore`。
- 大文件不进 Git，必要时使用对象存储、Release、DVC 或外部数据源。
- 提交源代码、配置示例、文档、测试和小型 fixture。

<a id="reference-engineering-practice-9-最低门禁"></a>
#### 9. 最低门禁

<a id="reference-engineering-practice-代码门禁"></a>
##### 代码门禁

- 语法检查通过。
- 单元测试覆盖核心业务。
- lint/format 有明确命令。
- 关键路径纳入版本控制。

<a id="reference-engineering-practice-结构门禁"></a>
##### 结构门禁

- 不允许临时脚本成为长期入口。
- 不允许同一职责存在多套实现入口。
- 不允许外部 SDK 类型污染核心业务模型。
- 数据服务不允许新逻辑回流 legacy 壳。

<a id="reference-engineering-practice-运行门禁"></a>
##### 运行门禁

- 服务能按 README 启动。
- `stop -> start -> status -> restart -> status` 可验证。
- 日志能证明真实执行源。
- PID、log、run metadata 可追踪。

<a id="reference-engineering-practice-数据门禁"></a>
##### 数据门禁

- 每个 active dataset 至少有 contract + writer + collect 或 backfill。
- resource_id 与 registry 一致。
- 质量检查至少覆盖空写、重复写、时间边界、幂等。

<a id="reference-engineering-practice-文档门禁"></a>
##### 文档门禁

- README 说明项目定位、安装、启动、测试和目录结构。
- AGENTS 说明 AI Agent 修改边界、验证命令和禁止事项。
- `.env.example` 说明必要配置。
- 架构变化同步更新文档。

<a id="reference-engineering-practice-10-gitignore-推荐模板"></a>
#### 10. `.gitignore` 推荐模板

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# Environment
.env
.venv/
env/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Data
data/
*.csv
*.db
*.sqlite
*.duckdb

# Logs
logs/
*.log

# Models
models/
*.h5
*.pkl
*.pt
*.onnx

# Temporary
tmp/
temp/
*.tmp
```

<a id="reference-engineering-practice-11-技术选型参考"></a>
#### 11. 技术选型参考

| 场景 | 推荐技术栈 |
| --- | --- |
| Web API | FastAPI + Pydantic + SQLAlchemy |
| 数据处理 | Pandas + NumPy + Polars |
| 机器学习 | Scikit-learn + XGBoost + LightGBM |
| 深度学习 | PyTorch / TensorFlow |
| 数据库 | PostgreSQL + Redis |
| 消息队列 | RabbitMQ / Kafka |
| 任务队列 | Celery |
| 监控 | Prometheus + Grafana |
| 部署 | Docker + Docker Compose |
| CI/CD | GitHub Actions / GitLab CI |

<a id="reference-engineering-practice-12-新项目检查清单"></a>
#### 12. 新项目检查清单

- [ ] 创建 `README.md`，说明项目目标、安装、启动、测试。
- [ ] 创建 `AGENTS.md`，说明 AI Agent 操作边界与必须验证命令。
- [ ] 创建 `LICENSE`。
- [ ] 创建 `.gitignore`。
- [ ] 创建 `.env.example`。
- [ ] 建立虚拟环境或包管理配置。
- [ ] 明确目录结构。
- [ ] 明确配置入口。
- [ ] 设置 lint/format/test 命令。
- [ ] 编写第一个测试用例。
- [ ] 记录架构决策和后续 TODO。

<a id="reference-engineering-practice-13-常见反模式"></a>
#### 13. 常见反模式

- 一开始就做微服务。
- 所有代码写在一个文件。
- 架构追求高级感，而不是可维护。
- 没想清楚数据流就开始写。
- 目录按技术名堆砌，但没有业务边界。
- 业务逻辑直接依赖第三方 SDK。
- 临时脚本长期成为生产入口。
- 数据服务没有 registry，dataset 清单散落在脚本里。
- 先写采集器，再倒推表结构。
- 每个 dataset 各自实现 start/status/restart。

<a id="reference-engineering-practice-14-一句话结论"></a>
#### 14. 一句话结论

项目架构的目标不是把目录做复杂，而是让职责、数据流、依赖和验证路径清楚。普通项目先选通用结构；稳定数据服务优先采用 Dataset First，用 contract、registry、runtime 和质量门禁固定长期演进边界。
