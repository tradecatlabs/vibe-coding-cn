# datawhalechina/easy-vibe 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`datawhalechina/easy-vibe`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、README 快照和本地仓库工作树。
- 观察日期：2026-07-03。

## L2 结论

`datawhalechina/easy-vibe` 是课程站点化最强的中文 Vibe Coding 对标对象。它不是简单 Markdown
教程，而是用 VitePress、多语言目录、交互式组件、站点部署脚本、`llms.txt`、`AGENTS.md` 和
`CLAUDE.md` 把课程包装成面向人类和 AI 的学习产品。

对本仓最有价值的点不是复制它的站点复杂度，而是学习它如何把“零基础学习路径”拆成用户目标、
学习阶段、视觉演示、交互组件和 AI 可读入口。

## 源码证据

- `raw/repository/README.md`：主叙事入口，包含学习路径、多语言入口、在线阅读和本地运行说明。
- `raw/repository/docs/`：VitePress 文档主体。
- `raw/repository/docs-readme/`：多语言 README 入口。
- `raw/repository/docs/zh-cn/index.md`：中文内容入口。
- `raw/repository/docs/en/index.md`：英文内容入口。
- `raw/repository/docs/public/llms.txt`：站点级 AI 读取入口。
- `raw/repository/llms.txt`：仓库级 AI 读取入口。
- `raw/repository/AGENTS.md`：Agent 操作入口。
- `raw/repository/CLAUDE.md`：Claude 入口。
- `raw/repository/docs/.vitepress/config.mjs`：站点配置、多语言和部署环境逻辑。
- `raw/repository/scripts/build-locales.mjs`：多语言构建脚本。
- `raw/repository/scripts/generate-sitemap.mjs`：站点 sitemap 生成脚本。
- `raw/repository/package.json`：VitePress、Vue、Element Plus、Mermaid、Reveal.js 等站点依赖和命令。

## 关键机制

### 学习路径按用户目标组织

Easy Vibe 的 README 把读者导向不同路径，而不是只按技术章节线性排列。它面向的是“我是谁、
我想做什么、应该从哪开始”的 onboarding 问题。这比纯目录更适合零基础和跨背景读者。

### 课程站点和 AI 入口并存

仓库同时保留 VitePress 站点、`llms.txt`、`AGENTS.md` 和 `CLAUDE.md`。这说明成熟教程需要同时
服务三类读取者：浏览器用户、搜索引擎/AI 引用系统、AI Agent。

### 多语言是产品能力，不是翻译附件

`docs-readme/`、多语言目录和 `config.mjs` 中的 locale 配置说明，多语言不是附属文件，而是站点
路由、构建、SEO 和内容维护的一部分。多语言会显著提升触达，但也显著提高维护成本。

### 交互式解释降低新手门槛

assets 中的 IDE、RAG、terminal、diffusion 等视觉材料说明，零基础教程不能只靠概念解释。
可视化和交互式组件能把抽象工程概念变成可感知流程。

## 可迁移模式

- 本仓 getting-started 应按“用户身份 + 目标产出 + 当前阶段”重组入口，而不只按知识分类。
- 对关键教程增加“你将做出什么”“需要什么前置条件”“卡住怎么验证”。
- `llms.txt` 和 `assets/ai-citation/llms-full.txt` 应继续作为 AI 入口维护，而不是事后补充。
- 如果未来站点化，应先保留轻量结构，避免过早引入多语言构建复杂度。
- 对 RAG、terminal、Git、IDE、agent 等抽象主题增加可视化解释或最小交互示例。

## 对本仓的影响

本仓当前优势是治理、研究域、资源和质量门禁；Easy Vibe 的优势是课程产品化和新手体验。
两者结合后，本仓可形成两层入口：

- `getting-started/`：面向新手的目标导向学习路径。
- `references/`、`workflow/`、`research/`：面向进阶用户和维护者的工程治理层。

关键取舍是：吸收学习路径和 AI 入口设计，不复制完整多语言站点复杂度。

## 风险和待验证项

- 多语言和站点组件会显著增加维护成本，本仓不能为了展示效果牺牲文档治理稳定性。
- 本轮没有运行 Easy Vibe 的构建、测试和多语言脚本。
- 站点视觉资产丰富，但不等同于工程治理成熟度。

## 下一步 L3 验证任务

- 对照 Easy Vibe 的学习路径，重审本仓 `docs/getting-started/` 是否按用户目标组织。
- 为本仓补一个“零基础到第一个可部署产物”的路径表。
- 抽取 AI 入口设计经验，更新 `llms.txt` / `llms-full.txt` 维护规则。
- 评估是否需要为关键概念增加图片、流程图或交互式示例。
