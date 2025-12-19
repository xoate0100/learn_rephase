# Template-Level Adjustments Needed for Pre-Versioned to Versioned Migration

## Executive Summary

Based on feedback from the first migration of a pre-versioned project to versioned state, four critical template-level adjustments are needed to streamline the migration process and eliminate manual workarounds.

## Issues Identified

### 1. CRITICAL: Chicken-and-Egg Problem with `template_update.py`

**Problem:**
- Pre-versioned projects don't have `template_update.py` script
- The script is needed to initialize versioning
- The script is part of the template itself, creating a circular dependency
- Users must manually clone template repo and copy the script

**Current Workaround:**
```bash
# Clone template repo → Copy template_update.py and migrations/ → Run initialization
```

**Template-Level Fix Required:**
1. **Create standalone initialization script** (`init_versioning.py` or similar)
   - Should be a minimal script that doesn't depend on template_update.py
   - Can be distributed separately or included in template root
   - Purpose: Initialize META_FRAMEWORK_VERSION.yaml for pre-versioned projects
   - Should detect template repo from git remote or prompt user
   - Should create initial version manifest with version "1.0.0"

2. **Update documentation** to prominently feature this initialization script
   - Add to `INITIALIZATION_GUIDE.md` or create `VERSIONING_MIGRATION_GUIDE.md`
   - Include clear step-by-step instructions for pre-versioned projects

**Recommended Implementation:**
```python
# 3_bootstrap_scripts/init_versioning.py (standalone, minimal)
# - Detects pre-versioned state
# - Prompts for or detects template repo URL
# - Creates META_FRAMEWORK_VERSION.yaml with version 1.0.0
# - Does NOT require template_update.py to exist
```

**Files to Modify:**
- Create: `3_bootstrap_scripts/init_versioning.py`
- Update: `INITIALIZATION_GUIDE.md` or create `VERSIONING_MIGRATION_GUIDE.md`
- Update: `README.md` to mention versioning migration path

---

### 2. CRITICAL: CLI `update-template` Command Missing in Pre-Versioned Projects

**Problem:**
- Pre-versioned projects have `cli.py` without `update-template` command
- Command was added to template after many projects were created
- Users must manually update `cli.py` before using update-template

**Current Workaround:**
- Manual copy of update-template command from template's cli.py

**Template-Level Fix Required:**
1. **Backward compatibility check in `template_update.py`**
   - When `--init-versioning` is used, check if CLI has update-template command
   - If missing, provide clear error message with instructions
   - Optionally, auto-update cli.py during initialization (risky, but helpful)

2. **Documentation update**
   - Add note in migration guide about CLI update requirement
   - Provide copy-paste snippet for adding command

**Recommended Implementation:**
```python
# In template_update.py, during --init-versioning:
def check_cli_support():
    """Check if cli.py has update-template command."""
    cli_path = pathlib.Path("3_bootstrap_scripts/cli.py")
    if not cli_path.exists():
        return False
    content = cli_path.read_text()
    return "update-template" in content

# If missing, provide helpful error message with instructions
```

**Files to Modify:**
- Update: `3_bootstrap_scripts/template_update.py` (add CLI check)
- Update: Migration documentation

---

### 3. CRITICAL: Version Manifest `update_history` Not Populated When Using `--force` with `latest`

**Problem:**
- When running `update-template --force`, target_version becomes "latest"
- `apply_migrations()` function tries to parse "latest" as version number
- This causes `ValueError` in `version_tuple()` function
- File updates complete, but `update_history` population fails
- Users must manually update `META_FRAMEWORK_VERSION.yaml`

**Root Cause:**
```python
# In template_update.py, line 237-242:
def version_tuple(v: str) -> Tuple[int, int, int]:
    parts = v.split("-")[0].split(".")
    return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0, ...)
# This fails when v = "latest"
```

**Template-Level Fix Required:**
1. **Resolve "latest" to actual version number before migration**
   - In `main()`, when `target_version == "latest"`, call `get_latest_template_version()`
   - If successful, use actual version number
   - If failed, use current version + 1 (or handle gracefully)

2. **Handle "latest" in `apply_migrations()` gracefully**
   - Add check: if version is "latest", skip migration logic
   - Or resolve to actual version before calling `apply_migrations()`

3. **Ensure `update_history` is always populated**
   - Move `update_version_manifest()` call to execute even if migrations fail
   - Use try/except around migrations, but always update manifest

