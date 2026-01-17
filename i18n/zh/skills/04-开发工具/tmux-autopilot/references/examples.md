# Long Examples

## 用例 1：巡检 + 自动救援脚本（bash）

```bash
#!/usr/bin/env bash
# 巡检所有窗口，标注输出并对 (y/n) 提示自动回车
set -euo pipefail

for w in $(tmux list-windows -a -F '#S:#I'); do
  panes=$(tmux list-panes -t "$w" -F '#S:#I.#P')
  for p in $panes; do
    log=$(tmux capture-pane -t "$p" -p -S -80)
    printf '--- [%s] ---\n%s\n' "$p" "$log"
    if echo "$log" | grep -qi "(y/n)"; then
      tmux send-keys -t "$p" "y" Enter
      echo "[action] sent y to $p"
    fi
  done
done
```
- 运行：保存为 `scan_and_rescue.sh`，`chmod +x` 后执行；建议放在 commander 窗口运行。
- 验收：匹配的 pane 自动继续，其他 pane 不受影响。

## 用例 2：批量录制 + 审计

```bash
#!/usr/bin/env bash
# 对 ai-hub 会话所有 pane 开启 pipe-pane 记录
set -euo pipefail

for p in $(tmux list-panes -a -F '#S:#I.#P #{session_name}' | awk '$2=="ai-hub"{print $1}'); do
  tmux pipe-pane -t "$p" -o "cat >> /tmp/${p//[:.]/-}.log"
done
echo "audit pipes enabled under /tmp/*-ai-hub-*.log"
```
- 用于长跑任务或多 AI 协作时保留证据；任务结束后记得 `tmux pipe-pane -t <p> -o cat` 关闭。

## 用例 3：Skill Seeker 抓取 oh-my-tmux 文档并生成补充参考

> 目的：在需要更全面文档时，用仓库自带的 `Skill_Seekers-development` 自动抓取 gpakosz/.tmux 与 README，生成扩展参考文件，再手动筛选进 `references/`。

```bash
cd /home/lenovo/zip/vibe-coding-cn/libs/external/Skill_Seekers-development
# 准备 Python 环境（如未安装）
uv tool install skill-seekers  # 或 pip install skill-seekers

# 直接抓取 GitHub 仓库并生成 skill 雏形
skill-seekers github --repo gpakosz/.tmux --name tmux-oh-my --output /tmp/skill-out

# 可选：抓取 README 站点或 PDF
# skill-seekers scrape --url https://github.com/gpakosz/.tmux --name tmux-oh-my-web --async

# 产物：/tmp/skill-out/tmux-oh-my.zip
# 解压后挑选与 tmux-autopilot 相关的 API/快捷键，整理到 references/api.md 或 examples.md
```
- 这样满足“严选来源 + 自动化抓取”要求，后续人工抽取精华补入本技能。

## 用例 4：多 AI 工作台一键启动（命令行版）

```bash
tmux new-session -d -s ai-hub -n commander 'bash'
for w in worker1 worker2 worker3; do
  tmux new-window -t ai-hub -n "$w" 'kiro-cli chat'
done
tmux select-window -t ai-hub:commander
tmux attach -t ai-hub
```
- 进入后执行用例 1 的巡检脚本即可形成「指挥+工人」模式。
