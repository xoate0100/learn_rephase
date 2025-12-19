# Legacy Project Upgrade Guide

## Overview

This guide explains how to upgrade existing projects (with no AI structure) to the project_initializer format. The upgrade process is designed to be safe, idempotent, and preserve all existing functionality.

## Quick Start

### For AI Agents

1. **Analyze Project**:
   ```bash
   python3 3_bootstrap_scripts/cli.py upgrade-legacy --analyze
   ```

2. **Review Analysis**:
   - Check `6_ai_runtime_context/UPGRADE_ANALYSIS.yaml`
   - Note edge cases and conflicts

3. **Generate Plan**:
   ```bash
   python3 3_bootstrap_scripts/cli.py upgrade-legacy --plan
   ```

4. **Review Plan**:
   - Check `6_ai_runtime_context/UPGRADE_PLAN.yaml`
   - Verify structure mappings
   - Adjust if needed

5. **Execute Upgrade**:
   ```bash
   python3 3_bootstrap_scripts/cli.py upgrade-legacy --execute --template-repo https://github.com/xoate0100/project_initializer.git
   ```

6. **Validate**:
   ```bash
   python3 3_bootstrap_scripts/cli.py upgrade-legacy --validate
   ```

### For Humans

Follow the same steps, but review each phase carefully before proceeding.

## Upgrade Phases

### Phase 1: Analysis

**Command**: `--analyze`

**What it does**:
- Detects project framework (Next.js, React, Python, etc.)
- Analyzes directory structure
- Identifies dependencies
- Detects edge cases (monorepo, mixed languages, etc.)
- Finds potential conflicts

**Output**: `6_ai_runtime_context/UPGRADE_ANALYSIS.yaml`

**Review**:
- Check framework detection is correct
- Verify structure analysis
- Note any edge cases
- Check for conflicts

### Phase 2: Planning

**Command**: `--plan`

**What it does**:
- Generates upgrade plan based on analysis
- Maps existing structure to template structure
- Identifies what to preserve
- Plans edge case handling

**Output**: `6_ai_runtime_context/UPGRADE_PLAN.yaml`

**Review**:
- Verify structure mappings are correct
- Check preserved items list
- Review edge case handling
- Adjust plan if needed (edit YAML)

### Phase 3: Execution

**Command**: `--execute --template-repo <url>`

**What it does**:
- Creates backup branch
- Creates meta-framework directories
- Generates `MVP_SPECIFICATION.yaml`
- Initializes version tracking
- Copies template files (if repo provided)
- Handles edge cases

**Safety**:
- Backup branch created first
- No existing files deleted
- No existing code modified
- Incremental execution

**After execution**:
1. Review changes: `git status`
2. Test project: Ensure it builds and runs
3. Validate: Run `--validate`
4. Commit incrementally

### Phase 4: Validation

**Command**: `--validate`

**What it does**:
- Verifies meta-framework structure
- Checks version tracking
- Validates configuration
- Ensures code preserved

**Fix issues**:
- Review validation errors
- Fix configuration if needed
- Re-run validation

## Example Projects Analysis

### google-form-generator-cli

**Expected Structure**:
- CLI tool (likely Node.js or Python)
- May have `src/` or root-level files
- Package.json or requirements.txt

**Upgrade Strategy**:
- Map to `backend/` if Python CLI
- Map to appropriate structure if Node.js
- Preserve CLI entry point
- Document in MVP_SPECIFICATION.yaml

### crypto-trading-bot

**Expected Structure**:
- Trading bot (likely Python)
- May have trading logic, API clients
- Configuration files

**Upgrade Strategy**:
- Map to `backend/`
- Preserve trading logic
- Preserve configuration
- Document trading-specific structure

### CutRatesLMS

**Expected Structure**:
- LMS system (likely full-stack)
- May have frontend and backend
- Database migrations

**Upgrade Strategy**:
- Map frontend to `frontend/`
- Map backend to `backend/`
- Preserve migrations
- Handle edge case: DATABASE_MIGRATIONS

### AutoBlogAssist

