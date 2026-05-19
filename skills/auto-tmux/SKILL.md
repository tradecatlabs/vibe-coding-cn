---
name: auto-tmux
description: "tmux 自动化操控：用 scripts/auto-tmux.sh 安全读取、发送、巡检、救援、录制 session|window|pane，用 swarm-state.sh 管理蜂群任务/锁/状态，并基于 oh-my-tmux 组织多 AI 终端协作。触发：capture-pane、send-keys、批量巡检、蜂群 AI 协作、卡死救援、tmux 工作台初始化。"
---

# auto-tmux Skill

让 AI 像熟练运维一样操作 tmux：优先使用 `scripts/auto-tmux.sh` 安全封装读取终端输出、发送按键、批量巡检、协作/救援其他终端；使用 `scripts/swarm-state.sh` 管理蜂群任务、锁、状态和结果；必要时再回退到 tmux 原生命令。默认兼容 `tools/external/.tmux`（gpakosz/oh-my-tmux），并在本技能内通过 `assets/oh-my-tmux` 与 `assets/tmux-src` 暴露上游 submodule。

## When to Use This Skill

触发条件（满足其一即可）：
- 需要远程读取/复制某个 tmux pane 的最新输出（日志、提示、错误）。
- 需要向指定 pane 发送按键/命令（确认 `y`、`Enter`、`Ctrl+C`、广播同一窗口）。
- 需要批量巡检/接管多 AI 终端（蜂群协作、自动救援卡死任务）。
- 需要初始化 AI 多终端工作台、等待输出 pattern、录制 pane 日志或保存巡检证据。
- 需要给 tmux 蜂群建立任务队列、状态日志、文件锁和结果报告。
- 需要快速回忆 oh-my-tmux 快捷键、前缀或同步面板操作。
- 需要在当前仓库复用 `tools/external/.tmux` 配置并避免修改主配置。
- 需要从技能目录内快速查看 oh-my-tmux 配置或 tmux 上游源码入口。

## Not For / Boundaries

- 不用于执行非 tmux 环境（目标不存在时先创建 session/window/pane）。
- 不直接编辑 `~/.tmux.conf` / `.tmux.conf`（遵循 oh-my-tmux：修改请放到 `.tmux.conf.local`）。
- 不盲发破坏性按键：`kill-server`、`rm -rf` 等必须先 capture-pane 确认目标上下文。
- 不把脚本当成权限绕过器；敏感会话、密码输入、生产数据库操作仍需人工确认。
- 如果 tmux 版本 < 2.6，需先升级再使用本技能的命令组合。

## Quick Reference

### 常用模式（≤20 条，直接复制即用）

**脚本帮助与语法检查**
```bash
bash -n skills/auto-tmux/scripts/auto-tmux.sh
bash -n skills/auto-tmux/scripts/swarm-state.sh
bash -n skills/auto-tmux/scripts/swarm-brief.sh
bash -n skills/auto-tmux/scripts/swarm-watch.sh
bash -n skills/auto-tmux/scripts/swarm-archive.sh
bash -n skills/auto-tmux/scripts/swarm-board.sh
bash -n skills/auto-tmux/scripts/swarm-deps-graph.sh
bash -n skills/auto-tmux/scripts/swarm-export.sh
bash -n skills/auto-tmux/scripts/swarm-timeline.sh
bash -n skills/auto-tmux/scripts/swarm-blockers.sh
bash -n skills/auto-tmux/scripts/swarm-assign.sh
bash -n skills/auto-tmux/scripts/swarm-health.sh
bash -n skills/auto-tmux/scripts/record-summary.sh
bash -n skills/auto-tmux/scripts/completion.bash
bash -n skills/auto-tmux/scripts/safety-check.sh
bash -n skills/auto-tmux/scripts/render-swarm-prompt.sh
bash -n skills/auto-tmux/scripts/swarm-dispatch.sh
bash -n skills/auto-tmux/scripts/validate-auto-tmux.sh
skills/auto-tmux/scripts/auto-tmux.sh help
skills/auto-tmux/scripts/swarm-state.sh help
```

**查看快捷键帮助**（oh-my-tmux 双前缀：主 `C-a`，备用 `C-b`，前缀后按 `?`）
```text
[按] <prefix> ?
```

**枚举拓扑（脚本优先）**
```bash
skills/auto-tmux/scripts/auto-tmux.sh topology
skills/auto-tmux/scripts/auto-tmux.sh topology --session ai-hub
```

**枚举拓扑（原生命令兜底）**
```bash
tmux list-sessions
tmux list-windows -a -F '#S:#I:#W#F'
tmux list-panes   -a -F '#S:#I.#P #{pane_current_command} #{pane_title}'
```

