#!/usr/bin/env python3
"""
Template Update System
Pulls updates from the template repository and merges them safely into existing projects.
Supports AI-assisted migration for pre-versioned projects.
"""

import argparse
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import yaml


VERSION_FILE = pathlib.Path("0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml")
VERSION_SCHEMA = pathlib.Path("7_schemas/meta_framework_version.schema.json")


def load_version_manifest() -> Optional[Dict[str, Any]]:
    """Load the version manifest if it exists."""
    if not VERSION_FILE.exists():
        return None
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR: Failed to load version manifest: {e}")
        return None


def save_version_manifest(manifest: Dict[str, Any]) -> bool:
    """Save the version manifest."""
    try:
        VERSION_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(VERSION_FILE, "w", encoding="utf-8") as f:
            yaml.dump(manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return True
    except Exception as e:
        print(f"ERROR: Failed to save version manifest: {e}")
        return False


def detect_pre_versioned_project() -> bool:
    """Detect if this is a pre-versioned project (no META_FRAMEWORK_VERSION.yaml)."""
    return not VERSION_FILE.exists()


def initialize_version_manifest(template_repo: str, version: str = "1.0.0") -> Dict[str, Any]:
    """Create initial version manifest for pre-versioned projects."""
    return {
        "template_version": version,
        "template_repo": template_repo,
        "installed_at": datetime.utcnow().isoformat() + "Z",
        "last_updated_at": None,
        "update_history": [],
        "features": {
            "dynamic_layout_adaptation": pathlib.Path("3_bootstrap_scripts/layout_adaptor.py").exists(),
            "guided_initialization": pathlib.Path("3_bootstrap_scripts/init_wizard.py").exists(),
            "dynamic_ai_context": pathlib.Path("3_bootstrap_scripts/generate_ai_context.py").exists(),
            "template_versioning": False,  # Being added now
            "drift_detection": pathlib.Path("scripts/meta_framework_drift_check.py").exists(),
        },
        "template_directories": [
            "0_phase0_bootstrap/",
            "1_global_standards/",
            "2_framework_templates/",
            "3_bootstrap_scripts/",
            "5_reference_architectures/",
            "7_schemas/",
            "8_ci/",
        ],
        "protected_files": [
            "0_phase0_bootstrap/MVP_SPECIFICATION.yaml",
            "0_phase0_bootstrap/feature_flags.yml",
        ],
        "project_directories": [
            "4_docs_index/",
            "6_ai_runtime_context/",
            "frontend/",
            "backend/",
            "shared/",
            "apps/",
            "packages/",
            "docs/",
        ],
    }


def get_latest_template_version(template_repo: str) -> Optional[str]:
    """Get the latest version from the template repository.
    
    Tries multiple methods:
    1. GitHub API (read from META_FRAMEWORK_VERSION.yaml) - PRIMARY
    2. Git tags - FALLBACK
    """
    # Method 1: Try GitHub API (read from version manifest file)
    try:
        import requests
        import re
        import base64
        
        # Extract owner/repo from URL
        match = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", template_repo)
        if match:
            owner, repo = match.groups()
            api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml"
            
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                content = base64.b64decode(response.json()["content"]).decode("utf-8")
                import yaml
                manifest = yaml.safe_load(content)
                version = manifest.get("template_version")
                if version:
                    return version
    except ImportError:
        # requests not available, skip API method
        pass
    except Exception:
        # API failed, continue to fallback
        pass
    
    # Method 2: Fallback to git tags
    try:
        result = subprocess.run(
            ["git", "ls-remote", "--tags", template_repo],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return None

        # Parse tags to find latest version
        tags = []
        for line in result.stdout.splitlines():
            if "refs/tags/" in line:
                tag = line.split("refs/tags/")[-1].split()[0]
                # Remove 'v' prefix if present for comparison
                clean_tag = tag[1:] if tag.startswith("v") else tag
                if any(c.isdigit() for c in clean_tag):
                    tags.append(clean_tag)

        if tags:
            # Sort versions properly (semver)
            try:
                sorted_tags = sorted(tags, key=lambda v: tuple(map(int, v.split("."))))
                return sorted_tags[-1]
            except (ValueError, AttributeError):
                # Fallback: return last tag
                return tags[-1]

        return None
    except Exception as e:
        print(f"WARN: Could not fetch latest version from template repo: {e}")
        return None


def clone_template_to_temp(template_repo: str, version: Optional[str] = None) -> Optional[pathlib.Path]:
    """Clone template repository to a temporary directory."""
    temp_dir = tempfile.mkdtemp(prefix="template_update_")
    try:
        cmd = ["git", "clone", "--depth", "1", template_repo, temp_dir]
        if version:
            cmd.extend(["--branch", version])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"ERROR: Failed to clone template: {result.stderr}")
            return None
        return pathlib.Path(temp_dir)
    except Exception as e:
        print(f"ERROR: Failed to clone template: {e}")
        return None


def get_template_directories(manifest: Dict[str, Any]) -> List[str]:
    """Get list of template directories from manifest."""
    return manifest.get("template_directories", [])


def get_protected_files(manifest: Dict[str, Any]) -> List[str]:
    """Get list of protected files that should not be overwritten."""
    return manifest.get("protected_files", [])


def should_update_file(file_path: str, protected_files: List[str]) -> bool:
    """Check if a file should be updated (not protected)."""
    for protected in protected_files:
        if file_path == protected or file_path.startswith(protected):
            return False
    return True


def copy_template_files(
    template_dir: pathlib.Path,
    target_dir: pathlib.Path,
    template_dirs: List[str],
    protected_files: List[str],
    dry_run: bool = False,
) -> Tuple[List[str], List[str]]:
    """Copy template files to target, respecting protected files."""
    updated_files = []
    skipped_files = []

    for template_dir_name in template_dirs:
        src_dir = template_dir / template_dir_name.rstrip("/")
        if not src_dir.exists():
            continue

        target_base = target_dir / template_dir_name.rstrip("/")
        target_base.parent.mkdir(parents=True, exist_ok=True)

        # Walk through template directory
        for src_file in src_dir.rglob("*"):
            if src_file.is_dir():
                continue

            # Get relative path from template root
            rel_path = src_file.relative_to(template_dir)
            rel_str = str(rel_path).replace("\\", "/")

            # Check if protected
            if not should_update_file(rel_str, protected_files):
                skipped_files.append(rel_str)
                continue

            target_file = target_dir / rel_path
            target_file.parent.mkdir(parents=True, exist_ok=True)

            if not dry_run:
                shutil.copy2(src_file, target_file)
            updated_files.append(rel_str)

    return updated_files, skipped_files


def update_version_manifest(
    manifest: Dict[str, Any],
    new_version: str,
    migration_applied: bool = False,
    notes: str = "",
) -> Dict[str, Any]:
    """Update version manifest with new version and history."""
    old_version = manifest.get("template_version", "unknown")

    manifest["template_version"] = new_version
    manifest["last_updated_at"] = datetime.utcnow().isoformat() + "Z"

    # Add to update history
    update_entry = {
        "from_version": old_version,
        "to_version": new_version,
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "migration_applied": migration_applied,
        "notes": notes,
    }
    manifest.setdefault("update_history", []).append(update_entry)

    return manifest


def apply_migrations(from_version: str, to_version: str, project_root: pathlib.Path = None) -> Tuple[bool, str]:
    """Apply migrations between versions. Returns (success, notes)."""
    if project_root is None:
        project_root = pathlib.Path(".")

    # Handle "latest" version - skip migrations if version is "latest"
    if to_version == "latest" or from_version == "latest":
        return False, "Skipped (latest version - migrations not applicable)"

    # Version comparison (simple semver-like)
    def version_tuple(v: str) -> Tuple[int, int, int]:
        # Skip if "latest" (shouldn't happen here, but defensive)
        if v == "latest":
            return (999, 999, 999)  # High version number
        parts = v.split("-")[0].split(".")
        return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0, int(parts[2]) if len(parts) > 2 else 0)

    from_v = version_tuple(from_version)
    to_v = version_tuple(to_version)

    notes = []
    migration_needed = False

    # Try to load migration modules
    try:
        import sys
        migrations_path = pathlib.Path(__file__).parent / "migrations"
        if migrations_path.exists():
            sys.path.insert(0, str(pathlib.Path(__file__).parent))
            from migrations.migration_1_0_0 import get_migration, list_available_migrations

            # Apply migrations in order
            available = list_available_migrations()
            for target_version in available:
                target_v = version_tuple(target_version)
                if from_v < target_v <= to_v:
                    migration_func = get_migration(target_version)
                    if migration_func:
                        success, migration_notes = migration_func(project_root)
                        if success:
                            notes.append(f"{target_version}: {migration_notes}")
                            migration_needed = True
                        else:
                            notes.append(f"{target_version}: Migration failed")
    except ImportError:
        # Fallback to simple migrations if module system not available
        if from_v < (1, 0, 0) and to_v >= (1, 0, 0):
            notes.append("Initialized template versioning system")
            migration_needed = True

    return migration_needed, "; ".join(notes) if notes else "No migrations required"


