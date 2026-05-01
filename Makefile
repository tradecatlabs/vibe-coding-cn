# Makefile for Vibe Coding Guide

.PHONY: help lint build test clean

help:
	@echo "Makefile for Vibe Coding Guide"
	@echo ""
	@echo "Available commands:"
	@echo "  help     - Show this help message"
	@echo "  lint     - Lint all markdown files"
	@echo "  build    - Build the project (Placeholder)"
	@echo "  test     - Run tests (Placeholder)"
	@echo "  clean    - Clean build artifacts (Placeholder)"
	@echo ""

lint:
	@echo "Linting markdown files..."
	@npm install -g markdownlint-cli
	@markdownlint --config .github/lint_config.json --ignore .history --ignore tools/external --ignore scripts/backups/gz '**/*.md'

build:
	@echo "Building the project..."
	# Add your project build commands here
	@echo "Build complete."

test:
	@echo "Running tests..."
	# Add your test commands here
	@echo "Tests complete."

clean:
	@echo "Cleaning up build artifacts..."
	# Add your clean commands here (e.g., rm -rf dist/ build/)
	@echo "Cleanup complete."
