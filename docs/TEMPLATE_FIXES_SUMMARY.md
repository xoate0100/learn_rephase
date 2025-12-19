# Template Fixes Summary - Pre-Versioned Migration Issues

## Quick Reference

Based on feedback from first pre-versioned → versioned migration, these template fixes are needed:

### 1. Create Standalone Initialization Script ⚠️ CRITICAL

**Issue:** `template_update.py` doesn't exist in pre-versioned projects but is needed to initialize versioning.

**Fix:** Create `3_bootstrap_scripts/init_versioning.py` - minimal script that:
- Detects pre-versioned state (no META_FRAMEWORK_VERSION.yaml)
- Detects/prompts for template repo URL
- Creates initial version manifest (version 1.0.0)
- Does NOT require template_update.py to exist

**Impact:** Eliminates manual template cloning step

---

### 2. Fix "latest" Version Handling ⚠️ CRITICAL

**Issue:** When using `--force`, target_version becomes "latest", causing `ValueError` in `apply_migrations()` when trying to parse "latest" as version number. Files update but `update_history` is not populated.

**Fix:** In `template_update.py`:
- Resolve "latest" to actual version number before migrations
- Handle "latest" gracefully in `apply_migrations()` (skip or resolve)
- Ensure `update_version_manifest()` always executes (even if migrations fail)

**Location:** `3_bootstrap_scripts/template_update.py` lines 231-274, 370-430

**Impact:** Ensures version tracking is always complete

---

### 3. Add CLI Command Detection ⚠️ CRITICAL

**Issue:** Pre-versioned projects have old `cli.py` without `update-template` command.

**Fix:** In `template_update.py` during `--init-versioning`:
- Check if CLI has `update-template` command
- Provide helpful error message if missing
- Optionally auto-update CLI (with confirmation)

**Location:** `3_bootstrap_scripts/template_update.py` (add check function)

**Impact:** Better user experience, fewer manual steps

---

### 4. Create Migration Documentation 📚 MEDIUM

**Issue:** Migration process not clearly documented, users discover workarounds through trial and error.

**Fix:** Create `docs/VERSIONING_MIGRATION_GUIDE.md` with:
- Step-by-step migration instructions
- Troubleshooting section
- Common issues and solutions
- Pre-migration checklist

**Impact:** Reduces user confusion and support burden

---

## Code Changes Required

### File: `3_bootstrap_scripts/init_versioning.py` (NEW)
```python
#!/usr/bin/env python3
"""Standalone script to initialize versioning for pre-versioned projects."""
# Minimal implementation that creates META_FRAMEWORK_VERSION.yaml
# without requiring template_update.py
```

### File: `3_bootstrap_scripts/template_update.py` (MODIFY)
- Line ~370: Resolve "latest" to actual version before migrations
- Line ~231: Handle "latest" in `apply_migrations()` gracefully
- Line ~425: Ensure `update_version_manifest()` always executes
- Add: `check_cli_support()` function

### File: `docs/VERSIONING_MIGRATION_GUIDE.md` (NEW)
- Complete migration guide for pre-versioned projects
- Troubleshooting section
- Common issues and solutions

---

## Testing Checklist

- [ ] Test pre-versioned project migration with new `init_versioning.py`
- [ ] Test `--force` flag with "latest" version (verify update_history populated)
- [ ] Test with old CLI (no update-template command)
- [ ] Test with updated CLI
- [ ] Verify protected files still preserved
- [ ] Follow migration guide end-to-end

---

## Estimated Impact

- **Before fixes:** 2 hours migration time, multiple manual steps
- **After fixes:** 15-30 minutes, mostly automated
- **User experience:** Significantly improved, fewer errors

---

## Related Files

- `Feedback/ai_feedback_log1 .json` - Source of issues
- `docs/TEMPLATE_LEVEL_ADJUSTMENTS_NEEDED.md` - Detailed analysis
- `3_bootstrap_scripts/template_update.py` - Script to fix
- `3_bootstrap_scripts/cli.py` - CLI to check/update
