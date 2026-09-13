#!/usr/bin/env python3
# 做什么：验证文献 provider 配置，或显式执行有界 live 健康检查。
# 怎么运行：python3 scripts/check_literature_providers.py [--live] [--provider ID]
# 需要什么：Python 3、jsonschema；live 所需凭据只能由受信管理器注入环境。

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from vibe_mathing.literature import (
    LiteratureProviderError,
    build_provider_request,
    check_provider_live,
    load_provider_registry,
)


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="文献 provider 配置与 live 健康检查")
    parser.add_argument("--live", action="store_true", help="显式访问 provider；默认只做离线契约检查")
    parser.add_argument("--provider", action="append", dest="providers", help="只检查指定 provider；可重复")
    parser.add_argument("--query", default="graph theory", help="健康检查检索词")
    args = parser.parse_args()
    try:
        registry = load_provider_registry(ROOT)
        selected = args.providers or list(registry)
        unknown = sorted(set(selected).difference(registry))
        if unknown:
            raise LiteratureProviderError(f"未知 provider：{', '.join(unknown)}")
        results = []
        for provider_id in selected:
            provider = registry[provider_id]
            if args.live:
                results.append(
                    check_provider_live(provider, args.query, environ=os.environ)
                )
            else:
                _, summary = build_provider_request(
                    provider,
                    args.query,
                    environ=os.environ,
                    require_credentials=False,
                )
                results.append({**summary, "status": "CONFIGURED"})
    except LiteratureProviderError as exc:
        parser.error(str(exc))
    print(json.dumps({"live": args.live, "providers": results}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
