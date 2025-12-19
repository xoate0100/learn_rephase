# Force Upgrade - AI Agent Prompt

## Instructions for AI Agent

You are tasked with **automatically upgrading** this project to the **latest version** of project_initializer. This is a "force upgrade" - you should proceed autonomously with minimal confirmation, while maintaining safety.

### Your Mission

Force upgrade this project to the latest project_initializer version by:
1. Checking the latest version available
2. Automatically applying updates
3. Ensuring all new features are available
4. Validating upgrade success

### Reference Repository

**Repository**: https://github.com/xoate0100/project_initializer

**Key Files to Discover**:
- `3_bootstrap_scripts/template_update.py` - Template update system
- `3_bootstrap_scripts/cli.py` - CLI with update-template command
- `docs/TEMPLATE_VERSIONING_GUIDE.md` - Versioning guide
- `docs/TEMPLATE_UPDATE_EXECUTION_RULES.md` - Update execution rules

### Prerequisites

This prompt is for projects that:
- ✅ Already have `META_FRAMEWORK_VERSION.yaml` (version tracking initialized)
- ✅ Have meta-framework structure
- ✅ Want to force upgrade to latest version

**If version tracking not initialized**, use `PRE_VERSIONED_UPGRADE_START_HERE.md` first.

### Discovery Process

1. **Examine the Repository**:
   - Read the project_initializer repository
   - Locate the template update system
   - Understand the update workflow

2. **Review Update System**:
   - Read `docs/TEMPLATE_UPDATE_EXECUTION_RULES.md` for update rules
   - Review `3_bootstrap_scripts/template_update.py` for update script
   - Understand protected files and update process

### Force Upgrade Workflow

Execute these steps **autonomously** with minimal confirmation:

#### Step 1: Check Current Version

```bash
# Check current version
cat 0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml | grep template_version

# Or use Python
python3 -c "import yaml; print(yaml.safe_load(open('0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml'))['template_version'])"
```

**Your Actions**:
- Read current version from version manifest
- Note the current version number

#### Step 2: Get Template Repository URL

```bash
# Get from version manifest
cat 0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml | grep template_repo

# Or use Python
python3 -c "import yaml; print(yaml.safe_load(open('0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml'))['template_repo'])"
```

**Your Actions**:
- Extract template repository URL
- Use this URL for update commands

#### Step 3: Check for Updates (Dry Run)

```bash
python3 3_bootstrap_scripts/cli.py update-template --dry-run
```

**What it does**:
- Compares current version with latest
- Shows what would be updated
- Identifies update type (MAJOR/MINOR/PATCH)

**Your Actions**:
- Run dry-run to see available updates
- Note update type and scope
- Proceed to force update

#### Step 4: Force Update to Latest

```bash
# Get template repo from manifest first
TEMPLATE_REPO=$(python3 -c "import yaml; print(yaml.safe_load(open('0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml'))['template_repo'])")

# Force update to latest
python3 3_bootstrap_scripts/cli.py update-template --template-repo "$TEMPLATE_REPO" --force
```

**Or if using update script directly**:

```bash
TEMPLATE_REPO=$(python3 -c "import yaml; print(yaml.safe_load(open('0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml'))['template_repo'])")
python3 3_bootstrap_scripts/template_update.py --template-repo "$TEMPLATE_REPO" --force
```

**What it does**:
- Fetches latest version from template repository
- Clones template to temporary directory
- Updates all template files (preserves protected files)
- Applies migrations automatically
- Updates version manifest

**Your Actions**:
- Execute force update command
- Monitor update progress
- Handle any errors immediately
- Continue even if minor warnings occur

#### Step 5: Validate Upgrade

```bash
# Check new version
cat 0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml | grep template_version

# Run validation
python3 3_bootstrap_scripts/cli.py validate

# Or run pre-commit hooks
pre-commit run --all-files
```

**What it checks**:
- Version manifest updated correctly
- Template files updated
- Configuration valid
- Project still functional

**Your Actions**:
- Verify version updated
- Run validation
- Fix any validation errors
- Test project builds/runs

