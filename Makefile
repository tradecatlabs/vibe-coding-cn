# Makefile for Vibe Coding Guide

.PHONY: help lint check-links check-details check-doc-structure check-directory-docs check-metadata check-gongfa test-gongfa check-ai-citation check-external-resources check-research-raw check-source-facts check-wiki fetch-research-raw sync-doc-toc build test clean clean-deps

.PHONY: sync-gongfa-catalog check-gongfa-catalog test-gongfa-catalog
.PHONY: sync-faqi-catalog check-faqi-catalog test-faqi-catalog

MARKDOWNLINT = npx --yes markdownlint-cli@0.48.0

help:
	@echo "Makefile for Vibe Coding Guide"
	@echo ""
	@echo "Available commands:"
	@echo "  help     - Show this help message"
	@echo "  lint     - Lint all markdown files"
	@echo "  check-links - Check local markdown links and anchors"
	@echo "  check-details - Check markdown details/summary blocks"
	@echo "  check-doc-structure - Check docs README anchors, order and duplicate anchors"
	@echo "  check-directory-docs - Check required README/AGENTS pairs"
	@echo "  check-metadata - Check metadata paths and anchors"
	@echo "  check-gongfa - 校验功法JSON、冻结来源与评级协议"
	@echo "  test-gongfa - 执行功法JSON的隔离CLI集成测试并保留工件"
	@echo "  sync-gongfa-catalog - 从当前登记与仓内候选快照重建唯一总表"
	@echo "  check-gongfa-catalog - 只读校验总表覆盖、源摘要与Markdown/Excel一致性"
	@echo "  test-gongfa-catalog - 验证总表维护行为并保留隔离工件"
	@echo "  sync-faqi-catalog - 重建法器来源初审与资源分流的只读清单"
	@echo "  check-faqi-catalog - 校验法器JSON、Git/SHA、覆盖与只读清单"
	@echo "  test-faqi-catalog - 验证法器清单维护并保留隔离工件"
	@echo "  check-ai-citation - Check AI citation paths, anchors, and repository identity"
	@echo "  check-external-resources - Check local external resources registry"
	@echo "  check-research-raw - Check research raw fact snapshots and repository clones"
	@echo "  check-source-facts - Check external source-fact mirrors and provenance"
	@echo "  check-wiki - Check local GitHub Wiki checkout when present"
	@echo "  fetch-research-raw - Fetch raw GitHub facts and repository clones for research domains"
	@echo "  sync-doc-toc - Regenerate docs fine-grained TOC blocks"
	@echo "  build    - Verify knowledge base has no build step"
	@echo "  test     - Run repository quality gates"
	@echo "  clean    - Remove ignored generated caches"
	@echo "  clean-deps - Remove local dependency caches"
	@echo ""

lint:
	@echo "Linting markdown files..."
	@$(MARKDOWNLINT) --config .github/lint_config.json --ignore .history --ignore tools/external --ignore 'research/**/raw/repository/**' --ignore 'research/facts/**' --ignore 'research/vibe-cybersecurity-cn/**' --ignore 'research/vibe-harness-cn/**' --ignore 'research/vibe-mathing-cn-public/**' '**/*.md'

check-links:
	@echo "Checking local markdown links and anchors..."
	@python3 scripts/check-local-links.py

check-details:
	@echo "Checking markdown details/summary blocks..."
	@python3 scripts/check-markdown-details.py

check-doc-structure:
	@echo "Checking docs README structure..."
	@python3 scripts/check-doc-structure.py

check-directory-docs:
	@echo "Checking required directory README/AGENTS pairs..."
	@python3 scripts/check-directory-docs.py

check-metadata:
	@echo "Checking metadata paths and anchors..."
	@python3 scripts/check-metadata.py

check-gongfa:
	@echo "校验功法JSON、冻结来源与评级引用..."
	@python3 scripts/check-gongfa.py

test-gongfa:
	@echo "执行功法JSON CLI集成测试..."
	@python3 scripts/test-gongfa.py

sync-gongfa-catalog:
	@python3 scripts/sync-gongfa-catalog.py --write

check-gongfa-catalog:
	@python3 scripts/sync-gongfa-catalog.py --check

test-gongfa-catalog:
	@python3 scripts/test-gongfa-catalog.py

sync-faqi-catalog:
	@python3 scripts/sync-faqi-catalog.py --write

check-faqi-catalog:
	@python3 scripts/sync-faqi-catalog.py --check

test-faqi-catalog:
	@python3 scripts/test-faqi-catalog.py

check-ai-citation:
	@echo "Checking AI citation paths, anchors, and repository identity..."
	@python3 scripts/check-ai-citation.py

check-external-resources:
	@echo "Checking local external resources registry..."
	@python3 scripts/check-external-resources.py

check-research-raw:
	@echo "Checking research raw fact snapshots and repository clones..."
	@python3 scripts/check-research-raw.py

check-source-facts:
	@echo "Checking external source-fact mirrors and provenance..."
	@python3 scripts/check-source-facts.py

check-wiki:
	@echo "Checking local GitHub Wiki checkout..."
	@python3 scripts/check-wiki.py --wiki-dir "$${WIKI_DIR:-/tmp/vibe-coding-cn.wiki}"
	@$(MARKDOWNLINT) --config .github/lint_config.json "$${WIKI_DIR:-/tmp/vibe-coding-cn.wiki}"/*.md

fetch-research-raw:
	@echo "Fetching raw GitHub facts and repository clones for research domains..."
	@python3 scripts/fetch-research-raw.py

sync-doc-toc:
	@echo "Regenerating docs fine-grained TOC blocks..."
	@python3 scripts/sync-doc-toc.py

build:
	@echo "No build step: this repository is a documentation and knowledge-base project."

test: lint check-links check-details check-doc-structure check-directory-docs check-metadata check-gongfa test-gongfa check-gongfa-catalog test-gongfa-catalog check-faqi-catalog test-faqi-catalog check-ai-citation check-external-resources check-research-raw check-source-facts
	@echo "Quality gates complete."

clean: clean-deps
	@echo "Cleaning ignored generated caches..."
	@find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	@rm -rf tools/prompts-library/prompt_jsonl
	@echo "Cleanup complete."

clean-deps:
	@echo "Cleaning local dependency caches..."
	@rm -rf node_modules
	@echo "Dependency cleanup complete."