**读取指定 pane 最近输出**
```bash
skills/auto-tmux/scripts/auto-tmux.sh inspect -t <session>:<window>.<pane> -n 40
skills/auto-tmux/scripts/auto-tmux.sh capture -t <session>:<window>.<pane> -n 120
```

**原生读取指定 pane 最近 120 行**
```bash
tmux capture-pane -t <session>:<window>.<pane> -p -S -120
```

**向指定 pane 发送命令或确认键**
```bash
skills/auto-tmux/scripts/safety-check.sh --text "make test"
skills/auto-tmux/scripts/auto-tmux.sh send -t <session>:<window>.<pane> --text "make test" --enter
skills/auto-tmux/scripts/safety-check.sh --file /tmp/prompt.md --strict
skills/auto-tmux/scripts/auto-tmux.sh paste -t <session>:<window>.<pane> --file /tmp/prompt.md --enter --dry-run
skills/auto-tmux/scripts/auto-tmux.sh rescue -t <session>:<window>.<pane> --pattern "(y/n)" --reply y
```

**原生发送确认键**
```bash
tmux send-keys -t <session>:<window>.<pane> "y" Enter
```

**安全中断挂住任务**
```bash
tmux send-keys -t <session>:<window>.<pane> C-c
```

**开启/关闭窗口内广播（同步全部 pane）**
```bash
tmux set-window-option synchronize-panes on
tmux set-window-option synchronize-panes off
```

**一次扫描全部窗口并截取最近输出（蜂群巡检）**
```bash
skills/auto-tmux/scripts/auto-tmux.sh scan --session ai-hub -n 80
skills/auto-tmux/scripts/auto-tmux.sh scan --session ai-hub --pattern "ERROR|Traceback" --save-dir /tmp/auto-tmux-scan
```

**受控广播到指定 session**
```bash
skills/auto-tmux/scripts/auto-tmux.sh broadcast --session ai-hub --text "pwd" --enter --dry-run
```

**生成证据快照/交接报告**
```bash
skills/auto-tmux/scripts/auto-tmux.sh snapshot --session ai-hub --dir /tmp/auto-tmux-snapshot -n 120
skills/auto-tmux/scripts/swarm-brief.sh --session ai-hub --swarm-dir /tmp/ai_swarm --out /tmp/auto-tmux-brief
skills/auto-tmux/scripts/swarm-watch.sh --session ai-hub --swarm-dir /tmp/ai_swarm --iterations 3 --interval 10
skills/auto-tmux/scripts/swarm-archive.sh --session ai-hub --swarm-dir /tmp/ai_swarm --out /tmp/ai-hub-handoff.tar.gz
skills/auto-tmux/scripts/swarm-board.sh --dir /tmp/ai_swarm --out /tmp/ai-swarm-board.md
skills/auto-tmux/scripts/swarm-deps-graph.sh --dir /tmp/ai_swarm --out /tmp/ai-swarm-deps.md
skills/auto-tmux/scripts/swarm-export.sh --dir /tmp/ai_swarm --out /tmp/ai-swarm-export
skills/auto-tmux/scripts/swarm-timeline.sh --dir /tmp/ai_swarm --out /tmp/ai-swarm-timeline.md
skills/auto-tmux/scripts/swarm-blockers.sh --dir /tmp/ai_swarm --out /tmp/ai-swarm-blockers.md
skills/auto-tmux/scripts/swarm-assign.sh --swarm-dir /tmp/ai_swarm --session ai-hub --out /tmp/ai-swarm-assign.md
skills/auto-tmux/scripts/swarm-health.sh --session ai-hub --swarm-dir /tmp/ai_swarm --out /tmp/auto-tmux-health
```

**远程救援：发现等待输入即发送 y**
```bash
target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"
skills/auto-tmux/scripts/auto-tmux.sh rescue -t "$target" --pattern "(y/n)" --reply y --dry-run
skills/auto-tmux/scripts/auto-tmux.sh rescue -t "$target" --pattern "(y/n)" --reply y
```

**新建 AI 蜂群工作台（1 指挥 + 3 工人）**
```bash
skills/auto-tmux/scripts/auto-tmux.sh hub --session ai-hub --workers 3 --cmd "codex"
skills/auto-tmux/scripts/auto-tmux.sh topology --session ai-hub
skills/auto-tmux/scripts/auto-tmux.sh cleanup --session ai-hub --dry-run
```

