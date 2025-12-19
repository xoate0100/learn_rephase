# Legacy Project Upgrade - AI Agent Instructions

## Overview

This document provides instructions and constraints for AI agents upgrading legacy projects to the project_initializer format. Follow these instructions precisely to ensure safe, idempotent, and non-breaking upgrades.

## Agent Constraints

### CRITICAL RULES (Never Violate)

1. **NEVER DELETE**: Do not delete any existing files or directories
2. **NEVER MODIFY**: Do not modify existing code files (only configuration)
3. **PRESERVE STRUCTURE**: Keep existing directory structure where possible
4. **INCREMENTAL**: Make changes incrementally, validate at each step
5. **ROLLBACK READY**: Every change must be reversible
6. **TEST PRESERVED**: Ensure all existing tests still pass
7. **DOCUMENT CHANGES**: Document all changes in upgrade log

### Safety Mechanisms

1. **Backup First**: Always create backup branch before starting
2. **Analysis Required**: Run analysis phase before planning
3. **Plan Review**: Review upgrade plan before execution
4. **Incremental Execution**: Execute in small, reversible steps
5. **Validation**: Validate after each major step

## Upgrade Workflow

### Phase 1: Analysis

```bash
python3 3_bootstrap_scripts/upgrade_legacy_project.py --analyze
```

**What it does:**
- Detects project framework and architecture
- Analyzes directory structure
- Identifies dependencies
- Detects edge cases
- Finds potential conflicts

**Output:** `6_ai_runtime_context/UPGRADE_ANALYSIS.yaml`

**Agent Actions:**
1. Run analysis command
2. Review analysis report
3. Note any edge cases or conflicts
4. Proceed to planning phase

### Phase 2: Planning

```bash
python3 3_bootstrap_scripts/upgrade_legacy_project.py --plan
```

**What it does:**
- Generates upgrade plan based on analysis
- Maps existing structure to template structure
- Identifies what to preserve
- Identifies what to create
- Plans edge case handling

**Output:** `6_ai_runtime_context/UPGRADE_PLAN.yaml`

**Agent Actions:**
1. Run planning command
2. Review upgrade plan carefully
3. Verify structure mappings are correct
4. Check preserved items list
5. Adjust plan if needed (edit YAML file)
6. Proceed to execution phase

### Phase 3: Execution

```bash
python3 3_bootstrap_scripts/upgrade_legacy_project.py --execute
```

**What it does:**
- Creates backup branch
- Executes upgrade plan step by step
- Creates meta-framework structure
- Generates MVP_SPECIFICATION.yaml
- Initializes version tracking
- Copies template files

**Agent Actions:**
1. Review plan one more time
2. Confirm execution (type "yes")
3. Monitor execution progress
4. Handle any errors immediately
5. Commit changes incrementally
6. Proceed to validation phase

### Phase 4: Validation

```bash
python3 3_bootstrap_scripts/upgrade_legacy_project.py --validate
```

**What it does:**
- Verifies meta-framework structure created
- Checks version tracking initialized
- Validates configuration files
- Ensures existing code preserved
- Runs tests if available

**Agent Actions:**
1. Run validation command
2. Review validation results
3. Fix any issues found
4. Re-run validation until all checks pass

## Structure Mapping Rules

### Next.js Projects

**App Router:**
- `app/` → Keep as-is (frontend root)
- `components/` → Keep as-is
- Create `frontend/` symlink or reference if needed

**Pages Router:**
- `pages/` → Keep as-is (frontend root)
- `components/` → Keep as-is
- Create `frontend/` symlink or reference if needed

### Standard Projects

**src/ structure:**
- `src/` → Map to `frontend/` or `backend/` based on content
- If contains React/UI code → `frontend/`
- If contains API/server code → `backend/`
- If mixed → Create both, split carefully

### Monorepo Projects

**apps/ and packages/:**
- `apps/` → Map to `apps/` (preserve structure)
- `packages/` → Map to `packages/` (preserve structure)
- Create `PROJECT_LAYOUT` with `adaptation.mode: adopt_existing`

### Python Projects

**Backend-only:**
- Root → `backend/`
- Preserve all Python files
- Keep `requirements.txt` or `pyproject.toml`

**Full-stack:**
- Frontend code → `frontend/`
- Backend code → `backend/`
- Shared code → `shared/`

## Edge Case Handling

### Edge Case: MONOREPO

**Detection:** `apps/` or `packages/` directories exist

**Handling:**
1. Preserve monorepo structure completely
2. Use `PROJECT_LAYOUT` with `adaptation.mode: adopt_existing`
3. Map each app/package individually
4. Don't force frontend/backend/shared structure

### Edge Case: MIXED_LANGUAGES

**Detection:** Both `package.json` and `requirements.txt` exist

**Handling:**
1. Create both `frontend/` and `backend/` components
2. Map Node.js code to `frontend/`
3. Map Python code to `backend/`
4. Configure both in `MVP_SPECIFICATION.yaml`

