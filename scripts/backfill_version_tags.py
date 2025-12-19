#!/usr/bin/env python3
"""
Backfill Version Tags
Creates git tags for all versions listed in the update history.
Useful for retroactively tagging versions that were released before tagging was implemented.
"""

import pathlib
import subprocess
import sys
from typing import List, Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)

VERSION_FILE = pathlib.Path("0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml")


def get_all_versions() -> List[str]:
    """Get all versions from update history."""
    if not VERSION_FILE.exists():
        print(f"ERROR: {VERSION_FILE} not found")
        return []
    
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
            
            versions = []
            # Add current version
            current = manifest.get("template_version")
            if current:
                versions.append(current)
            
            # Add all versions from update history
            update_history = manifest.get("update_history", [])
            for entry in update_history:
                from_v = entry.get("from_version")
                to_v = entry.get("to_version")
                if from_v and from_v not in versions:
                    versions.append(from_v)
                if to_v and to_v not in versions:
                    versions.append(to_v)
            
            # Sort versions (simple semver sort)
            def version_key(v: str) -> tuple:
                parts = v.split(".")
                return (int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0)
            
            return sorted(set(versions), key=version_key)
    except Exception as e:
        print(f"ERROR: Could not read versions: {e}")
        return []


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


def create_tag(version: str, push: bool = False) -> bool:
    """Create a git tag for the version."""
    tag = f"v{version}"
    
    if tag_exists(tag):
        print(f"  Tag {tag} already exists, skipping")
        return True
    
    try:
        # Find the commit where this version was set
        # Try to find commit that modified the version file to this version
        result = subprocess.run(
            ["git", "log", "--all", "--oneline", "--grep", version, "--", str(VERSION_FILE)],
            capture_output=True,
            text=True,
        )
        
        # If we can't find a specific commit, use HEAD
        commit = "HEAD"
        if result.stdout.strip():
            # Use the first matching commit
            commit = result.stdout.splitlines()[0].split()[0]
        
        # Create annotated tag
        subprocess.run(
            ["git", "tag", "-a", tag, commit, "-m", f"Template version {version}"],
            check=True,
        )
        print(f"  Created tag: {tag} at {commit}")
        
        if push:
            subprocess.run(
                ["git", "push", "origin", tag],
                check=True,
            )
            print(f"  Pushed tag: {tag}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ERROR: Failed to create tag {tag}: {e}")
        return False
    except Exception as e:
        print(f"  ERROR: Unexpected error: {e}")
        return False


def main() -> int:
    """Main backfill process."""
    if not pathlib.Path(".git").exists():
        print("ERROR: Not in a git repository")
        return 1
    
    if not VERSION_FILE.exists():
        print(f"ERROR: {VERSION_FILE} not found")
        return 1
    
    versions = get_all_versions()
    if not versions:
        print("No versions found")
        return 1
    
    print(f"Found {len(versions)} versions to tag:")
    for v in versions:
        print(f"  - {v}")
    
    push = "--push" in sys.argv
    
    print(f"\nCreating tags (push={'yes' if push else 'no'})...")
    success_count = 0
    for version in versions:
        if create_tag(version, push=push):
            success_count += 1
    
    print(f"\nCreated {success_count}/{len(versions)} tags")
    
    if not push:
        print("\nTo push all tags, run:")
        print("  git push origin --tags")
        print("Or run this script with --push flag")
    
    return 0 if success_count == len(versions) else 1


if __name__ == "__main__":
    raise SystemExit(main())

