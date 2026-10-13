<p align="center">
  <a href="./README.en.md">English</a> |
  <a href="./README.md"><strong>简体中文</strong></a>
</p>

<p align="center">
  <img src="./docs/public/logo.png" width="100" alt="Vibe Vibe"/>
</p>

<h1 align="center">Vibe Vibe </h1>

# Vibe Vibe —— 人人都能学会的 AI 编程（Vibe Coding）指南
> **面向零编程基础学习者的 AI 辅助编程系统化教程，从「我有一个想法」到「我做出了一个产品」，让人人都能成为 Builder。**

点击以访问教程主页：www.vibevibe.cn

### 核心理念

践行 OpenAI 联合创始人 **Andrej Karpathy** 提出的 Vibe Coding 理念——**从 Coder 到 Commander**：通过自然语言与 AI 对话，让编程从"写代码"转变为"对话式创作"。

> *"完全沉浸于编程的'氛围'中，忘记代码的存在。"*

### 快速开始

📖 **在线阅读**：[www.vibevibe.cn](https://www.vibevibe.cn)

| 你是谁 | 推荐起点 |
|-------|---------|
| 完全零基础 | 基础篇 → 第1章 觉醒 |
| 用过 ChatGPT 等大语言模型工具但没做过项目 | 基础篇 → 第2章 心法 |
| 有编程基础想学 Vibe Coding | 基础篇快速浏览 → 进阶篇 |
| 想直接动手做项目 | 基础篇 → 第4章 实战 |
| 想找项目练手 | 实践篇 |

### 私有化部署

如果你想在本地或内网环境部署本教程站点，仓库已经提供了可直接使用的 `Dockerfile` 和 `docker-compose.yml`：

```bash
docker compose up -d --build
```

默认访问地址为 `http://localhost:1024`。

更完整的部署方式、静态文件部署方案和离线环境注意事项，请查看[部署指南](./docs/deployment/index.md)。

### 教程定位

国内首个系统化的 Vibe Coding 开源教程，分为四大板块：

| 板块 | 定位 | 适合人群 |
|-----|------|---------|
| 📘 **基础篇** | AI 编程入门 + 心法 + 第一个项目 | 完全零基础、用过 ChatGPT 但没做过项目 |
| 📗 **进阶篇** | 16章"序言可阅读" · 从0到上线的避坑指南 | 想了解完整项目交付流程的开发者 |
| 📙 **实践篇** | 分人群项目实战 + 进阶技能训练 | 想通过动手练习巩固所学 |
| 📕 **优质文章篇** | 精选学习资源 + 行业前沿追踪 | 想持续学习、保持行业敏感度 |

- **为什么需要这份教程？** Vibe Coding 已成为全球趋势（越来越多的创业公司大部分代码由 AI 辅助生成），但国内学习资源碎片化严重，缺乏系统化、零基础友好、包含完整进阶路径的教程。

- **适合人群**：编程零基础者、大学生、创业者、传统程序员、职场人士，任何想用 AI 快速实现想法、提升工作效率或学习新范式的人。

### 进阶版预告：在线 IDE + Skills

我们即将推出**在线开发环境**，无需本地配置环境，打开浏览器即可开始学习：

- **云端 IDE** —— 内置完整的 Node.js 24、Python、Docker 等开发环境
- **50+ AI Skills** —— 预装丰富的 AI 辅助技能包，覆盖开发全流程
- **开箱即用** —— 无需安装任何软件，登录即可开始编程实践

让学习门槛降到最低，敬请期待！

### 学习产出

| 阶段 | 你将获得 |
|-----|---------|
| **基础篇** | 掌握 Vibe Coding 心法 · 用自然语言指挥 AI · 独立完成项目 · 部署上线能力 |
| **进阶篇** | 现代全栈技术栈 · 前后端架构 · 用户系统开发 · 生产级部署 · 工程化思维 |

## 贡献者名单

| 姓名 | 职责 | 简介 |
| :----| :---- | :---- |
| [符航康](https://www.hangkangfu.cn) | 项目负责人 & 核心贡献者 | 一位 AI 时代的原住民|
| [齐国皓](https://www.guohaoqi.cn) | 项目负责人 & 核心贡献者 | 现就读于新加坡国立大学计算机学院, 湖南大学金融科技协会创始人|
| 刘磊 | 「实践篇」贡献者、图像贡献者 | 中国科学院大学，一枚在职后端 Coder，热爱 Vibe，崇尚分享。 |
| 陈俊希 | 「优质文章篇」板块贡献者 | 湖南大学金融科技协会会长，湖南大学金融与统计学院24级本科生 |
| 金龙   |「实践篇」板块贡献者  | 北京大学学生创新学社AI俱乐部副部长，北京大学24级研究生|
| 舒璐璐 | 「实践篇」板块贡献者 | 湖南大学「麓山人文+」创始人，湖南大学岳麓书院23级本科生 |

## 目录

本教程分为**四大板块**，采用渐进式学习路径设计（点击展开详细目录）：

<details>
<summary><b>📘 基础篇：Vibe Coding 启示录（写给所有人的 AI 编程入门）</b></summary>

```
基础篇目录
│
├── 写在最前面
│   └── 找到你的位置
│
├── 第1章：觉醒 —— 为什么现在是编程最好的时代
│   ├── 1.1 编程已死，编程永生：从 Coder 到 Commander
│   ├── 1.2 核心概念：Vibe Coding 与 Spec Coding 详解
│   ├── 1.3 破除迷信：不懂英文、数学不好也能写代码吗？
│   ├── 1.4 工具初探：Cursor、Windsurf、Bolt.new 与 Replit 选型指南
│   └── 1.5 Hello World：你的第一个 3 分钟 AI 网页
│
├── 第2章：心法 —— 像产品经理一样思考
│   ├── 2.1 拒绝功能堆砌：为什么你的 AI 写不出复杂的 App？
│   ├── 2.2 MVP 思维：如何设计一个"能跑的最小版本"
│   ├── 2.3 灵魂三问：用户是谁？痛点在哪？为何用你？
│   └── 2.4 实战演练：拆解一个"背单词软件"的想法
│
├── 第3章：技法 —— 与 AI 对话的艺术
│   ├── 3.1 提示词工程基础：Context is King
│   ├── 3.2 用户旅程地图：把想法变成 AI 能懂的路径
│   ├── 3.3 编写第一份 PRD：让 AI 不再胡编乱造
│   └── 3.4 功能优先级 P0/P1/P2：学会对 AI 说"这个先不做"
│
├── 第4章：实战 —— 从 0 到 1 开发个人工具
│   ├── 4.1 环境准备：无需命令行的开发环境搭建
│   ├── 4.2 第一轮：生成静态页面 —— 先看"脸"
│   ├── 4.3 第二轮：注入逻辑与交互 —— 再长"脑"
│   ├── 4.4 第三轮：数据存储基础
│   └── 4.5 Debug 指南：当 AI 报错时，如何用 AI 修复 AI
│
├── 第5章：精进 —— 从"能用"到"好用"
│   ├── 5.1 后悔药：代码改崩了怎么办
│   ├── 5.2 见世面：把网页发到互联网上
│   ├── 5.3 护城河：AI 时代的安全意识
│   ├── 5.4 再进化：项目的持续迭代与优化
│   ├── 5.5 知边界：Vibe Coding 的能与不能
│   └── 5.6 启程前：本章总结与进阶预告
│
├── 结语：给未来的你
│
├── 下部预告：Vibe Coding 全栈实战教程
│
└── 附录
    ├── A. Prompt 速查清单
    ├── B. 常见错误与解决方案速查表
    ├── C. 术语表（中英对照）
    ├── D. 工具对比速查表
    └── E. 项目 idea 清单
```

</details>

<details>
<summary><b>📗 进阶篇：从0到上线的避坑指南</b></summary>

本篇以**完整的产品交付流程**为主线，共16章，每章序言均可阅读：

```
进阶篇目录
│
├── 第1章：环境搭建、代码形态与包管理器
├── 第2章：开发工具与 AI 调教
├── 第3章：PRD 与文档驱动开发
├── 第4章：开发常识与技术栈
├── 第5章：代码运行状态与构建原理
├── 第6章：界面（UI）与交互（UX）
├── 第7章：环境变量与安全机制
├── 第8章：数据持久化与数据库
├── 第9章：功能测试流程与自动化脚本
├── 第10章：Localhost 与公网访问
├── 第11章：Git 版本控制与跨平台协作
├── 第12章：无服务器部署与 CI/CD 自动化
├── 第13章：域名解析原理与网络接入
├── 第14章：云服务器运维与项目部署
├── 第15章：SEO、分享与数据统计
└── 第16章：用户反馈与产品迭代
```

**技术栈**：Next.js 16 · React · TypeScript · Tailwind CSS · shadcn/ui · Drizzle ORM · PostgreSQL

</details>

<details>
<summary><b>📙 实践篇：分人群项目实战</b></summary>

```
实践篇目录
│
├── 基础板块（按人群分类）
│   ├── 文科生/商科生项目 —— 内容创作、数据展示类
│   ├── 理工科学生项目 —— 算法可视化、数据处理类
│   └── 职场人士项目 —— 工作流自动化、效率提升类
│
└── 进阶板块（基于 Sean's Stories 系列）
    ├── 核心技能 —— 上线应用、数据库、后端部署、用户认证
    ├── AI Agent 开发 —— RAG、向量数据库、MCP 集成
    ├── 全栈项目实战 —— SaaS、地图应用、移动应用
    └── 工具与效率 —— n8n、GitHub 工作流、React/TS 进阶
```

</details>

<details>
<summary><b>📕 优质文章篇：精选学习资源</b></summary>

```
优质文章篇目录
│
├── 知名公司博客 —— OpenAI、Anthropic、Vercel 等技术博客
├── 优质播客 —— AI、开发者、创业者相关播客推荐
├── 研究报告 —— AI 发展报告、开发者调查、行业趋势
├── 优质 Newsletter —— 值得订阅的技术周刊
└── 开发者社区 —— Discord、Twitter、GitHub 优质资源
```

</details>

## 参与贡献

- 如果你发现了一些问题，可以提Issue进行反馈，如果提完没有人回复你可以联系[保姆团队](https://github.com/datawhalechina/DOPMC/blob/main/OP.md)的同学进行反馈跟进~
- 如果你想参与贡献本项目，可以提Pull request，如果提完没有人回复你可以联系[保姆团队](https://github.com/datawhalechina/DOPMC/blob/main/OP.md)的同学进行反馈跟进~
- 如果你对 Datawhale 很感兴趣并想要发起一个新的项目，请按照[Datawhale开源项目指南](https://github.com/datawhalechina/DOPMC/blob/main/GUIDE.md)进行操作即可~

## 关注我们

<div align=center>
<p>扫描下方二维码关注公众号：Datawhale</p>
<img src="https://raw.githubusercontent.com/datawhalechina/pumpkin-book/master/res/qrcode.jpeg" width = "180" height = "180">
</div>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=datawhalechina/vibe-vibe&type=Date)](https://star-history.com/#datawhalechina/vibe-vibe&Date)

## LICENSE

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey" /></a><br />本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