**启用 oh-my-tmux 配置（仓库内版本）**
```bash
repo_root="$(git rev-parse --show-toplevel)"
ln -sfn "$repo_root/skills/auto-tmux/assets/oh-my-tmux/.tmux.conf" ~/.tmux.conf
cp -n "$repo_root/skills/auto-tmux/assets/oh-my-tmux/.tmux.conf.local" ~/.tmux.conf.local
```

**记录 pane 输出到文件**
```bash
skills/auto-tmux/scripts/auto-tmux.sh record start -t <session>:<window>.<pane> --dir /tmp/auto-tmux-records
skills/auto-tmux/scripts/auto-tmux.sh record stop -t <session>:<window>.<pane>
skills/auto-tmux/scripts/record-summary.sh --dir /tmp/auto-tmux-records --out /tmp/auto-tmux-record-summary.md
```

**等待 pane 出现完成信号**
```bash
skills/auto-tmux/scripts/auto-tmux.sh wait -t <session>:<window>.<pane> --pattern "Tests passed|BUILD SUCCESS" --timeout 300
```

**初始化蜂群状态、任务和锁**
```bash
skills/auto-tmux/scripts/swarm-state.sh init --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh task-add --id task-001 --text "检查 README 链接"
skills/auto-tmux/scripts/swarm-state.sh task-import --file /tmp/tasks.txt --prefix batch --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh task-depend --id task-002 --blocked-by task-001 --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh task-ready --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh task-next --owner <session>:<window>.<pane>
skills/auto-tmux/scripts/swarm-state.sh lock-acquire --name README.md --owner <session>:<window>.<pane>
skills/auto-tmux/scripts/swarm-state.sh lock-prune --older-than 3600 --dry-run
skills/auto-tmux/scripts/swarm-state.sh task-block --id task-001 --owner <session>:<window>.<pane> --reason "等待输入"
skills/auto-tmux/scripts/swarm-state.sh task-fail --id task-001 --owner <session>:<window>.<pane> --reason "测试失败"
skills/auto-tmux/scripts/swarm-state.sh task-list --status FAIL --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh metrics --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh task-reopen --id task-001 --owner <session>:<window>.<pane> --reason "重新执行"
skills/auto-tmux/scripts/swarm-state.sh validate --dir /tmp/ai_swarm
skills/auto-tmux/scripts/swarm-state.sh report --dir /tmp/ai_swarm
```

**脚本端到端自测**
```bash
source skills/auto-tmux/scripts/completion.bash
skills/auto-tmux/scripts/auto-tmux-smoke-test.sh
skills/auto-tmux/scripts/validate-auto-tmux.sh
```

**渲染 commander / worker / reviewer 提示词**
```bash
skills/auto-tmux/scripts/render-swarm-prompt.sh commander --session ai-hub --task "拆分并推进任务"
skills/auto-tmux/scripts/render-swarm-prompt.sh worker --target <session>:<window>.<pane> --task "只处理指定子任务"
skills/auto-tmux/scripts/render-swarm-prompt.sh reviewer --session ai-hub --task "审查 worker 产出"
skills/auto-tmux/scripts/swarm-dispatch.sh --role worker --target <session>:<window>.<pane> --task "只处理指定子任务" --send --dry-run
```

## Rules & Constraints

- MUST：优先使用 `scripts/auto-tmux.sh`；直接使用 tmux 原生命令时必须保留同等安全约束。
- MUST：在发送按键前用 `capture-pane` 复核目标上下文；按键操作必须带 `<session>:<window>.<pane>` 绝对定位。
- MUST：遵循 oh-my-tmux 约定，不修改主配置文件；自定义写入 `~/.tmux.conf.local`。
- MUST：批量操作前先 `list-windows`/`list-panes` 建立白名单，避免误控用户窗口。
- SHOULD：救援/确认前先 grep 关键词（如 `(y/n)`、`password`），只对匹配目标发送。
- SHOULD：发送完整命令行时避免先发 `Escape`；先 `C-c` 中断、`C-u` 清行，再用 `send-keys -l` 逐字发送完整命令。
- SHOULD：长 prompt、文件粘贴、跨 worker 分发前运行 `scripts/safety-check.sh`，批量发送先 `--dry-run`。
- SHOULD：pane 处在 Codex UI 时，先发送 `/exit` 回到 shell 再执行命令。
- SHOULD：长任务开启 `pipe-pane` 记录审计；广播完成后立即 `synchronize-panes off`。
- SHOULD：多 worker 修改同一文件、目录或服务前，先用 `swarm-state.sh lock-acquire` 声明锁。
- SHOULD：批量下发先用 `broadcast --dry-run` 预览目标，再决定是否真实发送。
- NEVER：在未知 pane 发送破坏性命令；NEVER 在 root 会话不经确认发送 `Ctrl+C`/`Ctrl+D`。

