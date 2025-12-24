---
name: workflow-orchestrator
description: "自动化闭环开发工作流编排：基于状态机+文件系统 hook 驱动五步 Agent（规格/计划/实施/验证/总控），适用于需要最小依赖、可复现的全自动软件流水线。"
---

# workflow-orchestrator 技能

一个以「文件事件 hook + 轻量状态机」驱动的全自动开发闭环编排技能，连接现有五个 workflow_steps 提示词（step1~step5），在本地/CI 均可无服务依赖运行。

## 何时使用此技能

- 需要让 step1~step5 提示词按顺序自动执行，并在验证失败时回跳重跑计划/实施。
- 希望用最小依赖（仅文件系统与 shell）实现自动化，而非部署消息队列/微服务。
- 想在 CI 或本地通过简单命令/文件变更触发整条流水线。
- 需要总控（Step5）记录失败上下文并驱动循环直至所有任务完成。

## 不适用 / 边界

- 不处理外部云编排（Airflow/Temporal）；若需分布式调度请另用专用框架。
- 模型调用凭证/安全策略需由外部注入，本技能不管理密钥。
- 不创建新提示词内容，只编排已存在的 `workflow_steps/stepN_*.jsonl`。
- 输入需求缺失时，请先完成 Step1 的人工确认，再启动编排。

## 快速参考

- 目录约定  
  - 状态：`workflow_steps/state/current_step.json`  
  - 产物：`workflow_steps/artifacts/<run_id>/<step>.json|md`  
  - Hook 脚本：`workflow_engine/hook_runner.sh`（监听 state 变更）  
  - Runner：`workflow_engine/runner.py run --step N --input INPUT.json --state STATE.json`

- 状态文件最小 Schema
```json
{
  "run_id": "2025-12-25T05-00-00Z",
  "step": "step3",
  "status": "pending|running|success|failed",
  "payload_path": "artifacts/<run>/<prev>.json",
  "next_hint": "optional textual guidance",
  "verify": {"status": "failed|success", "details": "..."},
  "target_step": "step2|step5|done"
}
```

- Hook 触发（最小命令行示例）
```bash
# 启动监听（依赖 inotify-tools）
workflow_engine/hook_runner.sh
```
文件 `state/current_step.json` 每次更新即触发对应 `runner.py`：
- `step1 -> step2 -> step3 -> step4 -> step5`
- Step5 根据 `verify.status` 写入 `target_step=step2`（失败回跳）或 `done`（全部完成）。

- 手动启动/重跑
```bash
# 人工输入需求后触发 step1
python workflow_engine/runner.py run --step 1 --input user_request.json --state workflow_steps/state/current_step.json
```

## 示例

### 示例 1：全链路首轮
- 输入：`user_request.json` 包含原始需求。
- 步骤：运行 `runner.py step1` 生成规格书 → hook 自动推进 step2/3/4 → step5 归档。
- 期望：`artifacts/<run>/locked_spec.md`、计划、补丁、测试报告齐全；state 标记 `done`。

### 示例 2：验证失败回跳
- 输入：Step4 写出 `verify.status=failed`（含失败用例与日志）。
- 步骤：Step5 读取失败上下文写 `target_step=step2`；hook 触发 step2 重新规划 → step3 → step4。
- 期望：第二轮通过；state 历史包含失败记录；产物追加带版本号的补丁/报告。

### 示例 3：CI 集成
- 输入：CI job 上传需求与代码变更，触发 `runner.py step1`。
- 步骤：CI 中后台运行 `hook_runner.sh`；每个 step 输出工件到 `artifacts/` 并作为 job artifact。
- 期望：流水线失败时 CI 直接暴露 Step4 报告；通过后 Step5 归档并关闭 job。

## 参考资料

- `workflow_steps/step1_需求输入.jsonl` ... `step5_总控与循环.jsonl`
- `workflow_engine/hook_runner.sh`（需自建，监听 `state/current_step.json`）
- `workflow_engine/runner.py`（需自建，封装模型调用与状态写入）

## 维护

- 来源：仓库内现有五步提示词；不引用外部未验证信息。
- 最后更新：2025-12-25
- 已知限制：未内置凭证管理；需要 inotify-tools 或同类文件监听工具。
