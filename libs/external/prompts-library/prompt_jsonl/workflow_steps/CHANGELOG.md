# CHANGELOG

## 2025-12-25T05:45:00+08:00 - 实现 workflow_engine MVP
- 关键改动点：创建 `workflow_engine/` 目录，实现文件事件 Hook + 状态机调度器
- 涉及文件或模块：
  - `workflow_engine/runner.py` - 状态机调度器，支持 start/dispatch/status 命令
  - `workflow_engine/hook_runner.sh` - inotify 文件监听 Hook
  - `workflow_engine/state/current_step.json` - 状态文件
  - `workflow_engine/README.md` - 使用文档
- 验证方式与结果：`python runner.py start` 成功执行 step1→step5 全流程，产物落盘到 artifacts/
- 遗留问题与下一步：集成实际 LLM 调用替换 MOCK；添加 CI 集成示例

## 2025-12-25T04:58:27+08:00 - 工作流自动循环方案分析
- 关键改动点：调研 `workflow_steps` 下五个提示词，梳理闭环与总控需求，输出可落地的状态机/钩子式 orchestrator 设计（未改代码）。
- 涉及文件或模块：`step1_需求输入.jsonl`，`step2_执行计划.jsonl`，`step3_实施变更.jsonl`，`step4_验证发布.jsonl`，`step5_总控与循环.jsonl`（阅读）。
- 验证方式与结果：分析性输出，无代码运行，TODO。
- 遗留问题与下一步：落地 orchestrator MVP；校准 JSONL 与 PARE v3.0 结构；为总控循环增加持久化状态与任务队列。

## 2025-12-25T05:04:00+08:00 - 移动 workflow-orchestrator 技能目录
- 关键改动点：将 `i18n/zh/skills/01-AI工具/workflow-orchestrator` 迁移至 `prompt_jsonl/workflow_steps/` 目录。
- 涉及文件或模块：`workflow-orchestrator/SKILL.md`，`workflow-orchestrator/AGENTS.md`，`workflow-orchestrator/references/index.md`，`workflow-orchestrator/CHANGELOG.md`。
- 验证方式与结果：命令行 `mv` 后检查目录结构，文件完好。
- 遗留问题与下一步：后续在新位置补充 `workflow_engine` 脚本并与技能文档对齐。
