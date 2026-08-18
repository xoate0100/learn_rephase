# Command Interface Spec

**Status:** protocol (language-neutral)  
**Version:** 1.0.0  
**Schema companions:** `7_schemas/stack_adapter.schema.json`, `7_schemas/feedback_event.schema.json`

This document defines the **abstract lifecycle verbs** every stack adapter must implement.
No verb may require a specific language runtime. Adapters declare native commands that
satisfy each verb in a stack adapter manifest.

---

## 1. Design rules

1. Inputs/outputs are files, env vars, stdout/stderr, and exit codes — never language APIs.
2. Exit codes are part of the contract (see §3).
3. Verb names are stable; CLI aliases (e.g. Python `update-template` → `apply-updates`) live in adapters.
4. A child with `adapter: node` MUST complete every required verb with **no Python on PATH**.
5. A child with `adapter: python` MUST preserve today’s behavior (backward compatibility).

---

## 2. Required lifecycle verbs

| Verb | Purpose | Required |
|------|---------|----------|
| `init` | Initialize project structure from MVP / intent specs | yes |
| `generate-context` | Produce AI execution context from state + flags | yes |
| `validate` | Run the full quality/governance gate set | yes |
| `check-updates` | Compare local template version to hub; report only | yes |
| `apply-updates` | Pull and apply allowed template updates for this adapter | yes |
| `submit-feedback` | Emit conforming feedback event(s) to the hub channel | yes |
| `health` | Diagnose adapter + protocol installation | yes |

### Optional verbs (adapters MAY implement)

| Verb | Purpose |
|------|---------|
| `verify-integrity` | Checksum / integrity of synced template files |
| `template-status` | Human-readable version + drift summary |
| `upgrade-legacy` | Migrate pre-initializer projects |
| `hook-install` | Install the selected hook runner configuration |

---

## 3. Exit codes (all verbs)

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Validation / policy failure (expected business failure) |
| `2` | Usage error (bad args / missing required inputs) |
| `3` | Missing toolchain (adapter command not found) |
| `4` | Network / remote hub unreachable |
| `5` | Partial apply / needs human intervention |
| `10+` | Adapter-specific (document in manifest `notes`) |

Stdout SHOULD be human-readable. Structured machine output, when emitted, MUST be JSON on
stdout when env `META_FRAMEWORK_JSON=1` is set (or adapter-equivalent flag).

---

## 4. Verb contracts

### 4.1 `init`

**Inputs**
- `0_phase0_bootstrap/MVP_SPECIFICATION.yaml` (required unless guided mode provides equivalent)
- `0_phase0_bootstrap/feature_flags.yml` (created/updated)
- Optional: interactive prompts (adapter-defined)

**Outputs**
- Layout directories per write permissions
- Updated `feature_flags.yml` component languages from `TECH_STACK` when present
- Non-zero exit if MVP missing / invalid

**Must NOT**
- Require a foreign-stack runtime
- Overwrite protected files without explicit flag

---

### 4.2 `generate-context`

**Inputs**
- Active plan / task pointer under `6_ai_runtime_context/`
- `feature_flags.yml`, sandbox rules, registries as available

**Outputs**
- `6_ai_runtime_context/AI_CONTEXT.md` (or path declared in manifest)
- Exit `0` on write success

---

### 4.3 `validate`

**Inputs**
- Working tree (staged and/or all files — adapter flag)
- Hook contract checks (see `HOOK_CONTRACT.md`)

**Outputs**
- Aggregated pass/fail of required checks
- Exit `0` iff all required checks pass

**Must NOT**
- Hard-require Python `pre-commit`; any runner satisfying the hook contract is valid

---

### 4.4 `check-updates`

**Inputs**
- Local `META_FRAMEWORK_VERSION.yaml`
- Hub remote URL (from version manifest or env `TEMPLATE_REPO`)

**Outputs**
- Report: current version, remote version, update available (yes/no)
- Exit `0` always when check succeeds (warn-only by default)
- Exit `4` if hub unreachable (unless `--offline`)

---

### 4.5 `apply-updates`

**Inputs**
- Same as check-updates
- Active stack adapter id
- Template-update contract (what may sync)

**Outputs**
- Synced neutral protocol artifacts + **selected adapter only**
- Updated `update_history` in version manifest
- Exit `0` on success; `5` if migration needs human review

**Must NOT**
- Copy `adapters/python/**` into a non-Python child
- Overwrite protected files

---

### 4.6 `submit-feedback`

**Inputs**
- Feedback payload conforming to `7_schemas/feedback_event.schema.json`
- Auth via env (`GITHUB_TOKEN` or adapter-documented equivalent) — never inline secrets

**Outputs**
- Append to local feedback log (default `6_ai_runtime_context/ai_feedback_log.json`) when offline/local
- Optional remote issue creation when configured
- Exit `0` on accept; `2` on schema violation

---

### 4.7 `health`

**Inputs**
- Active adapter manifest
- Local toolchain

**Outputs**
- Pass/fail per declared toolchain check
- Exit `0` if adapter can run all required verbs’ toolchains
- Exit `3` if a required tool is missing

---

## 5. Invocation (neutral)

Children invoke verbs through the **neutral dispatcher** (Phase 2):

```text
meta <verb> [args...]
# or platform-native wrappers:
./meta.ps1 <verb> ...
./meta.sh <verb> ...
```

The dispatcher reads the active stack adapter manifest and executes the declared command for
that verb. No Python required unless the active adapter is `python`.

---

## 6. Mapping from legacy Python CLI

| Legacy `cli.py` command | Neutral verb |
|-------------------------|--------------|
| `init` | `init` |
| `generate-context` | `generate-context` |
| `validate` | `validate` |
| `template-status` / check path | `check-updates` / `template-status` |
| `update-template` | `apply-updates` |
| `verify-template` | `verify-integrity` |
| `submit-feedback` | `submit-feedback` |
| `health` | `health` |

Python adapter MUST keep legacy subcommand names as aliases.
