# Legacy Project Upgrade - Start Here

## Quick Start for AI Agents

You are upgrading this legacy project to the **project_initializer** format. Follow these steps autonomously.

### Step 1: Discover the Upgrade System

**Repository**: https://github.com/xoate0100/project_initializer

**Key Files to Read**:
1. `docs/LEGACY_UPGRADE_GUIDE.md` - Complete upgrade workflow
2. `6_ai_runtime_context/LEGACY_UPGRADE_AI_INSTRUCTIONS.md` - Your instructions
3. `3_bootstrap_scripts/upgrade_legacy_project.py` - The upgrade script
4. `docs/LEGACY_UPGRADE_EXAMPLE_PROJECTS.md` - Similar project examples

### Step 2: Get the Upgrade Script

If `3_bootstrap_scripts/upgrade_legacy_project.py` doesn't exist:

1. Get it from: https://github.com/xoate0100/project_initializer/blob/main/3_bootstrap_scripts/upgrade_legacy_project.py
2. Create directory: `mkdir -p 3_bootstrap_scripts`
3. Save the script to: `3_bootstrap_scripts/upgrade_legacy_project.py`
4. Make executable: `chmod +x 3_bootstrap_scripts/upgrade_legacy_project.py`

### Step 3: Run the Upgrade Workflow

```bash
# Phase 1: Analyze
python3 3_bootstrap_scripts/upgrade_legacy_project.py --analyze

# Phase 2: Plan
python3 3_bootstrap_scripts/upgrade_legacy_project.py --plan

# Phase 3: Execute
python3 3_bootstrap_scripts/upgrade_legacy_project.py --execute --template-repo https://github.com/xoate0100/project_initializer.git

# Phase 4: Validate
python3 3_bootstrap_scripts/upgrade_legacy_project.py --validate
```

### Critical Rules

- **NEVER delete** existing files
- **NEVER modify** existing code
- **ALWAYS preserve** existing structure
- **ALWAYS test** after changes
- **ALWAYS commit** incrementally

### Need Help?

Read the full instructions: `docs/LEGACY_UPGRADE_PROMPT.md`

---

**Start by discovering the upgrade system in the project_initializer repository!**

