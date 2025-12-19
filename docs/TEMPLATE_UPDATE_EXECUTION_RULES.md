# Template Update Execution Rules

## Overview

Projects initialized from this template automatically check for template updates on every commit. This ensures projects stay current with template improvements while maintaining safety through idempotent, non-breaking updates.

## Execution Rules

### Pre-Commit Hook

**Hook**: `check-template-updates`  
**Location**: `.pre-commit-config.yaml`  
**Runs**: On every commit  
**Behavior**: Checks for template updates and warns if available

### Configuration

Configure in `0_phase0_bootstrap/feature_flags.yml`:

```yaml
template_updates:
  check_on_commit: true      # Check for updates on every commit
  auto_update: false          # Automatically apply updates (default: false)
  check_frequency: "on_commit"  # on_commit, daily, weekly, manual
  warn_only: true             # Warn but don't block commits (default: true)
```

## Update Process

### 1. Check for Updates

On every commit, the pre-commit hook:
1. Reads `META_FRAMEWORK_VERSION.yaml` to get current version
2. Fetches latest version from template repository
3. Compares versions
4. Warns if update available (doesn't block commit by default)

### 2. Update Types

Updates are categorized:
- **MAJOR** (X.0.0): Breaking changes, migrations required
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes, backward compatible

### 3. Applying Updates

To apply updates:

```bash
# Manual update
python3 3_bootstrap_scripts/cli.py update-template

# Auto-update (if enabled)
python3 3_bootstrap_scripts/cli.py update-template --auto-update
```

## Idempotency

The update process is **idempotent**:

- **Safe to run multiple times**: Running update twice produces the same result
- **No duplicate changes**: Files are only updated if they differ
- **State tracking**: Update history prevents duplicate processing
- **Protected files**: Project customizations are never overwritten

### How Idempotency Works

1. **Version Check**: Compares current version with target version
2. **File Comparison**: Only updates files that differ
3. **History Tracking**: Records updates in `update_history`
4. **Protected Files**: Skips files in `protected_files` list

## Non-Breaking Updates

Updates are designed to be **non-breaking**:

### Protected Files

These files are **never overwritten**:
- `0_phase0_bootstrap/MVP_SPECIFICATION.yaml` - Project configuration
- `0_phase0_bootstrap/feature_flags.yml` - Project settings

### Protected Directories

These directories are **never updated**:
- `frontend/`, `backend/`, `shared/` - Project code
- `4_docs_index/`, `6_ai_runtime_context/` - Project state
- `apps/`, `packages/` - Project structure

### Safe Updates

Only template directories are updated:
- `0_phase0_bootstrap/` (except protected files)
- `1_global_standards/`
- `2_framework_templates/`
- `3_bootstrap_scripts/`
- `5_reference_architectures/`
- `7_schemas/`
- `8_ci/`

## Stateful Updates

Updates are **stateful**:

### Version Tracking

- Current version stored in `META_FRAMEWORK_VERSION.yaml`
- Update history maintained in `update_history`
- Last update timestamp tracked

### Update History

Each update is recorded:

```yaml
update_history:
  - from_version: "1.0.0"
    to_version: "1.1.0"
    updated_at: "2024-01-15T00:00:00Z"
    migration_applied: false
    notes: "Added feedback collection system"
```

### Migration Tracking

- Migrations are tracked per version
- Prevents duplicate migration execution
- Records migration success/failure

## Workflow

### Normal Workflow

1. **Developer commits code**
2. **Pre-commit hook runs**: Checks for template updates
3. **Warning displayed** (if update available): "Template update available: 1.0.0 → 1.1.0"
4. **Commit proceeds**: Update check doesn't block (warn_only: true)
5. **Developer updates later**: Runs `update-template` when convenient

### Auto-Update Workflow

If `auto_update: true`:

1. **Developer commits code**
2. **Pre-commit hook runs**: Checks for template updates
3. **Update detected**: Automatically applies update
4. **Commit proceeds**: With updated template files

### Manual Update Workflow

1. **Developer runs**: `python3 3_bootstrap_scripts/cli.py update-template`
2. **System checks**: Compares versions
3. **Update applied**: If newer version available
4. **History updated**: Records update in manifest

## Best Practices

### 1. Regular Updates

- **Check frequently**: Updates checked on every commit
- **Apply promptly**: Don't let versions drift too far
- **Review changes**: Check what changed before applying

### 2. Before Major Updates

- **Read release notes**: Check what changed in major versions
- **Test in branch**: Apply update in feature branch first
- **Review migrations**: Check if migrations are required

### 3. After Updates

- **Test thoroughly**: Ensure everything still works
- **Review changes**: Check updated files
- **Commit update**: Commit the version manifest update

## Troubleshooting

### "Could not determine latest template version"

**Causes**:
- Network connectivity issues
- Template repository not accessible
- GitHub API rate limiting

**Solutions**:
- Check internet connectivity
- Verify template repository URL
- Wait and retry

### "Update failed"

**Causes**:
- Protected files conflict
- Migration failure
- Network issues during clone

**Solutions**:
- Review error message
- Check protected files
- Retry update

### "Version check blocking commits"

**Solution**: Set `warn_only: true` in feature flags:

```yaml
template_updates:
  warn_only: true  # Don't block commits
```

## Configuration Examples

### Conservative (Default)

```yaml
template_updates:
  check_on_commit: true
  auto_update: false
  warn_only: true
```

**Behavior**: Check and warn, but don't auto-update or block commits.

### Aggressive

```yaml
template_updates:
  check_on_commit: true
  auto_update: true
  warn_only: false
```

**Behavior**: Check, auto-update, and block commits if update fails.

### Manual Only

```yaml
template_updates:
  check_on_commit: false
  auto_update: false
  warn_only: true
```

**Behavior**: Only check when manually running `update-template`.

## Summary

The template update execution rules ensure:

- ✅ **Automatic checking**: Updates checked on every commit
- ✅ **Idempotent**: Safe to run multiple times
- ✅ **Non-breaking**: Protected files never overwritten
- ✅ **Stateful**: Complete update history maintained
- ✅ **Configurable**: Behavior controlled via feature flags
- ✅ **Safe defaults**: Warns but doesn't block by default

This creates a self-maintaining system where projects automatically stay current with template improvements.

