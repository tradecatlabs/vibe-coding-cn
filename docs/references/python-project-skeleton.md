<a id="reference-engineering-practice-通用-python-项目骨架"></a>
# 通用 Python 项目骨架

适合大多数应用型项目、服务型项目、脚本工具项目，也可以轻微调整后用于 Python 库项目

---

#### Python 通用项目骨架说明文档

##### 1. 推荐目录结构示意图

```text
project/
├── src/
│   └── your_package/
│       ├── __init__.py
│       ├── main.py
│       ├── core/
│       │   ├── __init__.py
│       │   └── service.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       ├── utils/
│       │   ├── __init__.py
│       │   └── helpers.py
│       └── config.py
│
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_service.py
│   └── fixtures/
│       └── sample_data.json
│
├── scripts/
│   ├── dev.sh
│   ├── lint.sh
│   ├── test.sh
│   └── release.sh
│
├── config/
│   ├── default.toml
│   ├── development.toml
│   ├── production.toml
│   └── logging.yaml
│
├── docs/
│   ├── index.md
│   ├── architecture.md
│   ├── development.md
│   └── deployment.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .env.example
├── .gitignore
├── .python-version
├── AGENTS.md
├── Makefile
├── pyproject.toml
├── README.md
├── requirements.txt
├── requirements-dev.txt
└── requirements.lock.txt
```

---

##### 2. 本地生成目录，不应提交到 Git

这些文件或目录可以存在于项目根目录，但不属于仓库骨架的一部分：

```text
project/
├── .venv/
├── .env
├── .pytest_cache/
├── .ruff_cache/
├── __pycache__/
├── .coverage
├── htmlcov/
├── dist/
├── build/
└── *.egg-info/
```

它们应该写进 `.gitignore`。

---

##### 3. 各目录与文件说明

###### `src/`

项目源码目录。

推荐使用 `src` 布局，而不是把业务代码直接放在项目根目录。这样可以避免本地开发时错误导入根目录下的代码。

示例：

```text
src/
└── your_package/
    ├── __init__.py
    ├── main.py
    ├── core/
    ├── api/
    ├── models/
    └── utils/
```

其中：

| 路径              | 说明                    |
| --------------- | --------------------- |
| `your_package/` | 项目的主 Python 包名        |
| `main.py`       | 应用入口，可用于 CLI、服务启动或主流程 |
| `core/`         | 核心业务逻辑                |
| `api/`          | API 路由、接口层代码          |
| `models/`       | 数据模型、领域模型、ORM 模型      |
| `utils/`        | 工具函数、通用辅助模块           |
| `config.py`     | 配置读取与解析逻辑             |

---

###### `tests/`

测试目录。

```text
tests/
├── test_main.py
├── test_service.py
└── fixtures/
    └── sample_data.json
```

建议规则：

| 项      | 建议                   |
| ------ | -------------------- |
| 测试框架   | `pytest`             |
| 测试文件命名 | `test_*.py`          |
| 测试函数命名 | `test_*`             |
| 测试数据   | 放入 `tests/fixtures/` |
| 覆盖率    | 可使用 `pytest-cov`     |

---

###### `scripts/`

项目辅助脚本目录。

```text
scripts/
├── dev.sh
├── lint.sh
├── test.sh
└── release.sh
```

常见用途：

| 脚本           | 说明      |
| ------------ | ------- |
| `dev.sh`     | 启动开发环境  |
| `lint.sh`    | 执行代码检查  |
| `test.sh`    | 执行测试    |
| `release.sh` | 发布或打包流程 |

如果项目简单，也可以只用 `Makefile`，不一定需要 `scripts/`。

---

###### `config/`

配置文件目录。

```text
config/
├── default.toml
├── development.toml
├── production.toml
└── logging.yaml
```

注意：

| 文件             | 是否提交 | 说明     |
| -------------- | ---: | ------ |
| 默认配置           |    是 | 可以提交   |
| 环境模板配置         |    是 | 可以提交   |
| 密钥、Token、密码    |    否 | 不应提交   |
| `.env`         |    否 | 本地私密配置 |
| `.env.example` |    是 | 环境变量示例 |

---

