# AI 蜂群协作技术文档

> 基于 tmux 的多 AI Agent 协作系统设计与实现

---

## 目录

1. [核心思想](#1-核心思想)
2. [技术原理](#2-技术原理)
3. [命令参考](#3-命令参考)
4. [协作协议](#4-协作协议)
5. [架构模式](#5-架构模式)
6. [实战案例](#6-实战案例)
7. [提示词模板](#7-提示词模板)
8. [最佳实践](#8-最佳实践)
9. [风险与限制](#9-风险与限制)
10. [扩展方向](#10-扩展方向)

---

## 1. 核心思想

### 1.1 问题背景

传统 AI 编程助手的局限：
- 单一会话，无法感知其他任务
- 遇到等待/确认时需要人工干预
- 多任务并行时无法协调
- 重复工作，资源浪费

### 1.2 解决方案

利用 tmux 的终端复用能力，赋予 AI：

| 能力 | 实现方式 | 效果 |
|:---|:---|:---|
| **感知** | `capture-pane` | 读取任意终端内容 |
| **控制** | `send-keys` | 向任意终端发送按键 |
| **协调** | 共享状态文件 | 任务同步与分工 |

### 1.3 核心洞察

```
传统模式: 人 ←→ AI₁, 人 ←→ AI₂, 人 ←→ AI₃ (人是瓶颈)

蜂群模式: 人 → AI₁ ←→ AI₂ ←→ AI₃ (AI 自主协作)
```

**关键突破**：AI 不再是孤立的，而是可以互相感知、通讯、控制的集群。

---

## 2. 技术原理

### 2.1 tmux 架构

```
┌─────────────────────────────────────────────┐
│                 tmux server                  │
├─────────────────────────────────────────────┤
│  Session 0                                   │
│  ├── Window 0:1 [AI-1] ◄──┐                 │
│  ├── Window 0:2 [AI-2] ◄──┼── 互相可见/控制 │
│  ├── Window 0:3 [AI-3] ◄──┤                 │
│  └── Window 0:4 [AI-4] ◄──┘                 │
└─────────────────────────────────────────────┘
```

### 2.2 数据流

```
┌─────────┐  capture-pane   ┌─────────┐
│  AI-1   │ ◄───────────────│  AI-4   │
│ (执行)  │                 │ (监控)  │
└─────────┘  send-keys      └─────────┘
     ▲      ───────────────►     │
     │                           │
     └───────── 控制流 ──────────┘
```

### 2.3 通信机制

| 机制 | 方向 | 延迟 | 用途 |
|:---|:---|:---|:---|
| `capture-pane` | 读取 | 即时 | 获取终端输出 |
| `send-keys` | 写入 | 即时 | 发送命令/按键 |
| 共享文件 | 双向 | 文件IO | 状态持久化 |

---

## 3. 命令参考

### 3.1 信息获取

```bash
# 列出所有会话
tmux list-sessions

# 列出所有窗口
tmux list-windows -a

# 列出所有窗格
tmux list-panes -a

# 获取当前窗口标识
echo $TMUX_PANE
```

### 3.2 内容读取

```bash
# 读取指定窗口内容（最近 N 行）
tmux capture-pane -t <session>:<window> -p -S -<N>

# 示例：读取会话 0 窗口 1 最近 100 行
tmux capture-pane -t 0:1 -p -S -100

# 读取并保存到文件
tmux capture-pane -t 0:1 -p -S -500 > /tmp/window1.log

# 批量读取所有窗口
for w in $(tmux list-windows -a -F '#{session_name}:#{window_index}'); do
  echo "=== $w ==="
  tmux capture-pane -t "$w" -p -S -30
done
```

### 3.3 发送控制

```bash
# 发送文本 + 回车
tmux send-keys -t 0:1 "ls -la" Enter

# 发送确认
tmux send-keys -t 0:1 "y" Enter

# 发送特殊按键
tmux send-keys -t 0:1 C-c        # Ctrl+C
tmux send-keys -t 0:1 C-d        # Ctrl+D
tmux send-keys -t 0:1 C-z        # Ctrl+Z
tmux send-keys -t 0:1 Escape     # ESC
tmux send-keys -t 0:1 Up         # 上箭头
tmux send-keys -t 0:1 Down       # 下箭头
tmux send-keys -t 0:1 Tab        # Tab

# 组合操作
tmux send-keys -t 0:1 C-c        # 先中断
tmux send-keys -t 0:1 "cd /tmp" Enter  # 再执行新命令
```

### 3.4 窗口管理

```bash
# 创建新窗口
tmux new-window -n "ai-worker"

# 创建并执行命令
tmux new-window -n "ai-1" "kiro-cli chat"

# 关闭窗口
tmux kill-window -t 0:1

# 重命名窗口
tmux rename-window -t 0:1 "monitor"
```

---

## 4. 协作协议

### 4.1 状态定义

```bash
# 状态文件位置
/tmp/ai_swarm/
├── status.log      # 全局状态日志
├── tasks.json      # 任务队列
├── locks/          # 任务锁
│   ├── task_001.lock
│   └── task_002.lock
└── results/        # 结果存储
    ├── ai_1.json
    └── ai_2.json
```

### 4.2 状态格式

```bash
# 状态日志格式
[HH:MM:SS] [窗口ID] [状态] 描述

# 示例
[08:15:30] [0:1] [START] 开始处理 data-service 代码审计
[08:16:45] [0:1] [DONE] 完成代码审计，发现 5 个问题
[08:16:50] [0:2] [WAIT] 等待 0:1 审计结果
[08:17:00] [0:2] [START] 开始修复问题
```

### 4.3 协作规则

| 规则 | 描述 | 实现 |
|:---|:---|:---|
| **先查后做** | 开始前扫描其他终端 | `capture-pane` 全扫 |
| **避免冲突** | 相同任务只做一次 | 检查 locks 目录 |
| **主动救援** | 发现卡住主动帮助 | 检测 `[y/n]` 等待 |
| **状态广播** | 完成后通知其他 AI | 写入 status.log |

### 4.4 冲突处理

```
场景：AI-1 和 AI-2 同时要修改同一文件

解决方案：
1. 创建任务前先检查锁
2. 获取锁后才能执行
3. 完成后释放锁

# 获取锁
if [ ! -f /tmp/ai_swarm/locks/file_x.lock ]; then
  echo "$TMUX_PANE" > /tmp/ai_swarm/locks/file_x.lock
  # 执行任务
  rm /tmp/ai_swarm/locks/file_x.lock
fi
```

---

## 5. 架构模式

### 5.1 对等模式 (P2P)

```
┌─────┐     ┌─────┐
│ AI₁ │◄───►│ AI₂ │
└──┬──┘     └──┬──┘
   │           │
   ▼           ▼
┌─────┐     ┌─────┐
│ AI₃ │◄───►│ AI₄ │
└─────┘     └─────┘

特点：所有 AI 平等，互相监控
适用：简单任务，无明确依赖
```

### 5.2 主从模式 (Master-Worker)

```
        ┌──────────┐
        │ AI-Master│
        │  (指挥官) │
        └────┬─────┘
             │ 分发/监控
    ┌────────┼────────┐
    ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐
│Worker│ │Worker│ │Worker│
│ AI-1 │ │ AI-2 │ │ AI-3 │
└──────┘ └──────┘ └──────┘

特点：一个指挥，多个执行
适用：复杂项目，需要统一协调
```

### 5.3 流水线模式 (Pipeline)

```
┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐
│ AI₁ │───►│ AI₂ │───►│ AI₃ │───►│ AI₄ │
│分析 │    │设计 │    │实现 │    │测试 │
└─────┘    └─────┘    └─────┘    └─────┘

特点：任务串行流转
适用：有明确阶段的工作流
```

### 5.4 混合模式

```
           ┌──────────┐
           │ AI-Master│
           └────┬─────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
┌──────┐   ┌──────┐    ┌──────┐
│分析组 │   │开发组 │    │测试组 │
├──────┤   ├──────┤    ├──────┤
│AI-1  │   │AI-3  │    │AI-5  │
│AI-2  │   │AI-4  │    │AI-6  │
└──────┘   └──────┘    └──────┘

特点：分组协作 + 统一调度
适用：大型项目，多团队并行
```

---

## 6. 实战案例

### 6.1 案例：多服务并行开发

**场景**：同时开发 data-service、trading-service、telegram-service

**配置**：
```bash
# 窗口分配
0:1 - AI-Master (指挥官)
0:2 - AI-Data (data-service)
0:3 - AI-Trading (trading-service)
0:4 - AI-Telegram (telegram-service)
```

**指挥官提示词**：
```
你是项目指挥官，负责协调 3 个开发 AI。

每 2 分钟执行一次扫描：
for w in 2 3 4; do
  echo "=== 窗口 0:$w ===" 
  tmux capture-pane -t "0:$w" -p -S -20
done

发现问题时：
- 卡住等待 → send-keys 确认
- 报错 → 分析并给出建议
- 完成 → 记录并分配下一任务
```

### 6.2 案例：代码审计 + 自动修复

**场景**：AI-1 审计代码，AI-2 实时修复

**流程**：
```
AI-1 (审计):
1. 扫描代码，输出问题列表
2. 每发现一个问题，写入 /tmp/ai_swarm/issues.log

AI-2 (修复):
1. 监控 issues.log
2. 读取新问题
3. 自动修复
4. 标记完成
```

### 6.3 案例：7x24 值守

**场景**：AI 互相监控，自动救援

**配置**：
```bash
# 每个 AI 的监控逻辑
while true; do
  for w in $(tmux list-windows -a -F '#{window_index}'); do
    output=$(tmux capture-pane -t "0:$w" -p -S -5)
    
    # 检测卡住
    if echo "$output" | grep -q "\[y/n\]"; then
      tmux send-keys -t "0:$w" "y" Enter
      echo "已帮助窗口 $w 确认"
    fi
    
    # 检测错误
    if echo "$output" | grep -qi "error\|failed"; then
      echo "窗口 $w 出现错误，需要关注"
    fi
  done
  sleep 30
done
```

---

## 7. 提示词模板

### 7.1 基础版（Worker）

```markdown
## AI 蜂群协作模式

你在 tmux 环境中工作，可以感知和协助其他终端。

### 命令
# 扫描所有终端
tmux list-windows -a

# 读取终端内容
tmux capture-pane -t <session>:<window> -p -S -100

### 行为
- 开始任务前先扫描环境
- 发现相关任务主动协调
- 完成后广播状态
```

### 7.2 完整版（Worker）

```markdown
## 🐝 AI 蜂群协作协议 v2.0

你是 tmux 多终端 AI 集群中的一员。

### 感知能力

# 列出所有窗口
tmux list-windows -a

# 读取指定窗口（最近 100 行）
tmux capture-pane -t <session>:<window> -p -S -100

# 批量扫描
for w in $(tmux list-windows -a -F '#{session_name}:#{window_index}'); do
  echo "=== $w ===" && tmux capture-pane -t "$w" -p -S -20
done

### 控制能力

# 发送命令
tmux send-keys -t <窗口> "<命令>" Enter

# 发送确认
tmux send-keys -t <窗口> "y" Enter

# 中断任务
tmux send-keys -t <窗口> C-c

### 协作规则

1. **主动感知**：任务开始前扫描其他终端
2. **避免冲突**：相同任务不重复执行
3. **主动救援**：发现等待/卡住主动帮助
4. **状态广播**：完成后写入共享日志

### 状态同步

# 广播
echo "[$(date +%H:%M:%S)] [$TMUX_PANE] [DONE] <描述>" >> /tmp/ai_swarm/status.log

# 读取
tail -20 /tmp/ai_swarm/status.log

### 检查时机

- 🚦 任务开始前
- ⏳ 等待依赖时
- ✅ 任务完成后
- ❌ 遇到错误时
```

### 7.3 指挥官版（Master）

```markdown
## 🎖️ AI 集群指挥官协议

你是 AI 蜂群的指挥官，负责监控和协调所有 Worker AI。

### 核心职责

1. **全局监控**：定期扫描所有终端状态
2. **任务分配**：根据能力分配任务
3. **冲突解决**：发现重复工作时协调
4. **故障救援**：发现卡住/错误时介入
5. **进度汇总**：汇总各终端成果

### 监控命令

# 全局扫描（每 2 分钟执行）
echo "========== $(date) 状态扫描 =========="
for w in $(tmux list-windows -a -F '#{session_name}:#{window_index}'); do
  echo "--- $w ---"
  tmux capture-pane -t "$w" -p -S -15
done

### 干预命令

# 帮助确认
tmux send-keys -t <窗口> "y" Enter

# 中断错误任务
tmux send-keys -t <窗口> C-c

# 发送新指令
tmux send-keys -t <窗口> "<指令>" Enter

### 状态判断

检测到以下模式时介入：
- `[y/n]` `[Y/n]` `确认` → 需要确认
- `Error` `Failed` `Exception` → 出现错误
- `Waiting` `Blocked` → 任务阻塞
- 长时间无输出 → 可能卡死

### 汇报格式

每次扫描后输出：
| 窗口 | 状态 | 当前任务 | 备注 |
|:---|:---|:---|:---|
| 0:1 | ✅ 正常 | 代码审计 | 进度 80% |
| 0:2 | ⏳ 等待 | 等待确认 | 已自动确认 |
| 0:3 | ❌ 错误 | 编译失败 | 需要关注 |
```

---

## 8. 最佳实践

### 8.1 初始化流程

```bash
# 1. 创建共享目录
mkdir -p /tmp/ai_swarm/{locks,results}
touch /tmp/ai_swarm/status.log

# 2. 开启 tmux 会话
tmux new-session -d -s ai

# 3. 创建多个窗口
tmux new-window -t ai -n "master"
tmux new-window -t ai -n "worker-1"
tmux new-window -t ai -n "worker-2"
tmux new-window -t ai -n "worker-3"

# 4. 在每个窗口启动 AI
tmux send-keys -t ai:master "kiro-cli chat" Enter
tmux send-keys -t ai:worker-1 "kiro-cli chat" Enter
# ...

# 5. 发送蜂群提示词
```

### 8.2 命名规范

```bash
# 会话命名
ai          # AI 工作会话
dev         # 开发会话
monitor     # 监控会话

# 窗口命名
master      # 指挥官
worker-N    # 工作节点
data        # data-service 专用
trading     # trading-service 专用
```

### 8.3 日志规范

```bash
# 状态日志
[时间] [窗口] [状态] 描述

# 状态类型
[START]  - 开始任务
[DONE]   - 完成任务
[WAIT]   - 等待中
[ERROR]  - 出现错误
[HELP]   - 请求帮助
[SKIP]   - 跳过（已有人处理）
```

### 8.4 安全建议

1. **不要自动确认危险操作**：rm -rf、DROP TABLE 等
2. **设置操作白名单**：只允许特定命令
3. **保留操作日志**：记录所有 send-keys 操作
4. **定期人工检查**：不要完全无人值守

---

## 9. 风险与限制

### 9.1 已知风险

| 风险 | 描述 | 缓解措施 |
|:---|:---|:---|
| 误操作 | AI 发送错误命令 | 设置命令白名单 |
| 死循环 | AI 互相触发 | 添加冷却时间 |
| 资源竞争 | 同时修改同一文件 | 使用锁机制 |
| 信息泄露 | 敏感信息被读取 | 隔离敏感会话 |

### 9.2 技术限制

- tmux 必须在同一服务器
- 无法跨机器协作（需要 SSH）
- 终端输出有长度限制
- 无法读取密码输入（隐藏字符）

### 9.3 不适用场景

- 需要图形界面的操作
- 涉及敏感凭证的操作
- 需要实时交互的场景
- 跨网络的分布式协作

---

## 10. 扩展方向

### 10.1 跨机器协作

```bash
# 通过 SSH 读取远程 tmux
ssh user@remote "tmux capture-pane -t 0:1 -p"

# 通过 SSH 发送命令
ssh user@remote "tmux send-keys -t 0:1 'ls' Enter"
```

### 10.2 Web 监控面板

```python
# 简单的状态 API
from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/status')
def status():
    result = subprocess.run(
        ['tmux', 'list-windows', '-a', '-F', '#{window_name}:#{window_activity}'],
        capture_output=True, text=True
    )
    return jsonify({'windows': result.stdout.split('\n')})
```

### 10.3 智能调度

```python
# 基于负载的任务分配
def assign_task(task):
    windows = get_all_windows()
    
    # 找到最空闲的窗口
    idle_window = min(windows, key=lambda w: w.activity_time)
    
    # 分配任务
    send_keys(idle_window, f"处理任务: {task}")
```

### 10.4 与其他系统集成

- **Slack/Discord**：状态通知
- **Prometheus**：指标监控
- **Grafana**：可视化面板
- **GitHub Actions**：CI/CD 触发

---

## 附录

### A. 快速参考卡片

```
┌─────────────────────────────────────────────────────┐
│              AI 蜂群命令速查                         │
├─────────────────────────────────────────────────────┤
│ 列出窗口    tmux list-windows -a                    │
│ 读取内容    tmux capture-pane -t 0:1 -p -S -100     │
│ 发送命令    tmux send-keys -t 0:1 "cmd" Enter       │
│ 发送确认    tmux send-keys -t 0:1 "y" Enter         │
│ 中断任务    tmux send-keys -t 0:1 C-c               │
│ 新建窗口    tmux new-window -n "name"               │
└─────────────────────────────────────────────────────┘
```

### B. 故障排查

```bash
# tmux 不存在
which tmux || sudo apt install tmux

# 无法连接会话
tmux list-sessions  # 检查会话是否存在

# capture-pane 无输出
tmux capture-pane -t 0:1 -p -S -1000  # 增加行数

# send-keys 无效
tmux display-message -t 0:1 -p '#{pane_mode}'  # 检查模式
```

### C. 参考资料

- tmux 官方文档: https://github.com/tmux/tmux/wiki
- tmux 命令速查: `man tmux`

---

*文档版本: v1.0*
*最后更新: 2026-01-04*
