#!/usr/bin/env python3
"""
Config Splitter for Large Documentation Sites

Splits large documentation configs into multiple smaller, focused skill configs.
Supports multiple splitting strategies: category-based, size-based, and automatic.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict


class ConfigSplitter:
    """Splits large documentation configs into multiple focused configs"""

    def __init__(self, config_path: str, strategy: str = "auto", target_pages: int = 5000):
        self.config_path = Path(config_path)
        self.strategy = strategy
        self.target_pages = target_pages
        self.config = self.load_config()
        self.base_name = self.config['name']

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: Config file not found: {self.config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in config file: {e}")
            sys.exit(1)

    def get_split_strategy(self) -> str:
        """Determine split strategy"""
        # Check if strategy is defined in config
        if 'split_strategy' in self.config:
            config_strategy = self.config['split_strategy']
            if config_strategy != "none":
                return config_strategy

        # Use provided strategy or auto-detect
        if self.strategy == "auto":
            max_pages = self.config.get('max_pages', 500)

            if max_pages < 5000:
                print(f"ℹ️  Small documentation ({max_pages} pages) - no splitting needed")
                return "none"
            elif max_pages < 10000 and 'categories' in self.config:
                print(f"ℹ️  Medium documentation ({max_pages} pages) - category split recommended")
                return "category"
            elif 'categories' in self.config and len(self.config['categories']) >= 3:
                print(f"ℹ️  Large documentation ({max_pages} pages) - router + categories recommended")
                return "router"
            else:
                print(f"ℹ️  Large documentation ({max_pages} pages) - size-based split")
                return "size"

        return self.strategy

    def split_by_category(self, create_router: bool = False) -> List[Dict[str, Any]]:
        """Split config by categories"""
        if 'categories' not in self.config:
            print("❌ Error: No categories defined in config")
            sys.exit(1)

        categories = self.config['categories']
        split_categories = self.config.get('split_config', {}).get('split_by_categories')

        # If specific categories specified, use only those
        if split_categories:
            categories = {k: v for k, v in categories.items() if k in split_categories}

        configs = []

        for category_name, keywords in categories.items():
            # Create new config for this category
            new_config = self.config.copy()
            new_config['name'] = f"{self.base_name}-{category_name}"
            new_config['description'] = f"{self.base_name.capitalize()} - {category_name.replace('_', ' ').title()}. {self.config.get('description', '')}"

            # Update URL patterns to focus on this category
            url_patterns = new_config.get('url_patterns', {})

            # Add category keywords to includes
            includes = url_patterns.get('include', [])
            for keyword in keywords:
                if keyword.startswith('/'):
                    includes.append(keyword)

            if includes:
                url_patterns['include'] = list(set(includes))
                new_config['url_patterns'] = url_patterns

            # Keep only this category
            new_config['categories'] = {category_name: keywords}

            # Remove split config from child
            if 'split_strategy' in new_config:
                del new_config['split_strategy']
            if 'split_config' in new_config:
                del new_config['split_config']

            # Adjust max_pages estimate
            if 'max_pages' in new_config:
                new_config['max_pages'] = self.target_pages

            configs.append(new_config)

        print(f"✅ Created {len(configs)} category-based configs")

        # Optionally create router config
        if create_router:
            router_config = self.create_router_config(configs)
            configs.insert(0, router_config)
            print(f"✅ Created router config: {router_config['name']}")

        return configs

    def split_by_size(self) -> List[Dict[str, Any]]:
        """Split config by size (page count)"""
        max_pages = self.config.get('max_pages', 500)
        num_splits = (max_pages + self.target_pages - 1) // self.target_pages

        configs = []

        for i in range(num_splits):
            new_config = self.config.copy()
            part_num = i + 1
            new_config['name'] = f"{self.base_name}-part{part_num}"
            new_config['description'] = f"{self.base_name.capitalize()} - Part {part_num}. {self.config.get('description', '')}"
            new_config['max_pages'] = self.target_pages

            # Remove split config from child
            if 'split_strategy' in new_config:
                del new_config['split_strategy']
            if 'split_config' in new_config:
                del new_config['split_config']

            configs.append(new_config)

        print(f"✅ Created {len(configs)} size-based configs ({self.target_pages} pages each)")
        return configs

    def create_router_config(self, sub_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a router config that references sub-skills"""
        router_name = self.config.get('split_config', {}).get('router_name', self.base_name)

        router_config = {
            "name": router_name,
            "description": self.config.get('description', ''),
            "base_url": self.config['base_url'],
            "selectors": self.config['selectors'],
            "url_patterns": self.config.get('url_patterns', {}),
            "rate_limit": self.config.get('rate_limit', 0.5),
            "max_pages": 500,  # Router only needs overview pages
            "_router": True,
            "_sub_skills": [cfg['name'] for cfg in sub_configs],
            "_routing_keywords": {
                cfg['name']: list(cfg.get('categories', {}).keys())
                for cfg in sub_configs
            }
        }

        return router_config

    def split(self) -> List[Dict[str, Any]]:
        """Execute split based on strategy"""
        strategy = self.get_split_strategy()

        print(f"\n{'='*60}")
        print(f"CONFIG SPLITTER: {self.base_name}")
        print(f"{'='*60}")
        print(f"Strategy: {strategy}")
        print(f"Target pages per skill: {self.target_pages}")
        print("")

        if strategy == "none":
            print("ℹ️  No splitting required")
            return [self.config]

        elif strategy == "category":
            return self.split_by_category(create_router=False)

        elif strategy == "router":
            create_router = self.config.get('split_config', {}).get('create_router', True)
            return self.split_by_category(create_router=create_router)

        elif strategy == "size":
            return self.split_by_size()

        else:
            print(f"❌ Error: Unknown strategy: {strategy}")
            sys.exit(1)

    def save_configs(self, configs: List[Dict[str, Any]], output_dir: Path = None) -> List[Path]:
        """Save configs to files"""
        if output_dir is None:
            output_dir = self.config_path.parent

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        saved_files = []

        for config in configs:
            filename = f"{config['name']}.json"
            filepath = output_dir / filename

            with open(filepath, 'w') as f:
                json.dump(config, f, indent=2)

            saved_files.append(filepath)
            print(f"  💾 Saved: {filepath}")

        return saved_files


