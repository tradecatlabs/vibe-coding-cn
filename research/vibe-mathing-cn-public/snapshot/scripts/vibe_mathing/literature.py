"""文献 provider registry、脱敏请求构造和显式 live 健康检查。"""

from __future__ import annotations

import json
import os
import stat
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker, SchemaError


USER_AGENT = "vibe-mathing-cn/0.2 literature-provider-health"
DEFAULT_MAX_RESPONSE_BYTES = 1_000_000
ABSOLUTE_MAX_RESPONSE_BYTES = 30_000_000
MAX_PROVIDER_TIMEOUT_SECONDS = 300
MAX_PROVIDER_RETRIES = 10
MAX_QUERY_CHARS = 4_096
MAX_PATH_CHARS = 4_096
MAX_FIELD_CHARS = 8_192
MAX_PROVIDERS = 1_000
MAX_EXTRA_QUERY_ITEMS = 1_000


def _is_https_url(value: object, *, max_chars: int = MAX_FIELD_CHARS) -> bool:
    if not isinstance(value, str) or not value or len(value) > max_chars:
        return False
    try:
        parsed = urllib.parse.urlparse(value)
        return (
            parsed.scheme.lower() == "https"
            and bool(parsed.netloc)
            and not parsed.username
            and not parsed.password
        )
    except ValueError:
        return False


def _reject_json_constant(value: str) -> object:
    raise LiteratureProviderError(f"JSON contains illegal constant: {value}")


def _read_registry_file(path: Path, *, max_bytes: int = 5_000_000) -> bytes:
    path = Path(path)
    if (
        len(str(path)) > MAX_PATH_CHARS
        or "\x00" in str(path)
        or "\\" in str(path)
        or any(part in {".", ".."} for part in path.parts)
    ):
        raise LiteratureProviderError("provider registry path contains invalid components")
    if (
        isinstance(max_bytes, bool)
        or not isinstance(max_bytes, int)
        or max_bytes <= 0
        or max_bytes > ABSOLUTE_MAX_RESPONSE_BYTES
    ):
        raise LiteratureProviderError("provider registry 大小预算无效")
    root = path.parents[1].resolve()
    candidate = path if path.is_absolute() else root / path
    if candidate.resolve() != candidate or any(parent.is_symlink() for parent in candidate.parents):
        raise LiteratureProviderError("provider registry path cannot contain symlink")
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise LiteratureProviderError("provider registry 路径越界") from exc
    lexical = root
    for part in candidate.relative_to(root).parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise LiteratureProviderError("provider registry 路径不能包含 symlink")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise LiteratureProviderError("当前平台无法安全读取 provider registry")
    try:
        descriptor = os.open(candidate, os.O_RDONLY | nofollow)
    except OSError as exc:
        raise LiteratureProviderError("无法读取 provider registry") from exc
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise LiteratureProviderError("provider registry 不是普通文件")
        if file_stat.st_size > max_bytes:
            raise LiteratureProviderError("provider registry 超过大小预算")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, max_bytes - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > max_bytes:
                raise LiteratureProviderError("provider registry 超过大小预算")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


class HTTPSOnlyRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Reject redirect downgrades so provider TLS failures stay fail-closed."""

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> urllib.request.Request:
        target = urllib.parse.urljoin(req.full_url, newurl)
        if not _is_https_url(target):
            raise LiteratureProviderError(f"拒绝非 HTTPS provider 重定向：{target}")
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected is None:  # pragma: no cover - urllib contract guard
            raise LiteratureProviderError("provider 重定向未生成请求")
        return redirected


HTTPS_OPENER = urllib.request.build_opener(HTTPSOnlyRedirectHandler())


class LiteratureProviderError(RuntimeError):
    """Provider registry、凭据或 live 请求不满足契约。"""


def _set_response_timeout(response: Any, timeout: float) -> None:
    candidates: list[Any] = [response]
    current = response
    for attribute in ("fp", "raw", "_sock"):
        current = getattr(current, attribute, None)
        if current is None:
            break
        candidates.append(current)
    for candidate in candidates:
        setter = getattr(candidate, "settimeout", None)
        if callable(setter):
            try:
                setter(max(0.001, timeout))
            except OSError as exc:
                raise LiteratureProviderError("无法设置 provider 响应读取超时") from exc
            return


def load_provider_registry(project_root: Path) -> dict[str, dict[str, Any]]:
    """读取并验证 provider registry，返回按 ID 索引的只读配置。"""
    registry_path = project_root / "literature/providers.json"
    schema_path = project_root / "literature/schema/literature-providers.schema.json"
    try:
        registry = json.loads(
            _read_registry_file(registry_path).decode("utf-8"),
            parse_constant=_reject_json_constant,
        )
        schema = json.loads(
            _read_registry_file(schema_path).decode("utf-8"),
            parse_constant=_reject_json_constant,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, LiteratureProviderError) as exc:
        raise LiteratureProviderError("无法读取文献 provider registry 或 schema") from exc
    if not isinstance(registry, dict) or not isinstance(schema, dict):
        raise LiteratureProviderError("文献 provider registry/schema 顶层必须是 object")
    providers_value = registry.get("providers")
    if not isinstance(providers_value, list) or len(providers_value) > MAX_PROVIDERS:
        raise LiteratureProviderError("文献 provider 数量超过预算")
    try:
        errors = sorted(
            Draft202012Validator(
                schema, format_checker=FormatChecker()
            ).iter_errors(registry),
            key=lambda item: list(item.path),
        )
    except (SchemaError, TypeError, ValueError) as exc:
        raise LiteratureProviderError("文献 provider schema 无效") from exc
    if errors:
        raise LiteratureProviderError(
            f"文献 provider registry schema 无效：{errors[0].message}"
        )
    providers: dict[str, dict[str, Any]] = {}
    for provider in registry["providers"]:
        if not isinstance(provider, dict):
            raise LiteratureProviderError("文献 provider 条目必须是 object")
        provider_id = provider.get("id")
        if not isinstance(provider_id, str) or not provider_id or len(provider_id) > MAX_FIELD_CHARS:
            raise LiteratureProviderError("文献 provider ID 无效")
        if provider_id in providers:
            raise LiteratureProviderError(f"重复 provider ID：{provider_id}")
        auth = provider["auth"]
        if auth["mode"] == "none" and any(
            auth[field] is not None for field in ("name", "env")
        ):
            raise LiteratureProviderError(f"{provider_id}: auth=none 不得声明凭据")
        if auth["mode"] == "none" and auth["required_for_live"]:
            raise LiteratureProviderError(
                f"{provider_id}: auth=none 不得要求 live 凭据"
            )
        if auth["mode"] != "none" and not auth["name"]:
            raise LiteratureProviderError(f"{provider_id}: auth 缺少 name")
        if auth["mode"] != "none" and not auth["env"]:
            raise LiteratureProviderError(f"{provider_id}: auth 缺少 env")
        if not _is_https_url(provider.get("base_url")):
            raise LiteratureProviderError(f"{provider_id}: base_url 必须是无凭据 HTTPS URL")
        extra_query = provider.get("extra_query")
        if not isinstance(extra_query, dict) or len(extra_query) > MAX_EXTRA_QUERY_ITEMS:
            raise LiteratureProviderError(f"{provider_id}: extra_query 超过预算")
        if any(
            not isinstance(key, str)
            or not key
            or len(key) > MAX_FIELD_CHARS
            or not isinstance(value, (str, int, bool))
            or (isinstance(value, str) and len(value) > MAX_FIELD_CHARS)
            for key, value in extra_query.items()
        ):
            raise LiteratureProviderError(f"{provider_id}: extra_query 字段无效")
        contact = provider["contact"]
        if bool(contact["env"]) != bool(contact["query_parameter"]):
            raise LiteratureProviderError(
                f"{provider_id}: contact env 与 query_parameter 必须同时配置"
            )
        providers[provider_id] = provider
    return providers


def build_provider_request(
    provider: Mapping[str, Any],
    query: str,
    *,
    environ: Mapping[str, str],
    require_credentials: bool,
) -> tuple[urllib.request.Request, dict[str, Any]]:
    """构造真实请求和不含凭据值的审计摘要。"""
    if (
        not isinstance(provider, Mapping)
        or not isinstance(query, str)
        or not isinstance(environ, Mapping)
        or not isinstance(require_credentials, bool)
    ):
        raise LiteratureProviderError("provider/query/environment 类型无效")
    normalized_query = query.strip()
    if not normalized_query:
        raise LiteratureProviderError("检索 query 不能为空")
    if len(normalized_query) > MAX_QUERY_CHARS:
        raise LiteratureProviderError("检索 query 超过大小预算")
    provider_id = provider.get("id")
    base_url = provider.get("base_url")
    if (
        not isinstance(provider_id, str)
        or not provider_id
        or len(provider_id) > MAX_FIELD_CHARS
        or "\r" in provider_id
        or "\n" in provider_id
        or not isinstance(base_url, str)
        or not base_url
        or len(base_url) > MAX_FIELD_CHARS
        or not _is_https_url(base_url)
        or "?" in base_url
        or "#" in base_url
    ):
        raise LiteratureProviderError("provider base_url 必须是 HTTPS")
    max_response_value = provider.get("max_response_bytes")
    if isinstance(max_response_value, bool) or not isinstance(max_response_value, int):
        raise LiteratureProviderError("provider 响应大小预算无效")
    max_response_bytes = max_response_value
    if max_response_bytes <= 0 or max_response_bytes > ABSOLUTE_MAX_RESPONSE_BYTES:
        raise LiteratureProviderError("provider 响应大小预算无效")
    response_format = provider.get("response_format")
    if not isinstance(response_format, str) or response_format not in {"atom", "json"}:
        raise LiteratureProviderError("provider response_format 无效")
    try:
        extra_query = provider["extra_query"]
    except (KeyError, TypeError) as exc:
        raise LiteratureProviderError("provider extra_query 无效") from exc
    if not isinstance(extra_query, dict) or len(extra_query) > MAX_EXTRA_QUERY_ITEMS or any(
        not isinstance(key, str)
        or not key
        or len(key) > MAX_FIELD_CHARS
        or "\x00" in key
        or "\r" in key
        or "\n" in key
        or not isinstance(value, (str, int, bool))
        or (isinstance(value, str) and len(value) > MAX_FIELD_CHARS)
        for key, value in extra_query.items()
    ):
        raise LiteratureProviderError("provider extra_query 无效")
    timeout_value = provider.get("timeout_seconds")
    retries_value = provider.get("max_retries")
    if (
        isinstance(timeout_value, bool)
        or not isinstance(timeout_value, int)
        or isinstance(retries_value, bool)
        or not isinstance(retries_value, int)
    ):
        raise LiteratureProviderError("provider timeout/retries 无效")
    timeout_seconds = timeout_value
    max_retries = retries_value
    if (
        timeout_seconds <= 0
        or timeout_seconds > MAX_PROVIDER_TIMEOUT_SECONDS
        or max_retries < 0
        or max_retries > MAX_PROVIDER_RETRIES
    ):
        raise LiteratureProviderError("provider timeout/retries 超出预算")
    query_parameter = provider.get("query_parameter")
    if (
        not isinstance(query_parameter, str)
        or not query_parameter
        or len(query_parameter) > MAX_FIELD_CHARS
        or "\x00" in query_parameter
        or "\r" in query_parameter
        or "\n" in query_parameter
    ):
        raise LiteratureProviderError("provider query_parameter 无效")
    parameters = dict(extra_query)
    parameters[query_parameter] = normalized_query
    redacted_parameters = dict(parameters)
    headers = {"Accept": "application/json, application/atom+xml", "User-Agent": USER_AGENT}
    safe_headers = dict(headers)

    contact = provider.get("contact")
    if not isinstance(contact, Mapping):
        raise LiteratureProviderError("provider contact 无效")
    contact_env = contact.get("env")
    contact_parameter = contact.get("query_parameter")
    if bool(contact_env) != bool(contact_parameter):
        raise LiteratureProviderError("provider contact 配置不完整")
    if contact_env is not None:
        if (
            not isinstance(contact_env, str)
            or not contact_env
            or len(contact_env) > MAX_FIELD_CHARS
            or not isinstance(contact_parameter, str)
            or not contact_parameter
            or len(contact_parameter) > MAX_FIELD_CHARS
            or "\r" in contact_parameter
            or "\n" in contact_parameter
        ):
            raise LiteratureProviderError("provider contact 无效")
        contact_value = environ.get(contact_env, "")
        if not isinstance(contact_value, str) or len(contact_value) > MAX_FIELD_CHARS:
            raise LiteratureProviderError("provider contact 环境值无效")
        contact_value = contact_value.strip()
        if contact_value:
            parameters[contact_parameter] = contact_value
            redacted_parameters[contact_parameter] = "<configured>"

    auth = provider.get("auth")
    if not isinstance(auth, Mapping):
        raise LiteratureProviderError("provider auth 无效")
    auth_env = auth.get("env")
    auth_mode = auth.get("mode")
    required_for_live = auth.get("required_for_live")
    if not isinstance(required_for_live, bool):
        raise LiteratureProviderError("provider auth required_for_live 无效")
    if auth_mode not in {"none", "query", "header"}:
        raise LiteratureProviderError("provider auth mode 无效")
    auth_name_config = auth.get("name")
    if auth_mode == "none":
        if auth_env is not None or auth_name_config is not None or required_for_live:
            raise LiteratureProviderError("provider auth=none 配置无效")
    elif (
        not isinstance(auth_env, str)
        or not auth_env
        or len(auth_env) > MAX_FIELD_CHARS
        or not isinstance(auth_name_config, str)
        or not auth_name_config
        or len(auth_name_config) > MAX_FIELD_CHARS
        or "\r" in auth_name_config
        or "\n" in auth_name_config
    ):
        raise LiteratureProviderError("provider auth 配置不完整")
    secret = ""
    if auth_env is not None:
        if (
            not isinstance(auth_env, str)
            or not auth_env
            or len(auth_env) > MAX_FIELD_CHARS
        ):
            raise LiteratureProviderError("provider auth 环境名无效")
        secret = environ.get(auth_env, "")
        if not isinstance(secret, str) or len(secret) > MAX_FIELD_CHARS:
            raise LiteratureProviderError("provider auth 环境值无效")
        secret = secret.strip()
    if require_credentials and required_for_live and not secret:
        raise LiteratureProviderError(
            f"{provider_id}: 缺少受信凭据条目 {auth_env}"
        )
    if secret and auth_mode == "query":
        auth_name = auth.get("name")
        if (
            not isinstance(auth_name, str)
            or not auth_name
            or len(auth_name) > MAX_FIELD_CHARS
            or "\r" in auth_name
            or "\n" in auth_name
        ):
            raise LiteratureProviderError("provider auth name 无效")
        parameters[auth_name] = secret
        redacted_parameters[auth_name] = "<redacted>"
    elif secret and auth_mode == "header":
        auth_name = auth.get("name")
        if (
            not isinstance(auth_name, str)
            or not auth_name
            or len(auth_name) > MAX_FIELD_CHARS
            or "\r" in auth_name
            or "\n" in auth_name
        ):
            raise LiteratureProviderError("provider auth name 无效")
        headers[auth_name] = secret
        safe_headers[auth_name] = "<redacted>"

    url = f"{base_url}?{urllib.parse.urlencode(parameters)}"
    safe_url = f"{base_url}?{urllib.parse.urlencode(redacted_parameters)}"
    request = urllib.request.Request(url, headers=headers, method="GET")
    summary = {
        "provider": provider_id,
        "url": safe_url,
        "headers": safe_headers,
        "timeout_seconds": timeout_seconds,
        "max_retries": max_retries,
        "max_response_bytes": max_response_bytes,
        "response_format": response_format,
        "credential_env": auth_env,
        "credential_configured": bool(secret),
    }
    return request, summary


def check_provider_live(
    provider: Mapping[str, Any],
    query: str,
    *,
    environ: Mapping[str, str],
) -> dict[str, Any]:
    """执行一次有界 live 请求；只读取前 1 KiB，不保存响应正文。"""
    request, summary = build_provider_request(
        provider, query, environ=environ, require_credentials=True
    )
    retries = summary["max_retries"]
    timeout = summary["timeout_seconds"]
    max_bytes = summary["max_response_bytes"]
    last_error = ""
    started = time.monotonic()
    for attempt in range(retries + 1):
        try:
            with HTTPS_OPENER.open(request, timeout=timeout) as response:
                status = getattr(response, "status", 200)
                if isinstance(status, bool) or not isinstance(status, int):
                    raise LiteratureProviderError("provider HTTP status 无效")
                final_url = response.geturl()
                if not isinstance(final_url, str) or not _is_https_url(final_url):
                    raise LiteratureProviderError("provider 响应不是带主机的 HTTPS URL")
                declared_length = response.headers.get("Content-Length")
                if declared_length:
                    try:
                        declared_length_value = int(declared_length)
                    except (TypeError, ValueError) as exc:
                        raise LiteratureProviderError("provider Content-Length 无效") from exc
                    if declared_length_value > max_bytes:
                        raise LiteratureProviderError("provider 响应超过大小预算")
                    if declared_length_value < 0:
                        raise LiteratureProviderError("provider Content-Length 无效")
                total = 0
                deadline = time.monotonic() + timeout
                while True:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise LiteratureProviderError(f"provider 请求超时：{timeout}s")
                    # urllib applies a socket timeout per read; adjust the
                    # underlying socket as well so one slow read cannot outlive
                    # the monotonic deadline.
                    _set_response_timeout(response, min(timeout, remaining))
                    chunk = response.read(min(64 * 1024, max_bytes - total + 1))
                    if not isinstance(chunk, (bytes, bytearray)):
                        raise LiteratureProviderError("provider 响应块类型无效")
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > max_bytes:
                        raise LiteratureProviderError("provider 响应超过大小预算")
            if not 200 <= status < 300:
                raise LiteratureProviderError(
                    f"{provider['id']}: HTTP status={status}"
                )
            return {
                **summary,
                "status": "PASS",
                "http_status": status,
                "attempts": attempt + 1,
                "duration_seconds": round(time.monotonic() - started, 3),
            }
        except urllib.error.HTTPError as exc:
            last_error = f"HTTP {exc.code}"
            retryable = exc.code == 429 or 500 <= exc.code < 600
            if not retryable or attempt == retries:
                break
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = type(exc).__name__
            if attempt == retries:
                break
        if attempt < retries:
            time.sleep(min(2**attempt, 2))
    raise LiteratureProviderError(
        f"{provider['id']}: live health 失败（{last_error or 'unknown'}）"
    )
