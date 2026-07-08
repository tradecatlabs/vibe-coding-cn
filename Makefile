# Makefile for Vibe Coding Guide

.PHONY: help lint check-links check-details check-doc-structure check-directory-docs check-metadata check-ai-citation check-external-resources check-research-raw check-wiki fetch-research-raw sync-doc-toc build test clean clean-deps

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
	@echo "  check-ai-citation - Check llms and AI citation paths and anchors"
	@echo "  check-external-resources - Check local external resources registry"
	@echo "  check-research-raw - Check research raw fact snapshots and repository clones"
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
	@$(MARKDOWNLINT) --config .github/lint_config.json --ignore .history --ignore tools/external --ignore 'research/**/raw/repository/**' '**/*.md'

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

check-ai-citation:
	@echo "Checking llms and AI citation paths and anchors..."
	@python3 scripts/check-ai-citation.py

check-external-resources:
	@echo "Checking local external resources registry..."
	@python3 scripts/check-external-resources.py

check-research-raw:
	@echo "Checking research raw fact snapshots and repository clones..."
	@python3 scripts/check-research-raw.py

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

test: lint check-links check-details check-doc-structure check-directory-docs check-metadata check-ai-citation check-external-resources check-research-raw
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
