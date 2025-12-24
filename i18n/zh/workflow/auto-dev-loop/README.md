# 全自动开发闭环工作流

基于 **状态机 + 文件 Hook** 的五步 AI Agent 工作流系统。

## 目录结构

```
workflow/
├── .kiro/agents/workflow.json   # Kiro Agent 配置
├── workflow_engine/             # 状态机调度引擎
│   ├── runner.py               # 核心调度器
│   ├── hook_runner.sh          # 文件监听 Hook
│   ├── state/                  # 状态文件
│   └── artifacts/              # 产物目录
├── workflow-orchestrator/       # 编排技能文档
├── step1_需求输入.jsonl         # 规格锁定 Agent
├── step2_执行计划.jsonl         # 计划编排 Agent
├── step3_实施变更.jsonl         # 实施变更 Agent
├── step4_验证发布.jsonl         # 验证发布 Agent
├── step5_总控与循环.jsonl       # 总控循环 Agent
└── CHANGELOG.md
```

## 快速开始

### 方式 1：使用 Kiro CLI

```bash
# 进入工作流目录
cd ~/projects/vibe-coding-cn/i18n/zh/workflow

# 使用 workflow agent 启动
kiro-cli chat --agent workflow
```

### 方式 2：手动运行

```bash
cd ~/projects/vibe-coding-cn/i18n/zh/workflow

# 启动工作流
python3 workflow_engine/runner.py start

# 查看状态
python3 workflow_engine/runner.py status
```

### 方式 3：自动模式（Hook 监听）

```bash
# 终端 1: 启动文件监听
./workflow_engine/hook_runner.sh

# 终端 2: 触发工作流
python3 workflow_engine/runner.py start
```

## 工作流程

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Step1  │───▶│  Step2  │───▶│  Step3  │───▶│  Step4  │───▶│  Step5  │
│ 需求输入 │    │ 执行计划 │    │ 实施变更 │    │ 验证发布 │    │ 总控循环 │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └────┬────┘
                    ▲                                            │
                    │              失败回跳                       │
                    └────────────────────────────────────────────┘
```

## 核心机制

| 机制 | 说明 |
|------|------|
| 状态驱动 | `state/current_step.json` 作为唯一调度入口 |
| 文件 Hook | `inotifywait` 监听状态变更自动触发 |
| 循环控制 | Step5 根据验证结果决定回跳或完成 |
| 熔断保护 | 同一任务最多重试 3 次 |

## Kiro 集成

Agent 配置位于 `.kiro/agents/workflow.json`，包含：

- **hooks**: Agent 生命周期钩子
  - `agentSpawn`: 启动时读取状态
  - `stop`: 对话结束时检查状态
- **resources**: 自动加载提示词文件到上下文
- **toolsSettings**: 预授权文件操作和命令执行

## 下一步

- [ ] 集成实际 LLM 调用（替换 runner.py 中的 MOCK）
- [ ] 添加 CI/CD 集成示例
- [ ] 支持并行任务处理
