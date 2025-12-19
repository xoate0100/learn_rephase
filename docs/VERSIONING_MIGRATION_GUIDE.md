# Versioning Migration Guide

## Overview

This guide helps you migrate pre-versioned projects (created before template versioning was added) to the versioned template system. The versioning system enables safe template updates while preserving your project customizations.

## Quick Start

If your project was created before template versioning was added:

```bash
# 1. Initialize versioning
python3 3_bootstrap_scripts/init_versioning.py

# 2. Verify CLI support
python3 3_bootstrap_scripts/cli.py update-template --help

# 3. Run first update (dry-run to preview)
python3 3_bootstrap_scripts/cli.py update-template --dry-run

# 4. Apply updates
python3 3_bootstrap_scripts/cli.py update-template
```

## Step-by-Step Instructions

### Step 1: Initialize Versioning

For pre-versioned projects, use the standalone initialization script:

```bash
python3 3_bootstrap_scripts/init_versioning.py
```

This script:
- Detects if your project is pre-versioned (no `META_FRAMEWORK_VERSION.yaml`)
- Detects or prompts for your template repository URL
- Creates initial version manifest (version 1.0.0)
- Does NOT require `template_update.py` to exist (solves chicken-and-egg problem)

**Options:**
- `--template-repo URL`: Specify template repository URL directly
- `--version VERSION`: Set initial version (default: 1.0.0)

**Example:**
```bash
python3 3_bootstrap_scripts/init_versioning.py --template-repo https://github.com/your-org/project_initializer.git
```

### Step 2: Verify CLI Support

Check if your CLI has the `update-template` command:

```bash
python3 3_bootstrap_scripts/cli.py update-template --help
```

**If command not found:**

Your `cli.py` may be from an older version. You have two options:

**Option A: Use template_update.py directly**
```bash
python3 3_bootstrap_scripts/template_update.py --dry-run
python3 3_bootstrap_scripts/template_update.py
```

**Option B: Update cli.py manually**
1. Check the template repository's `cli.py` for the `update-template` command
2. Copy the command definition to your `cli.py`
3. Or wait for the first template update to bring in the new CLI

### Step 3: Preview Updates (Dry Run)

Always preview changes before applying:

```bash
python3 3_bootstrap_scripts/cli.py update-template --dry-run
```

This shows:
- Files that will be updated
- Protected files that will be skipped
- No actual changes are made

### Step 4: Apply Updates

Once you've reviewed the dry-run output:

```bash
python3 3_bootstrap_scripts/cli.py update-template
```

This will:
- Update template files from the repository
- Preserve your protected files (MVP_SPECIFICATION.yaml, feature_flags.yml)
- Update the version manifest
- Record the update in `update_history`

## Troubleshooting

### Issue: "This project does not have version tracking initialized"

**Solution:** Run initialization:
```bash
python3 3_bootstrap_scripts/init_versioning.py
```

### Issue: CLI Missing `update-template` Command

**Symptoms:** `cli.py update-template --help` fails with "invalid choice" or similar

**Solution 1:** Use template_update.py directly:
```bash
python3 3_bootstrap_scripts/template_update.py --dry-run
python3 3_bootstrap_scripts/template_update.py
```

**Solution 2:** Manually update cli.py:
1. Check template repository for latest `cli.py`
2. Copy the `update-template` command definition
3. Add it to your `cli.py` in the subparsers section

**Solution 3:** Wait for first update - the template update will bring in the new CLI

### Issue: `update_history` Not Populated After Update

**Symptoms:** Files updated but `META_FRAMEWORK_VERSION.yaml` `update_history` is empty

**Root Cause:** This was a bug in older versions when using `--force` with "latest" version

**Solution:** This is now fixed in the template. If you encounter this:
1. Manually add entry to `update_history` in `META_FRAMEWORK_VERSION.yaml`:
   ```yaml
   update_history:
     - from_version: "1.0.0"
       to_version: "1.2.0"
       updated_at: "2024-01-20T00:00:00Z"
       migration_applied: false
       notes: "Template update"
   ```
2. Update `last_updated_at` field
3. Update `template_version` to the new version

### Issue: "Could not resolve 'latest' version"

**Symptoms:** Warning message about not resolving "latest" version

**Solution:** Specify a version explicitly:
```bash
python3 3_bootstrap_scripts/cli.py update-template --version 1.2.0
```

### Issue: Protected Files Were Modified

**Symptoms:** Your customizations in `MVP_SPECIFICATION.yaml` or `feature_flags.yml` were overwritten

**Solution:** This should not happen. If it does:
1. Restore from git: `git checkout HEAD -- 0_phase0_bootstrap/MVP_SPECIFICATION.yaml`
2. Verify `protected_files` list in `META_FRAMEWORK_VERSION.yaml` includes these files
3. Report as a bug

## Understanding Protected Files

Protected files are never overwritten during template updates. By default:
- `0_phase0_bootstrap/MVP_SPECIFICATION.yaml` - Your project configuration
- `0_phase0_bootstrap/feature_flags.yml` - Your feature flags

You can add more protected files in `META_FRAMEWORK_VERSION.yaml`:
```yaml
protected_files:
  - "0_phase0_bootstrap/MVP_SPECIFICATION.yaml"
  - "0_phase0_bootstrap/feature_flags.yml"
  - "your/custom/file.yaml"  # Add your custom files here
```

## Understanding Template vs Project Directories

**Template directories** (updated during template updates):
- `0_phase0_bootstrap/` (except protected files)
- `1_global_standards/`
- `2_framework_templates/`
- `3_bootstrap_scripts/`
- `5_reference_architectures/`
- `7_schemas/`
- `8_ci/`

**Project directories** (never updated):
- `4_docs_index/`
- `6_ai_runtime_context/`
- `frontend/`, `backend/`, `shared/`
- `apps/`, `packages/`
- `docs/` (project-specific docs)

## Best Practices

1. **Always use dry-run first** - Preview changes before applying
2. **Commit before updating** - Create a backup commit before major updates
3. **Review changes** - Use `git diff` to review what changed after update
4. **Test after update** - Run your tests and verify systems work
5. **Document customizations** - If you customize template files, document them (they may be overwritten)

## Future Updates

Once versioning is initialized, future updates are simple:

```bash
# Check for updates
python3 3_bootstrap_scripts/cli.py update-template --dry-run

# Apply updates
python3 3_bootstrap_scripts/cli.py update-template
```

No manual steps needed! The process takes 15-30 minutes (vs 2 hours for initial migration).

## Related Documentation

- `docs/TEMPLATE_LEVEL_ADJUSTMENTS_NEEDED.md` - Detailed technical analysis
- `docs/TEMPLATE_FIXES_SUMMARY.md` - Quick reference summary
- `0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml` - Version manifest format

## Getting Help

If you encounter issues not covered here:

1. Check the feedback log: `Feedback/ai_feedback_log*.json`
2. Review template repository issues
3. Check `META_FRAMEWORK_VERSION.yaml` for configuration issues
4. Verify protected files list is correct
