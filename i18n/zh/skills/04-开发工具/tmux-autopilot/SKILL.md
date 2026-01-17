---
name: tmux-autopilot
description: "tmux 自动化操控：读取/广播/救援 session|window|pane，基于 oh-my-tmux 配置安全地让 AI 自控/互控终端。触发：需要 capture-pane/send-keys、批量巡检、蜂群 AI 协作、卡死救援或快速查看快捷键。"
---

# tmux-autopilot Skill

让 AI 像熟练运维一样操作 tmux：读取终端输出、发送按键、批量巡检、协作/救援其他终端，默认兼容 `libs/external/.tmux`（gpakosz/oh-my-tmux）。

## When to Use This Skill

触发条件（满足其一即可）：
- 需要远程读取/复制某个 tmux pane 的最新输出（日志、提示、错误）。
- 需要向指定 pane 发送按键/命令（确认 `y`、`Enter`、`Ctrl+C`、广播同一窗口）。
- 需要批量巡检/接管多 AI 终端（蜂群协作、自动救援卡死任务）。
- 需要快速回忆 oh-my-tmux 快捷键、前缀或同步面板操作。
- 需要在当前仓库复用 `libs/external/.tmux` 配置并避免修改主配置。

## Not For / Boundaries

- 不用于执行非 tmux 环境（目标不存在时先创建 session/window/pane）。
- 不直接编辑 `~/.tmux.conf` / `.tmux.conf`（遵循 oh-my-tmux：修改请放到 `.tmux.conf.local`）。
- 不盲发破坏性按键：`kill-server`、`rm -rf` 等必须先 capture-pane 确认目标上下文。
- 如果 tmux 版本 < 2.6，需先升级再使用本技能的命令组合。

## Quick Reference

### 常用模式（≤20 条，直接复制即用）

**查看快捷键帮助**（oh-my-tmux 双前缀：主 `C-a`，备用 `C-b`，前缀后按 `?`）
```text
[按] <prefix> ?
```

**枚举拓扑（session/window/pane）**
```bash
tmux list-sessions
tmux list-windows -a -F '#S:#I:#W#F'
tmux list-panes   -a -F '#S:#I.#P #{pane_current_command} #{pane_title}'
```

**读取指定 pane 最近 120 行**
```bash
tmux capture-pane -t <session>:<window>.<pane> -p -S -120
```

**向指定 pane 发送确认键**
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

**一次扫描全部窗口并截取最近输出（蜂群巡检骨架）**
```bash
for w in $(tmux list-windows -a -F '#S:#I'); do
  tmux capture-pane -t "$w" -p -S -80 | sed "s/^/[$w] /";
done
```

**远程救援：发现等待输入即发送 y**
```bash
target="0:3.0"  # 示例
tmux capture-pane -t "$target" -p -S -50 | grep -qi "(y/n)" && \
  tmux send-keys -t "$target" "y" Enter
```

**新建 AI 蜂群工作台（1 指挥 + 3 工人）**
```bash
tmux new-session -d -s ai-hub -n commander 'bash'
tmux new-window  -t ai-hub -n worker1 'kiro-cli chat'
tmux new-window  -t ai-hub -n worker2 'kiro-cli chat'
tmux new-window  -t ai-hub -n worker3 'kiro-cli chat'
tmux attach -t ai-hub
```

**启用 oh-my-tmux 配置（仓库内版本）**
```bash
ln -sfn /home/lenovo/zip/vibe-coding-cn/libs/external/.tmux/.tmux.conf ~/.tmux.conf
cp -n /home/lenovo/zip/vibe-coding-cn/libs/external/.tmux/.tmux.conf.local ~/.tmux.conf.local
```

**记录 pane 输出到文件**
```bash
tmux pipe-pane -t <session>:<window>.<pane> -o 'cat >> /tmp/tmux-<session>-<window>-<pane>.log'
```

## Rules & Constraints

- MUST：在发送按键前用 `capture-pane` 复核目标上下文；按键操作必须带 `<session>:<window>.<pane>` 绝对定位。
- MUST：遵循 oh-my-tmux 约定，不修改主配置文件；自定义写入 `~/.tmux.conf.local`。
- MUST：批量操作前先 `list-windows`/`list-panes` 建立白名单，避免误控用户窗口。
- SHOULD：救援/确认前先 grep 关键词（如 `(y/n)`、`password`），只对匹配目标发送。
- SHOULD：长任务开启 `pipe-pane` 记录审计；广播完成后立即 `synchronize-panes off`。
- NEVER：在未知 pane 发送破坏性命令；NEVER 在 root 会话不经确认发送 `Ctrl+C`/`Ctrl+D`。

## Examples

### Example 1：自动给卡住的安装脚本回车确认
- 输入：安装脚本停在 `Proceed? (y/n)`，位置在 `0:3.0`。
- 步骤：
  1) `tmux capture-pane -t 0:3.0 -p -S -50 | grep -qi "(y/n)"` 确认等待输入。
  2) `tmux send-keys -t 0:3.0 "y" Enter` 发送确认。
- 验收：脚本继续运行，无额外多余输入。

### Example 2：蜂群巡检 + 自动救援
- 输入：4 个 AI 终端分布在 session `ai-hub` 的多个窗口。
- 步骤：
  1) 运行 Quick Reference 巡检循环收集最近 80 行并观察状态。
  2) 对匹配 `"(y/n)"` 的 pane 触发「远程救援」片段自动发 `y`。
  3) 对输出包含 `Traceback` 或 `ERROR` 的 pane，先 `capture-pane` 记录再人工介入。
- 验收：等待确认的终端恢复，未误伤正常任务；巡检日志保存在本地。

### Example 3：快速搭建 oh-my-tmux AI 工作台
- 输入：需要 1 个指挥 + 3 个 worker，并使用仓库内 oh-my-tmux 配置。
- 步骤：
  1) 运行「启用 oh-my-tmux 配置」片段完成软链和本地副本（若已存在跳过）。
  2) 运行「新建 AI 蜂群工作台」片段创建 session 并 attach。
  3) 在 commander pane 使用「枚举拓扑」确认 worker 窗口存在。
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
- 发送命令没效果 → 目标 pane 可能在 copy-mode，先 `tmux send-keys -t <target> Escape` 退出再重发。

## References

- `references/index.md`: 导航与文件速览
- `references/getting_started.md`: 术语、oh-my-tmux 最小接入步骤
- `references/api.md`: tmux/oh-my-tmux 常用命令、选项与 gpakosz 特色键位
- `references/examples.md`: 蜂群协议脚本与长示例
- `references/troubleshooting.md`: 典型故障到修复路径

## Maintenance

- Sources: `libs/external/.tmux/README.md`、蜂群实战提示词、Skill Seeker 生成的抓取材料（如需扩展自动化）。
- Last updated: 2026-01-17
- Known limits: 未涵盖 tmux 插件管理（tpm）及多用户共享权限配置；需时再补充。

## Quality Gate

发布前自检（配合 `claude-skills` 校验脚本）：
1. `description` 已含“capture-pane/send-keys/蜂群”等触发关键词。
2. 「When to Use」「Not For」已覆盖边界；前缀/版本要求清晰。
3. Quick Reference ≤ 20 条且均可直接执行；无长篇解释。
4. ≥3 个端到端示例，含输入/步骤/验收。
5. 长文档放在 `references/` 并可导航；无文档堆砌。
6. 不确定项给出验证路径；禁止虚构 tmux 行为。
7. 运行 `i18n/zh/skills/00-元技能/claude-skills/scripts/validate-skill.sh i18n/zh/skills/04-开发工具/tmux-autopilot` 通过。