###### `docs/`

项目文档目录。

```text
docs/
├── index.md
├── architecture.md
├── development.md
└── deployment.md
```

推荐至少包含：

| 文档                | 说明   |
| ----------------- | ---- |
| `index.md`        | 文档首页 |
| `architecture.md` | 架构说明 |
| `development.md`  | 开发说明 |
| `deployment.md`   | 部署说明 |

小项目可以只保留 `README.md`，不用单独建 `docs/`。

---

###### `.github/workflows/`

GitHub Actions 自动化目录。

```text
.github/
└── workflows/
    └── ci.yml
```

常见用途：

| 文件            | 说明           |
| ------------- | ------------ |
| `ci.yml`      | 自动测试、Lint、构建 |
| `release.yml` | 自动发布         |
| `docs.yml`    | 自动构建文档       |

如果项目不用 GitHub，可以没有这个目录。

---

##### 4. 根目录核心文件说明

###### `pyproject.toml`

现代 Python 项目的核心配置文件。

建议把这些工具配置集中放在里面：

```text
[project]
[build-system]
[tool.pytest.ini_options]
[tool.ruff]
[tool.mypy]
[tool.coverage]
```

它可以统一管理：

| 内容      | 说明                               |
| ------- | -------------------------------- |
| 项目元数据   | 名称、版本、作者、描述                      |
| 构建系统    | setuptools、hatchling、poetry、uv 等 |
| 依赖声明    | 运行依赖、可选依赖                        |
| 测试配置    | pytest                           |
| Lint 配置 | ruff                             |
| 类型检查    | mypy、pyright                     |
| 覆盖率配置   | coverage                         |

---

###### `requirements.txt`

运行依赖文件。

适合应用型项目，例如：

```text
fastapi
uvicorn
pydantic
requests
```

如果项目依赖已经完全放进 `pyproject.toml`，这个文件可以由工具导出，而不是手写维护。

---

###### `requirements-dev.txt`

开发依赖文件。

例如：

```text
pytest
pytest-cov
ruff
mypy
pre-commit
```

用于开发、测试、格式化、类型检查。

---

###### `requirements.lock.txt`

锁定依赖版本的文件。

例如：

```text
fastapi==0.115.0
uvicorn==0.30.6
pydantic==2.8.2
```

作用是保证不同机器、不同环境安装到一致的依赖版本。

如果使用 `uv`、`poetry`、`pdm` 等工具，也可以换成：

```text
uv.lock
poetry.lock
pdm.lock
pylock.toml
```

---

###### `.env.example`

环境变量模板。

应该提交到仓库。

示例：

```env
APP_ENV=development
APP_DEBUG=true
DATABASE_URL=postgresql://user:password@localhost:5432/app
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=change-me
```

注意：这里可以放假值、示例值，但不能放真实密钥。

---

###### `.env`

本地真实环境变量。

不应提交。

示例：

```env
APP_ENV=development
APP_DEBUG=true
DATABASE_URL=postgresql://real_user:real_password@localhost:5432/app
SECRET_KEY=real-secret
```

---

###### `.gitignore`

推荐内容：

```gitignore
#### Python cache
__pycache__/
*.py[cod]
*$py.class

#### Virtual environments
.venv/
venv/
env/

#### Environment variables
.env
.env.*
!.env.example

#### Test / coverage
.pytest_cache/
.coverage
htmlcov/

#### Ruff
.ruff_cache/

#### Build artifacts
build/
dist/
*.egg-info/

#### IDE
.vscode/
.idea/

#### OS files
.DS_Store
Thumbs.db

#### Logs
*.log
logs/
```

---

###### `.python-version`

用于声明项目推荐 Python 版本。

示例：

```text
3.12
```

适合团队统一 Python 版本，尤其是使用 `pyenv`、`uv` 等工具时。

---

###### `Makefile`

统一开发命令入口。

示例：

```makefile
.PHONY: install dev test lint format clean

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements-dev.txt

test:
	pytest

lint:
	ruff check src tests

format:
	ruff format src tests

clean:
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov dist build
```

这样团队成员可以直接执行：

```bash
make install
make dev
make test
make lint
make format
make clean
```