## Examples

### Example 1：自动给卡住的安装脚本回车确认
- 输入：安装脚本停在 `Proceed? (y/n)`，先用 `topology` 找到真实 target。
- 步骤：
  1) `skills/auto-tmux/scripts/auto-tmux.sh topology` 找到目标 `<session>:<window>.<pane>`。
  2) `skills/auto-tmux/scripts/auto-tmux.sh rescue -t <target> --pattern "(y/n)" --reply y --dry-run` 确认命中。
  3) `skills/auto-tmux/scripts/auto-tmux.sh rescue -t <target> --pattern "(y/n)" --reply y` 发送确认。
- 验收：脚本继续运行，无额外多余输入。

### Example 2：蜂群巡检 + 自动救援
- 输入：4 个 AI 终端分布在 session `ai-hub` 的多个窗口。
- 步骤：
  1) `skills/auto-tmux/scripts/auto-tmux.sh scan --session ai-hub -n 80 --save-dir /tmp/auto-tmux-scan` 收集状态。
  2) 对匹配 `"(y/n)"` 的 pane 运行 `rescue --dry-run`，确认后再真实发送。
  3) 对输出包含 `Traceback` 或 `ERROR` 的 pane，先 `capture-pane` 记录再人工介入。
- 验收：等待确认的终端恢复，未误伤正常任务；巡检日志保存在本地。

### Example 3：快速搭建 oh-my-tmux AI 工作台
- 输入：需要 1 个指挥 + 3 个 worker，并使用仓库内 oh-my-tmux 配置。
- 步骤：
  1) 运行「启用 oh-my-tmux 配置」片段完成软链和本地副本（若已存在跳过）。
  2) `skills/auto-tmux/scripts/auto-tmux.sh hub --session ai-hub --workers 3 --cmd "codex"` 创建 session。
  3) `skills/auto-tmux/scripts/auto-tmux.sh topology --session ai-hub` 确认 worker 窗口存在。
- 验收：前缀键为 `C-a`，状态栏正常；4 个窗口可互相捕获/发送按键。

## FAQ

- Q: 为什么按 `C-b` 无反应？
  - A: oh-my-tmux 默认主前缀是 `C-a`，`C-b` 仅作备用；确保无其他程序占用 `C-a`。
- Q: 如何只广播当前窗口而不影响其他窗口？
  - A: 只对当前窗口执行 `set-window-option synchronize-panes on`，使用完立即关闭。
- Q: 远程发送命令前如何确认当前工作目录？
  - A: `tmux display-message -pt <target> '#{pane_current_path}'`，必要时先 `send-keys 'cd /path' Enter`。

## Troubleshooting

- `no such session/window/pane` → 检查目标名称，先 `list-sessions`/`list-windows` 校验再重试。
- 前缀键冲突 → 查看 `~/.tmux.conf.local` 是否改写前缀；可在其中设置 `set -g prefix C-b #!important`。
- 状态栏样式错乱/重复 → 按 README 建议用 `tmux -f /dev/null -L test` 排查；多半是终端宽字符/字体导致。
- 发送命令没效果 → 目标 pane 可能在 copy-mode；优先用 `tmux display-message -pt <target> '#{pane_in_mode}'` 判断，再用 `tmux send-keys -t <target> -X cancel` 退出；避免用 `Escape`（会触发 Meta 前缀，可能吞掉首字符）。

## References

