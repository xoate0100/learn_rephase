#!/usr/bin/env python3
"""Format only passed/staged files; propagate formatter failures."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

from pre_commit_utils import (  # noqa: E402
    FORMAT_TIMEOUT,
    PIP_TIMEOUT,
    files_from_argv_or_staged,
    norm_path,
    run_subprocess,
)


def _formatters_ready() -> bool:
    """True when pinned black/isort are importable (no static import names)."""
    import importlib.util

    return (
        importlib.util.find_spec("black") is not None
        and importlib.util.find_spec("isort") is not None
    )


def _ensure_formatters() -> bool:
    """Install black/isort with retry (GHA py3.14 pip can race on pathspec)."""
    if _formatters_ready():
        return True
    for attempt in range(1, 3):
        pip = run_subprocess(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--quiet",
                "--upgrade",
                "black",
                "isort",
            ],
            timeout=PIP_TIMEOUT,
        )
        if _formatters_ready():
            return True
        print(
            f"[enforce-format] WARN: formatter install attempt {attempt} "
            f"rc={pip.returncode}; retrying"
        )
    return _formatters_ready()


def run_python_formatters(py_files: list[str]) -> int:
    if not py_files:
        return 0
    if not _ensure_formatters():
        print("[enforce-format] FAILED: black/isort unavailable after install retry")
        return 1

    # isort first, black last: black must be the final writer so the
    # style hook is idempotent (isort-after-black left imports that
    # black would rewrite again on the next CI pass). Match editorconfig
    # line-length 100 used by flake8 spokes.
    isort = run_subprocess(
        [
            sys.executable,
            "-m",
            "isort",
            "--profile",
            "black",
            "--line-length",
            "100",
            *py_files,
        ],
        timeout=FORMAT_TIMEOUT,
    )
    if isort.returncode != 0:
        return isort.returncode

    black = run_subprocess(
        [sys.executable, "-m", "black", "--line-length", "100", *py_files],
        timeout=FORMAT_TIMEOUT,
    )
    return black.returncode


def run_prettier(files: list[str]) -> int:
    if not files:
        return 0
    cmd = ["npx", "--yes", "prettier", "-w", *files]
    result = run_subprocess(cmd, timeout=FORMAT_TIMEOUT)
    return result.returncode


def main() -> int:
    files = files_from_argv_or_staged(sys.argv)
    py_files = [f for f in files if norm_path(f).endswith(".py")]
    js_files = [f for f in files if norm_path(f).endswith((".ts", ".tsx", ".js", ".jsx"))]

    status = 0
    if py_files:
        status = run_python_formatters(py_files) or status
    if js_files:
        status = run_prettier(js_files) or status

    if status != 0:
        print("[enforce-format] FAILED: formatter returned non-zero exit code")
        return 1

    print("[enforce-format] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
