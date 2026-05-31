<a id="research-tmux-ai-swarm"></a>

# tmux 蜂群协作

> 用 tmux 让多个 AI 终端可感知、可调度、可救援的实验性协作范式。

### 是什么

tmux 蜂群协作是把多个 AI CLI 会话放进同一个 tmux 工作台，通过 `capture-pane` 读取输出、`send-keys` 发送按键、共享状态文件同步进度，再用脚本封装形成 commander + worker 的多终端协作系统。

在当前仓库中，tmux 蜂群协作的可执行能力收敛到 `skills/auto-tmux/`：

- 可执行入口：[auto-tmux skill](../../skills/auto-tmux/SKILL.md)
- 脚本入口：[auto-tmux.sh](../../skills/auto-tmux/scripts/auto-tmux.sh)
- 完整文档：[AI 蜂群协作](../../skills/auto-tmux/references/ai-swarm-collaboration.md)

### 解决什么问题

1. 多个 AI 会话互相不可见，导致重复工作、信息断裂和人工来回搬运。
2. AI CLI 卡在确认、报错或长任务等待时，需要人工不断盯屏。
3. 多任务并行时缺少统一巡检、分工、日志和验收证据。
4. 多终端协作缺少安全边界，容易误发命令或控制错误窗口。

### 当前判断

这是一种值得保留的实验性方法，但必须脚本化、目标化和门禁化。

推荐路线不是让 AI 直接随意执行 `tmux send-keys`，而是先使用 `skills/auto-tmux/scripts/auto-tmux.sh` 封装：

```bash
skills/auto-tmux/scripts/auto-tmux.sh hub --session ai-hub --workers 3 --cmd "codex"
skills/auto-tmux/scripts/auto-tmux.sh topology --session ai-hub
skills/auto-tmux/scripts/auto-tmux.sh scan --session ai-hub -n 80
```

这个封装层能做到：

- 先确认 target 存在。
- 默认对输出脱敏。
- 发送前打印目标上下文。
- 危险命令默认拒绝。
- 巡检、救援和录制都可重复执行。

### 适用场景

- 多个 AI CLI 并行处理互不冲突的子任务。
- commander 统一分配任务、巡检 worker、收集证据。
- 需要观察长时间运行的安装、测试、构建或调试任务。
- 需要把卡住的低风险确认交给脚本化救援。
- 需要保留 pane 日志，用于复盘、审计和验收。

### 不适用场景

- 涉及生产数据库、云资源删除、密钥输入和敏感凭证展示。
- 需要图形界面、复杂交互或强实时反馈的操作。
- 无法接受误输入、误中断或误控制的任务。
- 没有明确任务边界、锁、日志和验收标准的多 Agent 并发。

### 采用建议

最小可用结构：

```text
ai-hub
├── commander
├── worker1
├── worker2
└── worker3
```

推荐协议：

1. commander 负责拆任务、巡检、救援和最终验收。
2. worker 一次只处理一个明确子任务。
3. 所有发送动作必须使用完整 `<session>:<window>.<pane>` target。
4. 救援先 dry-run，再真实执行。
5. 长任务必须 record，完成后汇报命令、diff、测试和风险。

### 风险

| 风险 | 说明 | 约束 |
|:---|:---|:---|
| 误控 pane | target 错误会向错误窗口发命令 | 先 `topology`，再 `capture` |
| 死循环 | 多个 AI 互相救援或互相触发 | 设置 commander 单点调度 |
| 文件冲突 | 多 worker 改同一文件 | 子任务分工和锁机制 |
| 信息泄露 | capture 读到 token 或密码 | 默认脱敏，隔离敏感会话 |
| 幻觉放大 | 多 AI 同时错误执行 | 以测试、diff、日志和人工验收兜底 |

### 后续观察点

- 是否需要把 `/tmp/ai_swarm/tasks.json` 标准化为 schema。
- 是否需要增加 worker 状态机和锁文件脚本。
- 是否需要接入 GitHub Actions、Prometheus 或本地 Web 面板。
- 是否需要把 commander / worker prompt 模板独立成可复用 prompt。
