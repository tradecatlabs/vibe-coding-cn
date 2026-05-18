# AI 蜂群协作

> 基于 tmux 的多 AI Agent 协作系统设计与实现。

本文从历史文档 `AI蜂群协作-tmux多Agent协作系统.md` 整理而来，并按当前仓库结构升级为
`auto-tmux` skill 的长期参考资料。当前推荐优先使用
`skills/auto-tmux/scripts/auto-tmux.sh`，直接 tmux 命令作为兜底。

## 1. 核心思想

传统 AI 编程助手的局限：

- 单一会话，无法感知其他任务。
- 遇到等待、确认、卡住时需要人工干预。
- 多任务并行时缺少协调。
- 多个 AI 容易重复工作、争抢文件或互相覆盖。

tmux 蜂群协作的核心是：让 AI 不再只是孤立会话，而是通过 tmux 获得感知、控制和协调能力。

| 能力 | 实现方式 | 效果 |
|:---|:---|:---|
| 感知 | `capture-pane` / `auto-tmux.sh capture` | 读取指定终端输出 |
| 控制 | `send-keys` / `auto-tmux.sh send` | 向指定终端发送按键或命令 |
| 巡检 | `auto-tmux.sh scan` | 批量检查多个 pane 状态 |
| 救援 | `auto-tmux.sh rescue` | 对等待确认、卡住或异常的 pane 做最小干预 |
| 记录 | `pipe-pane` / `auto-tmux.sh record` | 保留长任务审计日志 |
| 协调 | 共享状态文件 + 明确 target | 任务同步、分工、避免冲突 |

```text
传统模式: 人 <-> AI1, 人 <-> AI2, 人 <-> AI3

蜂群模式: 人 -> commander -> worker1 / worker2 / worker3
                         \-> scan / capture / rescue / record
```

关键突破不是“让 AI 自动乱控终端”，而是把终端控制变成可观察、可定位、可审计、可回滚的工程动作。

## 2. 技术原理

tmux 的基本对象是：

```text
session
└── window
    └── pane
```

`auto-tmux` 要求所有控制都使用完整 target：

```text
<session>:<window>.<pane>
```

不要假设 pane 一定是 `.0`。不同 tmux 配置可能让 pane index 从 1 开始。正确做法是先查询拓扑：

```bash
skills/auto-tmux/scripts/auto-tmux.sh topology --session ai-hub
```

或用原生命令取真实 target：

```bash
target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"
```

## 3. 最小工作台

创建一个 commander + 3 个 worker 的工作台：

```bash
skills/auto-tmux/scripts/auto-tmux.sh hub --session ai-hub --workers 3 --cmd "codex"
```

查看拓扑：

```bash
skills/auto-tmux/scripts/auto-tmux.sh topology --session ai-hub
```

读取某个 worker：

```bash
target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"
skills/auto-tmux/scripts/auto-tmux.sh capture -t "$target" -n 120
```

发送任务：

```bash
skills/auto-tmux/scripts/auto-tmux.sh send -t "$target" --text "请运行 make test 并汇报失败原因" --enter
```

等待完成信号：

```bash
skills/auto-tmux/scripts/auto-tmux.sh wait -t "$target" --pattern "done|完成|Tests passed" --timeout 300
```

## 4. 协作协议

### 4.1 角色

| 角色 | 职责 |
|:---|:---|
| commander | 分配任务、巡检状态、救援卡住任务、汇总结果 |
| worker | 处理单一明确任务，输出状态、证据、风险和结果 |
| gate | 测试、lint、CI、脚本、人工确认等外部门禁 |

### 4.2 状态目录

可选共享状态目录：

```text
/tmp/ai_swarm/
├── status.log
├── tasks.json
├── locks/
└── results/
```

最小状态格式：

```text
[HH:MM:SS] [target] [STATUS] description
```

常用状态：

```text
[START]  开始任务
[DONE]   完成任务
[WAIT]   等待依赖或确认
[ERROR]  出现错误
[HELP]   请求帮助
[SKIP]   跳过，已有其他 worker 处理
```

### 4.3 协作规则

1. **先查后做**：开始前先 `topology` / `scan`，确认其他 worker 状态。
2. **目标明确**：发送命令必须指向明确 target，不使用模糊窗口号。
3. **单点职责**：一个 worker 一次只处理一个明确任务。
4. **避免冲突**：涉及同一文件、同一服务、同一配置时先加锁或等待。
5. **主动救援**：发现等待确认、卡死或明显错误时先 `capture`，再 `rescue --dry-run`。
6. **保留证据**：长任务开启 `record`，关键检查保存 scan 日志。
7. **人工兜底**：危险操作、敏感凭证、生产环境变更必须人工确认。

## 5. 架构模式

### 5.1 P2P 对等模式

```text
worker1 <-> worker2
   ^          ^
   |          |
worker3 <-> worker4
```

适合：简单探索、信息收集、互相巡检。

风险：缺少统一调度，容易重复劳动或互相干扰。

### 5.2 Master-Worker 主从模式

```text
commander
├── worker1
├── worker2
└── worker3
```

适合：复杂项目、明确分工、需要统一验收的任务。

当前仓库默认推荐这个模式，因为它更容易控制边界和回收证据。

### 5.3 Pipeline 流水线模式

```text
analysis -> design -> implementation -> test
```

适合：有明确阶段的工作，例如需求分析、方案设计、实现、测试。

风险：前一阶段输出质量差会向后传播，需要每阶段设置门禁。

### 5.4 Hybrid 混合模式

```text
commander
├── analysis group
├── implementation group
└── test group
```

适合：较大项目，多组并行。

风险：协调成本高，必须有状态记录、锁和强制验收标准。

## 6. 实战流程

### 6.1 多服务并行开发