### Force Upgrade Behavior

**Automatic Actions**:
- ✅ Proceed without extensive confirmation
- ✅ Apply updates automatically
- ✅ Handle migrations automatically
- ✅ Update version manifest automatically

**Safety Maintained**:
- ✅ Backup branch created (if git available)
- ✅ Protected files never overwritten
- ✅ Project code never modified
- ✅ Validation after update

### Protected Files (Never Overwritten)

These files are **always preserved**:
- `0_phase0_bootstrap/MVP_SPECIFICATION.yaml` - Project configuration
- `0_phase0_bootstrap/feature_flags.yml` - Project settings
- All project directories (frontend/, backend/, shared/, etc.)

### Update Types

**MAJOR (X.0.0)**: Breaking changes, migrations required
- Review migration notes carefully
- Test thoroughly after update
- May require manual steps

**MINOR (0.X.0)**: New features, backward compatible
- Usually safe to apply automatically
- New features available after update

**PATCH (0.0.X)**: Bug fixes, backward compatible
- Safe to apply automatically
- Fixes issues without breaking changes

### Error Handling

**If update fails**:

1. **Check error message**: Review what failed
2. **Retry**: Sometimes network issues, retry once
3. **Manual steps**: If migrations require manual steps, follow them
4. **Rollback**: If critical failure, rollback: `git checkout backup-before-upgrade`

**Common Issues**:

- **Network error**: Retry the update command
- **Permission error**: Check file permissions
- **Conflict**: Review protected files, may need manual merge
- **Migration failure**: Check migration notes, may need manual steps

### Post-Upgrade Actions

After successful upgrade:

1. **Review Changes**: `git status` and `git diff`
2. **Test Project**: Ensure it builds and runs
3. **Run Tests**: Execute test suite if available
4. **Check Features**: Verify new features are available
5. **Commit Changes**: Commit upgrade with clear message

**Commit Message Format**:
```
upgrade: template to version X.Y.Z

- Updated from version A.B.C to X.Y.Z
- Applied migrations: [list if any]
- New features: [list if any]
- Validated: All checks passed
```

### Success Criteria

Upgrade is successful when:
- ✅ Version manifest shows latest version
- ✅ Template files updated
- ✅ All existing functionality preserved
- ✅ Project builds and runs
- ✅ Tests pass (if available)
- ✅ Validation passes

### Autonomous Execution Checklist

- [ ] Check current version
- [ ] Get template repository URL
- [ ] Check for available updates (dry-run)
- [ ] Force update to latest version
- [ ] Validate upgrade success
- [ ] Test project functionality
- [ ] Commit changes

### Quick Command Reference

```bash
# One-liner force upgrade
TEMPLATE_REPO=$(python3 -c "import yaml; print(yaml.safe_load(open('0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml'))['template_repo'])") && \
python3 3_bootstrap_scripts/cli.py update-template --template-repo "$TEMPLATE_REPO" --force && \
python3 3_bootstrap_scripts/cli.py validate
```

### Force vs Regular Upgrade

**Force Upgrade** (this prompt):
- Automatic, minimal confirmation
- Proceeds even if versions match (re-applies)
- Designed for automated workflows
- Less human interaction

**Regular Upgrade**:
- Requires confirmation
- Skips if already at latest
- More cautious approach
- More human oversight

### When to Use Force Upgrade

Use force upgrade when:
- ✅ You want automatic updates
- ✅ You trust the update system
- ✅ You're in an automated workflow
- ✅ You want to ensure latest version

**Don't use** if:
- ❌ You need to review changes first
- ❌ You have critical customizations
- ❌ You're unsure about breaking changes

### Getting Help

If stuck:
1. Review `docs/TEMPLATE_VERSIONING_GUIDE.md`
2. Check `docs/TEMPLATE_UPDATE_EXECUTION_RULES.md`
3. Review error messages carefully
4. Check migration notes in version manifest

---

**Remember**: Force upgrade is automatic but safe. Protected files are never overwritten, and you can always rollback if needed.

**Start by checking the current version and forcing an update to the latest!**

