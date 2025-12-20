#!/usr/bin/env python3
"""
SKILL.md Enhancement Script
Uses Claude API to improve SKILL.md by analyzing reference documentation.

Usage:
    skill-seekers enhance output/steam-inventory/
    skill-seekers enhance output/react/
    skill-seekers enhance output/godot/ --api-key YOUR_API_KEY
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add parent directory to path for imports when run as script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill_seekers.cli.constants import API_CONTENT_LIMIT, API_PREVIEW_LIMIT
from skill_seekers.cli.utils import read_reference_files

try:
    import anthropic
except ImportError:
    print("❌ Error: anthropic package not installed")
    print("Install with: pip3 install anthropic")
    sys.exit(1)


class SkillEnhancer:
    def __init__(self, skill_dir, api_key=None):
        self.skill_dir = Path(skill_dir)
        self.references_dir = self.skill_dir / "references"
        self.skill_md_path = self.skill_dir / "SKILL.md"

        # Get API key
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError(
                "No API key provided. Set ANTHROPIC_API_KEY environment variable "
                "or use --api-key argument"
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def read_current_skill_md(self):
        """Read existing SKILL.md"""
        if not self.skill_md_path.exists():
            return None
        return self.skill_md_path.read_text(encoding='utf-8')

    def enhance_skill_md(self, references, current_skill_md):
        """Use Claude to enhance SKILL.md"""

        # Build prompt
        prompt = self._build_enhancement_prompt(references, current_skill_md)

        print("\n🤖 Asking Claude to enhance SKILL.md...")
        print(f"   Input: {len(prompt):,} characters")

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            enhanced_content = message.content[0].text
            return enhanced_content

        except Exception as e:
            print(f"❌ Error calling Claude API: {e}")
            return None

    def _build_enhancement_prompt(self, references, current_skill_md):
        """Build the prompt for Claude"""

        # Extract skill name and description
        skill_name = self.skill_dir.name

        prompt = f"""You are enhancing a Claude skill's SKILL.md file. This skill is about: {skill_name}

I've scraped documentation and organized it into reference files. Your job is to create an EXCELLENT SKILL.md that will help Claude use this documentation effectively.

CURRENT SKILL.MD:
{'```markdown' if current_skill_md else '(none - create from scratch)'}
{current_skill_md or 'No existing SKILL.md'}
{'```' if current_skill_md else ''}

REFERENCE DOCUMENTATION:
"""

        for filename, content in references.items():
            prompt += f"\n\n## {filename}\n```markdown\n{content[:30000]}\n```\n"

        prompt += """

YOUR TASK:
Create an enhanced SKILL.md that includes:

1. **Clear "When to Use This Skill" section** - Be specific about trigger conditions
2. **Excellent Quick Reference section** - Extract 5-10 of the BEST, most practical code examples from the reference docs
   - Choose SHORT, clear examples that demonstrate common tasks
   - Include both simple and intermediate examples
   - Annotate examples with clear descriptions
   - Use proper language tags (cpp, python, javascript, json, etc.)
3. **Detailed Reference Files description** - Explain what's in each reference file
4. **Practical "Working with This Skill" section** - Give users clear guidance on how to navigate the skill
5. **Key Concepts section** (if applicable) - Explain core concepts
6. **Keep the frontmatter** (---\nname: ...\n---) intact

IMPORTANT:
- Extract REAL examples from the reference docs, don't make them up
- Prioritize SHORT, clear examples (5-20 lines max)
- Make it actionable and practical
- Don't be too verbose - be concise but useful
- Maintain the markdown structure for Claude skills
- Keep code examples properly formatted with language tags

