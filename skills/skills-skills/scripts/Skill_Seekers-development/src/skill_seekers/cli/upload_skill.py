#!/usr/bin/env python3
"""
Automatic Skill Uploader
Uploads a skill .zip file to Claude using the Anthropic API

Usage:
    # Set API key (one-time)
    export ANTHROPIC_API_KEY=sk-ant-...

    # Upload skill
    python3 upload_skill.py output/react.zip
    python3 upload_skill.py output/godot.zip
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Import utilities
try:
    from utils import (
        get_api_key,
        get_upload_url,
        print_upload_instructions,
        validate_zip_file
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from utils import (
        get_api_key,
        get_upload_url,
        print_upload_instructions,
        validate_zip_file
    )


def upload_skill_api(zip_path):
    """
    Upload skill to Claude via Anthropic API

    Args:
        zip_path: Path to skill .zip file

    Returns:
        tuple: (success, message)
    """
    # Check for requests library
    try:
        import requests
    except ImportError:
        return False, "requests library not installed. Run: pip install requests"

    # Validate zip file
    is_valid, error_msg = validate_zip_file(zip_path)
    if not is_valid:
        return False, error_msg

    # Get API key
    api_key = get_api_key()
    if not api_key:
        return False, "ANTHROPIC_API_KEY not set. Run: export ANTHROPIC_API_KEY=sk-ant-..."

    zip_path = Path(zip_path)
    skill_name = zip_path.stem

    print(f"📤 Uploading skill: {skill_name}")
    print(f"   Source: {zip_path}")
    print(f"   Size: {zip_path.stat().st_size:,} bytes")
    print()

    # Prepare API request
    api_url = "https://api.anthropic.com/v1/skills"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "skills-2025-10-02"
    }

    try:
        # Read zip file
        with open(zip_path, 'rb') as f:
            zip_data = f.read()

        # Upload skill
        print("⏳ Uploading to Anthropic API...")

        files = {
            'files[]': (zip_path.name, zip_data, 'application/zip')
        }

        response = requests.post(
            api_url,
            headers=headers,
            files=files,
            timeout=60
        )

        # Check response
        if response.status_code == 200:
            print()
            print("✅ Skill uploaded successfully!")
            print()
            print("Your skill is now available in Claude at:")
            print(f"   {get_upload_url()}")
            print()
            return True, "Upload successful"

        elif response.status_code == 401:
            return False, "Authentication failed. Check your ANTHROPIC_API_KEY"

        elif response.status_code == 400:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            return False, f"Invalid skill format: {error_msg}"

        else:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            return False, f"Upload failed ({response.status_code}): {error_msg}"

    except requests.exceptions.Timeout:
        return False, "Upload timed out. Try again or use manual upload"

    except requests.exceptions.ConnectionError:
        return False, "Connection error. Check your internet connection"

    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def main():
    parser = argparse.ArgumentParser(
        description="Upload a skill .zip file to Claude via Anthropic API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Setup:
  1. Get your Anthropic API key from https://console.anthropic.com/
  2. Set the API key:
     export ANTHROPIC_API_KEY=sk-ant-...

Examples:
  # Upload skill
  python3 upload_skill.py output/react.zip

  # Upload with explicit path
  python3 upload_skill.py /path/to/skill.zip

Requirements:
  - ANTHROPIC_API_KEY environment variable must be set
  - requests library (pip install requests)
        """
    )

    parser.add_argument(
        'zip_file',
        help='Path to skill .zip file (e.g., output/react.zip)'
    )

    args = parser.parse_args()

    # Upload skill
    success, message = upload_skill_api(args.zip_file)

    if success:
        sys.exit(0)
    else:
        print(f"\n❌ Upload failed: {message}")
        print()
        print("📝 Manual upload instructions:")
        print_upload_instructions(args.zip_file)
        sys.exit(1)


if __name__ == "__main__":
    main()
