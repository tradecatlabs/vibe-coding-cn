# AGENTS - workflow-orchestrator

## 目录骨架
```
workflow-orchestrator/
├── AGENTS.md              # 本文件（目录级约束）
├── SKILL.md               # 技能入口，状态机与 hook 约定
├── CHANGELOG.md           # 变更记录
├── references/
│   └── index.md           # 参考索引与待补充子文档
```

## 职责与依赖
- 职责：用文件事件 hook + 轻量状态机，编排 `step1~step5` 的自动执行，支持失败回跳、归档与闭环。
- 上游：`../step1_需求输入.jsonl` ... `../step5_总控与循环.jsonl`（五步提示词定义）。
- 下游：`../workflow_engine/*`（状态机引擎与 Hook），产物落盘到 `../workflow_engine/artifacts/`。

## 使用要点
- 状态文件：`../workflow_engine/state/current_step.json` 为唯一调度入口；每次更新即触发对应 Runner。
- 总控逻辑：Step5 依据 `verify.status` 回跳 step2 或标记完成；防止无限循环需在 Runner 中实现熔断计数。
- 产物：按 `../workflow_engine/artifacts/<run_id>/<step>.{json,md}` 落盘，便于审计与归档。
