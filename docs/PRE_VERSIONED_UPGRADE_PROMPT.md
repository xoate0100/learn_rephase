# Pre-Versioned Project Upgrade - AI Agent Prompt

## Instructions for AI Agent

You are tasked with upgrading a project that was initialized with **project_initializer** but from before version tracking was added (pre-version 1.0.0). This project has some meta-framework structure but lacks version tracking and may be missing newer features.

### Your Mission

Upgrade this pre-versioned project to the latest project_initializer format by:
1. Discovering the versioning and update system in the project_initializer repository
2. Initializing version tracking
3. Updating to the latest template version
4. Ensuring all new features are available

### Reference Repository

**Repository**: https://github.com/xoate0100/project_initializer

**Key Files to Discover**:
- `3_bootstrap_scripts/template_update.py` - Template update system
- `docs/TEMPLATE_VERSIONING_GUIDE.md` - Versioning guide
- `docs/TEMPLATE_UPDATE_EXECUTION_RULES.md` - Update execution rules
- `0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml` - Version manifest template

### Detection: Is This a Pre-Versioned Project?

**Indicators**:
- ✅ Has meta-framework structure (0_phase0_bootstrap/, 3_bootstrap_scripts/, etc.)
- ✅ Has `feature_flags.yml` and `AI_SANDBOX_RULES.md`
- ❌ Missing `META_FRAMEWORK_VERSION.yaml`
- ❌ No version tracking
- ❌ May be missing newer features (feedback collection, template updates, etc.)

**Check**:
```bash
# Check if version manifest exists
ls 0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml

# If file doesn't exist, this is a pre-versioned project
```

### Discovery Process

1. **Examine the Repository**:
   - Read the project_initializer repository structure
   - Locate the template update system
   - Understand version tracking and update workflow

2. **Review Update Instructions**:
   - Read `docs/TEMPLATE_VERSIONING_GUIDE.md` for versioning system
   - Review `docs/TEMPLATE_UPDATE_EXECUTION_RULES.md` for update rules
   - Check `3_bootstrap_scripts/template_update.py` for update script

3. **Understand Version Tracking**:
   - Learn about `META_FRAMEWORK_VERSION.yaml`
   - Understand update history tracking
   - Learn about feature flags

### Upgrade Workflow

Follow these steps **autonomously**:

#### Step 1: Get the Update Script

If `3_bootstrap_scripts/template_update.py` doesn't exist:

1. Get it from: https://github.com/xoate0100/project_initializer/blob/main/3_bootstrap_scripts/template_update.py
2. Ensure directory exists: `mkdir -p 3_bootstrap_scripts`
3. Save the script
4. Install dependencies: `pip install pyyaml` (if needed)

#### Step 2: Initialize Version Tracking

```bash
python3 3_bootstrap_scripts/template_update.py --init-versioning --template-repo https://github.com/xoate0100/project_initializer.git
```

**What it does**:
- Detects template repository (from git remote or prompts)
- Creates `META_FRAMEWORK_VERSION.yaml`
- Detects available features
- Initializes update tracking

**Your Actions**:
- Run the initialization command
- Provide template repository URL if prompted
- Review the generated version manifest

#### Step 3: Check for Updates

```bash
python3 3_bootstrap_scripts/template_update.py --dry-run
```

**What it does**:
- Compares current version with latest
- Shows what would be updated
- Identifies new features available

**Your Actions**:
- Run dry-run to see available updates
- Review what would change
- Note any new features

#### Step 4: Update to Latest Version

```bash
python3 3_bootstrap_scripts/template_update.py --template-repo https://github.com/xoate0100/project_initializer.git
```

**What it does**:
- Fetches latest version from template repository
- Clones template to temporary directory
- Updates template files (preserves project customizations)
- Applies migrations if needed
- Updates version manifest

**Your Actions**:
- Run update command
- Monitor update progress
- Review updated files
- Test that project still works

#### Step 5: Validate Update

```bash
# Check version manifest
cat 0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml

# Run validation
python3 3_bootstrap_scripts/cli.py validate
```

**What it checks**:
- Version manifest exists and is valid
- Template files updated correctly
- Project customizations preserved
- All tests pass

