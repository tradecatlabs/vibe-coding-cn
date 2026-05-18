# Swarm State and Lock Protocol

`scripts/swarm-state.sh` 是 `auto-tmux` 的最小蜂群状态管理脚本，用于在 tmux 多 AI 协作时记录状态、分配任务、声明锁和汇总报告。

它不依赖数据库、`jq` 或后台服务，默认把状态写入 `/tmp/ai_swarm`。需要隔离不同项目时，用 `--dir DIR` 或环境变量 `AUTO_TMUX_SWARM_DIR` 指定目录。

## 文件结构

```text
/tmp/ai_swarm/
├── status.log
├── tasks.tsv
├── locks/
│   └── <name>.lock.d/
│       ├── owner
│       └── created_at
└── results/
    └── <task-id>.txt
```

## 初始化

```bash
skills/auto-tmux/scripts/swarm-state.sh init
```

指定目录：

```bash
skills/auto-tmux/scripts/swarm-state.sh init --dir /tmp/my-ai-swarm
```

## 状态日志

写入状态：

```bash
skills/auto-tmux/scripts/swarm-state.sh log \
  --target "ai-hub:2.1" \
  --status START \
  --message "开始执行 make test"
```

查看最近状态：

```bash
skills/auto-tmux/scripts/swarm-state.sh status -n 20
```

状态建议：

| 状态 | 含义 |
|:---|:---|
| `START` | 开始任务 |
| `DONE` | 完成任务 |
| `BLOCKED` | 阻塞，等待依赖、输入或权限 |
| `FAIL` | 任务失败，需要 commander 处理 |
| `WAIT` | 等待依赖、输入或门禁 |
| `ERROR` | 出现错误 |
| `HELP` | 请求帮助 |
| `SKIP` | 跳过，已有其他 worker 处理 |
| `LOCK` | 获取锁 |
| `UNLOCK` | 释放锁 |

## 任务管理

新增任务：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-add --id task-001 --text "检查 README 链接"
```

从文本文件批量导入任务：

```bash
cat > /tmp/tasks.txt <<'EOF'
- 检查 README 链接
- 运行 make test
- 汇总风险和下一步
EOF

skills/auto-tmux/scripts/swarm-state.sh task-import --file /tmp/tasks.txt --prefix batch
```

`task-import` 会跳过空行和 `#` 注释行，自动去掉行首 `- ` 或 `* `，并生成 `batch-001` 这类任务 ID。

声明任务依赖：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-depend --id batch-002 --blocked-by batch-001
skills/auto-tmux/scripts/swarm-state.sh task-ready
```

`task-ready` 只列出状态为 `TODO` 且所有依赖都已经 `DONE` 的任务，适合 commander 给空闲 worker 分配下一步。

认领任务：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-claim --id task-001 --owner "ai-hub:2.1"
```

领取下一条 `TODO` 任务：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-next --owner "ai-hub:2.1"
```

完成任务：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-done \
  --id task-001 \
  --owner "ai-hub:2.1" \
  --result "make test passed"
```

标记阻塞：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-block \
  --id task-001 \
  --owner "ai-hub:2.1" \
  --reason "等待用户确认 API key 配置"
```

标记失败：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-fail \
  --id task-001 \
  --owner "ai-hub:2.1" \
  --reason "make test failed"
```

查看任务：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-list
skills/auto-tmux/scripts/swarm-state.sh task-list --status FAIL
skills/auto-tmux/scripts/swarm-state.sh task-list --owner "ai-hub:2.1"
```

重开失败或阻塞任务：

```bash
skills/auto-tmux/scripts/swarm-state.sh task-reopen \
  --id task-001 \
  --owner "ai-hub:2.1" \
  --reason "修复依赖后重新执行"
```

`task-reopen` 会把任务状态改回 `TODO`，同时在状态日志中记录 `REOPEN`。

校验状态一致性：

```bash
skills/auto-tmux/scripts/swarm-state.sh metrics
skills/auto-tmux/scripts/swarm-state.sh validate
skills/auto-tmux/scripts/swarm-board.sh --dir /tmp/ai_swarm --out /tmp/ai-swarm-board.md
```

`metrics` 会按任务状态、owner 和当前锁数量输出摘要，适合 commander 快速判断蜂群是否堵塞。

`validate` 会检查 `tasks.tsv` 表头、字段数量、重复任务 ID、非法状态、终态任务结果文件，以及锁目录中的 `owner` / `created_at`。

`swarm-board.sh` 会把 `tasks.tsv`、`deps.tsv`、锁目录和最近状态日志渲染成 Markdown 看板，适合交接给 commander 或 reviewer。

## 锁管理

锁用于避免多个 worker 同时修改同一文件、目录或服务。

获取锁：

```bash
skills/auto-tmux/scripts/swarm-state.sh lock-acquire \
  --name "README.md" \
  --owner "ai-hub:2.1"
```

释放锁：

```bash
skills/auto-tmux/scripts/swarm-state.sh lock-release \
  --name "README.md" \
  --owner "ai-hub:2.1"
```

查看锁：

```bash
skills/auto-tmux/scripts/swarm-state.sh lock-list
```

清理过期锁前先演练：

```bash
skills/auto-tmux/scripts/swarm-state.sh lock-prune --older-than 3600 --dry-run
skills/auto-tmux/scripts/swarm-state.sh lock-prune --older-than 3600
```

锁使用 `mkdir` 创建目录，具备基本原子性。若锁归属不匹配，默认拒绝释放；确需人工回收时才使用 `--force`。
`lock-prune` 用于 worker 崩溃或会话中断后的过期锁回收，必须先 `--dry-run` 确认目标。

## 报告

生成汇总报告：

```bash
skills/auto-tmux/scripts/swarm-state.sh report
```

报告包含：

- 任务列表。
- 当前锁。
- 最近状态日志。

报告前建议先运行 `validate`，避免把坏状态继续传给 commander 或 reviewer。

## 推荐协作流

1. commander 初始化状态目录。
2. commander 将任务写入 `tasks.tsv`。
3. worker 获取文件或服务锁。
4. worker 用 `task-next` 或 `task-claim` 认领任务并写入 `START`。
5. worker 执行任务，必要时用 `auto-tmux.sh record` 保留日志。
6. worker 完成后写入 `DONE` 和结果；无法继续时写入 `BLOCKED` 或 `FAIL`。
7. commander 用 `report` 汇总状态，再用测试、diff、日志做验收。

## 安全边界

- `swarm-state.sh` 只管理状态，不直接控制 tmux pane。
- 真实发送命令仍必须走 `auto-tmux.sh send` 或 `auto-tmux.sh rescue`。
- 状态文件默认在 `/tmp`，不保存密钥、Token、密码或私密项目内容。
- 锁只能降低冲突概率，不能替代 Git diff、测试和人工验收。
