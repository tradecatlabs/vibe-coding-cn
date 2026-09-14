#!/usr/bin/env python3
# 做什么：离线验证 provider registry、请求构造、凭据脱敏和失败语义。
# 怎么运行：python3 scripts/test_literature_providers.py
# 需要什么：Python 3、jsonschema；不访问网络、不读取真实凭据。

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

from vibe_mathing.literature import (
    LiteratureProviderError,
    build_provider_request,
    load_provider_registry,
)


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    registry = load_provider_registry(ROOT)
    assert list(registry) == ["arxiv", "crossref", "openalex", "semantic-scholar"]
    fake_env = {
        "CROSSREF_MAILTO": "contact-value",
        "OPENALEX_API_KEY": "openalex-test-value",
        "SEMANTIC_SCHOLAR_API_KEY": "semantic-test-value",
    }
    summaries = []
    for provider in registry.values():
        request, summary = build_provider_request(
            provider,
            "spectral graph theory",
            environ=fake_env,
            require_credentials=True,
        )
        assert request.full_url.startswith("https://")
        assert summary["url"].startswith("https://")
        summaries.append(summary)
    encoded = json.dumps(summaries, ensure_ascii=False)
    assert "openalex-test-value" not in encoded
    assert "semantic-test-value" not in encoded
    assert "contact-value" not in encoded
    decoded_query_values = {
        value
        for summary in summaries
        for values in urllib.parse.parse_qs(
            urllib.parse.urlsplit(summary["url"]).query
        ).values()
        for value in values
    }
    assert "<redacted>" in decoded_query_values
    assert "<configured>" in decoded_query_values

    try:
        build_provider_request(
            registry["openalex"],
            "graph theory",
            environ={},
            require_credentials=True,
        )
    except LiteratureProviderError as exc:
        assert "OPENALEX_API_KEY" in str(exc)
    else:
        raise AssertionError("OpenAlex live 检查缺凭据时必须失败")

    insecure_provider = dict(registry["arxiv"])
    insecure_provider["base_url"] = "http://insecure.invalid/api"
    try:
        build_provider_request(
            insecure_provider,
            "graph theory",
            environ={},
            require_credentials=False,
        )
    except LiteratureProviderError as exc:
        assert "HTTPS" in str(exc)
    else:
        raise AssertionError("非 HTTPS provider 请求必须在构造阶段失败")

    with tempfile.TemporaryDirectory(prefix="vibe-mathing-provider-schema-") as temporary:
        base = Path(temporary)
        (base / "literature/schema").mkdir(parents=True)
        shutil.copy2(
            ROOT / "literature/schema/literature-providers.schema.json",
            base / "literature/schema/literature-providers.schema.json",
        )
        source = json.loads(
            (ROOT / "literature/providers.json").read_text(encoding="utf-8")
        )
        invalid_cases = []

        insecure = json.loads(json.dumps(source))
        insecure["providers"][0]["base_url"] = "http://insecure.invalid"
        invalid_cases.append((insecure, "schema 无效", "非 HTTPS provider"))

        impossible_auth = json.loads(json.dumps(source))
        impossible_auth["providers"][0]["auth"]["required_for_live"] = True
        invalid_cases.append((impossible_auth, "不得要求 live 凭据", "无认证 live 凭据"))

        incomplete_contact = json.loads(json.dumps(source))
        incomplete_contact["providers"][1]["contact"]["query_parameter"] = None
        invalid_cases.append((incomplete_contact, "必须同时配置", "不完整 contact"))

        for invalid, expected, label in invalid_cases:
            (base / "literature/providers.json").write_text(
                json.dumps(invalid), encoding="utf-8"
            )
            try:
                load_provider_registry(base)
            except LiteratureProviderError as exc:
                assert expected in str(exc)
            else:
                raise AssertionError(f"{label} 必须被拒绝")

    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts/check_literature_providers.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
        env={"PATH": "/usr/bin:/bin"},
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["live"] is False
    assert {item["status"] for item in payload["providers"]} == {"CONFIGURED"}
    print("文献 provider 测试通过：4 个 registry 条目、脱敏请求与离线失败语义成立。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
