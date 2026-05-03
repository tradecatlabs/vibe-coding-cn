# Makefile for Vibe Coding Guide

.PHONY: help lint check-links check-details build test clean

help:
	@echo "Makefile for Vibe Coding Guide"
	@echo ""
	@echo "Available commands:"
	@echo "  help     - Show this help message"
	@echo "  lint     - Lint all markdown files"
	@echo "  check-links - Check local markdown links and anchors"
	@echo "  check-details - Check markdown details/summary blocks"
	@echo "  build    - Verify knowledge base has no build step"
	@echo "  test     - Run repository quality gates"
	@echo "  clean    - Remove ignored generated caches"
	@echo ""

lint:
	@echo "Linting markdown files..."
	@npm install -g markdownlint-cli
	@markdownlint --config .github/lint_config.json --ignore .history --ignore tools/external '**/*.md'

check-links:
	@echo "Checking local markdown links and anchors..."
	@python3 scripts/check-local-links.py

check-details:
	@echo "Checking markdown details/summary blocks..."
	@python3 scripts/check-markdown-details.py

build:
	@echo "No build step: this repository is a documentation and knowledge-base project."

test: lint check-links check-details
	@echo "Quality gates complete."

clean:
	@echo "Cleaning ignored generated caches..."
	@find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	@rm -rf tools/prompts-library/prompt_jsonl
	@echo "Cleanup complete."