**Recommended Implementation:**
```python
# In template_update.py main():

# Resolve "latest" to actual version
if target_version == "latest":
    resolved_version = get_latest_template_version(template_repo)
    if resolved_version:
        target_version = resolved_version
    else:
        print("WARN: Could not resolve 'latest', using current version")
        target_version = current_version

# Apply migrations (with error handling)
try:
    migration_applied, migration_notes = apply_migrations(
        current_version, target_version, pathlib.Path(".")
    )
except ValueError as e:
    if "latest" in str(e).lower():
        print("WARN: Skipping migrations for 'latest' version")
        migration_applied = False
        migration_notes = "Skipped (latest version)"
    else:
        raise

# Always update manifest (even if migrations failed)
manifest = update_version_manifest(manifest, target_version, migration_applied, migration_notes)
```

**Files to Modify:**
- Update: `3_bootstrap_scripts/template_update.py` (lines 231-274, 370-430)
- Add: Better error handling for version resolution

---

### 4. MEDIUM: Documentation Gaps for Migration Process

**Problem:**
- Migration process requires multiple manual steps
- Documentation doesn't clearly explain pre-versioned → versioned migration
- Users must discover workarounds through trial and error

**Template-Level Fix Required:**
1. **Create comprehensive migration guide**
   - `docs/VERSIONING_MIGRATION_GUIDE.md`
   - Step-by-step instructions for pre-versioned projects
   - Troubleshooting section
   - Common issues and solutions

2. **Update existing documentation**
   - Add migration section to `INITIALIZATION_GUIDE.md`
   - Update `README.md` with versioning information
   - Add migration checklist

**Recommended Content:**
```markdown
# Versioning Migration Guide

## For Pre-Versioned Projects

If your project was created before template versioning was added:

1. **Initialize Versioning**
   ```bash
   python3 3_bootstrap_scripts/init_versioning.py
   ```

2. **Verify CLI Support**
   ```bash
   python3 3_bootstrap_scripts/cli.py update-template --help
   ```
   If command not found, see "CLI Update" section below.

3. **Run First Update**
   ```bash
   python3 3_bootstrap_scripts/cli.py update-template --dry-run
   python3 3_bootstrap_scripts/cli.py update-template
   ```

## Troubleshooting

### CLI Missing update-template Command
[Instructions for manual update]

### update_history Not Populated
[Instructions for manual fix]
```

**Files to Create/Modify:**
- Create: `docs/VERSIONING_MIGRATION_GUIDE.md`
- Update: `INITIALIZATION_GUIDE.md`
- Update: `README.md`

---

## Priority Summary

| Issue | Priority | Impact | Effort | Files Affected |
|-------|----------|--------|--------|----------------|
| 1. Chicken-and-egg problem | **CRITICAL** | High - Blocks migration | Medium | `init_versioning.py` (new), docs |
| 2. CLI command missing | **CRITICAL** | High - Blocks usage | Low | `template_update.py`, docs |
| 3. update_history bug | **CRITICAL** | Medium - Incomplete tracking | Low | `template_update.py` |
| 4. Documentation gaps | **MEDIUM** | Medium - User confusion | Medium | Multiple docs |

---

## Implementation Checklist

### Phase 1: Critical Fixes (Must Have)
- [ ] Create `init_versioning.py` standalone script
- [ ] Fix `template_update.py` to resolve "latest" version
- [ ] Fix `template_update.py` to handle "latest" in migrations
- [ ] Add CLI check in `template_update.py`
- [ ] Ensure `update_history` always populated

### Phase 2: Documentation (Should Have)
- [ ] Create `VERSIONING_MIGRATION_GUIDE.md`
- [ ] Update `INITIALIZATION_GUIDE.md` with migration section
- [ ] Update `README.md` with versioning info
- [ ] Add troubleshooting section

### Phase 3: Enhancements (Nice to Have)
- [ ] Auto-update CLI during initialization (with confirmation)
- [ ] Better error messages with actionable steps
- [ ] Migration validation script
- [ ] Pre-migration checklist

---

## Testing Recommendations

1. **Test pre-versioned migration**
   - Create test project without versioning
   - Run migration process
   - Verify all fixes work

2. **Test "latest" version handling**
   - Run update with `--force` flag
   - Verify `update_history` populated correctly
   - Verify no ValueError exceptions

3. **Test CLI detection**
   - Test with old CLI (no update-template)
   - Verify helpful error message
   - Test with updated CLI

4. **Test documentation**
   - Follow migration guide step-by-step
   - Verify all steps work as documented
   - Identify any gaps

---

## Related Feedback Log Entries

- Entry 264-277: Chicken-and-egg problem
- Entry 279-290: CLI command missing
- Entry 291-305: update_history bug
- Entry 228-262: Overall migration process

---

## Notes

- All fixes should be backward compatible
- Pre-versioned projects should be able to migrate smoothly
- Future updates should be straightforward (15-30 minutes vs 2 hours)
- Protected files mechanism works perfectly (no changes needed)
