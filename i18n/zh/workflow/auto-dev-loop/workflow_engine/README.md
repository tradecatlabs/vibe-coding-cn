# workflow_engine

全自动开发闭环的轻量编排引擎，基于 **文件事件 Hook + 状态机** 实现。

## 目录结构

```
workflow_engine/
├── runner.py           # 状态机调度器
├── hook_runner.sh      # 文件监听 Hook (inotify)
├── state/
│   └── current_step.json   # 当前状态
└── artifacts/
    └── <run_id>/       # 每次运行的产物
        ├── step1.json
        ├── step2.json
        └── ...
```

## 快速开始

### 1. 手动模式（无 Hook）

```bash
# 启动新工作流
python runner.py start

# 查看状态
python runner.py status
```

### 2. 自动模式（Hook 监听）

```bash
# 终端 1: 启动 Hook 监听
./hook_runner.sh

# 终端 2: 启动工作流（状态变更会自动触发后续步骤）
python runner.py start
```

## 状态文件 Schema

```json
{
  "run_id": "20251225T053800",
  "step": "step3",
  "status": "running|success|failed|completed|fatal_error",
  "payload_path": "artifacts/20251225T053800/step2.json",
  "verify": {"status": "success|failed", "details": "..."},
  "target_step": "step2|step5|done",
  "retry_count": 0
}
```

## 流程控制

```
step1 → step2 → step3 → step4 → step5
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
              verify=failed               verify=success
                    │                           │
                    ▼                           ▼
              target_step=step2           target_step=done
              (回跳重规划)                 (流程结束)
```

## 熔断机制

- 同一任务最多重试 3 次
- 超过后状态变为 `fatal_error`，需人工介入

## TODO

- [ ] 集成实际 LLM 调用（替换 runner.py 中的 MOCK）
- [ ] 添加 CI 集成示例
- [ ] 支持并行任务处理
