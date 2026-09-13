"""可恢复运行状态机、预算、超时与有界子进程执行。"""

from __future__ import annotations

import hashlib
import json
import math
import os
import selectors
import signal
import stat
import subprocess
import time
try:
    import resource as posix_resource
except ImportError:  # pragma: no cover - Windows has no POSIX rlimit API
    posix_resource = None
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker, SchemaError

try:
    import fcntl
except ImportError:  # pragma: no cover - unsupported platforms fail closed on use.
    fcntl = None  # type: ignore[assignment]


TERMINAL_STATES = {"accepted", "rejected", "blocked", "failed", "cancelled"}
TRANSITIONS = {
    "planned": {"routed", "cancelled"},
    "routed": {"running", "cancelled"},
    "running": {"candidate_ready", "blocked", "failed", "cancelled"},
    "candidate_ready": {"verifying", "blocked", "failed", "cancelled"},
    "verifying": {"accepted", "rejected", "blocked", "failed", "cancelled"},
}
MAX_STATE_BYTES = 5_000_000
MAX_TIMEOUT_SECONDS = 86_400
MAX_OUTPUT_BYTES = 128_000_000
MAX_MEMORY_BUDGET_MB = 131_072
MAX_THREADS = 1_024
MAX_ARGV_ITEMS = 4_096
MAX_ARGV_BYTES = 8_000_000
MAX_ENV_BYTES = 4_000_000
MAX_TRANSITIONS = 10_000
MAX_RETRIES = 1_000
MAX_ERROR_CHARS = 4_096
SAFE_ENV_KEYS = frozenset({
    "PATH",
    "HOME",
    "LANG",
    "LC_ALL",
    "TMPDIR",
    "LEAN_PATH",
    "GIT_NO_LAZY_FETCH",
    "GIT_TERMINAL_PROMPT",
})
DEFAULT_BUDGETS = {
    "max_transitions": 16,
    "max_retries": 2,
    "timeout_seconds": 30,
    "max_output_bytes": 1_048_576,
    "memory_budget_mb": 256,
    "threads_max": 1,
}


class RuntimeErrorBase(RuntimeError):
    """运行状态或预算契约失败。"""


class InjectedInterruption(RuntimeErrorBase):
    """测试用可恢复中断，不改变真实业务逻辑。"""


def _reject_json_constant(value: str) -> Any:
    raise RuntimeErrorBase(f"运行时 JSON 含非法常量：{value}")


def _safe_path(project_root: Path, path: Path) -> Path:
    root = project_root.resolve()
    path = Path(path)
    if (
        len(str(path)) > 4_096
        or "\x00" in str(path)
        or "\\" in str(path)
        or any(part in {".", ".."} for part in path.parts)
    ):
        raise RuntimeErrorBase(f"运行时路径包含非法组件：{path}")
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise RuntimeErrorBase(f"运行时路径越界：{path}") from exc
    lexical = root
    for part in relative.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise RuntimeErrorBase(f"运行时路径不能包含 symlink：{path}")
    if not path.is_absolute() or path.resolve() != path:
        raise RuntimeErrorBase(f"运行时路径不是规范绝对路径：{path}")
    return path