**Expected Structure**:
- Blog automation tool
- May have multiple components
- API integrations

**Upgrade Strategy**:
- Analyze structure first
- Map based on detected framework
- Preserve all integrations
- Document custom structure

## Edge Cases

### Monorepo

**Detection**: `apps/` or `packages/` directories

**Handling**:
- Use `PROJECT_LAYOUT` with `adaptation.mode: adopt_existing`
- Map each app/package individually
- Don't force frontend/backend/shared structure
- Preserve workspace configuration

### Mixed Languages

**Detection**: Both `package.json` and `requirements.txt`

**Handling**:
- Create both `frontend/` and `backend/` components
- Map Node.js code to `frontend/`
- Map Python code to `backend/`
- Configure both in MVP_SPECIFICATION.yaml

### Existing CI/CD

**Detection**: `.github/workflows/` or `.gitlab-ci.yml`

**Handling**:
- Preserve all existing workflows
- Add template CI alongside (don't overwrite)
- Merge configurations if compatible
- Document in MVP_SPECIFICATION.yaml

### Database Migrations

**Detection**: Migration files (Alembic, Prisma, etc.)

**Handling**:
- Preserve migration directory structure
- Document in MVP_SPECIFICATION.yaml
- Don't move migration files
- Keep migration commands

### Custom Build Systems

**Detection**: Makefile, custom scripts

**Handling**:
- Preserve build system
- Document in MVP_SPECIFICATION.yaml
- Add meta-framework alongside
- Don't modify build process

## Safety Mechanisms

### Backup

- Backup branch created automatically: `backup-before-upgrade`
- Switch back: `git checkout backup-before-upgrade`
- All changes reversible

### Preservation

- **Never deletes**: Existing files preserved
- **Never modifies**: Existing code unchanged
- **Adds only**: Meta-framework added alongside

### Validation

- Structure validation
- Configuration validation
- Test execution (if available)
- Build verification

## Troubleshooting

### "Analysis failed"

**Causes**:
- Project structure too unusual
- Missing dependencies

**Solutions**:
- Review error messages
- Manually adjust analysis if needed
- Proceed with custom plan

### "Plan generation failed"

**Causes**:
- Analysis incomplete
- Edge cases not handled

**Solutions**:
- Review analysis file
- Manually edit plan YAML
- Add custom handling

### "Execution failed"

**Causes**:
- File conflicts
- Permission issues
- Network issues (template copy)

**Solutions**:
- Check error messages
- Resolve conflicts manually
- Rollback if needed: `git checkout backup-before-upgrade`

### "Validation failed"

**Causes**:
- Missing required files
- Invalid configuration
- Structure mismatch

**Solutions**:
- Review validation errors
- Fix configuration
- Re-run validation

## Rollback

If upgrade fails:

1. **Stop immediately**: Don't continue
2. **Switch to backup**: `git checkout backup-before-upgrade`
3. **Review errors**: Check upgrade log
4. **Fix issues**: Address problems
5. **Retry**: Start from analysis phase

## Post-Upgrade

After successful upgrade:

1. **Review changes**: `git diff backup-before-upgrade`
2. **Test thoroughly**: Ensure everything works
3. **Update documentation**: Document any customizations
4. **Commit incrementally**: Commit changes in logical groups
5. **Run initialization**: `python3 3_bootstrap_scripts/cli.py init`

## Best Practices

1. **Analyze first**: Always run analysis before planning
2. **Review plans**: Don't execute without reviewing plan
3. **Test after**: Validate after each major step
4. **Commit incrementally**: Don't commit everything at once
5. **Document customizations**: Note any manual adjustments

## AI Agent Instructions

See `6_ai_runtime_context/LEGACY_UPGRADE_AI_INSTRUCTIONS.md` for detailed AI agent instructions and constraints.

## Summary

The legacy upgrade system provides:
- ✅ Safe upgrade process
- ✅ Automatic analysis and planning
- ✅ Edge case handling
- ✅ Rollback capability
- ✅ AI-agent friendly
- ✅ Comprehensive documentation

Follow the phases, review carefully, and test thoroughly for best results.

