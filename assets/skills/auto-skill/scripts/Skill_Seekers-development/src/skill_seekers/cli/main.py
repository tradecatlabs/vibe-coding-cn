#!/usr/bin/env python3
"""
Skill Seekers - Unified CLI Entry Point

Provides a git-style unified command-line interface for all Skill Seekers tools.

Usage:
    skill-seekers <command> [options]

Commands:
    scrape      Scrape documentation website
    github      Scrape GitHub repository
    pdf         Extract from PDF file
    unified     Multi-source scraping (docs + GitHub + PDF)
    enhance     AI-powered enhancement (local, no API key)
    package     Package skill into .zip file
    upload      Upload skill to Claude
    estimate    Estimate page count before scraping

Examples:
    skill-seekers scrape --config configs/react.json
    skill-seekers github --repo microsoft/TypeScript
    skill-seekers unified --config configs/react_unified.json
    skill-seekers package output/react/
"""

import sys
import argparse
from typing import List, Optional


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="skill-seekers",
        description="Convert documentation, GitHub repos, and PDFs into Claude AI skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape documentation
  skill-seekers scrape --config configs/react.json

  # Scrape GitHub repository
  skill-seekers github --repo microsoft/TypeScript --name typescript

  # Multi-source scraping (unified)
  skill-seekers unified --config configs/react_unified.json

  # AI-powered enhancement
  skill-seekers enhance output/react/

  # Package and upload
  skill-seekers package output/react/
  skill-seekers upload output/react.zip