**Your Actions**:
- Verify version manifest
- Run validation
- Test project functionality
- Fix any issues

### Critical Constraints

**NEVER**:
- ❌ Overwrite `MVP_SPECIFICATION.yaml` (project-specific)
- ❌ Overwrite `feature_flags.yml` (may have project customizations)
- ❌ Delete or modify project code
- ❌ Break existing functionality

**ALWAYS**:
- ✅ Preserve project customizations
- ✅ Test after update
- ✅ Commit incrementally
- ✅ Review changes before committing

### Protected Files

These files are **never overwritten** during updates:
- `0_phase0_bootstrap/MVP_SPECIFICATION.yaml` - Project configuration
- `0_phase0_bootstrap/feature_flags.yml` - Project settings (may have customizations)
- All project directories (frontend/, backend/, shared/, etc.)

### Update Process

The update system:
1. **Clones template** to temporary directory
2. **Copies template files** while respecting protected files
3. **Applies migrations** for breaking changes
4. **Updates version manifest** with new version and history
5. **Preserves project code** completely

### New Features Available

After updating, you may gain access to:
- **Template Versioning**: Track template version and receive updates
- **Feedback Collection**: Send anonymized feedback to improve template
- **Dynamic AI Context**: Auto-generated AI context document
- **Template Update Execution**: Automatic update checking on commits
- **Legacy Upgrade System**: Upgrade other legacy projects
- **Version Bump Quality Gate**: Ensure version discipline

### Migration Handling

If migrations are required:
- Migrations are applied automatically
- Migration notes are recorded in version manifest
- Breaking changes are documented
- Manual steps (if any) are noted

### Troubleshooting

**"Template repository URL required"**:
- Set `--template-repo` argument
- Or set in version manifest after initialization

**"Failed to clone template"**:
- Check network connectivity
- Verify repository URL is correct
- Check repository access

**"Update failed"**:
- Review error messages
- Check protected files aren't conflicting
- Retry update

**"Version check blocking commits"**:
- This is normal for template repository
- Use `--no-verify` if updating template itself
- Projects using template won't have this issue

### Post-Upgrade Steps

After successful upgrade:

1. **Review Changes**: `git status` and `git diff`
2. **Test Thoroughly**: Ensure everything works
3. **Check Features**: Verify new features are available
4. **Update Documentation**: Document any manual steps taken
5. **Commit Changes**: Commit incrementally with clear messages

### Success Criteria

Upgrade is successful when:
- ✅ `META_FRAMEWORK_VERSION.yaml` exists
- ✅ Version tracking initialized
- ✅ Template files updated to latest
- ✅ All existing functionality preserved
- ✅ New features available
- ✅ Project builds and runs
- ✅ Tests pass (if available)

### Autonomous Execution

You should:
- **Discover** the update system from project_initializer repository
- **Initialize** version tracking
- **Check** for available updates
- **Update** to latest version
- **Validate** update success
- **Test** that everything works
- **Document** any issues or customizations

### Questions to Answer

Before starting, discover answers to:
1. What is the template versioning system?
2. How do I initialize version tracking?
3. How do I check for updates?
4. How do I apply updates safely?
5. What features are available in latest version?

### Start Here

1. **Examine project_initializer repository**: https://github.com/xoate0100/project_initializer
2. **Read versioning guide**: Find and read `docs/TEMPLATE_VERSIONING_GUIDE.md`
3. **Understand update system**: Review `3_bootstrap_scripts/template_update.py`
4. **Begin upgrade**: Start with version initialization

### Quick Command Reference

```bash
# Initialize versioning
python3 3_bootstrap_scripts/template_update.py --init-versioning --template-repo https://github.com/xoate0100/project_initializer.git

# Check for updates (dry-run)
python3 3_bootstrap_scripts/template_update.py --dry-run

# Update to latest
python3 3_bootstrap_scripts/template_update.py --template-repo https://github.com/xoate0100/project_initializer.git

# Or use CLI
python3 3_bootstrap_scripts/cli.py update-template --init-versioning
python3 3_bootstrap_scripts/cli.py update-template
```

---

**Remember**: Your goal is to add version tracking and update to the latest template version while preserving all project customizations. The update system is designed to be safe and non-breaking.

Good luck! 🚀

