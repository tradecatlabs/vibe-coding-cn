# datawhalechina/vibe-vibe 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`datawhalechina/vibe-vibe`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、README 快照和本地仓库工作树。
- 观察日期：2026-07-03。

## L2 结论

`datawhalechina/vibe-vibe` 是面向零基础用户的系统教程仓库。它的核心不是工具实现，而是把
Vibe Coding 解释成基础篇、进阶篇、实践篇和优质文章篇四层学习路径，并通过 VitePress、demo
项目、Docker 部署和 PWA/SEO 配置把教程做成可访问、可部署、可持续阅读的产品。

对本仓最有价值的是它的课程分层和“从想法到产品”的读者叙事；最需要警惕的是教程产品化很容易
引入站点工程复杂度，偏离本仓作为工程知识库和 Agent 控制面的主轴。

## 源码证据

- `raw/repository/README.md`：中文主入口，定义教程定位、推荐起点、板块和学习产出。
- `raw/repository/README.en.md`：英文入口。
- `raw/repository/docs/Basic/`：基础篇。
- `raw/repository/docs/Advanced/`：进阶篇。
- `raw/repository/docs/Practice/`：实践篇。
- `raw/repository/docs/Articles/`：优质文章篇。
- `raw/repository/demos/`：示例项目入口。
- `raw/repository/demos/demo-01-todo/`：第一个 todo demo。
- `raw/repository/demos/demo-02-todo-auth/`：带认证 demo。
- `raw/repository/demos/demo-03-social-schema/`：schema 练习 demo。
- `raw/repository/docs/deployment/index.md`：部署说明。
- `raw/repository/Dockerfile`：容器化部署入口。
- `raw/repository/docker-compose.yml`：本地私有化部署入口。
- `raw/repository/docs/public/llms.txt`：AI 读取入口。
- `raw/repository/docs/.vitepress/config.mts`：站点、SEO、PWA、FAQ、RSS 和侧边栏配置。

## 关键机制

### 四层课程结构

基础篇解决“能不能开始”，进阶篇解决“能不能完整交付”，实践篇解决“能不能动手练”，文章篇解决
“能不能持续追踪”。这是一种很适合中文用户的学习漏斗。

### Demo 是教程可信度来源

仓库不是只讲理念，还提供 `demos/`。这对零基础教程很关键：读者需要看到具体可运行对象，
否则很容易停在“AI 很厉害”的抽象叙事里。

### 部署能力被前置

README 和 `docs/deployment/index.md` 都强调私有化部署和本地运行。对 Vibe Coding 教程来说，
“能部署给别人看”比“写出代码”更接近真实成就感。

### 站点配置承担传播和检索

`config.mts` 中包含 SEO、RSS、FAQ、PWA、侧边栏和 Mermaid 等能力，说明教程产品化后，传播、
索引和结构导航会成为工程任务。

## 可迁移模式

- 本仓入门路径应明确“基础、进阶、实践、持续追踪”四类入口。
- 每个核心概念最好配一个可运行 demo 或最小任务，而不是只写定义。
- 部署上线应进入入门路径早期，而不是进阶尾部。
- 对面向新手的内容，先写学习产出，再写工具和概念。
- 站点化可以作为未来选项，但本仓当前仍应优先维护 Markdown 可读性和门禁。

## 对本仓的影响

本仓可以吸收 Vibe Vibe 的教程节奏，但要保持自己的差异：

- 本仓更偏工程治理、Agent 协作、研究域和资源治理。
- Vibe Vibe 更偏零基础教育和站点化课程。
- 合理方向是将本仓 getting-started 改得更像“学习路径”，而不是把全仓改成课程站点。

## 风险和待验证项

- 本轮没有运行 VitePress 构建、Docker 部署或 demo 项目。
- 部分 demo 目录可能只是模板或未完成项目，需要逐个验证。
- 面向零基础的表达会有必要简化，不能直接替代本仓进阶工程规范。

## 下一步 L3 验证任务

- 选取 `demos/demo-01-todo/` 作为最小 demo，验证是否可运行。
- 将 Vibe Vibe 的四层课程结构映射到本仓 `getting-started`、`workflow` 和 `references`。
- 为本仓补“学习产出表”：每个阶段读者能做出什么。
- 评估是否需要将部署上线前移到入门路径。