- `references/index.md`: 导航与文件速览
- `references/getting_started.md`: 术语、oh-my-tmux 最小接入步骤
- `references/api.md`: tmux/oh-my-tmux 常用命令、选项与 gpakosz 特色键位
- `references/automation.md`: `scripts/auto-tmux.sh` 子命令、安全模型与 AI 蜂群协作流程
- `references/safety-policy.md`: 发送、广播、清理、归档和敏感信息处理的安全策略
- `references/swarm-state.md`: 蜂群状态、任务、锁和报告协议
- `references/prompt-templates.md`: commander/worker/reviewer 提示词模板和下发方式
- `references/ai-swarm-collaboration.md`: tmux 蜂群协作历史文档、架构模式、协议、案例和风险限制
- `references/iteration-roadmap.md`: 多轮迭代记录、能力层和后续候选方向
- `references/examples.md`: 蜂群协议脚本与长示例
- `references/troubleshooting.md`: 典型故障到修复路径
- `scripts/auto-tmux.sh`: 安全封装的 tmux 自动化脚本入口
- `scripts/swarm-state.sh`: 蜂群任务、锁、状态和报告脚本
- `scripts/swarm-brief.sh`: 只读生成 tmux 蜂群交接报告
- `scripts/swarm-watch.sh`: 有限轮次巡检 tmux 蜂群输出和状态报告
- `scripts/swarm-archive.sh`: 打包 brief、snapshot 和 swarm state 的交接归档
- `scripts/swarm-board.sh`: 渲染任务、依赖、锁和状态日志的 Markdown 看板
- `scripts/swarm-deps-graph.sh`: 渲染 `deps.tsv` 的 Mermaid 依赖图
- `scripts/swarm-export.sh`: 导出任务、依赖和锁的 JSONL 状态包
- `scripts/swarm-timeline.sh`: 渲染 `status.log` 的 Markdown 时间线
- `scripts/swarm-blockers.sh`: 聚合 BLOCKED/FAIL 任务、锁和最近异常状态
- `scripts/swarm-assign.sh`: 根据 ready tasks 和 worker pane 生成只读分配建议
- `scripts/swarm-health.sh`: 汇总 tmux 与 swarm state 的只读健康检查报告包
- `scripts/record-summary.sh`: 汇总 pane 录制日志并生成复盘摘要
- `scripts/completion.bash`: Bash completion，补全 `auto-tmux.sh` 与 `swarm-state.sh`
- `scripts/safety-check.sh`: 发送/粘贴/分发前检查危险命令、敏感信息和过大 payload
- `scripts/render-swarm-prompt.sh`: commander/worker/reviewer 提示词渲染脚本
- `scripts/swarm-dispatch.sh`: 渲染并可选下发 commander/worker/reviewer 提示词
- `scripts/auto-tmux-smoke-test.sh`: tmux 自动化脚本端到端自测
- `scripts/validate-auto-tmux.sh`: auto-tmux 专属质量门禁
- `assets/oh-my-tmux`: gpakosz/oh-my-tmux submodule 的相对软链接入口
- `assets/tmux-src`: tmux/tmux submodule 的相对软链接入口

## Maintenance

- Sources: `skills/auto-tmux/assets/oh-my-tmux`、`skills/auto-tmux/assets/tmux-src`、蜂群实战提示词、Skill Seeker 生成的抓取材料（如需扩展自动化）。
- Last updated: 2026-05-19
- Known limits: 未涵盖 tmux 插件管理（tpm）及多用户共享权限配置；需时再补充。

## Quality Gate

发布前自检（配合 `auto-skill` 校验脚本）：
1. `description` 已含“capture-pane/send-keys/蜂群”等触发关键词。
2. 「When to Use」「Not For」已覆盖边界；前缀/版本要求清晰。
3. Quick Reference ≤ 20 条且均可直接执行；无长篇解释。
4. ≥3 个端到端示例，含输入/步骤/验收。
5. 长文档放在 `references/` 并可导航；无文档堆砌。
6. 不确定项给出验证路径；禁止虚构 tmux 行为。
7. `bash -n skills/auto-tmux/scripts/auto-tmux.sh`、`bash -n skills/auto-tmux/scripts/swarm-state.sh`、`bash -n skills/auto-tmux/scripts/swarm-brief.sh`、`bash -n skills/auto-tmux/scripts/swarm-watch.sh`、`bash -n skills/auto-tmux/scripts/swarm-archive.sh`、`bash -n skills/auto-tmux/scripts/swarm-board.sh`、`bash -n skills/auto-tmux/scripts/swarm-deps-graph.sh`、`bash -n skills/auto-tmux/scripts/swarm-export.sh`、`bash -n skills/auto-tmux/scripts/swarm-timeline.sh`、`bash -n skills/auto-tmux/scripts/swarm-blockers.sh`、`bash -n skills/auto-tmux/scripts/swarm-assign.sh`、`bash -n skills/auto-tmux/scripts/swarm-health.sh`、`bash -n skills/auto-tmux/scripts/record-summary.sh`、`bash -n skills/auto-tmux/scripts/completion.bash`、`bash -n skills/auto-tmux/scripts/safety-check.sh`、`bash -n skills/auto-tmux/scripts/render-swarm-prompt.sh`、`bash -n skills/auto-tmux/scripts/swarm-dispatch.sh` 与 `bash -n skills/auto-tmux/scripts/validate-auto-tmux.sh` 通过。
8. `skills/auto-tmux/scripts/auto-tmux-smoke-test.sh` 通过或在无 tmux 环境下明确跳过。
9. 运行 `skills/auto-tmux/scripts/validate-auto-tmux.sh` 和 `skills/auto-skill/scripts/validate-skill.sh skills/auto-tmux --strict` 通过。