---

###### `README.md`

项目入口说明文档。

建议包含：

```text
#### Project Name

##### Introduction
项目简介。

##### Features
核心功能。

##### Requirements
运行要求。

##### Installation
安装方法。

##### Usage
使用方法。

##### Development
开发说明。

##### Testing
测试说明。

##### Deployment
部署说明。

##### License
许可证。
```

---

###### `AGENTS.md`

给 AI 编程助手、自动化代理或协作工具看的项目说明。

不是 Python 官方标准文件，但现在越来越常见。

建议内容包括：

```text
#### AGENTS.md

##### Project Overview
本项目的目标、技术栈、代码边界。

##### Coding Rules
代码风格、命名规范、禁止事项。

##### Test Commands
如何运行测试。

##### Lint Commands
如何运行代码检查。

##### Project Structure
目录说明。

##### Notes
开发注意事项。
```

---

##### 5. 推荐的最小可用版本

如果项目不复杂，可以使用这个精简版：

```text
project/
├── src/
│   └── your_package/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_main.py
├── .env.example
├── .gitignore
├── .python-version
├── Makefile
├── pyproject.toml
├── README.md
├── requirements.txt
└── requirements-dev.txt
```

这个版本适合：

| 类型          | 是否适合 |
| ----------- | ---: |
| 小型工具项目      |    是 |
| 内部脚本项目      |    是 |
| FastAPI 小服务 |    是 |
| 数据处理项目      |    是 |
| 命令行工具       |    是 |
| 大型平台项目      | 需要扩展 |

---

##### 6. 推荐的完整企业/团队版本

如果是团队协作、后端服务、AI 应用、数据平台或长期维护项目，推荐使用完整版本：

```text
project/
├── src/
│   └── your_package/
│       ├── __init__.py
│       ├── main.py
│       ├── core/
│       ├── api/
│       ├── models/
│       ├── services/
│       ├── repositories/
│       ├── schemas/
│       ├── utils/
│       └── config.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── scripts/
├── config/
├── docs/
├── .github/
│   └── workflows/
├── .env.example
├── .gitignore
├── .python-version
├── AGENTS.md
├── Makefile
├── pyproject.toml
├── README.md
├── requirements.txt
├── requirements-dev.txt
└── requirements.lock.txt
```

额外模块说明：

| 目录                   | 说明               |
| -------------------- | ---------------- |
| `services/`          | 应用服务层，组织业务流程     |
| `repositories/`      | 数据访问层，封装数据库、外部存储 |
| `schemas/`           | 请求、响应、校验模型       |
| `tests/unit/`        | 单元测试             |
| `tests/integration/` | 集成测试             |
| `.github/workflows/` | CI/CD 自动化        |

---

##### 7. 最终推荐原则

这套骨架遵循几个原则：

| 原则      | 说明                                |
| ------- | --------------------------------- |
| 源码隔离    | 业务代码统一放入 `src/`                   |
| 测试独立    | 测试代码统一放入 `tests/`                 |
| 配置分层    | 示例配置进仓库，真实密钥不进仓库                  |
| 工具集中    | 主要工具配置尽量放入 `pyproject.toml`       |
| 本地文件不提交 | `.venv/`、`.env`、缓存目录全部忽略          |
| 命令统一    | 用 `Makefile` 或脚本统一开发命令            |
| 文档随仓库维护 | `README.md` 负责入口说明，`docs/` 负责详细文档 |
| 可扩展     | 小项目可精简，大项目可扩展                     |

---

##### 8. 最终结论

这份项目骨架可以作为通用 Python 仓库模板：

```text
project/
├── src/
├── tests/
├── scripts/
├── config/
├── docs/
├── .github/
├── .env.example
├── .gitignore
├── .python-version
├── AGENTS.md
├── Makefile
├── pyproject.toml
├── README.md
├── requirements.txt
├── requirements-dev.txt
└── requirements.lock.txt
```

其中：

```text
.venv/
.env
.pytest_cache/
.ruff_cache/
__pycache__/
```

只属于本地环境，不应进入仓库。

这就是一个比较稳妥、通用、可维护的 Python 项目根目录设计。