### Edge Case: EXISTING_CI

**Detection:** `.github/workflows/` or `.gitlab-ci.yml` exists

**Handling:**
1. Preserve all existing CI workflows
2. Add template CI workflows alongside (don't overwrite)
3. Merge configurations if compatible
4. Document in `MVP_SPECIFICATION.yaml`

### Edge Case: DATABASE_MIGRATIONS

**Detection:** Migration files (Alembic, Prisma, etc.)

**Handling:**
1. Preserve migration directory structure
2. Document migration system in `MVP_SPECIFICATION.yaml`
3. Don't move migration files
4. Keep migration commands in scripts

### Edge Case: ENV_CONFIGS

**Detection:** `.env*` files exist

**Handling:**
1. Preserve all `.env*` files
2. Document in `MVP_SPECIFICATION.yaml` → `ENVIRONMENT_AND_CONFIG`
3. Add to `.gitignore` if not already
4. Don't modify environment variable names

### Edge Case: EXISTING_DOCS

**Detection:** `docs/` directory exists

**Handling:**
1. Preserve `docs/` directory completely
2. Create `4_docs_index/` for meta-framework docs
3. Link existing docs in `DOCUMENTATION_INDEX.md`
4. Don't merge or reorganize existing docs

## Configuration Generation

### MVP_SPECIFICATION.yaml

Generate from analysis:

```yaml
Project: <detected-project-name>
Maturity: L2.5
Architecture: <detected-architecture>
Execution_Mode: Controlled Agentic Execution

GOALS_AND_PRINCIPLES:
  goals:
    - <preserve existing goals if documented>
  principles:
    - Test-driven development
    - Code quality through automation

TECH_STACK:
  frontend:
    framework: <detected-frontend-framework>
    language: <detected-language>
  backend:
    framework: <detected-backend-framework>
    language: <detected-language>

PROJECT_LAYOUT:
  adaptation:
    mode: adopt_existing  # Always use this for upgrades
    auto_apply: false
  components:
    frontend:
      directories: <mapped-frontend-directories>
    backend:
      directories: <mapped-backend-directories>
```

### feature_flags.yml

Copy from template, but:
- Preserve any existing component configurations
- Adjust `permissions.write_to` based on mapped structure
- Keep existing test/coverage thresholds if set

## Validation Checklist

After upgrade, verify:

- [ ] Meta-framework directories created
- [ ] `MVP_SPECIFICATION.yaml` generated and valid
- [ ] `META_FRAMEWORK_VERSION.yaml` initialized
- [ ] All existing code preserved (no deletions)
- [ ] All existing tests still pass
- [ ] Project still builds and runs
- [ ] Configuration files migrated correctly
- [ ] Edge cases handled appropriately
- [ ] Documentation updated
- [ ] Upgrade log created

## Rollback Procedure

If upgrade fails:

1. **Stop immediately**: Don't continue if errors occur
2. **Check backup branch**: `git branch` should show `backup-before-upgrade`
3. **Switch to backup**: `git checkout backup-before-upgrade`
4. **Review errors**: Check upgrade log for issues
5. **Fix issues**: Address problems in upgrade plan
6. **Retry**: Start from analysis phase again

## Commit Strategy

Commit incrementally:

1. **After backup**: Commit backup branch creation
2. **After structure**: Commit meta-framework directories
3. **After config**: Commit configuration files
4. **After template files**: Commit template files copy
5. **After validation**: Commit validation results

Each commit should have clear message:
```
upgrade: <phase> - <description>

Example:
upgrade: structure - Create meta-framework directories
upgrade: config - Generate MVP_SPECIFICATION.yaml from analysis
```

## Common Pitfalls

### ❌ DON'T

- Delete existing files to "clean up"
- Force structure into frontend/backend/shared if it doesn't fit
- Modify existing code to "fix" structure
- Overwrite existing CI/CD workflows
- Move files that are referenced by build system
- Change import paths without updating all references

### ✅ DO

- Preserve everything that exists
- Use `adopt_existing` mode for structure
- Add meta-framework alongside existing structure
- Document custom structures in MVP_SPECIFICATION.yaml
- Test after each major change
- Commit incrementally

## Success Criteria

Upgrade is successful when:

1. ✅ Meta-framework structure exists
2. ✅ Version tracking initialized
3. ✅ All existing code preserved
4. ✅ All tests pass
5. ✅ Project builds and runs
6. ✅ Configuration valid
7. ✅ Documentation updated

## Getting Help

If stuck:

1. Review `UPGRADE_ANALYSIS.yaml` for project details
2. Review `UPGRADE_PLAN.yaml` for planned changes
3. Check `LEGACY_UPGRADE_LOG.yaml` for execution log
4. Review edge case handling in this document
5. Consult template documentation

Remember: **When in doubt, preserve existing structure and document it.**

