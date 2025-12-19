# Master Git Meta-Framework (L2.5 Single-Agent Sandbox)

## Use

### Initial Setup (One Time)

1. **Customize MVP Specification** (optional but recommended):
   - Edit `0_phase0_bootstrap/MVP_SPECIFICATION.yaml` with your project details

2. **Run initialization**:
   ```bash
   python3 3_bootstrap_scripts/cli.py init --guided
   ```

   Fully non-interactive (answers-file mode):
   ```bash
   python3 3_bootstrap_scripts/cli.py init --guided --answers 6_ai_runtime_context/INIT_WIZARD_ANSWERS.yaml
   ```

3. **Review generated plan**:
   - Check `6_ai_runtime_context/ACTIVE_PLAN.yaml`
   - Modify if needed

### Development Workflow

4. In Cursor, open `6_ai_runtime_context/AI_CONTEXT.md` first (auto-generated, always current), then run your plan
5. The agent commits autonomously when all hooks pass, then open a PR

**Dynamic Context:** `AI_CONTEXT.md` is automatically regenerated from source files (state, flags, rules) and stays current via pre-commit hooks.

**Template Versioning:** Projects can pull updates from the template repository to receive bug fixes and new features. See `docs/TEMPLATE_VERSIONING_GUIDE.md` for details.

**Feedback Loop:** Projects automatically send anonymized AI feedback to improve the template. See `docs/FEEDBACK_SYSTEM_USAGE.md` for details.

**Legacy Upgrade:** Upgrade existing projects (with no AI structure) to project_initializer format. See `docs/LEGACY_UPGRADE_GUIDE.md` for details. For AI agents, see `docs/LEGACY_UPGRADE_PROMPT.md` or `LEGACY_UPGRADE_START_HERE.md`.

**Pre-Versioned Upgrade:** Upgrade projects initialized before versioning was added. See `docs/TEMPLATE_VERSIONING_GUIDE.md` for details. For AI agents, see `docs/PRE_VERSIONED_UPGRADE_PROMPT.md` or `PRE_VERSIONED_UPGRADE_START_HERE.md`.

**Force Upgrade:** Automatically upgrade to latest template version. For AI agents, see `docs/FORCE_UPGRADE_PROMPT.md` or `FORCE_UPGRADE_START_HERE.md`.

**Version Tagging:** The template uses git tags for version tracking. See `docs/VERSION_TAGGING_GUIDE.md` for details on creating and managing version tags.

**Hub-and-Spoke Model:** project_initializer acts as the central hub, with child projects as spokes. See `docs/HUB_AND_SPOKE_MODEL.md` for the architecture. Child projects use standardized feedback reporting (`docs/STANDARDIZED_FEEDBACK_GUIDE.md`) and are compelled to pull updates automatically.

**GitHub Labels:** The feedback system requires specific GitHub labels. Run `python3 scripts/setup_github_labels.py` to create them, or use the GitHub Actions workflow.

See `INITIALIZATION_GUIDE.md` for detailed instructions.

## Multi-Component
- frontend/, backend/, shared/ with per-component routing and thresholds.
- Architecture boundaries enforced via `5_reference_architectures/LAYER_RULES.yaml`.

## Quality Gates
- Pre-commit: syntax, format, static/type, security, architecture, AI behavior, tests+coverage, docs, complexity, performance, commit schema.
- CI PR checks mirror and publish reports.

## Maturity
- Current: **L2.5** (Single-Agent Sandbox).
- Path to L3: flip flags in `feature_flags.yml` when ready (docs auto-updates, standards sync PRs, limited auto-refactors).
