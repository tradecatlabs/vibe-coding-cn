# skills/auto-tmux/scripts

本目录承载 `auto-tmux` 的可执行脚本层。脚本必须安全封装 tmux 常用操作，减少手写 `capture-pane` / `send-keys` 时的误控风险。

## 目录结构

```text
scripts/
├── AGENTS.md       # 本文件：脚本维护规则
├── README.md       # 面向人类的脚本入口说明
├── auto-tmux.sh    # 统一 tmux 自动化命令入口
├── swarm-state.sh  # 蜂群状态、任务、锁和报告管理
├── swarm-brief.sh  # 只读生成蜂群交接报告
├── swarm-watch.sh  # 有限轮次只读巡检和状态采样
├── swarm-archive.sh # 打包 brief、snapshot 和 swarm state
├── swarm-board.sh # 从 swarm state 渲染 Markdown 看板
├── swarm-deps-graph.sh # 从 deps.tsv 渲染 Mermaid 依赖图
├── swarm-export.sh # 导出 JSONL 状态包
├── swarm-timeline.sh # 从 status.log 渲染 Markdown 时间线
├── swarm-blockers.sh # 聚合 BLOCKED/FAIL、锁和异常状态
├── swarm-results.sh # 汇总 DONE/FAIL/BLOCKED worker 结果
├── swarm-report-pack.sh # 聚合只读报告包
├── swarm-assign.sh # 生成 ready task 到 worker pane 的分配建议
├── swarm-health.sh # 汇总只读健康检查报告包
├── remote-readonly.sh # SSH 只读采集远端 tmux 证据
├── record-summary.sh # 汇总 pipe-pane 录制日志
├── check-jsonl.sh # 轻量 JSONL 字段门禁
├── review-checklist.sh # report pack reviewer 审计清单
├── verify-report-pack.sh # report pack 统一验证入口
├── incident-report.sh # 事故复盘模板生成
├── audit-package.sh # auto-tmux 包索引一致性审计
├── completion.bash # Bash completion
├── safety-check.sh # 发送/粘贴/分发前的 payload 安全预检
├── render-swarm-prompt.sh # commander/worker/reviewer 提示词渲染
├── swarm-dispatch.sh # 渲染并可选下发蜂群提示词
├── auto-tmux-smoke-test.sh # 临时 tmux 会话端到端自测
└── validate-auto-tmux.sh # auto-tmux 专属质量门禁
```

## 维护规则

- 脚本必须使用 Bash 标准能力，不引入额外运行时依赖。
- 发送按键类功能必须先验证目标 pane 存在，并优先打印上下文。
- 捕获输出默认脱敏；只有显式 `--no-redact` 才允许输出原文。
- 批量救援必须通过 pattern 匹配触发，不允许无条件向所有 pane 发送输入。
- 批量广播必须要求显式 session，并支持 `--dry-run`。
- Prompt 渲染脚本只输出文本，不直接控制 tmux。
- Prompt 下发脚本默认只写文件；真实发送必须显式 `--send`，批量使用前先 `--dry-run`。
- 交接报告脚本只读调用 doctor/topology/scan/report，不直接发送按键。
- 巡检脚本必须是有限轮次，不允许默认无限循环。
- 归档脚本只复制状态和只读证据，不修改 tmux pane 或 swarm state。
- 看板脚本只读 `tasks.tsv`、`deps.tsv`、锁和状态日志，不改写状态目录。
- 依赖图脚本只读 `tasks.tsv` 和 `deps.tsv`，不改写状态目录。
- 导出脚本只读 `tasks.tsv`、`deps.tsv` 和锁目录，只写显式输出目录。
- 时间线脚本只读 `status.log`，不改写状态目录。
- 阻塞报告脚本只读任务、锁和状态日志，不做自动修复。
- 结果收敛脚本只读任务、结果文件和状态日志，不改写状态目录。
- 报告包脚本只编排只读脚本并写入显式输出目录，不 claim 任务、不发送 prompt。
- 分配建议脚本只读任务和 pane 拓扑，不 claim 任务、不发送 prompt。
- 健康检查脚本只读 tmux 与 swarm state，失败项写入报告，不做自动修复。
- 远端脚本只能运行 tmux list/capture 等只读命令，不允许 send-keys、kill 或配置写入。
- 录制摘要脚本只读 record 日志，输出默认脱敏，不修改日志源文件。
- JSONL 检查脚本只能做轻量字段门禁，不替代完整 JSON parser。
- 审计清单脚本只读报告包目录，不修改报告源文件。
- 报告包验证脚本只组合本目录已有只读门禁，不修改报告包内容。
- 事故报告脚本只生成模板，不自动判断责任或影响范围。
- 包审计脚本只检查索引、入口和 validator 的一致性，不修改任何文件。
- completion 文件只能定义 shell completion，不执行 tmux 写操作。
- 安全预检脚本只能读取文本或文件，不控制 tmux，不写状态目录。
- 状态脚本只能写入显式状态目录，不保存密钥、Token、密码或私密项目内容。
- 自测脚本必须创建独立临时 tmux session，并在退出时清理。
- 专属校验脚本必须覆盖脚本权限、语法、help 输出、关键索引、strict 校验和 smoke test。
- 新增脚本后必须更新 `README.md`、`SKILL.md`、`references/index.md`，并运行 `bash -n` 与 skill strict 校验。