def _read_bounded(path: Path, *, max_bytes: int) -> bytes:
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_STATE_BYTES
    ):
        raise RuntimeErrorBase("运行时文件读取预算无效")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeErrorBase("当前平台无法安全读取运行时文件")
    try:
        descriptor = os.open(path, os.O_RDONLY | nofollow)
    except OSError as exc:
        raise RuntimeErrorBase(f"无法读取运行时文件：{path}") from exc
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise RuntimeErrorBase(f"运行时路径不是普通文件：{path}")
        if file_stat.st_size > max_bytes:
            raise RuntimeErrorBase(f"运行时文件超过大小预算：{path}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, max_bytes - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > max_bytes:
                raise RuntimeErrorBase(f"运行时文件超过大小预算：{path}")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def _validate_state(project_root: Path, state: dict[str, Any]) -> None:
    schema_path = _safe_path(
        project_root, project_root.resolve() / "research" / "schema" / "run-state.schema.json"
    )
    try:
        schema = json.loads(
            _read_bounded(schema_path, max_bytes=MAX_STATE_BYTES).decode("utf-8"),
            parse_constant=_reject_json_constant,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, RuntimeErrorBase) as exc:
        raise RuntimeErrorBase(f"无法读取运行状态 schema：{schema_path}") from exc
    if not isinstance(schema, dict) or not isinstance(state, dict):
        raise RuntimeErrorBase("运行状态 schema/state 必须是对象")
    try:
        errors = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(state),
            key=lambda item: list(item.path),
        )
    except (SchemaError, TypeError, ValueError) as exc:
        raise RuntimeErrorBase("运行状态 schema 无效") from exc
    if errors:
        raise RuntimeErrorBase(f"运行状态 schema 无效：{errors[0].message}")


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_run_id(problem_id: str, adapter: str) -> str:
    value = hashlib.sha256(f"{problem_id}\0{adapter}\0v1".encode()).hexdigest()[:20]
    return f"run:{value}"


def run_path(project_root: Path, run_id: str) -> Path:
    if not isinstance(run_id, str):
        raise RuntimeErrorBase("run_id 格式无效")
    safe_id = run_id.removeprefix("run:")
    if not safe_id or len(safe_id) > 64 or not all(character in "0123456789abcdef" for character in safe_id):
        raise RuntimeErrorBase("run_id 格式无效")
    root = project_root.resolve()
    if not root.is_dir():
        raise RuntimeErrorBase(f"运行时项目根目录不存在：{root}")
    return _safe_path(root, root / "research" / "runs" / safe_id / "run.json")


@contextmanager
def locked_run(project_root: Path, run_id: str) -> Any:
    """序列化同一 run 的所有副作用，避免并发状态与 artifact 竞争。"""
    if fcntl is None:
        raise RuntimeErrorBase("当前平台不支持 fail-closed 文件锁")
    path = run_path(project_root, run_id).with_name("run.lock")
    root = project_root.resolve()
    _safe_path(root, path)
    path.parent.mkdir(parents=True, exist_ok=True)
    _safe_path(root, path.parent)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeErrorBase("当前平台无法安全打开运行锁")
    try:
        descriptor = os.open(path, os.O_RDWR | os.O_CREAT | nofollow, 0o600)
    except OSError as exc:
        raise RuntimeErrorBase(f"无法打开运行锁：{path}") from exc
    try:
        with os.fdopen(descriptor, "a+b") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            yield
    finally:
        try:
            os.close(descriptor)
        except OSError:
            pass


