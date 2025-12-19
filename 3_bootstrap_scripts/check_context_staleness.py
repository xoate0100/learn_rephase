#!/usr/bin/env python3
"""
Pre-commit hook: Check if AI_CONTEXT.md is stale relative to source files.

Warns (non-blocking) if generated context is older than source files.
Auto-regenerates if stale.
"""

import sys
import pathlib
from datetime import datetime

try:
    import yaml
except ImportError:
    print("[context-staleness] WARN: PyYAML not available, skipping staleness check")
    sys.exit(0)


def get_file_mtime(path: pathlib.Path) -> float:
    """Get file modification time, or 0 if doesn't exist"""
    if path.exists():
        return path.stat().st_mtime
    return 0.0


def main() -> int:
    """Check if AI_CONTEXT.md is stale"""
    root = pathlib.Path(".").resolve()

    # Source files that affect context
    source_files = [
        root / "0_phase0_bootstrap" / "AI_SANDBOX_RULES.md",
        root / "0_phase0_bootstrap" / "feature_flags.yml",
        root / "6_ai_runtime_context" / "ACTIVE_PLAN.yaml",
        root / "6_ai_runtime_context" / "ACTIVE_TASK_POINTER.yaml",
        root / "5_reference_architectures" / "LAYER_RULES.yaml",
    ]

    # Generated file
    context_file = root / "6_ai_runtime_context" / "AI_CONTEXT.md"

    if not context_file.exists():
        print("[context-staleness] INFO: AI_CONTEXT.md not found, will be generated on next commit")
        return 0

    context_mtime = get_file_mtime(context_file)

    # Check if any source file is newer
    stale = False
    newest_source = ""
    newest_mtime = 0.0

    for source_file in source_files:
        if source_file.exists():
            mtime = get_file_mtime(source_file)
            if mtime > newest_mtime:
                newest_mtime = mtime
                newest_source = source_file.name
            if mtime > context_mtime:
                stale = True

    if stale:
        print(f"[context-staleness] WARN: AI_CONTEXT.md is stale (newer source: {newest_source})")
        print("[context-staleness] Regenerating...")

        # Auto-regenerate
        import subprocess
        result = subprocess.run(
            ["python3", "3_bootstrap_scripts/generate_ai_context.py"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("[context-staleness] OK: Regenerated AI_CONTEXT.md")
            # Stage the regenerated file
            subprocess.run(["git", "add", str(context_file)], capture_output=True)
        else:
            print(f"[context-staleness] ERROR: Failed to regenerate: {result.stderr}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
