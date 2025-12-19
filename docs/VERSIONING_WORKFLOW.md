# Template Versioning Workflow

## Overview

This document describes the versioning workflow for the template repository. All template changes must be accompanied by version bumps to ensure projects can track and update to new versions.

## Version Numbering

The template uses [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes that require migrations
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes, backward compatible

### Current Version

Check `0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml` for the current version.

## Version Bump Quality Gate

A pre-commit hook (`scripts/check_version_bump.py`) ensures that:

1. **Template files changed** → Version must be bumped
2. **Version file changed** → Version must increase
3. **No template files changed** → Version bump not required

### What Triggers Version Bump

Any changes to template directories:
- `0_phase0_bootstrap/` (except `MVP_SPECIFICATION.yaml` and `feature_flags.yml` in projects)
- `1_global_standards/`
- `2_framework_templates/`
- `3_bootstrap_scripts/`
- `5_reference_architectures/`
- `7_schemas/`
- `8_ci/`
- `.github/`
- `.pre-commit-config.yaml`
- `requirements.txt`

### What Doesn't Trigger Version Bump

- Project-specific files (frontend/, backend/, shared/, etc.)
- Documentation in `docs/` (project-specific)
- `4_docs_index/` and `6_ai_runtime_context/` (project state)

## Workflow

### 1. Make Template Changes

Edit template files as needed.

### 2. Update Version

Update `0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml`:

```yaml
template_version: "1.2.0"  # Bump version
last_updated_at: "2024-01-20T00:00:00Z"  # Update timestamp

update_history:
  - from_version: "1.1.0"
    to_version: "1.2.0"
    updated_at: "2024-01-20T00:00:00Z"
    migration_applied: false
    notes: "Description of changes"
```

### 3. Update Features List

If adding new features, update the `features` section:

```yaml
features:
  dynamic_layout_adaptation: true
  guided_initialization: true
  dynamic_ai_context: true
  template_versioning: true
  drift_detection: true
  feedback_collection: true  # New feature
  new_feature: true  # Add new features here
```

### 4. Create Migration (If Needed)

For breaking changes (MAJOR version), create a migration:

```python
# 3_bootstrap_scripts/migrations/migration_1_2_0.py
def migrate_to_1_2_0(project_root: pathlib.Path) -> Tuple[bool, str]:
    """Migrate to version 1.2.0: Breaking change description"""
    # Apply migration logic
    return True, "Migration notes"
```

### 5. Commit Changes

The pre-commit hook will verify:
- Version was bumped if template files changed
- Version actually increased
- Version bump is appropriate

### 6. Tag Release

After committing and pushing:

```bash
git tag v1.2.0
git push origin v1.2.0
```

## Version Bump Guidelines

### When to Bump MAJOR (X.0.0)

- Breaking changes to schemas
- Changes that require manual migration
- Changes that break backward compatibility
- Major architectural changes

### When to Bump MINOR (0.X.0)

- New features
- New scripts or tools
- New configuration options
- Enhancements to existing features
- New documentation or guides

### When to Bump PATCH (0.0.X)

- Bug fixes
- Documentation corrections
- Minor improvements
- Performance optimizations
- Security patches

## Examples

### Example 1: New Feature (MINOR bump)

**Changes:**
- Added `feedback_collector.py`
- Added feedback collection to feature flags
- Added documentation

**Version:** `1.0.0` → `1.1.0`

### Example 2: Bug Fix (PATCH bump)

**Changes:**
- Fixed Unicode encoding issue in `guardrail_enforcement.py`
- Fixed path handling in `template_update.py`

**Version:** `1.1.0` → `1.1.1`

### Example 3: Breaking Change (MAJOR bump)

**Changes:**
- Changed `MVP_SPECIFICATION.yaml` schema structure
- Requires migration for existing projects

**Version:** `1.1.0` → `2.0.0`
**Migration:** Create `migration_2_0_0.py`

## Bypassing the Check

If you need to bypass the version check (not recommended):

```bash
git commit --no-verify
```

**Warning:** Only bypass if you have a good reason (e.g., fixing the version check itself).

## Troubleshooting

### "Template files changed but version not bumped"

**Solution:** Update `META_FRAMEWORK_VERSION.yaml` with a new version number.

### "Version file changed but version did not increase"

**Solution:** Ensure the new version is higher than the previous version.

### "Version check failing in projects"

**Solution:** The version check should only run in the template repository. If it runs in projects, it's a bug. The check should skip if it detects it's not the template repo.

## Best Practices

1. **Always bump version** when changing template files
2. **Update features list** when adding new capabilities
3. **Document changes** in `update_history`
4. **Create migrations** for breaking changes
5. **Tag releases** after pushing changes
6. **Test updates** in a test project before releasing

## Automation

The version check is automated via pre-commit hook. It:
- Runs on every commit
- Checks if template files changed
- Verifies version was bumped
- Provides clear error messages

This ensures version discipline without manual oversight.

