# Workflow 目录 Agent 指南

`assets/documents/workflow/` 存放可复用的工作流模板：把“需求 → 计划 → 实施 → 验证 → 总控复盘”等流程固化为可重复、可审计的自动化路径。

## 目录结构（当前）

```text
assets/documents/workflow/
├── AGENTS.md                         # 本文件（目录级行为准则）
├── README.md                         # workflow 总览
├── auto-dev-loop/                    # 全自动开发闭环（五步状态机）
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── step1_需求输入.jsonl
│   ├── step2_执行计划.jsonl
│   ├── step3_实施变更.jsonl
│   ├── step4_验证发布.jsonl
│   ├── step5_总控与循环.jsonl
│   ├── .kiro/                        # Kiro 集成配置
│   ├── workflow_engine/              # 轻量状态机引擎（state + hook）
│   └── workflow-orchestrator/        # 编排技能文档与规范
```

## 操作规范

### 允许
- 新增工作流模板（新建 `<workflow-name>/` 子目录）
- 迭代现有工作流的 `README.md`、提示词/模板/脚本
- 为工作流补齐最小可运行路径（输入 → 执行 → 产物）

### 禁止 / 不推荐
- 破坏现有工作流的“入口约定”（例如把 `README.md` / 关键提示词文件移走）
- 在脚本中写死个人环境路径（优先相对路径或通过参数注入）

## 工作流落地标准（建议）

- 必有：`README.md`（一页讲清：目的、输入输出、如何运行、失败怎么排）
- 有状态机/脚本的工作流：必须明确 **唯一状态入口文件**（例如 `state/current_step.json`）与产物落盘目录（例如 `artifacts/`）
