.PHONY: install check check-public-readme index-public-problems check-full check-production sync-supply-chain

install:
	python3 -m pip install -r requirements.txt

check:
	bash scripts/check.sh

check-public-readme:
	python3 scripts/check_public_readme.py --project-root .
	python3 scripts/check_ai_citation_assets.py --project-root .

index-public-problems:
	python3 scripts/query_vibemathing_public.py --catalog

check-full: check
	python3 scripts/sync_supply_chain.py --check
	python3 scripts/validate_problem_library.py
	python3 scripts/test_problem_library.py
	@if test -e problem-library/raw/candidates/inventory.json || test -e problem-library/derived/candidate-observations/latest.json; then \
		python3 scripts/validate_candidate_problem_library.py --verify-raw; \
	fi
	python3 scripts/validate_literature.py

check-production: check
	python3 scripts/pipeline_maturity_audit.py --strict

sync-supply-chain:
	python3 scripts/sync_supply_chain.py