def _write_atomic(path: Path, payload: dict[str, Any]) -> None:
    project_root = path.parents[3].resolve()
    _safe_path(project_root, path)
    _validate_state(project_root, payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    _safe_path(project_root, path.parent)
    try:
        data = (
            json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
                indent=2,
                allow_nan=False,
            )
            + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise RuntimeErrorBase("运行状态不是可移植 JSON") from exc
    if len(data) > MAX_STATE_BYTES:
        raise RuntimeErrorBase("运行状态超过大小预算")
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeErrorBase("当前平台无法安全创建运行状态")
    descriptor = os.open(
        temporary,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow,
        0o600,
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory = getattr(os, "O_DIRECTORY", None)
        if directory is None:
            raise RuntimeErrorBase("当前平台无法安全持久化运行状态")
        directory_descriptor = os.open(
            path.parent,
            os.O_RDONLY | directory | nofollow,
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def create_run(
    project_root: Path,
    problem_id: str,
    adapter: str,
    budgets: dict[str, int] | None = None,
) -> dict[str, Any]:
    run_id = stable_run_id(problem_id, adapter)
    path = run_path(project_root, run_id)
    if path.is_file():
        return load_run(project_root, run_id)
    effective = {**DEFAULT_BUDGETS, **(budgets or {})}
    if any(
        not isinstance(value, int) or isinstance(value, bool) or value <= 0
        for value in effective.values()
    ):
        raise RuntimeErrorBase("所有运行预算必须是正整数")
    if (
        effective["max_transitions"] > MAX_TRANSITIONS
        or effective["max_retries"] > MAX_RETRIES
        or effective["timeout_seconds"] > MAX_TIMEOUT_SECONDS
        or effective["max_output_bytes"] > MAX_OUTPUT_BYTES
        or effective["memory_budget_mb"] > MAX_MEMORY_BUDGET_MB
        or effective["threads_max"] > MAX_THREADS
    ):
        raise RuntimeErrorBase("运行预算超过平台上限")
    created = now()
    state = {
        "schema_version": "1.0.0",
        "run_id": run_id,
        "problem_id": problem_id,
        "adapter": adapter,
        "status": "planned",
        "transition_count": 0,
        "retry_count": 0,
        "budgets": effective,
        "checkpoints": [{"status": "planned", "at": created}],
        "last_error": None,
        "created_at": created,
        "updated_at": created,
    }
    _write_atomic(path, state)
    return state


def load_run(project_root: Path, run_id: str) -> dict[str, Any]:
    path = run_path(project_root, run_id)
    try:
        state = json.loads(
        _read_bounded(path, max_bytes=MAX_STATE_BYTES).decode("utf-8"),
        parse_constant=_reject_json_constant,
    )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, RuntimeErrorBase) as exc:
        raise RuntimeErrorBase(f"无法读取运行状态：{run_id}") from exc
    _validate_state(project_root, state)
    if state.get("run_id") != run_id:
        raise RuntimeErrorBase("运行状态身份或 schema_version 漂移")
    return state


def transition(project_root: Path, state: dict[str, Any], target: str) -> dict[str, Any]:
    current = state.get("status")
    if current in TERMINAL_STATES or target not in TRANSITIONS.get(current, set()):
        raise RuntimeErrorBase(f"非法运行状态转换：{current} -> {target}")
    count = state["transition_count"] + 1
    if count > state["budgets"]["max_transitions"]:
        raise RuntimeErrorBase("运行转换预算耗尽")
    changed = {**state, "status": target, "transition_count": count, "updated_at": now()}
    changed["checkpoints"] = [*state["checkpoints"], {"status": target, "at": changed["updated_at"]}]
    _write_atomic(run_path(project_root, state["run_id"]), changed)
    return changed


def execute_bounded(
    argv: list[str],
    *,
    cwd: Path,
    timeout_seconds: int | float,
    max_output_bytes: int,
    memory_budget_mb: int | None = None,
    threads_max: int | None = None,
    env: dict[str, str] | None = None,
    input_text: str | bytes | None = None,
) -> dict[str, Any]:
    if (
        not argv
        or len(argv) > MAX_ARGV_ITEMS
        or any(not isinstance(item, str) or not item for item in argv)
        or sum(len(item.encode("utf-8")) + 1 for item in argv) > MAX_ARGV_BYTES
    ):
        raise RuntimeErrorBase("子进程 argv 无效或超过大小预算")
    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, (int, float))
        or not math.isfinite(timeout_seconds)
        or timeout_seconds <= 0
        or timeout_seconds > MAX_TIMEOUT_SECONDS
        or isinstance(max_output_bytes, bool)
        or not isinstance(max_output_bytes, int)
        or max_output_bytes <= 0
        or max_output_bytes > MAX_OUTPUT_BYTES
    ):
        raise RuntimeErrorBase("子进程 timeout 与输出预算必须在平台上限内")
    cwd = Path(cwd)
    if not cwd.is_absolute():
        cwd = (Path.cwd() / cwd).absolute()
    if not cwd.is_dir() or cwd.is_symlink() or cwd.resolve() != cwd:
        raise RuntimeErrorBase("子进程 cwd 必须是非 symlink 目录")
    if input_text is not None and not isinstance(input_text, (str, bytes)):
        raise RuntimeErrorBase("子进程 stdin 必须是字符串或字节")
    input_bytes = (
        input_text.encode() if isinstance(input_text, str) else input_text
    )
    if input_bytes is not None and len(input_bytes) > max_output_bytes:
        raise RuntimeErrorBase("子进程 stdin 超过输出预算")
    if memory_budget_mb is None:
        memory_budget_mb = 512
    if threads_max is None:
        threads_max = 1
    if memory_budget_mb is not None and (
        not isinstance(memory_budget_mb, int)
        or isinstance(memory_budget_mb, bool)
        or memory_budget_mb <= 0
        or memory_budget_mb > MAX_MEMORY_BUDGET_MB
    ):
        raise RuntimeErrorBase("子进程 memory budget 必须在平台上限内")
    if threads_max is not None and (
        not isinstance(threads_max, int)
        or isinstance(threads_max, bool)
        or threads_max <= 0
        or threads_max > MAX_THREADS
    ):
        raise RuntimeErrorBase("子进程 threads budget 必须在平台上限内")

    if env is not None and not isinstance(env, dict):
        raise RuntimeErrorBase("子进程环境必须是字典")
    if env is not None and (
        any(
            not isinstance(key, str)
            or key not in SAFE_ENV_KEYS
            or not isinstance(value, str)
            for key, value in env.items()
        )
        or sum(len(key.encode()) + len(value.encode()) + 2 for key, value in env.items()) > MAX_ENV_BYTES
    ):
        raise RuntimeErrorBase("子进程环境包含未授权键或超过大小预算")
    child_env = {
        key: value for key, value in os.environ.items() if key in SAFE_ENV_KEYS
    } if env is None else dict(env)
    if sum(len(key.encode()) + len(value.encode()) + 2 for key, value in child_env.items()) > MAX_ENV_BYTES:
        raise RuntimeErrorBase("子进程环境超过大小预算")
    if threads_max is not None:
        for variable in (
            "OMP_NUM_THREADS",
            "OPENBLAS_NUM_THREADS",
            "MKL_NUM_THREADS",
            "NUMEXPR_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS",
        ):
            child_env[variable] = str(threads_max)
    if sum(len(key.encode()) + len(value.encode()) + 2 for key, value in child_env.items()) > MAX_ENV_BYTES:
        raise RuntimeErrorBase("子进程环境超过大小预算")

    preexec_fn = None
    if memory_budget_mb is not None:
        if posix_resource is None:
            raise RuntimeErrorBase("当前平台无法强制 memory budget，拒绝启动子进程")
        memory_limit = memory_budget_mb * 1024 * 1024

        def apply_memory_limit() -> None:
            soft, hard = posix_resource.getrlimit(posix_resource.RLIMIT_AS)
            bounded_hard = memory_limit if hard == posix_resource.RLIM_INFINITY else min(hard, memory_limit)
            bounded_soft = bounded_hard if soft == posix_resource.RLIM_INFINITY else min(soft, bounded_hard)
            posix_resource.setrlimit(posix_resource.RLIMIT_AS, (bounded_soft, bounded_hard))

        preexec_fn = apply_memory_limit

    try:
        process = subprocess.Popen(
            argv,
            cwd=cwd,
            env=child_env,
            stdin=subprocess.PIPE if input_bytes is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
            preexec_fn=preexec_fn,
            close_fds=True,
        )
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        raise RuntimeErrorBase(f"无法启动有界子进程：{argv[0]}") from exc
    if process.stdout is None or process.stderr is None:
        raise RuntimeErrorBase("无法建立子进程输出通道")

    def terminate_group() -> None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (PermissionError, ProcessLookupError):
            pass
        try:
            process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=1)
            except subprocess.TimeoutExpired as second_exc:
                raise RuntimeErrorBase("无法在终止预算内回收子进程") from second_exc

    streams = {
        process.stdout: bytearray(),
        process.stderr: bytearray(),
    }
    for stream in streams:
        os.set_blocking(stream.fileno(), False)
    if process.stdin is not None:
        os.set_blocking(process.stdin.fileno(), False)
    selector = selectors.DefaultSelector()
    for stream in streams:
        selector.register(stream, selectors.EVENT_READ)
    input_stream = process.stdin
    input_offset = 0
    input_closed = input_stream is None

    def close_input() -> None:
        nonlocal input_closed
        if input_stream is not None and not input_closed:
            try:
                selector.unregister(input_stream)
            except KeyError:
                pass
            input_stream.close()
            input_closed = True

    if input_stream is not None:
        selector.register(input_stream, selectors.EVENT_WRITE)
    deadline = time.monotonic() + timeout_seconds
    return_code: int | None = None
    try:
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                terminate_group()
                raise RuntimeErrorBase(f"子进程超时：{timeout_seconds}s")
            for key, _ in selector.select(timeout=min(remaining, 0.1)):
                stream = key.fileobj
                if input_stream is not None and stream is input_stream:
                    if input_bytes is None or input_offset >= len(input_bytes):
                        close_input()
                        continue
                    try:
                        written = os.write(
                            input_stream.fileno(),
                            input_bytes[input_offset:input_offset + 65_536],
                        )
                    except (BrokenPipeError, BlockingIOError):
                        close_input()
                    else:
                        input_offset += written
                        if input_offset >= len(input_bytes):
                            close_input()
                    continue
                try:
                    chunk = os.read(stream.fileno(), 65_536)
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(stream)
                    continue
                total_output = sum(len(buffer) for buffer in streams.values())
                if total_output + len(chunk) > max_output_bytes:
                    terminate_group()
                    raise RuntimeErrorBase("子进程 stdout/stderr 合计超过输出预算")
                streams[stream].extend(chunk)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            terminate_group()
            raise RuntimeErrorBase(f"子进程超时：{timeout_seconds}s")
        try:
            return_code = process.wait(timeout=remaining)
        except subprocess.TimeoutExpired as exc:
            terminate_group()
            raise RuntimeErrorBase(f"子进程超时：{timeout_seconds}s") from exc
    except BaseException:
        if process.poll() is None:
            terminate_group()
        raise
    finally:
        close_input()
        selector.close()
        process.stdout.close()
        process.stderr.close()

    if return_code is None:
        raise RuntimeErrorBase("子进程未产生退出状态")
    if return_code < 0:
        raise RuntimeErrorBase(f"子进程被信号终止：{-return_code}")
    stdout = bytes(streams[process.stdout])
    stderr = bytes(streams[process.stderr])
    return {
        "argv": argv,
        "exit_code": return_code,
        "stdout": stdout.decode(errors="replace"),
        "stderr": stderr.decode(errors="replace"),
    }


