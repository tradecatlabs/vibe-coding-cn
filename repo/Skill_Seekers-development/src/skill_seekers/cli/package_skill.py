#!/usr/bin/env python3
"""
Simple Skill Packager
Packages a skill directory into a .zip file for Claude.

Usage:
    skill-seekers package output/steam-inventory/
    skill-seekers package output/react/
    skill-seekers package output/react/ --no-open  # Don't open folder
"""

import os
import sys
import zipfile
import argparse
from pathlib import Path

# Import utilities
try:
    from utils import (
        open_folder,
        print_upload_instructions,
        format_file_size,
        validate_skill_directory
    )
    from quality_checker import SkillQualityChecker, print_report
except ImportError:
    # If running from different directory, add cli to path
    sys.path.insert(0, str(Path(__file__).parent))
    from utils import (
        open_folder,
        print_upload_instructions,
        format_file_size,
        validate_skill_directory
    )
    from quality_checker import SkillQualityChecker, print_report


def package_skill(skill_dir, open_folder_after=True, skip_quality_check=False):
    """
    Package a skill directory into a .zip file

    Args:
        skill_dir: Path to skill directory
        open_folder_after: Whether to open the output folder after packaging
        skip_quality_check: Skip quality checks before packaging

    Returns:
        tuple: (success, zip_path) where success is bool and zip_path is Path or None
    """
    skill_path = Path(skill_dir)

    # Validate skill directory
    is_valid, error_msg = validate_skill_directory(skill_path)
    if not is_valid:
        print(f"❌ Error: {error_msg}")
        return False, None

    # Run quality checks (unless skipped)
    if not skip_quality_check:
        print("\n" + "=" * 60)
        print("QUALITY CHECK")
        print("=" * 60)

        checker = SkillQualityChecker(skill_path)
        report = checker.check_all()

        # Print report
        print_report(report, verbose=False)

        # If there are errors or warnings, ask user to confirm
        if report.has_errors or report.has_warnings:
            print("=" * 60)
            response = input("\nContinue with packaging? (y/n): ").strip().lower()
            if response != 'y':
                print("\n❌ Packaging cancelled by user")
                return False, None
            print()
        else:
            print("=" * 60)
            print()

    # Create zip filename
    skill_name = skill_path.name
    zip_path = skill_path.parent / f"{skill_name}.zip"

    print(f"📦 Packaging skill: {skill_name}")
    print(f"   Source: {skill_path}")
    print(f"   Output: {zip_path}")

    # Create zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_path):
            # Skip backup files
            files = [f for f in files if not f.endswith('.backup')]

            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_path)
                zf.write(file_path, arcname)
                print(f"   + {arcname}")

    # Get zip size
    zip_size = zip_path.stat().st_size
    print(f"\n✅ Package created: {zip_path}")
    print(f"   Size: {zip_size:,} bytes ({format_file_size(zip_size)})")

    # Open folder in file browser
    if open_folder_after:
        print(f"\n📂 Opening folder: {zip_path.parent}")
        open_folder(zip_path.parent)

    # Print upload instructions
    print_upload_instructions(zip_path)

    return True, zip_path


def main():
    parser = argparse.ArgumentParser(
        description="Package a skill directory into a .zip file for Claude",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Package skill with quality checks (recommended)
  skill-seekers package output/react/

  # Package skill without opening folder
  skill-seekers package output/react/ --no-open

  # Skip quality checks (faster, but not recommended)
  skill-seekers package output/react/ --skip-quality-check

  # Package and auto-upload to Claude
  skill-seekers package output/react/ --upload

  # Get help
  skill-seekers package --help
        """
    )

    parser.add_argument(
        'skill_dir',
        help='Path to skill directory (e.g., output/react/)'
    )

    parser.add_argument(
        '--no-open',
        action='store_true',
        help='Do not open the output folder after packaging'
    )

    parser.add_argument(
        '--skip-quality-check',
        action='store_true',
        help='Skip quality checks before packaging'
    )

    parser.add_argument(
        '--upload',
        action='store_true',
        help='Automatically upload to Claude after packaging (requires ANTHROPIC_API_KEY)'
    )

    args = parser.parse_args()

    success, zip_path = package_skill(
        args.skill_dir,
        open_folder_after=not args.no_open,
        skip_quality_check=args.skip_quality_check
    )

    if not success:
        sys.exit(1)

    # Auto-upload if requested
    if args.upload:
        # Check if API key is set BEFORE attempting upload
        api_key = os.environ.get('ANTHROPIC_API_KEY', '').strip()

        if not api_key:
            # No API key - show helpful message but DON'T fail
            print("\n" + "="*60)
            print("💡 Automatic Upload")
            print("="*60)
            print()
            print("To enable automatic upload:")
            print("  1. Get API key from https://console.anthropic.com/")
            print("  2. Set: export ANTHROPIC_API_KEY=sk-ant-...")
            print("  3. Run package_skill.py with --upload flag")
            print()
            print("For now, use manual upload (instructions above) ☝️")
            print("="*60)
            # Exit successfully - packaging worked!
            sys.exit(0)

        # API key exists - try upload
        try:
            from upload_skill import upload_skill_api
            print("\n" + "="*60)
            upload_success, message = upload_skill_api(zip_path)
            if not upload_success:
                print(f"❌ Upload failed: {message}")
                print()
                print("💡 Try manual upload instead (instructions above) ☝️")
                print("="*60)
                # Exit successfully - packaging worked even if upload failed
                sys.exit(0)
            else:
                print("="*60)
                sys.exit(0)
        except ImportError:
            print("\n❌ Error: upload_skill.py not found")
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
