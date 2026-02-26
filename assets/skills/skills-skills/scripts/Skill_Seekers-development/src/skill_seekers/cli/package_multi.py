#!/usr/bin/env python3
"""
Multi-Skill Packager

Package multiple skills at once. Useful for packaging router + sub-skills together.
"""

import sys
import argparse
from pathlib import Path
import subprocess


def package_skill(skill_dir: Path) -> bool:
    """Package a single skill"""
    try:
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "package_skill.py"), str(skill_dir)],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error packaging {skill_dir}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Package multiple skills at once",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Package all godot skills
  python3 package_multi.py output/godot*/

  # Package specific skills
  python3 package_multi.py output/godot-2d/ output/godot-3d/ output/godot-scripting/
        """
    )

    parser.add_argument(
        'skill_dirs',
        nargs='+',
        help='Skill directories to package'
    )

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"MULTI-SKILL PACKAGER")
    print(f"{'='*60}\n")

    skill_dirs = [Path(d) for d in args.skill_dirs]
    success_count = 0
    total_count = len(skill_dirs)

    for skill_dir in skill_dirs:
        if not skill_dir.exists():
            print(f"⚠️  Skipping (not found): {skill_dir}")
            continue

        if not (skill_dir / "SKILL.md").exists():
            print(f"⚠️  Skipping (no SKILL.md): {skill_dir}")
            continue

        print(f"📦 Packaging: {skill_dir.name}")
        if package_skill(skill_dir):
            success_count += 1
            print(f"   ✅ Success")
        else:
            print(f"   ❌ Failed")
        print("")

    print(f"{'='*60}")
    print(f"SUMMARY: {success_count}/{total_count} skills packaged")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
