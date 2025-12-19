# Pre-Versioned Project Upgrade - Start Here

## Quick Start for AI Agents

You are upgrading a pre-versioned project (initialized with project_initializer before versioning was added) to the latest version with version tracking.

### Detection

**Is this a pre-versioned project?**
- ✅ Has meta-framework structure (0_phase0_bootstrap/, etc.)
- ❌ Missing `META_FRAMEWORK_VERSION.yaml`

**Check**:
```bash
ls 0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml
# If file doesn't exist → pre-versioned project
```

### Step 1: Discover the Update System

**Repository**: https://github.com/xoate0100/project_initializer

**Key Files**:
- `3_bootstrap_scripts/template_update.py` - Update script
- `docs/TEMPLATE_VERSIONING_GUIDE.md` - Versioning guide
- `docs/TEMPLATE_UPDATE_EXECUTION_RULES.md` - Update rules

### Step 2: Get the Update Script

If `3_bootstrap_scripts/template_update.py` doesn't exist:

1. Get from: https://github.com/xoate0100/project_initializer/blob/main/3_bootstrap_scripts/template_update.py
2. Save to: `3_bootstrap_scripts/template_update.py`
3. Install: `pip install pyyaml` (if needed)

### Step 3: Initialize Version Tracking

```bash
python3 3_bootstrap_scripts/template_update.py --init-versioning --template-repo https://github.com/xoate0100/project_initializer.git
```

This creates `META_FRAMEWORK_VERSION.yaml` and initializes version tracking.

### Step 4: Update to Latest

```bash
# Check what would be updated
python3 3_bootstrap_scripts/template_update.py --dry-run

# Apply updates
python3 3_bootstrap_scripts/template_update.py --template-repo https://github.com/xoate0100/project_initializer.git
```

### Step 5: Validate

```bash
# Check version
cat 0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml

# Validate
python3 3_bootstrap_scripts/cli.py validate
```

### Critical Rules

- **NEVER overwrite** `MVP_SPECIFICATION.yaml` or `feature_flags.yml`
- **ALWAYS preserve** project customizations
- **ALWAYS test** after update

### Need Help?

Read full instructions: `docs/PRE_VERSIONED_UPGRADE_PROMPT.md`

---

**Start by discovering the update system in the project_initializer repository!**

