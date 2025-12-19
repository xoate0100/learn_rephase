#!/usr/bin/env python3
"""
Meta-framework drift checker (template-level).

Goal: detect mismatches between declared sandbox rules and enforcement config,
before they cause guardrail failures or confusing AI behavior.

This script is intentionally read-only and safe to run in CI/pre-commit.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Set, Tuple


def _read_text(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return None


def _extract_backticked_paths(md_text: str, heading: str) -> List[str]:
    """
    Extract backticked paths from a section headed by '## <heading>'.
    This is intentionally simple and resilient to minor formatting changes.
    """
    # Find the section body from its heading to the next '## ' heading (or EOF).
    pattern = rf"^##\s+{re.escape(heading)}\s*$"
    lines = md_text.splitlines()
    start_idx = None
    for i, line in enumerate(lines):
        if re.match(pattern, line.strip()):
            start_idx = i + 1
            break
    if start_idx is None:
        return []

    body: List[str] = []
    for j in range(start_idx, len(lines)):
        if lines[j].startswith("## "):
            break
        body.append(lines[j])

    body_text = "\n".join(body)
    # Extract `path/` style tokens.
    return re.findall(r"`([^`]+)`", body_text)


def _normalize_dir_prefix(p: str) -> str:
    p = p.strip().replace("\\", "/")
    if not p:
        return p
    # Ensure directory-like prefixes end with /
    if not p.endswith("/"):
        # allow root files (README.md) to remain as-is
        if "/" not in p and "." in p:
            return p
        return p + "/"
    return p


def _load_yaml_write_to(flags_path: Path) -> Set[str]:
    try:
        import yaml  # type: ignore
    except Exception:
        return set()

    data = yaml.safe_load(flags_path.read_text(encoding="utf-8", errors="replace")) or {}
    write_to = data.get("permissions", {}).get("write_to", []) or []
    return {_normalize_dir_prefix(str(x)) for x in write_to if str(x).strip()}


def _load_yaml(path: Path) -> Optional[dict]:
    try:
        import yaml  # type: ignore
    except Exception:
        return None
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8", errors="replace")) or {}
    except Exception:
        return None


def _load_drift_config(flags_path: Path) -> dict:
    """
    Optional config lives in feature_flags.yml to keep templates self-contained.

    Schema (all optional):
      meta_framework_validations:
        drift_check:
          enabled: true
          sandbox_rules_file: "0_phase0_bootstrap/AI_SANDBOX_RULES.md"
          feature_flags_file: "0_phase0_bootstrap/feature_flags.yml"
          compare_write_paths: true
          automation_writers:
            - script: "3_bootstrap_scripts/docs_sync.py"
              writes_to: "4_docs_index/"
    """
    flags = _load_yaml(flags_path) if flags_path.exists() else None
    cfg = (((flags or {}).get("meta_framework_validations") or {}).get("drift_check") or {}) if isinstance(flags, dict) else {}
    if not isinstance(cfg, dict):
        return {}
    return cfg


@dataclass(frozen=True)
class DriftFinding:
    code: str
    message: str
    severity: str  # "ERROR" | "WARN"


def _compare_allowed_writes(sandbox_allowed: Set[str], flags_allowed: Set[str]) -> List[DriftFinding]:
    findings: List[DriftFinding] = []
    only_in_sandbox = sorted(sandbox_allowed - flags_allowed)
    only_in_flags = sorted(flags_allowed - sandbox_allowed)

    if only_in_sandbox:
        findings.append(
            DriftFinding(
                code="WRITE_PATH_DRIFT_SANDBOX_GT_FLAGS",
                severity="ERROR",
                message=(
                    "AI_SANDBOX_RULES allows writes to paths not allowed by feature_flags.yml permissions.write_to: "
                    + ", ".join(only_in_sandbox)
                ),
            )
        )
    if only_in_flags:
        findings.append(
            DriftFinding(
                code="WRITE_PATH_DRIFT_FLAGS_GT_SANDBOX",
                severity="WARN",
                message=(
                    "feature_flags.yml permissions.write_to includes paths not listed as writable in AI_SANDBOX_RULES: "
                    + ", ".join(only_in_flags)
                ),
            )
        )
    return findings


def _detect_rule_violating_automation(
    sandbox_forbidden: Set[str], known_writers: Sequence[Tuple[str, str]]
) -> List[DriftFinding]:
    """
    Detect template scripts that target forbidden directories.
    known_writers: list of (script_path, target_dir_prefix)
    """
    forbidden_prefixes = {_normalize_dir_prefix(x) for x in sandbox_forbidden if x.endswith("/")}
    findings: List[DriftFinding] = []
    for script_path, target in known_writers:
        tnorm = _normalize_dir_prefix(target)
        if any(tnorm.startswith(fp) for fp in forbidden_prefixes):
            findings.append(
                DriftFinding(
                    code="AUTOMATION_WRITES_FORBIDDEN_DIR",
                    severity="ERROR",
                    message=f"Automation '{script_path}' writes to forbidden dir '{tnorm}' per AI_SANDBOX_RULES.",
                )
            )
    return findings


def main(argv: Sequence[str]) -> int:
    root = Path(".")
    default_flags_path = root / "0_phase0_bootstrap" / "feature_flags.yml"
    cfg = _load_drift_config(default_flags_path)

    if cfg.get("enabled") is False:
        print("[drift] SKIP: disabled by feature_flags.yml meta_framework_validations.drift_check.enabled=false")
        return 0

    sandbox_path = (root / str(cfg.get("sandbox_rules_file") or "0_phase0_bootstrap/AI_SANDBOX_RULES.md")).resolve()
    flags_path = (root / str(cfg.get("feature_flags_file") or "0_phase0_bootstrap/feature_flags.yml")).resolve()

    sandbox_text = _read_text(sandbox_path)
    if sandbox_text is None:
        print(f"[drift] WARN: Missing sandbox rules file '{sandbox_path.as_posix()}'; skipping.")
        return 0

    flags_allowed = _load_yaml_write_to(flags_path) if flags_path.exists() else set()

    allowed_tokens = _extract_backticked_paths(sandbox_text, "Allowed")
    forbidden_tokens = _extract_backticked_paths(sandbox_text, "Forbidden")

    # Allowed section includes both directories and occasional file references; for drift checks
    # we only consider directory-ish entries (ending in /).
    sandbox_allowed = {
        _normalize_dir_prefix(t.strip().strip(","))
        for t in allowed_tokens
        if t.strip().strip(",").replace("\\", "/").endswith("/")
    }

    sandbox_forbidden = {_normalize_dir_prefix(t.strip().strip(",")) for t in forbidden_tokens if "/" in t}

    findings: List[DriftFinding] = []
    if cfg.get("compare_write_paths", True) and flags_allowed:
        findings.extend(_compare_allowed_writes(sandbox_allowed, flags_allowed))
    elif cfg.get("compare_write_paths", True):
        findings.append(
            DriftFinding(
                code="FEATURE_FLAGS_MISSING_OR_UNREADABLE",
                severity="WARN",
                message="feature_flags.yml missing or unreadable (PyYAML not installed?) — skipping flags drift checks.",
            )
        )

    # Optional: validate known automation outputs (template remains generic by making this opt-in config).
    automation_writers_cfg = cfg.get("automation_writers") or []
    known_writers: List[Tuple[str, str]] = []
    if isinstance(automation_writers_cfg, list):
        for item in automation_writers_cfg:
            if not isinstance(item, dict):
                continue
            script = str(item.get("script") or "").strip()
            writes_to = str(item.get("writes_to") or "").strip()
            if script and writes_to:
                known_writers.append((script, writes_to))

    findings.extend(_detect_rule_violating_automation(sandbox_forbidden, known_writers))

    errors = [f for f in findings if f.severity == "ERROR"]
    warns = [f for f in findings if f.severity == "WARN"]

    for f in errors + warns:
        print(f"[drift] {f.severity} {f.code}: {f.message}")

    if errors:
        print("[drift] FAIL: meta-framework drift detected (errors).")
        return 2

    print("[drift] OK: no blocking drift detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
