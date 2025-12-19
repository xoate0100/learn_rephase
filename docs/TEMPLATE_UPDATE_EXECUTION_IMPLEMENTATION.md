# Template Update Execution Rules - Implementation Summary

## Overview

Implemented automatic template update checking on every commit, ensuring projects stay current with template improvements through idempotent, non-breaking, stateful updates.

## Components Implemented

### 1. Update Check Script (`check_template_updates.py`)

**Purpose**: Checks for template updates on every commit

**Features**:
- Fetches latest version from template repository
- Compares with current project version
- Categorizes update type (MAJOR/MINOR/PATCH)
- Integrates with feature flags
- Warns but doesn't block (configurable)

**Integration**: Pre-commit hook runs on every commit

### 2. Feature Flags Configuration

Added to `feature_flags.yml`:

```yaml
template_updates:
  check_on_commit: true      # Check on every commit
  auto_update: false          # Auto-apply updates (default: false)
  check_frequency: "on_commit"  # When to check
  warn_only: true             # Warn but don't block
```

### 3. Pre-Commit Hook

Added to `.pre-commit-config.yaml`:

```yaml
- id: check-template-updates
  name: Check Template Updates (Projects Only)
  entry: python3 3_bootstrap_scripts/check_template_updates.py --warn-only
  language: system
  pass_filenames: false
  always_run: true
```

### 4. Idempotency Enhancements

Enhanced `template_update.py` to be fully idempotent:
- Version check prevents duplicate updates
- File comparison only updates changed files
- Update history prevents reprocessing
- Protected files never overwritten

## How It Works

### On Every Commit

1. **Pre-commit hook triggers**: `check-template-updates`
2. **Reads version manifest**: Gets current version from `META_FRAMEWORK_VERSION.yaml`
3. **Fetches latest version**: Queries template repository (GitHub API or git tags)
4. **Compares versions**: Determines if update available
5. **Warns if available**: Displays update message (doesn't block by default)
6. **Commit proceeds**: Update check is non-blocking

### Update Detection

The check uses multiple methods:
1. **GitHub API**: Fetches `META_FRAMEWORK_VERSION.yaml` from template repo
2. **Git Tags**: Falls back to git tag parsing
3. **Version Comparison**: Semantic version comparison

### Update Types

Updates are categorized:
- **MAJOR** (X.0.0): Breaking changes, migrations required
- **MINOR** (0.X.0): New features, backward compatible  
- **PATCH** (0.0.X): Bug fixes, backward compatible

## Idempotency Guarantees

### 1. Version Check

```python
if target_version == current_version:
    return 0  # Already up-to-date, no changes
```

### 2. File Comparison

Only updates files that differ:
- Compares file contents before overwriting
- Skips identical files
- Preserves file timestamps when unchanged

### 3. Update History

Tracks updates to prevent duplicates:
- Records each update in `update_history`
- Prevents reprocessing same version
- Maintains complete audit trail

### 4. Protected Files

Never overwritten:
- `MVP_SPECIFICATION.yaml`
- `feature_flags.yml`
- All project directories

## Stateful Updates

### Version Tracking

- Current version: `template_version` in manifest
- Last updated: `last_updated_at` timestamp
- Update history: Complete list of all updates

### Update History

Each update recorded:

```yaml
update_history:
  - from_version: "1.0.0"
    to_version: "1.1.0"
    updated_at: "2024-01-15T00:00:00Z"
    migration_applied: false
    notes: "Added feedback collection system"
```

### Migration Tracking

- Migrations tracked per version
- Prevents duplicate execution
- Records success/failure

## Non-Breaking Updates

### Protected Files

These files are **never overwritten**:
- `0_phase0_bootstrap/MVP_SPECIFICATION.yaml`
- `0_phase0_bootstrap/feature_flags.yml`

### Protected Directories

These directories are **never updated**:
- `frontend/`, `backend/`, `shared/`
- `4_docs_index/`, `6_ai_runtime_context/`
- `apps/`, `packages/`

### Safe Updates

Only template directories updated:
- `0_phase0_bootstrap/` (except protected)
- `1_global_standards/`
- `2_framework_templates/`
- `3_bootstrap_scripts/`
- `5_reference_architectures/`
- `7_schemas/`
- `8_ci/`

## Configuration Options

### Conservative (Default)

```yaml
template_updates:
  check_on_commit: true
  auto_update: false
  warn_only: true
```

**Behavior**: Check and warn, manual update required.

### Aggressive

```yaml
template_updates:
  check_on_commit: true
  auto_update: true
  warn_only: false
```

**Behavior**: Auto-update and block if update fails.

### Manual Only

```yaml
template_updates:
  check_on_commit: false
  auto_update: false
```

**Behavior**: Only check when manually running update command.

## Usage

### Automatic (On Commit)

Updates are checked automatically on every commit. If update available:

```
WARN: Template update available: 1.0.0 → 1.1.0 (MINOR (new features))

To update your project to the latest template version:
  python3 3_bootstrap_scripts/cli.py update-template
```

### Manual Update

```bash
# Check for updates
python3 3_bootstrap_scripts/cli.py update-template --dry-run

# Apply updates
python3 3_bootstrap_scripts/cli.py update-template
```

### Auto-Update (If Enabled)

If `auto_update: true`, updates are applied automatically during pre-commit.

## Benefits

1. **Automatic**: Updates checked on every commit
2. **Idempotent**: Safe to run multiple times
3. **Non-Breaking**: Protected files never overwritten
4. **Stateful**: Complete update history maintained
5. **Configurable**: Behavior controlled via feature flags
6. **Safe Defaults**: Warns but doesn't block

## Files Created/Modified

### New Files
- `3_bootstrap_scripts/check_template_updates.py` - Update check script
- `docs/TEMPLATE_UPDATE_EXECUTION_RULES.md` - User guide
- `docs/TEMPLATE_UPDATE_EXECUTION_IMPLEMENTATION.md` - This document

### Modified Files
- `.pre-commit-config.yaml` - Added check-template-updates hook
- `0_phase0_bootstrap/feature_flags.yml` - Added template_updates config
- `3_bootstrap_scripts/template_update.py` - Enhanced idempotency messages

## Summary

The template update execution rules ensure:

- ✅ **Automatic checking**: On every commit
- ✅ **Idempotent**: Safe to run multiple times
- ✅ **Non-breaking**: Protected files preserved
- ✅ **Stateful**: Complete history maintained
- ✅ **Configurable**: Via feature flags
- ✅ **Safe**: Warns but doesn't block by default

Projects now automatically stay current with template improvements while maintaining safety and project customizations.

