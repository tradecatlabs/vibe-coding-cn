# datawhalechina/easy-vibe 研究分析

## 本轮结论

- Easy Vibe 是中文 Vibe Coding 课程型站点，重点在学习路径、课程包装和面向不同目标的路线分流。
- 它比单纯 awesome list 更接近产品化教程，有 `docs/`、`config/`、`scripts/`、`llms.txt`、`AGENTS.md`、`CLAUDE.md` 等 AI/文档工程资产。
- 本仓应重点吸收它的学习路径分层、课程入口设计、Agent 文档入口和多语言/站点化组织方式。

## 本地证据

- 研究对象：`datawhalechina/easy-vibe`
- 当前研究角色：中文分阶段交互式课程
- 本轮成熟度：L1 初步理解
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`

## 结构观察

- 根目录包含 `docs/`、`docs-readme/`、`config/`、`scripts/`、`assets/`、`Dockerfile`、`package.json`。
- README 将用户分成 fast first win、idea to prototype、full-stack products、AI-Native advanced workflow、reference material 等学习路径。
- 存在 `AGENTS.md`、`CLAUDE.md` 和 `llms.txt`，说明它已经考虑 AI Agent 可读入口。

## 可借鉴点

- 学习路线不应只按技术栈组织，也应按用户目标和阶段组织。
- 课程站点可以同时服务人类读者和 AI 助手，关键是保留 `llms.txt` 与目录规则。
- 适合对照本仓 getting-started 和 docs/README 的新手路径设计。

## 风险和边界

- 课程内容规模大且多语言/多目录，直接迁移会增加维护成本。
- 它偏学习体验，不等同于企业级工程治理模板。
- 站点生成和课程结构需要拆开研究，不能混成一个结论。

## 下一轮研究任务

- 读取 `docs/` 的学习路径结构，抽象为本仓学习地图改进建议。
- 研究 `AGENTS.md`、`CLAUDE.md`、`llms.txt` 如何服务 AI 读取。

## 沉淀判断

- 本轮只完成 L1 理解，不直接迁入 concepts、references、workflow 或 skills。
- 只有经过 L2 源码阅读、实验验证或交叉对照后的结论，才进入稳定层。