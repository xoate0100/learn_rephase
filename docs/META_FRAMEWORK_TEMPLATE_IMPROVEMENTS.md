# Meta-Framework Template Improvements (Preventing Known AI Failure Modes)

This document captures **template-level** improvements that prevent recurring AI/guardrail issues observed in `ai_feedback_log*.json`.

## High-leverage template fixes (ranked)

### 1) Single source of truth for “allowed write paths”

**Observed failure mode**: guardrails block legitimate changes because `AI_SANDBOX_RULES.md` and `feature_flags.yml` disagree about writable paths.

**Template fix**:
- Make `0_phase0_bootstrap/feature_flags.yml` `permissions.write_to` the **canonical** list.
- Generate or validate `AI_SANDBOX_RULES.md` from that canonical list (or add a drift check).

**Template validation**:
- Run `scripts/meta_framework_drift_check.py` in pre-commit/CI.

### 1.1) Guided layout selection (answers-file mode)

**Observed failure mode**: derived repos frequently use layouts that don’t match `frontend/ backend/ shared/` roots (Next.js root, apps/packages, src-only), leading to scanners/guardrails missing real code or blocking legitimate writes.

**Template fix**:
- Run `python3 3_bootstrap_scripts/cli.py init --guided`
- For fully deterministic bootstraps across varied architectures, use:
  - `6_ai_runtime_context/INIT_WIZARD_ANSWERS.yaml`
  - `python3 3_bootstrap_scripts/cli.py init --guided --answers 6_ai_runtime_context/INIT_WIZARD_ANSWERS.yaml`

**State outputs**:
- `6_ai_runtime_context/INIT_WIZARD_RESULT.yaml`
- `6_ai_runtime_context/LAYOUT_REARRANGEMENT_PLAN.yaml` (proposal; apply only when explicitly enabled via MVP spec)

### 2) Drift detector for automation vs sandbox constraints

**Observed failure mode**: an automation script writes to a directory that sandbox rules forbid (example: `3_bootstrap_scripts/docs_sync.py` writes to `4_docs_index/`).

**Template fix**:
- Either (a) adjust sandbox rules to permit the automation’s outputs, or (b) relocate outputs to an allowed directory, or (c) change the automation to be read-only.

**Template validation**:
- Encode “known writers” and compare with forbidden directories (implemented in `scripts/meta_framework_drift_check.py`).

### 3) Static analysis checkers must ship with regression tests

**Observed failure mode**: SRP/ISP false positives from brittle regex parsing (arrow functions vs assignments, indexing bugs, brace tracking).

**Template fix**:
- Treat checkers as production code: add a small corpus of fixtures and tests.
- Add “golden” cases for:
  - arrow functions vs call results
  - nested helper functions
  - multiline declarations
  - brace-level boundary detection
  - 1-index vs 0-index line mapping

### 4) Guardrail failures must be actionable (diagnostics first)

**Observed failure mode**: timeouts or guardrail transaction failures that don’t include command, exit code, or captured output.

**Template fix**:
- Standardize failure output to include:
  - command executed
  - exit code
  - captured stderr/stdout (truncated)
  - step name / gate name
  - duration + timeout threshold

### 5) Documentation lifecycle rules as automation, not policy-only

**Observed failure mode**: documentation redundancy, broken cross-references, multiple “final” status docs.

**Template fix**:
- Provide:
  - a single “start here” index
  - an archive/historical convention
  - a link checker and/or doc index generator

## Recommended “template contract” (what every repo should enforce)

- **No policy drift**: sandbox rules, flags, and guardrails remain consistent.
- **No silent bypass**: hooks cannot be bypassed in normal workflows; bypass attempts must be visible.
- **Checkers are tested**: architecture/SOLID checkers ship with tests and fixtures.
- **Diagnostics are rich**: failures explain how to fix them, not just that they happened.
