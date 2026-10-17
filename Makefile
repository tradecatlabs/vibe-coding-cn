# Vibe Coding工具箱：保留现有质量入口，路径统一为三域。
.PHONY: help lint check-links check-details test-details check-doc-structure check-directory-docs check-metadata check-gongfa test-gongfa sync-gongfa-catalog check-gongfa-catalog test-gongfa-catalog sync-faqi-catalog check-faqi-catalog test-faqi-catalog test-source-archive check-ai-citation check-external-resources check-research-raw check-source-facts check-wiki fetch-research-raw sync-doc-toc build test clean clean-deps

MARKDOWNLINT = npx --yes markdownlint-cli@0.48.0
EXT = .github/extensions
# 原tools/external各来源分别平铺；不能忽略整个Extensions，否则会漏掉自有工具。
SOURCE_IGNORES = --ignore .history --ignore '$(EXT)/Skill_Seekers-development/**' --ignore '$(EXT)/claude-official-skills/**' --ignore '$(EXT)/tmux/**' --ignore '$(EXT)/oh-my-tmux/**' --ignore '$(EXT)/MCPlayerTransfer/**' --ignore '$(EXT)/XHS-image-to-PDF-conversion/**' --ignore '$(EXT)/my-nvim/**' --ignore '$(EXT)/html-tools-main.md' --ignore '.github/context/research/**/raw/repository/**' --ignore '.github/context/research/facts/**' --ignore '.github/context/research/vibe-cybersecurity-cn/**' --ignore '.github/context/research/vibe-harness-cn/**' --ignore '.github/context/research/vibe-mathing-cn-public/**'

help:
	@echo "Vibe Coding工具箱"
	@echo "lint / check-links / check-details / test-details：Markdown格式、内链、折叠与回归"
	@echo "check-doc-structure / check-directory-docs / check-metadata：阅读结构、目录职责与机器索引"
	@echo "check-gongfa / test-gongfa：功法来源与既有评级协议"
	@echo "sync-gongfa-catalog / check-gongfa-catalog / test-gongfa-catalog：功法单一Markdown视图"
	@echo "sync-faqi-catalog / check-faqi-catalog / test-faqi-catalog：法器来源与单一Markdown视图"
	@echo "test-source-archive：原始字节、摘要、来源边界和文集导航契约"
	@echo "check-ai-citation / check-external-resources：AI引用与资源登记"
	@echo "check-research-raw / check-source-facts：研究事实及来源镜像"
	@echo "check-wiki WIKI_DIR=<本地目录>：独立Wiki检查"
	@echo "fetch-research-raw：显式联网刷新研究原始事实，不属于日常测试"
	@echo "sync-doc-toc：同步自有文档目录；生成文集由各自sync目标维护"
	@echo "build：说明本仓无需构建；test：运行本地质量检查"
	@echo "clean / clean-deps：现有清理入口，有删除副作用；不作为验证命令执行"

lint:
	@$(MARKDOWNLINT) --config .github/lint_config.json $(SOURCE_IGNORES) '**/*.md' '.github/context/**/*.md' '.github/skills/**/*.md' '.github/extensions/**/*.md'

check-links:
	@python3 $(EXT)/check-local-links.py

check-details:
	@python3 $(EXT)/check-markdown-details.py

test-details:
	@python3 $(EXT)/test-markdown-details.py

check-doc-structure:
	@python3 $(EXT)/check-doc-structure.py

check-directory-docs:
	@python3 $(EXT)/check-directory-docs.py

check-metadata:
	@python3 $(EXT)/check-metadata.py

check-gongfa:
	@python3 $(EXT)/check-gongfa.py

test-gongfa:
	@python3 $(EXT)/test-gongfa.py

sync-gongfa-catalog:
	@python3 $(EXT)/sync-gongfa-catalog.py --write

check-gongfa-catalog:
	@python3 $(EXT)/sync-gongfa-catalog.py --check

test-gongfa-catalog:
	@python3 $(EXT)/test-gongfa-catalog.py

sync-faqi-catalog:
	@python3 $(EXT)/sync-faqi-catalog.py --write

check-faqi-catalog:
	@python3 $(EXT)/sync-faqi-catalog.py --check

test-faqi-catalog:
	@python3 $(EXT)/test-faqi-catalog.py

test-source-archive:
	@python3 $(EXT)/test-source-archive.py

check-ai-citation:
	@python3 $(EXT)/check-ai-citation.py

check-external-resources:
	@python3 $(EXT)/check-external-resources.py

check-research-raw:
	@python3 $(EXT)/check-research-raw.py

check-source-facts:
	@python3 $(EXT)/check-source-facts.py

check-wiki:
	@python3 $(EXT)/check-wiki.py --wiki-dir "$${WIKI_DIR:-/tmp/vibe-coding-cn.wiki}"
	@$(MARKDOWNLINT) --config .github/lint_config.json "$${WIKI_DIR:-/tmp/vibe-coding-cn.wiki}"/*.md

fetch-research-raw:
	@python3 $(EXT)/fetch-research-raw.py

sync-doc-toc:
	@python3 $(EXT)/sync-doc-toc.py

build:
	@echo "无需构建；本仓是文档、既有Skills和小工具的资源集合。"

test: lint check-links check-details test-details check-doc-structure check-directory-docs check-metadata check-gongfa test-gongfa check-gongfa-catalog test-gongfa-catalog check-faqi-catalog test-faqi-catalog test-source-archive check-ai-citation check-external-resources check-research-raw check-source-facts
	@echo "本地质量检查完成；不代表工具效果、运行可用性或许可批准。"

clean: clean-deps
	@find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	@rm -rf .github/extensions/prompts-library/prompt_jsonl

clean-deps:
	@rm -rf node_modules