示例分工：

```text
commander  任务分配、巡检、验收
worker1    data-service
worker2    trading-service
worker3    telegram-service
```

巡检：

```bash
skills/auto-tmux/scripts/auto-tmux.sh scan --session ai-hub -n 100 --save-dir /tmp/auto-tmux-scan
```

发现错误：

```bash
skills/auto-tmux/scripts/auto-tmux.sh scan --session ai-hub --pattern "ERROR|Traceback|failed"
```

### 6.2 代码审计 + 自动修复

推荐分工：

```text
worker1: 审计代码，输出问题列表
worker2: 根据问题列表修复
commander: 验收 diff、测试和风险
```

最小规则：

- 审计 worker 不直接修复。
- 修复 worker 不扩大范围。
- commander 只接受有测试、diff 和风险说明的结果。

### 6.3 自动值守

自动值守只能用于低风险场景，例如等待测试、安装确认、日志观察。

推荐先 dry-run：

```bash
target="$(tmux list-panes -t ai-hub:worker1 -F '#S:#I.#P' | head -n 1)"
skills/auto-tmux/scripts/auto-tmux.sh rescue -t "$target" --pattern "(y/n)" --reply y --dry-run
```

确认后再执行：

```bash
skills/auto-tmux/scripts/auto-tmux.sh rescue -t "$target" --pattern "(y/n)" --reply y
```

## 7. 提示词模板

### 7.1 Worker 模板

```markdown
你是 tmux AI 蜂群中的 worker。

你的职责：
1. 只处理分配给你的单一任务。
2. 开始前确认任务目标、边界和验收标准。
3. 执行中保留关键命令、错误和测试结果。
4. 完成后输出：状态、修改文件、验证结果、风险。
5. 不主动修改无关文件，不覆盖其他 worker 的成果。
```

### 7.2 Commander 模板

```markdown
你是 tmux AI 蜂群中的 commander。

你的职责：
1. 把总任务拆成互不冲突的 worker 子任务。
2. 用 topology / scan / capture 读取 worker 状态。
3. 对卡住任务先 dry-run 救援，再最小干预。
4. 汇总每个 worker 的产出、测试和风险。
5. 最终以测试、diff、日志和提交记录作为验收依据。
```

### 7.3 巡检汇报模板

```markdown
| target | 状态 | 当前任务 | 证据 | 下一步 |
|:---|:---|:---|:---|:---|
| ai-hub:1.1 | running | 执行测试 | 输出 make test | 等待完成 |
| ai-hub:2.1 | blocked | 等待确认 | 出现 (y/n) | rescue dry-run |
| ai-hub:3.1 | failed | 构建失败 | Traceback | 分配修复 |
```

## 8. 最佳实践

### 8.1 命名规范

```text
session:
  ai-hub      AI 协作工作台
  dev         开发任务
  monitor     监控任务

window:
  commander   指挥官
  worker1     工作节点 1
  worker2     工作节点 2
  worker3     工作节点 3
```

### 8.2 日志规范

```text
[time] [target] [START] description
[time] [target] [DONE] description
[time] [target] [WAIT] description
[time] [target] [ERROR] description
```

### 8.3 安全建议

1. 不自动确认危险操作。
2. 不在含敏感凭证的 pane 做批量 capture。
3. 不对未知 target 发送按键。
4. 广播或同步 pane 后必须立即关闭。
5. 长任务要记录日志，方便审计。
6. 任何生产环境操作必须人工确认。

## 9. 风险与限制

| 风险 | 描述 | 缓解措施 |
|:---|:---|:---|
| 误操作 | AI 向错误 pane 发送命令 | 使用完整 target，先 topology，再 capture |
| 死循环 | AI 互相触发或反复救援 | 使用 dry-run、冷却时间和人工确认 |
| 资源竞争 | 多 worker 同时修改同一文件 | 使用任务锁和明确分工 |
| 信息泄露 | capture 读到敏感信息 | 默认脱敏，隔离敏感会话 |
| 架构漂移 | 多 worker 各自为政 | commander 统一验收，门禁拦截 |

不适用场景：

- 需要图形界面的操作。
- 涉及密码输入、密钥展示或私密生产会话。
- 高风险数据库、云资源、生产环境变更。
- 无法容忍误输入或误中断的任务。

## 10. 扩展方向

- 跨机器协作：通过 SSH 包装远程 tmux，但必须先解决权限、审计和网络边界。
- Web 面板：把 topology、scan、record 状态暴露为只读监控页面。
- 智能调度：根据 worker 空闲程度、任务类型和失败状态分配任务。
- CI 集成：让 GitHub Actions 或本地 gate 接收 worker 结果，统一决定是否通过。
- 状态机治理：用 JSON schema 约束 `/tmp/ai_swarm/tasks.json` 与 `results/`。

## 11. 快速参考

```bash
# 查看拓扑
skills/auto-tmux/scripts/auto-tmux.sh topology --session ai-hub

# 扫描状态
skills/auto-tmux/scripts/auto-tmux.sh scan --session ai-hub -n 80

# 捕获输出
skills/auto-tmux/scripts/auto-tmux.sh capture -t <target> -n 120

# 发送任务
skills/auto-tmux/scripts/auto-tmux.sh send -t <target> --text "任务内容" --enter

# 救援等待确认
skills/auto-tmux/scripts/auto-tmux.sh rescue -t <target> --pattern "(y/n)" --reply y --dry-run
skills/auto-tmux/scripts/auto-tmux.sh rescue -t <target> --pattern "(y/n)" --reply y

# 记录日志
skills/auto-tmux/scripts/auto-tmux.sh record start -t <target> --dir /tmp/auto-tmux-records
skills/auto-tmux/scripts/auto-tmux.sh record stop -t <target>
```
