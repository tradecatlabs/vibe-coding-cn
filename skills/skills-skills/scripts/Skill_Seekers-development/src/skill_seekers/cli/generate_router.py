#!/usr/bin/env python3
"""
Router Skill Generator

Creates a router/hub skill that intelligently directs queries to specialized sub-skills.
This is used for large documentation sites split into multiple focused skills.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple


class RouterGenerator:
    """Generates router skills that direct to specialized sub-skills"""

    def __init__(self, config_paths: List[str], router_name: str = None):
        self.config_paths = [Path(p) for p in config_paths]
        self.configs = [self.load_config(p) for p in self.config_paths]
        self.router_name = router_name or self.infer_router_name()
        self.base_config = self.configs[0]  # Use first as template

    def load_config(self, path: Path) -> Dict[str, Any]:
        """Load a config file"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading {path}: {e}")
            sys.exit(1)

    def infer_router_name(self) -> str:
        """Infer router name from sub-skill names"""
        # Find common prefix
        names = [cfg['name'] for cfg in self.configs]
        if not names:
            return "router"

        # Get common prefix before first dash
        first_name = names[0]
        if '-' in first_name:
            return first_name.split('-')[0]
        return first_name

    def extract_routing_keywords(self) -> Dict[str, List[str]]:
        """Extract keywords for routing to each skill"""
        routing = {}

        for config in self.configs:
            name = config['name']
            keywords = []

            # Extract from categories
            if 'categories' in config:
                keywords.extend(config['categories'].keys())

            # Extract from name (part after dash)
            if '-' in name:
                skill_topic = name.split('-', 1)[1]
                keywords.append(skill_topic)

            routing[name] = keywords

        return routing

    def generate_skill_md(self) -> str:
        """Generate router SKILL.md content"""
        routing_keywords = self.extract_routing_keywords()

        skill_md = f"""# {self.router_name.replace('-', ' ').title()} Documentation (Router)

## When to Use This Skill

{self.base_config.get('description', f'Use for {self.router_name} development and programming.')}

This is a router skill that directs your questions to specialized sub-skills for efficient, focused assistance.

## How It Works

This skill analyzes your question and activates the appropriate specialized skill(s):

"""

        # List sub-skills
        for config in self.configs:
            name = config['name']
            desc = config.get('description', '')
            # Remove router name prefix from description if present
            if desc.startswith(f"{self.router_name.title()} -"):
                desc = desc.split(' - ', 1)[1]

            skill_md += f"### {name}\n{desc}\n\n"

        # Routing logic
        skill_md += """## Routing Logic

The router analyzes your question for topic keywords and activates relevant skills:

**Keywords → Skills:**
"""

        for skill_name, keywords in routing_keywords.items():
            keyword_str = ", ".join(keywords)
            skill_md += f"- {keyword_str} → **{skill_name}**\n"

        # Quick reference
        skill_md += f"""

## Quick Reference

For quick answers, this router provides basic overview information. For detailed documentation, the specialized skills contain comprehensive references.

### Getting Started

1. Ask your question naturally - mention the topic area
2. The router will activate the appropriate skill(s)
3. You'll receive focused, detailed answers from specialized documentation

### Examples

**Question:** "How do I create a 2D sprite?"
**Activates:** {self.router_name}-2d skill

**Question:** "GDScript function syntax"
**Activates:** {self.router_name}-scripting skill

**Question:** "Physics collision handling in 3D"
**Activates:** {self.router_name}-3d + {self.router_name}-physics skills

### All Available Skills

"""

        # List all skills
        for config in self.configs:
            skill_md += f"- **{config['name']}**\n"

        skill_md += f"""

## Need Help?

Simply ask your question and mention the topic. The router will find the right specialized skill for you!

---

*This is a router skill. For complete documentation, see the specialized skills listed above.*
"""

        return skill_md

    def create_router_config(self) -> Dict[str, Any]:
        """Create router configuration"""
        routing_keywords = self.extract_routing_keywords()

        router_config = {
            "name": self.router_name,
            "description": self.base_config.get('description', f'{self.router_name.title()} documentation router'),
            "base_url": self.base_config['base_url'],
            "selectors": self.base_config.get('selectors', {}),
            "url_patterns": self.base_config.get('url_patterns', {}),
            "rate_limit": self.base_config.get('rate_limit', 0.5),
            "max_pages": 500,  # Router only scrapes overview pages
            "_router": True,
            "_sub_skills": [cfg['name'] for cfg in self.configs],
            "_routing_keywords": routing_keywords
        }

        return router_config

    def generate(self, output_dir: Path = None) -> Tuple[Path, Path]:
        """Generate router skill and config"""
        if output_dir is None:
            output_dir = self.config_paths[0].parent

        output_dir = Path(output_dir)

        # Generate SKILL.md
        skill_md = self.generate_skill_md()
        skill_path = output_dir.parent / f"output/{self.router_name}/SKILL.md"
        skill_path.parent.mkdir(parents=True, exist_ok=True)

        with open(skill_path, 'w') as f:
            f.write(skill_md)

        # Generate config
        router_config = self.create_router_config()
        config_path = output_dir / f"{self.router_name}.json"

        with open(config_path, 'w') as f:
            json.dump(router_config, f, indent=2)

        return config_path, skill_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate router/hub skill for split documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate router from multiple configs
  python3 generate_router.py configs/godot-2d.json configs/godot-3d.json configs/godot-scripting.json

  # Use glob pattern
  python3 generate_router.py configs/godot-*.json

  # Custom router name
  python3 generate_router.py configs/godot-*.json --name godot-hub

  # Custom output directory
  python3 generate_router.py configs/godot-*.json --output-dir configs/routers/
        """
    )

    parser.add_argument(
        'configs',
        nargs='+',
        help='Sub-skill config files'
    )

    parser.add_argument(
        '--name',
        help='Router skill name (default: inferred from sub-skills)'
    )

    parser.add_argument(
        '--output-dir',
        help='Output directory (default: same as input configs)'
    )

    args = parser.parse_args()

    # Filter out router configs (avoid recursion)
    config_files = []
    for path_str in args.configs:
        path = Path(path_str)
        if path.exists() and not path.stem.endswith('-router'):
            config_files.append(path_str)

    if not config_files:
        print("❌ Error: No valid config files provided")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("ROUTER SKILL GENERATOR")
    print(f"{'='*60}")
    print(f"Sub-skills: {len(config_files)}")
    for cfg in config_files:
        print(f"  - {Path(cfg).stem}")
    print("")

    # Generate router
    generator = RouterGenerator(config_files, args.name)
    config_path, skill_path = generator.generate(args.output_dir)

    print(f"✅ Router config created: {config_path}")
    print(f"✅ Router SKILL.md created: {skill_path}")
    print("")
    print(f"{'='*60}")
    print("NEXT STEPS")
    print(f"{'='*60}")
    print(f"1. Review router SKILL.md: {skill_path}")
    print(f"2. Optionally scrape router (for overview pages):")
    print(f"     skill-seekers scrape --config {config_path}")
    print("3. Package router skill:")
    print(f"     skill-seekers package output/{generator.router_name}/")
    print("4. Upload router + all sub-skills to Claude")
    print("")


if __name__ == "__main__":
    main()
