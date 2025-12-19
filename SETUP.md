# Template Setup Guide

This is a Master Git Meta-Framework template repository. Use it to initialize new projects with AI-operable, stack-agnostic scaffolding.

## Quick Start

1. **Clone this repository** as your new project's starting point
   ```bash
   git clone <this-repo-url> <your-project-name>
   cd <your-project-name>
   ```

2. **Install pre-commit hooks**
   ```bash
   pipx install pre-commit || pip3 install pre-commit
   pre-commit install
   ```

3. **Set up your first plan**
   - Edit `6_ai_runtime_context/ACTIVE_PLAN.yaml` with your project goals
   - Configure component settings in `0_phase0_bootstrap/feature_flags.yml`

4. **Start developing**
   - In Cursor, read `0_phase0_bootstrap/AI_SANDBOX_RULES.md`
   - The AI agent will execute your plan autonomously within defined boundaries

## Directory Structure

- `0_phase0_bootstrap/` - AI execution rules and feature flags
- `1_global_standards/` - Code style, testing, security, Git, CI/CD standards
- `2_framework_templates/` - Templates for PRs, commits, issues, editor configs
- `3_bootstrap_scripts/` - Pre-commit validation scripts
- `4_docs_index/` - Documentation index and traceability
- `5_reference_architectures/` - Architecture layer rules
- `6_ai_runtime_context/` - Active plans, task tracking, memory state
- `7_schemas/` - JSON schemas for validation
- `8_ci/` - CI workflow definitions
- `frontend/`, `backend/`, `shared/` - Component directories (empty, ready for your code)

## Customization

- **Components**: Update `0_phase0_bootstrap/feature_flags.yml` to configure component languages and thresholds
- **Architecture**: Modify `5_reference_architectures/LAYER_RULES.yaml` to define your layer boundaries
- **Standards**: Adjust standards in `1_global_standards/` to match your team's preferences
- **CI**: Customize workflows in `8_ci/` for your deployment needs

## Maturity Level

This template is configured for **L2.5 (Single-Agent Sandbox)**:
- ✅ Cursor agent can execute plans autonomously
- ✅ All commits validated by pre-commit hooks
- ✅ Human review required for PRs
- ✅ Meta-framework can be updated during initialization/bootstrap as needed (template admin)
- ❌ No multi-agent orchestration

Upgrade path to L3 available via feature flags when ready.