def check_for_updates(template_repo: str, current_version: Optional[str] = None) -> Optional[str]:
    """Check if updates are available."""
    latest = get_latest_template_version(template_repo)
    if not latest:
        return None
    if current_version and latest == current_version:
        return None
    return latest


def check_cli_support() -> Tuple[bool, str]:
    """Check if cli.py has update-template command. Returns (has_command, error_message)."""
    cli_path = pathlib.Path("3_bootstrap_scripts/cli.py")
    if not cli_path.exists():
        return False, "cli.py not found"
    try:
        content = cli_path.read_text(encoding="utf-8")
        if "update-template" in content:
            return True, ""
        return False, "cli.py missing update-template command"
    except Exception as e:
        return False, f"Failed to read cli.py: {e}"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="template_update.py",
        description="Update template files from the template repository",
    )
    parser.add_argument(
        "--template-repo",
        default="",
        help="Template repository URL (default: from version manifest or detect)",
    )
    parser.add_argument(
        "--version",
        default="",
        help="Specific version to update to (default: latest)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be updated without making changes",
    )
    parser.add_argument(
        "--init-versioning",
        action="store_true",
        help="Initialize versioning for pre-versioned projects (AI-assisted)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force update even if versions match",
    )

    args = parser.parse_args(argv)

    # Load or initialize version manifest
    manifest = load_version_manifest()
    is_pre_versioned = detect_pre_versioned_project()

    if is_pre_versioned:
        if not args.init_versioning:
            print("WARN: This project does not have version tracking initialized.")
            print("Run with --init-versioning to initialize versioning (AI-assisted).")
            print("This will detect your template source and create a version manifest.")
            return 1

        # AI-assisted initialization for pre-versioned projects
        print("Initializing version tracking for pre-versioned project...")

        # Try to detect template repo from git remote
        template_repo = args.template_repo
        if not template_repo:
            try:
                result = subprocess.run(
                    ["git", "remote", "get-url", "origin"],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    # For now, assume origin is the template (or user can specify)
                    detected_repo = result.stdout.strip()
                    print(f"Detected git remote: {detected_repo}")
                    print("If this is not your template repo, specify --template-repo")
                    template_repo = detected_repo
            except Exception:
                pass

        if not template_repo:
            template_repo = input("Enter template repository URL: ").strip()
            if not template_repo:
                print("ERROR: Template repository URL required")
                return 1

        manifest = initialize_version_manifest(template_repo)
        if not save_version_manifest(manifest):
            return 1
        print("OK: Version tracking initialized")

        # Check if CLI has update-template command
        has_cli, cli_error = check_cli_support()
        if not has_cli:
            print("\nWARN: CLI may not have update-template command.")
            print(f"      Issue: {cli_error}")
            print("      You may need to update cli.py manually or use template_update.py directly.")
            print("      See docs/VERSIONING_MIGRATION_GUIDE.md for details.")

    # Get template repo from manifest if not provided
    template_repo = args.template_repo or manifest.get("template_repo", "")
    if not template_repo:
        print("ERROR: Template repository URL required (specify --template-repo or set in manifest)")
        return 1

    current_version = manifest.get("template_version", "unknown")
    target_version = args.version or check_for_updates(template_repo, current_version)

    if not target_version:
        if args.force:
            # Resolve "latest" to actual version before proceeding
            resolved_latest = get_latest_template_version(template_repo)
            if resolved_latest:
                target_version = resolved_latest
            else:
                target_version = "latest"
                print("WARN: Could not resolve 'latest' version, proceeding with 'latest'")
        else:
            print(f"INFO: Already at latest version ({current_version})")
            return 0

    # If target_version is still "latest", try to resolve it
    if target_version == "latest":
        resolved_latest = get_latest_template_version(template_repo)
        if resolved_latest:
            print(f"Resolved 'latest' to version {resolved_latest}")
            target_version = resolved_latest
        else:
            print("WARN: Could not resolve 'latest' version. Migrations will be skipped.")

    if not args.force and target_version == current_version:
        print(f"INFO: Already at version {current_version} (idempotent: no changes needed)")
        return 0

    print(f"Updating template from {current_version} to {target_version}...")

    # Clone template
    print("Cloning template repository...")
    template_dir = clone_template_to_temp(template_repo, target_version if target_version != "latest" else None)
    if not template_dir:
        return 1

    try:
        # Get template directories and protected files
        template_dirs = get_template_directories(manifest)
        protected_files = get_protected_files(manifest)

        # Copy files
        print("Updating template files...")
        updated, skipped = copy_template_files(
            template_dir,
            pathlib.Path("."),
            template_dirs,
            protected_files,
            dry_run=args.dry_run,
        )

        if args.dry_run:
            print(f"\nDRY RUN: Would update {len(updated)} files, skip {len(skipped)} protected files")
            if updated:
                print("\nFiles to be updated:")
                for f in updated[:20]:  # Show first 20
                    print(f"  - {f}")
                if len(updated) > 20:
                    print(f"  ... and {len(updated) - 20} more")
            if skipped:
                print("\nProtected files (not updated):")
                for f in skipped[:10]:
                    print(f"  - {f}")
                if len(skipped) > 10:
                    print(f"  ... and {len(skipped) - 10} more")
            return 0

        # Apply migrations (with error handling to ensure manifest is always updated)
        migration_applied = False
        migration_notes = "No migrations required"
        try:
            migration_applied, migration_notes = apply_migrations(current_version, target_version, pathlib.Path("."))
        except ValueError as e:
            # Handle case where version parsing fails (e.g., "latest" not resolved)
            if "latest" in str(e).lower() or "invalid literal" in str(e).lower():
                print(f"WARN: Skipping migrations due to version parsing issue: {e}")
                migration_notes = f"Skipped (version parsing issue: {e})"
            else:
                # Re-raise if it's a different error
                raise
        except Exception as e:
            print(f"WARN: Migration failed: {e}")
            migration_notes = f"Migration error: {e}"

        # Always update version manifest (even if migrations failed)
        manifest = update_version_manifest(manifest, target_version, migration_applied, migration_notes)
        if not save_version_manifest(manifest):
            return 1

        print(f"OK: Updated to version {target_version}")
        print(f"Updated {len(updated)} files, skipped {len(skipped)} protected files")
        if migration_notes:
            print(f"Migration notes: {migration_notes}")

        return 0

    finally:
        # Cleanup temp directory
        if template_dir.exists():
            shutil.rmtree(template_dir, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
