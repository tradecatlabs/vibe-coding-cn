#!/usr/bin/env python3
"""
workflow_engine/runner.py - 轻量状态机调度器
用于编排 step1~step5 的全自动开发闭环
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
STATE_FILE = BASE_DIR / "workflow_engine/state/current_step.json"
ARTIFACTS_DIR = BASE_DIR / "workflow_engine/artifacts"
PROMPTS_DIR = BASE_DIR

STEP_MAP = {
    "step1": "step1_需求输入.jsonl",
    "step2": "step2_执行计划.jsonl",
    "step3": "step3_实施变更.jsonl",
    "step4": "step4_验证发布.jsonl",
    "step5": "step5_总控与循环.jsonl",
}

STEP_FLOW = ["step1", "step2", "step3", "step4", "step5"]


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"run_id": None, "step": None, "status": "idle"}


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def get_run_id() -> str:
    return datetime.now().strftime("%Y%m%dT%H%M%S")


def get_artifact_path(run_id: str, step: str, ext: str = "json") -> Path:
    path = ARTIFACTS_DIR / run_id
    path.mkdir(parents=True, exist_ok=True)
    return path / f"{step}.{ext}"


def next_step(current: str) -> str | None:
    """返回下一步，step5 后返回 None"""
    try:
        idx = STEP_FLOW.index(current)
        return STEP_FLOW[idx + 1] if idx + 1 < len(STEP_FLOW) else None
    except ValueError:
        return None


def run_step(step: str, state: dict, input_data: dict = None):
    """执行单个步骤（实际调用模型的占位）"""
    prompt_file = PROMPTS_DIR / STEP_MAP.get(step, "")
    if not prompt_file.exists():
        print(f"[ERROR] Prompt file not found: {prompt_file}")
        return None

    run_id = state.get("run_id") or get_run_id()
    
    # 更新状态为 running
    state.update({"run_id": run_id, "step": step, "status": "running"})
    save_state(state)
    
    print(f"[RUN] {step} | run_id={run_id}")
    print(f"      prompt: {prompt_file.name}")
    
    # === 这里是模型调用占位 ===
    # 实际实现时替换为：
    # result = call_llm(prompt_file.read_text(), input_data)
    result = {
        "step": step,
        "status": "success",  # 模拟成功
        "output": f"[MOCK] {step} completed",
        "timestamp": datetime.now().isoformat()
    }
    # ========================
    
    # 保存产物
    artifact_path = get_artifact_path(run_id, step)
    artifact_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"      artifact: {artifact_path}")
    
    return result


def dispatch():
    """根据当前状态分发到下一步"""
    state = load_state()
    target = state.get("target_step")
    
    if target == "done":
        print("[DONE] 所有任务完成")
        return
    
    if target:
        # 有明确的目标步骤（来自 step5 的指令）
        run_step(target, state)
    else:
        print("[IDLE] 无待执行任务，使用 'run --step 1' 启动")


def start_workflow(input_file: str = None):
    """从 step1 启动新的工作流"""
    run_id = get_run_id()
    state = {"run_id": run_id, "step": None, "status": "pending"}
    
    input_data = None
    if input_file and Path(input_file).exists():
        input_data = json.loads(Path(input_file).read_text(encoding="utf-8"))
    
    print(f"[START] 新工作流 run_id={run_id}")
    
    # 依次执行 step1 -> step5
    for step in STEP_FLOW:
        result = run_step(step, state, input_data)
        
        if not result:
            state["status"] = "error"
            save_state(state)
            return
        
        # step4 后检查验证结果
        if step == "step4":
            verify_status = result.get("verify", {}).get("status", "success")
            state["verify"] = {"status": verify_status}
        
        # step5 决定下一步
        if step == "step5":
            # 模拟 step5 的决策逻辑
            if state.get("verify", {}).get("status") == "failed":
                state["target_step"] = "step2"  # 失败回跳
                state["status"] = "retry"
                print(f"[RETRY] 验证失败，返回 step2 重规划")
            else:
                state["target_step"] = "done"
                state["status"] = "completed"
                print(f"[COMPLETE] 工作流完成")
        
        save_state(state)
        
        # 如果需要回跳，递归处理（带熔断）
        if state.get("target_step") == "step2":
            retry_count = state.get("retry_count", 0) + 1
            if retry_count > 3:
                print(f"[FATAL] 超过最大重试次数")
                state["status"] = "fatal_error"
                save_state(state)
                return
            state["retry_count"] = retry_count
            # 从 step2 重新开始
            for retry_step in STEP_FLOW[1:]:  # step2 onwards
                run_step(retry_step, state)
            break


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python runner.py start [input.json]  - 启动新工作流")
        print("  python runner.py dispatch            - 根据状态分发")
        print("  python runner.py status              - 查看当前状态")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "start":
        input_file = sys.argv[2] if len(sys.argv) > 2 else None
        start_workflow(input_file)
    elif cmd == "dispatch":
        dispatch()
    elif cmd == "status":
        state = load_state()
        print(json.dumps(state, ensure_ascii=False, indent=2))
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
