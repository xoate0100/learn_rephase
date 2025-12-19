# Force Upgrade - Start Here

## Quick Start for AI Agents

You are **force upgrading** this project to the latest project_initializer version automatically.

### Prerequisites

- ✅ Project has `META_FRAMEWORK_VERSION.yaml` (version tracking)
- ✅ Meta-framework structure exists

**If no version tracking**, use `PRE_VERSIONED_UPGRADE_START_HERE.md` first.

### Step 1: Get Template Repository

```bash
TEMPLATE_REPO=$(python3 -c "import yaml; print(yaml.safe_load(open('0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml'))['template_repo'])")
echo "Template repo: $TEMPLATE_REPO"
```

### Step 2: Force Update

```bash
# Check what would be updated
python3 3_bootstrap_scripts/cli.py update-template --template-repo "$TEMPLATE_REPO" --dry-run

# Force update to latest
python3 3_bootstrap_scripts/cli.py update-template --template-repo "$TEMPLATE_REPO" --force
```

### Step 3: Validate

```bash
# Check new version
cat 0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml | grep template_version

# Validate
python3 3_bootstrap_scripts/cli.py validate
```

### One-Liner (All Steps)

```bash
TEMPLATE_REPO=$(python3 -c "import yaml; print(yaml.safe_load(open('0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml'))['template_repo'])") && \
python3 3_bootstrap_scripts/cli.py update-template --template-repo "$TEMPLATE_REPO" --force && \
python3 3_bootstrap_scripts/cli.py validate
```

### Critical Rules

- **NEVER overwrites** `MVP_SPECIFICATION.yaml` or `feature_flags.yml`
- **ALWAYS preserves** project code
- **ALWAYS validates** after update

### Need Help?

Read full instructions: `docs/FORCE_UPGRADE_PROMPT.md`

---

**Execute the force upgrade now!**

