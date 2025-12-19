# Bootstrap Layout Guidance (Generated)

This file helps AI agents understand the **actual repo layout** and what (if anything) must be rearranged.

## What this is
- A **bootstrap-time output** intended to prevent “structure drift” (e.g., Next.js repos not matching `frontend/` / `backend/` defaults).
- It should be regenerated when `0_phase0_bootstrap/MVP_SPECIFICATION.yaml` or `0_phase0_bootstrap/feature_flags.yml` changes.

## Current contract for agents
- **Authoritative component roots** live in `0_phase0_bootstrap/feature_flags.yml` under `components.*.directories`.
- **Allowed write paths** live in `0_phase0_bootstrap/feature_flags.yml` under `permissions.write_to`.
- Architecture/SOLID checks and guardrails must use those values (no hardcoded `frontend/ backend/ shared/` assumptions).
- **Layout adaptation plan** (if present) lives at `6_ai_runtime_context/LAYOUT_REARRANGEMENT_PLAN.yaml`.
- **Wizard result** (if guided init used) lives at `6_ai_runtime_context/INIT_WIZARD_RESULT.yaml`.

## Rearrangement policy
- Do **not** move folders automatically unless the current plan explicitly authorizes it.
- If a mismatch is detected:
  - Prefer updating `PROJECT_LAYOUT` in `MVP_SPECIFICATION.yaml` to reflect reality.
  - Then re-run initialization to regenerate derived config.
