# Project Initialization Guide

## Quick Start

After cloning this template repository, run:

```bash
python3 3_bootstrap_scripts/cli.py init --guided
```

The guided mode minimizes structure mismatches by generating `PROJECT_LAYOUT` automatically.

### Fully non-interactive (answers-file mode)

1. Edit `6_ai_runtime_context/INIT_WIZARD_ANSWERS.yaml` to match your repo layout (e.g., Next.js root, apps/web, packages/shared).
2. Run:

```bash
python3 3_bootstrap_scripts/cli.py init --guided --answers 6_ai_runtime_context/INIT_WIZARD_ANSWERS.yaml
```

## What Happens During Initialization

The initialization process (`cli.py init`) performs the following steps:

1. **Detect Initial State** - Checks if already initialized (via `.initialized` file)
2. **Load Meta-Framework** - Loads `feature_flags.yml` and `MVP_SPECIFICATION.yaml`
3. **Validate Schemas** - Ensures all configuration files are valid
4. **Guided Layout (Wizard)** - Writes/refreshes `PROJECT_LAYOUT` (optional, when `--guided` is used)
   - **State outputs**:
     - `6_ai_runtime_context/INIT_WIZARD_RESULT.yaml`
     - `6_ai_runtime_context/INIT_WIZARD_ANSWERS.yaml` (optional input)
5. **Layout Adaptation Plan** - Emits `6_ai_runtime_context/LAYOUT_REARRANGEMENT_PLAN.yaml` (proposal; apply only if explicitly enabled)
4. **Verify Sandbox** - Confirms L2.5 sandbox mode is enabled
5. **Install Dependencies** - Installs Python and Node dependencies
6. **Scaffold Structure** - Creates folder structure from `MONOREPO_LAYOUT` or `PROJECT_LAYOUT` (preferred for non-standard layouts)
7. **Generate Plan** - Creates `ACTIVE_PLAN.yaml` from MVP spec template
8. **Init AI Context** - Sets up feedback logs and memory state
9. **Install Hooks** - Installs pre-commit hooks
10. **Run Self-Checks** - Validates architecture and sandbox integrity
11. **Generate Report** - Creates initialization report
12. **Mark Initialized** - Creates `.initialized` marker file

## Before Initialization

1. **Customize MVP Specification** (Optional but Recommended):
   - Edit `0_phase0_bootstrap/MVP_SPECIFICATION.yaml`
   - Update `project_name`, `project_description`
   - Configure `tech_stack` for your needs
   - Prefer `PROJECT_LAYOUT` for Next.js / apps-packages / src-only layouts
   - Use `MONOREPO_LAYOUT` when you want directory scaffolding from a nested object model
   - Customize `ACTIVE_PLAN_TEMPLATE` for your initial plan

2. **Review Feature Flags**:
   - Check `0_phase0_bootstrap/feature_flags.yml`
   - Ensure `cursor_agent_mode: sandboxed`
   - Verify component settings match your tech stack

## After Initialization

1. **Review Generated Plan**:
   - Check `6_ai_runtime_context/ACTIVE_PLAN.yaml`
   - Modify tasks if needed

2. **Start Development**:
   - In Cursor, read `6_ai_runtime_context/AI_CONTEXT.md` first (auto-generated, always current)
   - Reference `0_phase0_bootstrap/AI_SANDBOX_RULES.md` for complete details
   - The AI agent will execute the plan autonomously
   - All commits must pass pre-commit hooks

3. **Keep Template Updated** (Optional but Recommended):
   - Check for template updates: `python3 3_bootstrap_scripts/cli.py update-template --dry-run`
   - Apply updates: `python3 3_bootstrap_scripts/cli.py update-template`
   - See `docs/TEMPLATE_VERSIONING_GUIDE.md` for detailed update workflow

   **Note:** `AI_CONTEXT.md` is automatically regenerated when state/flags change. Pre-commit hook ensures it's always current.

## Troubleshooting

### "Missing meta-framework files"
- Ensure `MVP_SPECIFICATION.yaml` exists in `0_phase0_bootstrap/`

### "Schema validation failed"
- Check that `MVP_SPECIFICATION.yaml` matches `7_schemas/mvp_specification.schema.json`
- Validate YAML syntax

### "Pre-commit not available"
- Install with: `pip install pre-commit` or `pipx install pre-commit`
- Then run: `pre-commit install`

### Re-initialization
- Remove `.initialized` file
- Run `cli.py init` again

## Manual Initialization

If you prefer to initialize manually, follow the steps in `expected_flow.md` sequentially.
