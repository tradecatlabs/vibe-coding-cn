# datawhalechina/vibe-vibe 研究分析

## 本轮结论

- Vibe Vibe 是面向零基础用户的中文 AI 编程指南，核心价值是把 Vibe Coding 讲成可学习、可部署、可演示的课程。
- 仓库包含 `docs/`、`demos/`、`Dockerfile`、`docker-compose.yml`，说明它强调教程、示例和私有化部署。
- 本仓应吸收它对零基础用户的解释方式和 demo 驱动学习路径，但工程治理层仍需本仓自己定义。

## 本地证据

- 研究对象：`datawhalechina/vibe-vibe`
- 当前研究角色：中文零基础系统教程
- 本轮成熟度：L1 初步理解
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`

## 结构观察

- 根目录包含 `docs/`、`demos/`、`package.json`、`pnpm-lock.yaml`、`Dockerfile`、`docker-compose.yml`。
- README 的核心理念、快速开始、私有化部署、教程定位、进阶版预告和学习产出结构清晰。
- 课程形态比工具实现更强，适合作为 onboarding 研究对象。

## 可借鉴点

- 零基础内容需要先给学习产出，再给工具和概念。
- demo 目录能降低抽象教程的理解成本。
- 私有化部署说明适合补充本仓“教程站点/知识库发布”参考。

## 风险和边界

- 面向零基础会简化工程细节，不能直接当作高级工程规范。
- 大体量课程仓库需要区分原创内容、站点框架和生成资产。
- 进阶版能力需要继续观察是否真实落地。

## 下一轮研究任务

- 整理它的课程目录和 demo 类型，对照本仓 getting-started。
- 分析私有化部署部分是否能沉淀到 references。

## 沉淀判断

- 本轮只完成 L1 理解，不直接迁入 concepts、references、workflow 或 skills。
- 只有经过 L2 源码阅读、实验验证或交叉对照后的结论，才进入稳定层。