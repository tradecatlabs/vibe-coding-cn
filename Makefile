# Makefile for Vibe Coding Guide

.PHONY: help lint check-links check-details check-doc-structure check-metadata check-ai-citation build test clean

help:
	@echo "Makefile for Vibe Coding Guide"
	@echo ""
	@echo "Available commands:"
	@echo "  help     - Show this help message"
	@echo "  lint     - Lint all markdown files"
	@echo "  check-links - Check local markdown links and anchors"
	@echo "  check-details - Check markdown details/summary blocks"
	@echo "  check-doc-structure - Check docs README anchors, order and duplicate anchors"
	@echo "  check-metadata - Check metadata paths and anchors"
	@echo "  check-ai-citation - Check llms and AI citation paths and anchors"
	@echo "  build    - Verify knowledge base has no build step"
	@echo "  test     - Run repository quality gates"
	@echo "  clean    - Remove ignored generated caches"
	@echo ""

node_modules/.bin/markdownlint: package.json package-lock.json
	@npm ci

lint: node_modules/.bin/markdownlint
	@echo "Linting markdown files..."
	@npm run lint:md

check-links:
	@echo "Checking local markdown links and anchors..."
	@python3 scripts/check-local-links.py

check-details:
	@echo "Checking markdown details/summary blocks..."
	@python3 scripts/check-markdown-details.py

check-doc-structure:
	@echo "Checking docs README structure..."
	@python3 scripts/check-doc-structure.py

check-metadata:
	@echo "Checking metadata paths and anchors..."
	@python3 scripts/check-metadata.py

check-ai-citation:
	@echo "Checking llms and AI citation paths and anchors..."
	@python3 scripts/check-ai-citation.py

build:
	@echo "No build step: this repository is a documentation and knowledge-base project."

test: lint check-links check-details check-doc-structure check-metadata check-ai-citation
	@echo "Quality gates complete."

clean:
	@echo "Cleaning ignored generated caches..."
	@find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	@rm -rf tools/prompts-library/prompt_jsonl
	@echo "Cleanup complete."
