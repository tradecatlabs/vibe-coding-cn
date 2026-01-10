# AI Swarm Collaboration Technical Documentation

> Design and implementation of multi AI Agent collaboration system based on tmux

---

## Table of Contents

1. [Core Concept](#1-core-concept)
2. [Technical Principles](#2-technical-principles)
3. [Command Reference](#3-command-reference)
4. [Collaboration Protocol](#4-collaboration-protocol)
5. [Architecture Patterns](#5-architecture-patterns)
6. [Practical Cases](#6-practical-cases)
7. [Prompt Templates](#7-prompt-templates)
8. [Best Practices](#8-best-practices)
9. [Risks and Limitations](#9-risks-and-limitations)
10. [Extension Directions](#10-extension-directions)

---

## 1. Core Concept

### 1.1 Problem Background

Limitations of traditional AI programming assistants:
- Single session, unable to perceive other tasks
- Requires manual intervention when waiting/confirming
- Unable to coordinate during multi-task parallelism
- Repetitive work, resource waste

### 1.2 Solution

Leveraging tmux's terminal multiplexing capabilities to give AI:

| Capability | Implementation | Effect |
|:---|:---|:---|
| **Perception** | `capture-pane` | Read any terminal content |
| **Control** | `send-keys` | Send keystrokes to any terminal |
| **Coordination** | Shared state files | Task synchronization and distribution |

### 1.3 Core Insight

```
Traditional mode: Human ←→ AI₁, Human ←→ AI₂, Human ←→ AI₃ (Human is the bottleneck)

Swarm mode: Human → AI₁ ←→ AI₂ ←→ AI₃ (AI autonomous collaboration)
```

**Key Breakthrough**: AI is no longer isolated, but a cluster that can perceive, communicate, and control each other.

---

## 2. Technical Principles

### 2.1 tmux Architecture

```
┌─────────────────────────────────────────────┐
│                 tmux server                  │
├─────────────────────────────────────────────┤
│  Session 0                                   │
│  ├── Window 0:1 [AI-1] ◄──┐                 │
│  ├── Window 0:2 [AI-2] ◄──┼── Mutually      │
│  ├── Window 0:3 [AI-3] ◄──┤   visible/      │
│  └── Window 0:4 [AI-4] ◄──┘   controllable  │
└─────────────────────────────────────────────┘
```

### 2.2 Data Flow

```
┌─────────┐  capture-pane   ┌─────────┐
│  AI-1   │ ◄───────────────│  AI-4   │
│ (exec)  │                 │ (monitor)│
└─────────┘  send-keys      └─────────┘
     ▲      ───────────────►     │
     │                           │
     └───────── Control flow ────┘
```

### 2.3 Communication Mechanisms

| Mechanism | Direction | Latency | Use Case |
|:---|:---|:---|:---|
| `capture-pane` | Read | Instant | Get terminal output |
| `send-keys` | Write | Instant | Send commands/keys |
| Shared files | Bidirectional | File IO | State persistence |

---

## 3. Command Reference

### 3.1 Information Retrieval

```bash
# List all sessions
tmux list-sessions

# List all windows
tmux list-windows -a

# List all panes
tmux list-panes -a

# Get current window identifier
echo $TMUX_PANE
```

### 3.2 Content Reading

```bash
# Read specified window content (last N lines)
tmux capture-pane -t <session>:<window> -p -S -<N>

# Example: Read last 100 lines from session 0 window 1
tmux capture-pane -t 0:1 -p -S -100

# Read and save to file
tmux capture-pane -t 0:1 -p -S -500 > /tmp/window1.log

# Batch read all windows
for w in $(tmux list-windows -a -F '#{session_name}:#{window_index}'); do
  echo "=== $w ==="
  tmux capture-pane -t "$w" -p -S -30
done
```

### 3.3 Sending Controls

```bash
# Send text + Enter
tmux send-keys -t 0:1 "ls -la" Enter

# Send confirmation
tmux send-keys -t 0:1 "y" Enter

# Send special keys
tmux send-keys -t 0:1 C-c        # Ctrl+C
tmux send-keys -t 0:1 C-d        # Ctrl+D
tmux send-keys -t 0:1 C-z        # Ctrl+Z
tmux send-keys -t 0:1 Escape     # ESC
tmux send-keys -t 0:1 Up         # Up arrow
tmux send-keys -t 0:1 Down       # Down arrow
tmux send-keys -t 0:1 Tab        # Tab

# Combined operations
tmux send-keys -t 0:1 C-c        # First interrupt
tmux send-keys -t 0:1 "cd /tmp" Enter  # Then execute new command
```

### 3.4 Window Management

```bash
# Create new window
tmux new-window -n "ai-worker"

# Create and execute command
tmux new-window -n "ai-1" "kiro-cli chat"

# Close window
tmux kill-window -t 0:1

# Rename window
tmux rename-window -t 0:1 "monitor"
```

---

## 4. Collaboration Protocol

### 4.1 State Definition

```bash
# State file location
/tmp/ai_swarm/
├── status.log      # Global status log
├── tasks.json      # Task queue
├── locks/          # Task locks
│   ├── task_001.lock
│   └── task_002.lock
└── results/        # Results storage
    ├── ai_1.json
    └── ai_2.json
```

### 4.2 Status Format

```bash
# Status log format
[HH:MM:SS] [WindowID] [Status] Description

# Examples
[08:15:30] [0:1] [START] Starting data-service code audit
[08:16:45] [0:1] [DONE] Completed code audit, found 5 issues
[08:16:50] [0:2] [WAIT] Waiting for 0:1 audit results
[08:17:00] [0:2] [START] Starting to fix issues
```

### 4.3 Collaboration Rules

| Rule | Description | Implementation |
|:---|:---|:---|
| **Check before action** | Scan other terminals before starting | `capture-pane` full scan |
| **Avoid conflicts** | Same task only done once | Check locks directory |
| **Proactive rescue** | Help when stuck detected | Detect `[y/n]` waiting |
| **Status broadcast** | Notify other AIs after completion | Write to status.log |

### 4.4 Conflict Handling

```
Scenario: AI-1 and AI-2 want to modify the same file simultaneously

Solution:
1. Check lock before creating task
2. Can only execute after acquiring lock
3. Release lock after completion

# Acquire lock
if [ ! -f /tmp/ai_swarm/locks/file_x.lock ]; then
  echo "$TMUX_PANE" > /tmp/ai_swarm/locks/file_x.lock
  # Execute task
  rm /tmp/ai_swarm/locks/file_x.lock
fi
```

---

## 5. Architecture Patterns

### 5.1 Peer-to-Peer (P2P)

```
┌─────┐     ┌─────┐
│ AI₁ │◄───►│ AI₂ │
└──┬──┘     └──┬──┘
   │           │
   ▼           ▼
┌─────┐     ┌─────┐
│ AI₃ │◄───►│ AI₄ │
└─────┘     └─────┘

Features: All AIs are equal, mutually monitoring
Suitable for: Simple tasks, no clear dependencies
```

### 5.2 Master-Worker

```
        ┌──────────┐
        │ AI-Master│
        │(Commander)│
        └────┬─────┘
             │ Distribute/Monitor
    ┌────────┼────────┐
    ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐
│Worker│ │Worker│ │Worker│
│ AI-1 │ │ AI-2 │ │ AI-3 │
└──────┘ └──────┘ └──────┘

Features: One commander, multiple executors
Suitable for: Complex projects, requires unified coordination
```

### 5.3 Pipeline

```
┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐
│ AI₁ │───►│ AI₂ │───►│ AI₃ │───►│ AI₄ │
│Analyze│  │Design│   │Implement│ │Test │
└─────┘    └─────┘    └─────┘    └─────┘

Features: Sequential task flow
Suitable for: Workflows with clear phases
```

### 5.4 Hybrid

```
           ┌──────────┐
           │ AI-Master│
           └────┬─────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
┌──────┐   ┌──────┐    ┌──────┐
│Analysis│ │Dev Team│   │Test  │
│ Team  │  │       │    │ Team │
├──────┤   ├──────┤    ├──────┤
│AI-1  │   │AI-3  │    │AI-5  │
│AI-2  │   │AI-4  │    │AI-6  │
└──────┘   └──────┘    └──────┘

Features: Group collaboration + unified scheduling
Suitable for: Large projects, multi-team parallelism
```

---

## 6. Practical Cases

### 6.1 Case: Multi-Service Parallel Development

**Scenario**: Simultaneously develop data-service, trading-service, telegram-service

**Configuration**:
```bash
# Window allocation
0:1 - AI-Master (Commander)
0:2 - AI-Data (data-service)
0:3 - AI-Trading (trading-service)
0:4 - AI-Telegram (telegram-service)
```

**Commander Prompt**:
```
You are the project commander, responsible for coordinating 3 development AIs.

Execute a scan every 2 minutes:
for w in 2 3 4; do
  echo "=== Window 0:$w ===" 
  tmux capture-pane -t "0:$w" -p -S -20
done

When issues are detected:
- Stuck waiting → send-keys to confirm
- Error → analyze and provide suggestions
- Completed → record and assign next task
```

### 6.2 Case: Code Audit + Auto Fix

**Scenario**: AI-1 audits code, AI-2 fixes in real-time

**Flow**:
```
AI-1 (Audit):
1. Scan code, output issue list
2. Write to /tmp/ai_swarm/issues.log for each issue found

AI-2 (Fix):
1. Monitor issues.log
2. Read new issues
3. Auto fix
4. Mark as completed
```

### 6.3 Case: 24/7 Watch

**Scenario**: AIs monitor each other, auto rescue

**Configuration**:
```bash
# Monitoring logic for each AI
while true; do
  for w in $(tmux list-windows -a -F '#{window_index}'); do
    output=$(tmux capture-pane -t "0:$w" -p -S -5)
    
    # Detect stuck
    if echo "$output" | grep -q "\[y/n\]"; then
      tmux send-keys -t "0:$w" "y" Enter
      echo "Helped window $w confirm"
    fi
    
    # Detect errors
    if echo "$output" | grep -qi "error\|failed"; then
      echo "Window $w has errors, needs attention"
    fi
  done
  sleep 30
done
```

---

## 7. Prompt Templates

### 7.1 Basic Version (Worker)

```markdown
## AI Swarm Collaboration Mode

You work in a tmux environment and can perceive and assist other terminals.

### Commands
# Scan all terminals
tmux list-windows -a

# Read terminal content
tmux capture-pane -t <session>:<window> -p -S -100

### Behavior
- Scan environment before starting tasks
- Proactively coordinate when related tasks are found
- Broadcast status after completion
```

### 7.2 Complete Version (Worker)

```markdown
## 🐝 AI Swarm Collaboration Protocol v2.0

You are a member of the tmux multi-terminal AI cluster.

### Perception Capabilities

# List all windows
tmux list-windows -a

# Read specified window (last 100 lines)
tmux capture-pane -t <session>:<window> -p -S -100

# Batch scan
for w in $(tmux list-windows -a -F '#{session_name}:#{window_index}'); do
  echo "=== $w ===" && tmux capture-pane -t "$w" -p -S -20
done

### Control Capabilities

# Send command
tmux send-keys -t <window> "<command>" Enter

# Send confirmation
tmux send-keys -t <window> "y" Enter

# Interrupt task
tmux send-keys -t <window> C-c

### Collaboration Rules

1. **Proactive perception**: Scan other terminals before task starts
2. **Avoid conflicts**: Don't repeat the same task
3. **Proactive rescue**: Help when waiting/stuck is detected
4. **Status broadcast**: Write to shared log after completion

### Status Sync

# Broadcast
echo "[$(date +%H:%M:%S)] [$TMUX_PANE] [DONE] <description>" >> /tmp/ai_swarm/status.log

# Read
tail -20 /tmp/ai_swarm/status.log

### Check Timing

- 🚦 Before task starts
- ⏳ When waiting for dependencies
- ✅ After task completion
- ❌ When errors occur
```

### 7.3 Commander Version (Master)

```markdown
## 🎖️ AI Cluster Commander Protocol

You are the commander of the AI swarm, responsible for monitoring and coordinating all Worker AIs.

### Core Responsibilities

1. **Global monitoring**: Regularly scan all terminal states
2. **Task assignment**: Assign tasks based on capabilities
3. **Conflict resolution**: Coordinate when duplicate work is found
4. **Fault rescue**: Intervene when stuck/errors are detected
5. **Progress summary**: Summarize results from all terminals

### Monitoring Commands

# Global scan (execute every 2 minutes)
echo "========== $(date) Status Scan =========="
for w in $(tmux list-windows -a -F '#{session_name}:#{window_index}'); do
  echo "--- $w ---"
  tmux capture-pane -t "$w" -p -S -15
done

### Intervention Commands

# Help confirm
tmux send-keys -t <window> "y" Enter

# Interrupt erroneous task
tmux send-keys -t <window> C-c

# Send new instruction
tmux send-keys -t <window> "<instruction>" Enter

### Status Judgment

Intervene when these patterns are detected:
- `[y/n]` `[Y/n]` `confirm` → Needs confirmation
- `Error` `Failed` `Exception` → Error occurred
- `Waiting` `Blocked` → Task blocked
- No output for long time → May be dead

### Report Format

Output after each scan:
| Window | Status | Current Task | Notes |
|:---|:---|:---|:---|
| 0:1 | ✅ Normal | Code audit | 80% progress |
| 0:2 | ⏳ Waiting | Waiting confirm | Auto confirmed |
| 0:3 | ❌ Error | Build failed | Needs attention |
```

---

## 8. Best Practices

### 8.1 Initialization Flow

```bash
# 1. Create shared directory
mkdir -p /tmp/ai_swarm/{locks,results}
touch /tmp/ai_swarm/status.log

# 2. Start tmux session
tmux new-session -d -s ai

# 3. Create multiple windows
tmux new-window -t ai -n "master"
tmux new-window -t ai -n "worker-1"
tmux new-window -t ai -n "worker-2"
tmux new-window -t ai -n "worker-3"

# 4. Start AI in each window
tmux send-keys -t ai:master "kiro-cli chat" Enter
tmux send-keys -t ai:worker-1 "kiro-cli chat" Enter
# ...

# 5. Send swarm prompts
```

### 8.2 Naming Conventions

```bash
# Session naming
ai          # AI work session
dev         # Development session
monitor     # Monitoring session

# Window naming
master      # Commander
worker-N    # Worker nodes
data        # data-service dedicated
trading     # trading-service dedicated
```

### 8.3 Log Standards

```bash
# Status log
[Time] [Window] [Status] Description

# Status types
[START]  - Task started
[DONE]   - Task completed
[WAIT]   - Waiting
[ERROR]  - Error occurred
[HELP]   - Help requested
[SKIP]   - Skipped (already being handled)
```

### 8.4 Security Recommendations

1. **Don't auto-confirm dangerous operations**: rm -rf, DROP TABLE, etc.
2. **Set operation whitelist**: Only allow specific commands
3. **Keep operation logs**: Record all send-keys operations
4. **Regular manual checks**: Don't go completely unattended

---

## 9. Risks and Limitations

### 9.1 Known Risks

| Risk | Description | Mitigation |
|:---|:---|:---|
| Misoperation | AI sends wrong commands | Set command whitelist |
| Infinite loop | AIs trigger each other | Add cooldown time |
| Resource contention | Simultaneous file modification | Use lock mechanism |
| Information leak | Sensitive info read | Isolate sensitive sessions |

### 9.2 Technical Limitations

- tmux must be on the same server
- Cannot collaborate across machines (requires SSH)
- Terminal output has length limits
- Cannot read password input (hidden characters)

### 9.3 Unsuitable Scenarios

- Operations requiring GUI
- Operations involving sensitive credentials
- Scenarios requiring real-time interaction
- Cross-network distributed collaboration

---

## 10. Extension Directions

### 10.1 Cross-Machine Collaboration

```bash
# Read remote tmux via SSH
ssh user@remote "tmux capture-pane -t 0:1 -p"

# Send commands via SSH
ssh user@remote "tmux send-keys -t 0:1 'ls' Enter"
```

### 10.2 Web Monitoring Panel

```python
# Simple status API
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

### 10.3 Intelligent Scheduling

```python
# Load-based task assignment
def assign_task(task):
    windows = get_all_windows()
    
    # Find the most idle window
    idle_window = min(windows, key=lambda w: w.activity_time)
    
    # Assign task
    send_keys(idle_window, f"Process task: {task}")
```

### 10.4 Integration with Other Systems

- **Slack/Discord**: Status notifications
- **Prometheus**: Metrics monitoring
- **Grafana**: Visualization panel
- **GitHub Actions**: CI/CD triggers

---

## Appendix

### A. Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│              AI Swarm Command Cheatsheet             │
├─────────────────────────────────────────────────────┤
│ List windows   tmux list-windows -a                 │
│ Read content   tmux capture-pane -t 0:1 -p -S -100  │
│ Send command   tmux send-keys -t 0:1 "cmd" Enter    │
│ Send confirm   tmux send-keys -t 0:1 "y" Enter      │
│ Interrupt      tmux send-keys -t 0:1 C-c            │
│ New window     tmux new-window -n "name"            │
└─────────────────────────────────────────────────────┘
```

### B. Troubleshooting

```bash
# tmux doesn't exist
which tmux || sudo apt install tmux

# Cannot connect to session
tmux list-sessions  # Check if session exists

# capture-pane no output
tmux capture-pane -t 0:1 -p -S -1000  # Increase line count

# send-keys not working
tmux display-message -t 0:1 -p '#{pane_mode}'  # Check mode
```

### C. References

- tmux official documentation: https://github.com/tmux/tmux/wiki
- tmux command reference: `man tmux`

---

*Document version: v1.0*
*Last updated: 2026-01-04*
