#!/usr/bin/env python3
"""
Version Bump Quality Gate
Ensures that template changes are accompanied by version bumps.
This script is for the template repository only (not for projects using the template).
"""

import pathlib
import subprocess
import sys
from typing import List, Set

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)

VERSION_FILE = pathlib.Path("0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml")
TEMPLATE_DIRS = [
    "0_phase0_bootstrap/",
    "1_global_standards/",
    "2_framework_templates/",
    "3_bootstrap_scripts/",
    "5_reference_architectures/",
    "7_schemas/",
    "8_ci/",
    ".github/",
    ".pre-commit-config.yaml",
    "requirements.txt",
]


def get_staged_files() -> Set[str]:
    """Get list of staged files."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True,
        )
        return set(result.stdout.strip().splitlines())
    except Exception:
        return set()


def is_template_file(file_path: str) -> bool:
    """Check if file is part of the template (not project-specific)."""
    # Ignore project-specific directories
    if any(file_path.startswith(d) for d in ["frontend/", "backend/", "shared/", "apps/", "packages/"]):
        return False
    # Ignore project-specific files
    if file_path.startswith("4_docs_index/") or file_path.startswith("6_ai_runtime_context/"):
        return False
    # Check if it's a template directory
    return any(file_path.startswith(d) for d in TEMPLATE_DIRS) or file_path in TEMPLATE_DIRS


def get_current_version() -> str:
    """Get current version from version manifest."""
    if not VERSION_FILE.exists():
        return "0.0.0"
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
            return manifest.get("template_version", "0.0.0")
    except Exception:
        return "0.0.0"


def get_previous_version() -> str:
    """Get previous version from git (HEAD version)."""
    try:
        result = subprocess.run(
            ["git", "show", "HEAD:0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml"],
            capture_output=True,
            text=True,
            check=True,
        )
        manifest = yaml.safe_load(result.stdout)
        return manifest.get("template_version", "0.0.0")
    except Exception:
        # File doesn't exist in HEAD (new file)
        return "0.0.0"


def parse_version(version: str) -> tuple[int, int, int]:
    """Parse semantic version string."""
    parts = version.split("-")[0].split(".")
    major = int(parts[0]) if len(parts) > 0 else 0
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2]) if len(parts) > 2 else 0
    return (major, minor, patch)


def version_bumped(current: str, previous: str) -> bool:
    """Check if version was bumped."""
    if current == previous:
        return False
    curr_v = parse_version(current)
    prev_v = parse_version(previous)
    # Version must increase
    return curr_v > prev_v


def check_version_bump() -> tuple[bool, str]:
    """Check if version was bumped when template files changed."""
    staged_files = get_staged_files()
    
    # Check if any template files are staged
    template_files_changed = [f for f in staged_files if is_template_file(f)]
    
    if not template_files_changed:
        # No template files changed, version bump not required
        return True, ""

    # Template files changed, check if version was bumped
    version_file_changed = str(VERSION_FILE) in staged_files
    
    if not version_file_changed:
        return False, (
            f"ERROR: Template files changed but version not bumped!\n"
            f"  Changed template files: {len(template_files_changed)}\n"
            f"  Example: {template_files_changed[0] if template_files_changed else 'N/A'}\n"
            f"  Please update {VERSION_FILE} with a new version number.\n"
            f"  Current version: {get_current_version()}\n"
            f"  Suggested: Bump minor version (e.g., 1.0.0 -> 1.1.0) for new features"
        )

    # Version file changed, check if version actually increased
    current_version = get_current_version()
    previous_version = get_previous_version()
    
    if not version_bumped(current_version, previous_version):
        return False, (
            f"ERROR: Version file changed but version did not increase!\n"
            f"  Previous version: {previous_version}\n"
            f"  Current version: {current_version}\n"
            f"  Version must increase when template files change.\n"
            f"  Suggested: Bump minor version (e.g., {previous_version} -> {increment_minor(previous_version)})"
        )

    return True, f"OK: Version bumped from {previous_version} to {current_version}"


def increment_minor(version: str) -> str:
    """Increment minor version."""
    major, minor, patch = parse_version(version)
    return f"{major}.{minor + 1}.0"


def main() -> int:
    """Main version bump check."""
    # Check if we're in the template repository (not a project using the template)
    # This is a heuristic: if .git exists and we have META_FRAMEWORK_VERSION.yaml, we're likely the template
    if not pathlib.Path(".git").exists():
        # Not a git repo, skip check
        return 0

    if not VERSION_FILE.exists():
        # Version file doesn't exist, might be a project (not template)
        # Skip check for projects
        return 0

    success, message = check_version_bump()
    
    if not success:
        print(message)
        print("\nTo bypass this check (not recommended):")
        print("  git commit --no-verify")
        return 1

    if message:
        print(message)
        # Remind about creating git tag
        if version_bumped(get_current_version(), get_previous_version()):
            current = get_current_version()
            print(f"\nNOTE: After committing, create a git tag for this version:")
            print(f"  python3 scripts/create_version_tag.py")
            print(f"  Or manually: git tag -a v{current} -m 'Template version {current}' && git push origin v{current}")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

