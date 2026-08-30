# Legacy Workflow Removal Receipt

**Sweep:** legacy-workflow-sweep (NA-16)  
**Repo:** xoate0100/learn_rephase  
**Date:** 2026-08-29

## Removed workflows

- `process_feedback.yml` — process_feedback.yml autonomously creates improvement/fix PRs (feeds legacy auto-fixer); invokes `.github/scripts/create_improvement_prs.py` (autonomous fix/PR generation); invokes `create_improvement_prs.py` (autonomous fix/PR generation)

## Reason

These workflows matched the **legacy ungoverned auto-remediation** profile defined in the hub's
`docs/factory/LEGACY_WORKFLOW_PROFILE.md`: autonomous fix generation and/or PR creation without
two-key gate, conformance gate, or agent-reviewer routing.

## Governed remediation path

Remediation is **propose-only** via the capability platform behavioral daemon (two-key gated).
Wave E feedback pipes (`workspace_feedback_emit.yml`, `ingest_workspace_feedback.yml`) and
`capability-drift.yml` were **not** modified.

## Orphaned scripts (follow-up — not deleted this pass)

- `.github/scripts/create_improvement_prs.py`