For more information: https://github.com/yusufkaraaslan/Skill_Seekers
        """
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 2.1.1"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        description="Available Skill Seekers commands",
        help="Command to run"
    )

    # === scrape subcommand ===
    scrape_parser = subparsers.add_parser(
        "scrape",
        help="Scrape documentation website",
        description="Scrape documentation website and generate skill"
    )
    scrape_parser.add_argument("--config", help="Config JSON file")
    scrape_parser.add_argument("--name", help="Skill name")
    scrape_parser.add_argument("--url", help="Documentation URL")
    scrape_parser.add_argument("--description", help="Skill description")
    scrape_parser.add_argument("--skip-scrape", action="store_true", help="Skip scraping, use cached data")
    scrape_parser.add_argument("--enhance", action="store_true", help="AI enhancement (API)")
    scrape_parser.add_argument("--enhance-local", action="store_true", help="AI enhancement (local)")
    scrape_parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    scrape_parser.add_argument("--async", dest="async_mode", action="store_true", help="Use async scraping")
    scrape_parser.add_argument("--workers", type=int, help="Number of async workers")

    # === github subcommand ===
    github_parser = subparsers.add_parser(
        "github",
        help="Scrape GitHub repository",
        description="Scrape GitHub repository and generate skill"
    )
    github_parser.add_argument("--config", help="Config JSON file")
    github_parser.add_argument("--repo", help="GitHub repo (owner/repo)")
    github_parser.add_argument("--name", help="Skill name")
    github_parser.add_argument("--description", help="Skill description")

    # === pdf subcommand ===
    pdf_parser = subparsers.add_parser(
        "pdf",
        help="Extract from PDF file",
        description="Extract content from PDF and generate skill"
    )
    pdf_parser.add_argument("--config", help="Config JSON file")
    pdf_parser.add_argument("--pdf", help="PDF file path")
    pdf_parser.add_argument("--name", help="Skill name")
    pdf_parser.add_argument("--description", help="Skill description")
    pdf_parser.add_argument("--from-json", help="Build from extracted JSON")

    # === unified subcommand ===
    unified_parser = subparsers.add_parser(
        "unified",
        help="Multi-source scraping (docs + GitHub + PDF)",
        description="Combine multiple sources into one skill"
    )
    unified_parser.add_argument("--config", required=True, help="Unified config JSON file")
    unified_parser.add_argument("--merge-mode", help="Merge mode (rule-based, claude-enhanced)")
    unified_parser.add_argument("--dry-run", action="store_true", help="Dry run mode")

    # === enhance subcommand ===
    enhance_parser = subparsers.add_parser(
        "enhance",
        help="AI-powered enhancement (local, no API key)",
        description="Enhance SKILL.md using Claude Code (local)"
    )
    enhance_parser.add_argument("skill_directory", help="Skill directory path")

    # === package subcommand ===
    package_parser = subparsers.add_parser(
        "package",
        help="Package skill into .zip file",
        description="Package skill directory into uploadable .zip"
    )
    package_parser.add_argument("skill_directory", help="Skill directory path")
    package_parser.add_argument("--no-open", action="store_true", help="Don't open output folder")
    package_parser.add_argument("--upload", action="store_true", help="Auto-upload after packaging")

    # === upload subcommand ===
    upload_parser = subparsers.add_parser(
        "upload",
        help="Upload skill to Claude",
        description="Upload .zip file to Claude via Anthropic API"
    )
    upload_parser.add_argument("zip_file", help=".zip file to upload")
    upload_parser.add_argument("--api-key", help="Anthropic API key")

    # === estimate subcommand ===
    estimate_parser = subparsers.add_parser(
        "estimate",
        help="Estimate page count before scraping",
        description="Estimate total pages for documentation scraping"
    )
    estimate_parser.add_argument("config", help="Config JSON file")
    estimate_parser.add_argument("--max-discovery", type=int, help="Max pages to discover")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the unified CLI.

    Args:
        argv: Command-line arguments (defaults to sys.argv)

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    # Delegate to the appropriate tool
    try:
        if args.command == "scrape":
            from skill_seekers.cli.doc_scraper import main as scrape_main
            # Convert args namespace to sys.argv format for doc_scraper
            sys.argv = ["doc_scraper.py"]
            if args.config:
                sys.argv.extend(["--config", args.config])
            if args.name:
                sys.argv.extend(["--name", args.name])
            if args.url:
                sys.argv.extend(["--url", args.url])
            if args.description:
                sys.argv.extend(["--description", args.description])
            if args.skip_scrape:
                sys.argv.append("--skip-scrape")
            if args.enhance:
                sys.argv.append("--enhance")
            if args.enhance_local:
                sys.argv.append("--enhance-local")
            if args.dry_run:
                sys.argv.append("--dry-run")
            if args.async_mode:
                sys.argv.append("--async")
            if args.workers:
                sys.argv.extend(["--workers", str(args.workers)])
            return scrape_main() or 0

        elif args.command == "github":
            from skill_seekers.cli.github_scraper import main as github_main
            sys.argv = ["github_scraper.py"]
            if args.config:
                sys.argv.extend(["--config", args.config])
            if args.repo:
                sys.argv.extend(["--repo", args.repo])
            if args.name:
                sys.argv.extend(["--name", args.name])
            if args.description:
                sys.argv.extend(["--description", args.description])
            return github_main() or 0

        elif args.command == "pdf":
            from skill_seekers.cli.pdf_scraper import main as pdf_main
            sys.argv = ["pdf_scraper.py"]
            if args.config:
                sys.argv.extend(["--config", args.config])
            if args.pdf:
                sys.argv.extend(["--pdf", args.pdf])
            if args.name:
                sys.argv.extend(["--name", args.name])
            if args.description:
                sys.argv.extend(["--description", args.description])
            if args.from_json:
                sys.argv.extend(["--from-json", args.from_json])
            return pdf_main() or 0

        elif args.command == "unified":
            from skill_seekers.cli.unified_scraper import main as unified_main
            sys.argv = ["unified_scraper.py", "--config", args.config]
            if args.merge_mode:
                sys.argv.extend(["--merge-mode", args.merge_mode])
            if args.dry_run:
                sys.argv.append("--dry-run")
            return unified_main() or 0

        elif args.command == "enhance":
            from skill_seekers.cli.enhance_skill_local import main as enhance_main
            sys.argv = ["enhance_skill_local.py", args.skill_directory]
            return enhance_main() or 0

        elif args.command == "package":
            from skill_seekers.cli.package_skill import main as package_main
            sys.argv = ["package_skill.py", args.skill_directory]
            if args.no_open:
                sys.argv.append("--no-open")
            if args.upload:
                sys.argv.append("--upload")
            return package_main() or 0

        elif args.command == "upload":
            from skill_seekers.cli.upload_skill import main as upload_main
            sys.argv = ["upload_skill.py", args.zip_file]
            if args.api_key:
                sys.argv.extend(["--api-key", args.api_key])
            return upload_main() or 0

        elif args.command == "estimate":
            from skill_seekers.cli.estimate_pages import main as estimate_main
            sys.argv = ["estimate_pages.py", args.config]
            if args.max_discovery:
                sys.argv.extend(["--max-discovery", str(args.max_discovery)])
            return estimate_main() or 0

        else:
            print(f"Error: Unknown command '{args.command}'", file=sys.stderr)
            parser.print_help()
            return 1

    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