def main():
    parser = argparse.ArgumentParser(
        description="Split large documentation configs into multiple focused skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-detect strategy
  python3 split_config.py configs/godot.json

  # Use category-based split
  python3 split_config.py configs/godot.json --strategy category

  # Use router + categories
  python3 split_config.py configs/godot.json --strategy router

  # Custom target size
  python3 split_config.py configs/godot.json --target-pages 3000

  # Dry run (don't save files)
  python3 split_config.py configs/godot.json --dry-run

Split Strategies:
  none     - No splitting (single skill)
  auto     - Automatically choose best strategy
  category - Split by categories defined in config
  router   - Create router + category-based sub-skills
  size     - Split by page count
        """
    )

    parser.add_argument(
        'config',
        help='Path to config file (e.g., configs/godot.json)'
    )

    parser.add_argument(
        '--strategy',
        choices=['auto', 'none', 'category', 'router', 'size'],
        default='auto',
        help='Splitting strategy (default: auto)'
    )

    parser.add_argument(
        '--target-pages',
        type=int,
        default=5000,
        help='Target pages per skill (default: 5000)'
    )

    parser.add_argument(
        '--output-dir',
        help='Output directory for configs (default: same as input)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be created without saving files'
    )

    args = parser.parse_args()

    # Create splitter
    splitter = ConfigSplitter(args.config, args.strategy, args.target_pages)

    # Split config
    configs = splitter.split()

    if args.dry_run:
        print(f"\n{'='*60}")
        print("DRY RUN - No files saved")
        print(f"{'='*60}")
        print(f"Would create {len(configs)} config files:")
        for cfg in configs:
            is_router = cfg.get('_router', False)
            router_marker = " (ROUTER)" if is_router else ""
            print(f"  📄 {cfg['name']}.json{router_marker}")
    else:
        print(f"\n{'='*60}")
        print("SAVING CONFIGS")
        print(f"{'='*60}")
        saved_files = splitter.save_configs(configs, args.output_dir)

        print(f"\n{'='*60}")
        print("NEXT STEPS")
        print(f"{'='*60}")
        print("1. Review generated configs")
        print("2. Scrape each config:")
        for filepath in saved_files:
            print(f"     skill-seekers scrape --config {filepath}")
        print("3. Package skills:")
        print("     skill-seekers-package-multi configs/<name>-*.json")
        print("")


if __name__ == "__main__":
    main()
