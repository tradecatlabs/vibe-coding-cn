# Vibe Coding CN Skill

> 基于 [tukuaiai/vibe-coding-cn](https://github.com/tukuaiai/vibe-coding-cn) 生成的 AI Skill

通过与 AI 结对编程，将想法变为现实的终极工作站。本 Skill 提供完整的 Vibe Coding 方法论、工作流程和实战指南。

---

## 📦 文件结构

```
.
├── README.md                    # 本文件 - 项目说明
├── SKILL.md                     # Skill 主文件（Claude Code 入口）
├── AGENTS.md                    # AI Agent 行为指南
└── references/
    ├── index.md                 # 参考资料索引
    ├── philosophy.md            # Vibe Coding 哲学原理
    ├── glue-coding.md           # 胶水编程方法论
    ├── canvas-dev.md            # Canvas 白板驱动开发
    ├── language-layers.md       # 12 层语言要素
    ├── workflow.md              # 标准工作流
    ├── quality-checklist.md     # 质量检查清单
    └── agents-guidelines.md     # AI Agent 行为准则（完整版）
```

---

## 🚀 快速开始

### 在 Claude Code 中使用

1. 将本仓库配置为 Claude Code 的 Skill
2. 或在对话中引用：`加载 vibe-coding-cn Skill`

### 使用方式

激活 Skill 后，你可以：

| 场景 | 示例指令 |
|:---|:---|
| 从零开发项目 | "用 Vibe Coding 方式帮我做一个 XXX" |
| 胶水编程 | "帮我找成熟的开源库来实现 XXX 功能" |
| 理解项目架构 | "用 Canvas 白板分析这个项目的架构" |
| 多 Agent 协作 | "用 tmux 蜂群模式并行处理这些任务" |
| 提升代码理解 | "用 12 层语言要素分析这段代码" |

---

## 📖 核心内容

### 方法论

| 主题 | 说明 | 入口 |
|:---|:---|:---|
| **Vibe Coding 哲学** | "一二三万物"核心理念 | [`SKILL.md`](./SKILL.md#核心哲学) |
| **胶水编程** | 能抄不写，能连不造 | [`references/glue-coding.md`](./references/glue-coding.md) |
| **Canvas 白板** | 图形驱动开发 | [`references/canvas-dev.md`](./references/canvas-dev.md) |
| **AI 蜂群协作** | tmux 多 Agent 系统 | [`SKILL.md`](./SKILL.md#ai-蜂群协作 tmux-多 agent-系统) |

### 工作流程

| 步骤 | 说明 | 入口 |
|:---|:---|:---|
| 1 | 游戏设计文档（GDD） | [`references/workflow.md`](./references/workflow.md) |
| 2 | 技术栈与 Agent 规则 | [`references/workflow.md`](./references/workflow.md) |
| 3 | 实施计划 | [`references/workflow.md`](./references/workflow.md) |
| 4 | 记忆库（Memory Bank） | [`references/workflow.md`](./references/workflow.md) |
| 5 | 增量式开发 | [`references/workflow.md`](./references/workflow.md) |
| 6 | 添加功能 | [`references/workflow.md`](./references/workflow.md) |

### 约束条件

| 类型 | 数量 | 入口 |
|:---|:---|:---|
| 通用开发约束 | 34 条 | [`SKILL.md`](./SKILL.md#通用开发约束 34 条核心) |
| 胶水开发约束 | 23 条 | [`SKILL.md`](./SKILL.md#胶水开发约束 23 条核心) |
| 系统提示词原则 | 15 条精要 | [`SKILL.md`](./SKILL.md#系统提示词构建原则精要版) |

### 能力提升

| 主题 | 说明 | 入口 |
|:---|:---|:---|
| **12 层语言要素** | 看懂 100% 代码的 12 个层级 | [`references/language-layers.md`](./references/language-layers.md) |
| **质量检查清单** | 各阶段检查项 | [`references/quality-checklist.md`](./references/quality-checklist.md) |

---

## 🎯 使用场景

| 场景 | 推荐文档 |
|:---|:---|
| 从零开始开发项目 | [`references/workflow.md`](./references/workflow.md) |
| 寻找开源库复用 | [`references/glue-coding.md`](./references/glue-coding.md) |
| 理解复杂项目架构 | [`references/canvas-dev.md`](./references/canvas-dev.md) |
| 看不懂代码 | [`references/language-layers.md`](./references/language-layers.md) |
| 确保代码质量 | [`references/quality-checklist.md`](./references/quality-checklist.md) |
| 配置 AI 行为 | [`AGENTS.md`](./AGENTS.md) |

---

## 📚 参考资料导航

完整参考资料索引 → [`references/index.md`](./references/index.md)

### 学习路径

**新手（从 0 到 1）：**
```
philosophy.md → workflow.md → glue-coding.md → language-layers.md
```

**进阶（提升效率）：**
```
glue-coding.md → canvas-dev.md → quality-checklist.md
```

**高级（架构与优化）：**
```
canvas-dev.md → language-layers.md → agents-guidelines.md
```

---

## 🙏 致谢

本 Skill 基于以下开源项目生成：

### 主要参考

| 项目 | 说明 |
|:---|:---|
| **[tukuaiai/vibe-coding-cn](https://github.com/tukuaiai/vibe-coding-cn)** | Vibe Coding 中文指南 - 本 Skill 的核心内容来源 |

### 感谢

感谢 [tukuaiai](https://github.com/tukuaiai) 及其贡献者们创建并维护这个优秀的开源项目，为 AI 辅助开发提供了系统化的方法论和实战指南。

---

## 📄 许可证

本项目继承自原仓库的 MIT 许可证。

---

## 🔗 相关资源

| 资源 | 链接 |
|:---|:---|
| Vibe Coding 中文指南（原仓库） | [GitHub](https://github.com/tukuaiai/vibe-coding-cn) |
| 提示词在线表格 | [Google Sheets](https://docs.google.com/spreadsheets/d/1Ifk_dLF25ULSxcfGem1hXzJsi7_RBUNAki8SBCuvkJA) |
| Claude Code 官方文档 | [Docs](https://docs.claude.com/) |
| Skills.sh | [Skills 大全](https://skills.sh/) |

---

## 📝 维护

- **最后更新**：2026-03-23
- **版本**：v2.0
- **贡献**：欢迎提交 Issue 和 PR