def record_retry(project_root: Path, state: dict[str, Any], error: str) -> dict[str, Any]:
    if not isinstance(error, str) or len(error) > MAX_ERROR_CHARS:
        raise RuntimeErrorBase("运行错误信息超过大小预算")
    retries = state["retry_count"] + 1
    if retries > state["budgets"]["max_retries"]:
        raise RuntimeErrorBase("运行重试预算耗尽")
    changed = {**state, "retry_count": retries, "last_error": error, "updated_at": now()}
    _write_atomic(run_path(project_root, state["run_id"]), changed)
    return changed


def cancel_run(project_root: Path, run_id: str) -> dict[str, Any]:
    """在 run 互斥锁内执行显式取消；终态取消保持幂等。"""
    with locked_run(project_root, run_id):
        state = load_run(project_root, run_id)
        if state["status"] == "cancelled":
            return state
        current = state["status"]
        if current in TERMINAL_STATES or "cancelled" not in TRANSITIONS.get(current, set()):
            raise RuntimeErrorBase(f"非法运行状态转换：{current} -> cancelled")
        cancelled_at = now()
        changed = {
            **state,
            "status": "cancelled",
            "updated_at": cancelled_at,
            "last_error": "用户或监管器显式取消",
            "checkpoints": [
                *state["checkpoints"],
                {"status": "cancelled", "at": cancelled_at},
            ],
        }
        _write_atomic(run_path(project_root, run_id), changed)
        return changed