OUTPUT:
Return ONLY the complete SKILL.md content, starting with the frontmatter (---).
"""

        return prompt

    def save_enhanced_skill_md(self, content):
        """Save the enhanced SKILL.md"""
        # Backup original
        if self.skill_md_path.exists():
            backup_path = self.skill_md_path.with_suffix('.md.backup')
            self.skill_md_path.rename(backup_path)
            print(f"  💾 Backed up original to: {backup_path.name}")

        # Save enhanced version
        self.skill_md_path.write_text(content, encoding='utf-8')
        print(f"  ✅ Saved enhanced SKILL.md")

    def run(self):
        """Main enhancement workflow"""
        print(f"\n{'='*60}")
        print(f"ENHANCING SKILL: {self.skill_dir.name}")
        print(f"{'='*60}\n")

        # Read reference files
        print("📖 Reading reference documentation...")
        references = read_reference_files(
            self.skill_dir,
            max_chars=API_CONTENT_LIMIT,
            preview_limit=API_PREVIEW_LIMIT
        )

        if not references:
            print("❌ No reference files found to analyze")
            return False

        print(f"  ✓ Read {len(references)} reference files")
        total_size = sum(len(c) for c in references.values())
        print(f"  ✓ Total size: {total_size:,} characters\n")

        # Read current SKILL.md
        current_skill_md = self.read_current_skill_md()
        if current_skill_md:
            print(f"  ℹ Found existing SKILL.md ({len(current_skill_md)} chars)")
        else:
            print(f"  ℹ No existing SKILL.md, will create new one")

        # Enhance with Claude
        enhanced = self.enhance_skill_md(references, current_skill_md)

        if not enhanced:
            print("❌ Enhancement failed")
            return False

        print(f"  ✓ Generated enhanced SKILL.md ({len(enhanced)} chars)\n")

        # Save
        print("💾 Saving enhanced SKILL.md...")
        self.save_enhanced_skill_md(enhanced)

        print(f"\n✅ Enhancement complete!")
        print(f"\nNext steps:")
        print(f"  1. Review: {self.skill_md_path}")
        print(f"  2. If you don't like it, restore backup: {self.skill_md_path.with_suffix('.md.backup')}")
        print(f"  3. Package your skill:")
        print(f"     skill-seekers package {self.skill_dir}/")

        return True


def main():
    parser = argparse.ArgumentParser(
        description='Enhance SKILL.md using Claude API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using ANTHROPIC_API_KEY environment variable
  export ANTHROPIC_API_KEY=sk-ant-...
  skill-seekers enhance output/steam-inventory/

  # Providing API key directly
  skill-seekers enhance output/react/ --api-key sk-ant-...

  # Show what would be done (dry run)
  skill-seekers enhance output/godot/ --dry-run
"""
    )

    parser.add_argument('skill_dir', type=str,
                       help='Path to skill directory (e.g., output/steam-inventory/)')
    parser.add_argument('--api-key', type=str,
                       help='Anthropic API key (or set ANTHROPIC_API_KEY env var)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without calling API')

    args = parser.parse_args()

    # Validate skill directory
    skill_dir = Path(args.skill_dir)
    if not skill_dir.exists():
        print(f"❌ Error: Directory not found: {skill_dir}")
        sys.exit(1)

    if not skill_dir.is_dir():
        print(f"❌ Error: Not a directory: {skill_dir}")
        sys.exit(1)

    # Dry run mode
    if args.dry_run:
        print(f"🔍 DRY RUN MODE")
        print(f"   Would enhance: {skill_dir}")
        print(f"   References: {skill_dir / 'references'}")
        print(f"   SKILL.md: {skill_dir / 'SKILL.md'}")

        refs_dir = skill_dir / "references"
        if refs_dir.exists():
            ref_files = list(refs_dir.glob("*.md"))
            print(f"   Found {len(ref_files)} reference files:")
            for rf in ref_files:
                size = rf.stat().st_size
                print(f"     - {rf.name} ({size:,} bytes)")

        print("\nTo actually run enhancement:")
        print(f"  skill-seekers enhance {skill_dir}")
        return

    # Create enhancer and run
    try:
        enhancer = SkillEnhancer(skill_dir, api_key=args.api_key)
        success = enhancer.run()
        sys.exit(0 if success else 1)

    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nSet your API key:")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        print("Or provide it directly:")
        print(f"  skill-seekers enhance {skill_dir} --api-key sk-ant-...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
