#!/usr/bin/env python3
"""
Create Version Tag
Automatically creates and pushes a git tag when the version is updated.
This script should be run after updating META_FRAMEWORK_VERSION.yaml.
"""

import pathlib
import subprocess
import sys
from typing import Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)

VERSION_FILE = pathlib.Path("0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml")


def get_current_version() -> Optional[str]:
    """Get current version from version manifest."""
    if not VERSION_FILE.exists():
        print(f"ERROR: {VERSION_FILE} not found")
        return None
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
            return manifest.get("template_version")
    except Exception as e:
        print(f"ERROR: Could not read version from {VERSION_FILE}: {e}")
        return None


def tag_exists(tag: str) -> bool:
    """Check if git tag already exists."""
    try:
        result = subprocess.run(
            ["git", "tag", "-l", tag],
            capture_output=True,
            text=True,
            check=True,
        )
        return bool(result.stdout.strip())
    except Exception:
        return False


def create_tag(version: str, push: bool = True) -> bool:
    """Create and optionally push a git tag for the version."""
    # Format tag as v1.2.3
    tag = f"v{version}"
    
    if tag_exists(tag):
        print(f"Tag {tag} already exists. Skipping tag creation.")
        return True
    
    try:
        # Create annotated tag
        subprocess.run(
            ["git", "tag", "-a", tag, "-m", f"Template version {version}"],
            check=True,
        )
        print(f"Created tag: {tag}")
        
        if push:
            # Push tag to remote
            subprocess.run(
                ["git", "push", "origin", tag],
                check=True,
            )
            print(f"Pushed tag: {tag} to origin")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to create/push tag: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return False


def main() -> int:
    """Main tag creation."""
    # Check if we're in a git repository
    if not pathlib.Path(".git").exists():
        print("WARN: Not in a git repository. Skipping tag creation.")
        return 0
    
    # Check if version file exists
    if not VERSION_FILE.exists():
        print(f"WARN: {VERSION_FILE} not found. Skipping tag creation.")
        return 0
    
    # Get version
    version = get_current_version()
    if not version:
        return 1
    
    # Check if we should push (default: yes, unless --no-push)
    push = "--no-push" not in sys.argv
    
    # Create and push tag
    if create_tag(version, push=push):
        return 0
    else:
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

