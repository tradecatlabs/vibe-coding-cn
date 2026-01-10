# Fully Automated Development Loop Workflow

A 5-step AI Agent workflow system based on **state machine + file hooks**.

## Directory Structure

```
workflow/
├── .kiro/agents/workflow.json   # Kiro Agent configuration
├── workflow_engine/             # State machine scheduling engine
│   ├── runner.py               # Core scheduler
│   ├── hook_runner.sh          # File watching hook
│   ├── state/                  # State files
│   └── artifacts/              # Artifacts directory
├── workflow-orchestrator/       # Orchestration skill documentation
├── step1_requirements.jsonl     # Requirements locking Agent
├── step2_execution_plan.jsonl   # Plan orchestration Agent
├── step3_implementation.jsonl   # Implementation changes Agent
├── step4_verification.jsonl     # Verification & release Agent
├── step5_controller.jsonl       # Master control & loop Agent
└── CHANGELOG.md
```

## Quick Start

### Method 1: Using Kiro CLI

```bash
# Navigate to workflow directory
cd ~/projects/vibe-coding-cn/i18n/en/workflow

# Start with workflow agent
kiro-cli chat --agent workflow
```

### Method 2: Manual Execution

```bash
cd ~/projects/vibe-coding-cn/i18n/en/workflow

# Start workflow
python3 workflow_engine/runner.py start

# Check status
python3 workflow_engine/runner.py status
```

### Method 3: Auto Mode (Hook Watching)

```bash
# Terminal 1: Start file watching
./workflow_engine/hook_runner.sh

# Terminal 2: Trigger workflow
python3 workflow_engine/runner.py start
```

## Workflow Process

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Step1  │───▶│  Step2  │───▶│  Step3  │───▶│  Step4  │───▶│  Step5  │
│  Input  │    │  Plan   │    │  Impl   │    │ Verify  │    │ Control │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └────┬────┘
                    ▲                                            │
                    │              Failure rollback              │
                    └────────────────────────────────────────────┘
```

## Core Mechanisms

| Mechanism | Description |
|-----------|-------------|
| State-driven | `state/current_step.json` as the single scheduling entry point |
| File Hook | `inotifywait` watches state changes and triggers automatically |
| Loop Control | Step5 decides rollback or completion based on verification results |
| Circuit Breaker | Maximum 3 retries per task |

## Kiro Integration

Agent configuration is located at `.kiro/agents/workflow.json`, including:

- **hooks**: Agent lifecycle hooks
  - `agentSpawn`: Read state on startup
  - `stop`: Check state when conversation ends
- **resources**: Auto-load prompt files into context
- **toolsSettings**: Pre-authorize file operations and command execution

## Next Steps

- [ ] Integrate actual LLM calls (replace MOCK in runner.py)
- [ ] Add CI/CD integration examples
- [ ] Support parallel task processing
