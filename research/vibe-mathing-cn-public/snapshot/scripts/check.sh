#!/usr/bin/env bash
# 做什么：运行不依赖本地缓存和电子书二进制的项目统一质量门。
# 怎么运行：bash scripts/check.sh
# 需要什么：Python 3、requirements.txt；任一检查失败即非零退出。

set -euo pipefail

python3 scripts/test_validate_public_boundary.py
python3 scripts/validate_public_boundary.py --project-root .
python3 scripts/check_public_readme.py --project-root .
python3 scripts/test_audit_public_status.py
python3 scripts/audit_public_status.py --project-root . --expect-empty
python3 scripts/check_ai_citation_assets.py --project-root .
python3 scripts/validate_plfb_metamodel.py --project-root .
python3 scripts/test_validate_plfb_metamodel.py
python3 scripts/validate_project.py
python3 scripts/smoke_math.py
python3 scripts/validate_math_tool_maturity.py
python3 scripts/test_validate_math_tool_maturity.py
python3 scripts/test_check_math_tools.py
python3 scripts/test_run_math_tool_canaries.py
python3 scripts/test_validate_math_tool_canaries.py
python3 scripts/test_literature_providers.py
python3 scripts/check_literature_providers.py
python3 scripts/test_validate_candidate_problem_library.py
python3 scripts/test_build_candidate_observations.py
python3 scripts/test_fetch_candidates.py
python3 scripts/test_query_problem_library.py
python3 scripts/test_query_vibemathing_public.py
python3 scripts/test_query_ai_citation.py
python3 scripts/validate_portable_problem_library.py
python3 scripts/validate_portable_literature.py
python3 scripts/validate_research_spaces.py
python3 scripts/test_trusted_evidence.py
python3 scripts/test_evidence_attacks.py
python3 scripts/test_research_spaces.py
python3 scripts/test_problem_contract.py
python3 scripts/test_research_bundle.py
python3 scripts/test_smt_pipeline.py
python3 scripts/test_validate_failed_routes.py
python3 scripts/validate_failed_routes.py
python3 scripts/test_research_store.py
python3 scripts/test_vibe_mathing_runtime.py
python3 scripts/test_vibe_mathing_pipeline.py
python3 scripts/test_sync_supply_chain.py
python3 governance/tools/validate_governance_package.py --project-root . --strict
python3 governance/tools/governance_health_report.py --project-root . --strict
