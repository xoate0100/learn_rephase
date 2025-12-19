# Legacy Project Upgrade System - Design

## Overview

A comprehensive system to upgrade existing projects (with no AI structure) to the project_initializer format. Designed to be AI-agent friendly, robust, and handle edge cases across different architectures and frameworks.

## Goals

1. **Zero-Structure Detection**: Identify projects with no AI/meta-framework structure
2. **Architecture Agnostic**: Work with any framework (Next.js, React, Python, etc.)
3. **State Preservation**: Preserve existing code, dependencies, and functionality
4. **AI-Agent Friendly**: Clear instructions and constraints for AI agents
5. **Idempotent**: Safe to run multiple times
6. **Non-Breaking**: Never breaks existing functionality

## Upgrade Process Phases

### Phase 1: Discovery & Analysis
- Detect project structure
- Identify framework/architecture
- Analyze existing dependencies
- Map current structure to template structure
- Detect conflicts and edge cases

### Phase 2: Planning
- Generate upgrade plan
- Identify what needs to be created
- Identify what needs to be preserved
- Identify what needs to be migrated
- Create rollback strategy

### Phase 3: Execution
- Create meta-framework structure
- Migrate configuration
- Preserve project code
- Update dependencies if needed
- Initialize version tracking

### Phase 4: Validation
- Verify structure matches template
- Ensure functionality preserved
- Run tests if available
- Validate configuration

## Detection Strategy

### Indicators of Legacy Project

1. **Missing Meta-Framework Files**:
   - No `0_phase0_bootstrap/` directory
   - No `META_FRAMEWORK_VERSION.yaml`
   - No `feature_flags.yml`
   - No `AI_SANDBOX_RULES.md`

2. **Missing Structure**:
   - No `1_global_standards/`
   - No `3_bootstrap_scripts/`
   - No `7_schemas/`

3. **Project-Specific Indicators**:
   - Standard project structure (src/, app/, components/, etc.)
   - Framework-specific configs (package.json, requirements.txt, etc.)
   - Existing git repository

### Architecture Detection

Detect framework/architecture from:
- `package.json` (Node.js/TypeScript projects)
- `requirements.txt` or `pyproject.toml` (Python projects)
- `next.config.js` (Next.js)
- `vite.config.js` (Vite)
- `tsconfig.json` (TypeScript)
- Directory structure patterns

## Upgrade Strategy

### Conservative Approach

1. **Preserve Everything**: Never delete or modify existing code
2. **Add Structure**: Create meta-framework structure alongside existing code
3. **Migrate Gradually**: Move files only when safe
4. **Configuration First**: Set up configuration, then structure

### Structure Mapping

Map existing structure to template structure:

```
Existing Project          →  Template Structure
─────────────────────────────────────────────
src/                     →  frontend/ or backend/
app/                     →  frontend/ (Next.js)
components/              →  frontend/components/
lib/                     →  shared/ or backend/
tests/                   →  tests/ (preserved)
docs/                    →  docs/ (preserved, may add 4_docs_index/)
config/                  →  0_phase0_bootstrap/ (migrate configs)
```

## Edge Cases

### 1. Monorepo Structure
- **Detection**: Multiple package.json files, workspace configs
- **Strategy**: Map to `apps/` and `packages/` structure
- **Preserve**: Workspace configuration

### 2. Mixed Languages
- **Detection**: Both package.json and requirements.txt
- **Strategy**: Create both frontend/ and backend/ components
- **Preserve**: All dependencies

### 3. Custom Build Systems
- **Detection**: Non-standard build configs
- **Strategy**: Preserve build system, add meta-framework alongside
- **Document**: Custom build in MVP_SPECIFICATION.yaml

### 4. Existing CI/CD
- **Detection**: .github/workflows/ or .gitlab-ci.yml
- **Strategy**: Merge with template CI, preserve existing
- **Preserve**: All existing workflows

### 5. Database Migrations
- **Detection**: Migration files (Alembic, Prisma, etc.)
- **Strategy**: Preserve migration structure
- **Document**: In MVP_SPECIFICATION.yaml

### 6. Environment Configs
- **Detection**: .env files, config/ directories
- **Strategy**: Preserve, document in MVP_SPECIFICATION.yaml
- **Migrate**: To ENVIRONMENT_AND_CONFIG section if appropriate

### 7. Documentation Structure
- **Detection**: Existing docs/ directory
- **Strategy**: Preserve, add 4_docs_index/ for meta-framework docs
- **Integrate**: Link existing docs in DOCUMENTATION_INDEX.md

## AI Agent Instructions

### Upgrade Command

```bash
python3 3_bootstrap_scripts/upgrade_legacy_project.py --analyze
python3 3_bootstrap_scripts/upgrade_legacy_project.py --plan
python3 3_bootstrap_scripts/upgrade_legacy_project.py --execute
```

### Agent Constraints

1. **Never Delete**: Do not delete any existing files
2. **Preserve Structure**: Keep existing directory structure where possible
3. **Incremental**: Make changes incrementally, validate at each step
4. **Rollback Ready**: Every change must be reversible
5. **Test Preserved**: Ensure all existing tests still pass
6. **Document Changes**: Document all changes in upgrade log

### Agent Workflow

1. **Analyze**: Run analysis phase, review results
2. **Plan Review**: Review upgrade plan, adjust if needed
3. **Execute**: Run execution phase incrementally
4. **Validate**: Run validation after each major step
5. **Commit**: Commit changes incrementally with clear messages

## Implementation Plan

### Core Script: `upgrade_legacy_project.py`

**Phases**:
1. `--analyze`: Discover project structure, generate analysis report
2. `--plan`: Create upgrade plan based on analysis
3. `--execute`: Execute upgrade plan (with confirmation)
4. `--validate`: Validate upgrade success
5. `--rollback`: Rollback upgrade if needed

### Supporting Scripts

1. **Project Analyzer**: Detect framework, structure, dependencies
2. **Structure Mapper**: Map existing structure to template structure
3. **Config Migrator**: Migrate configuration files
4. **Validator**: Validate upgrade success

### AI Context Generator

Generate upgrade-specific AI context:
- Current project state
- Upgrade plan
- Constraints and rules
- Edge cases detected
- Rollback procedures

## Safety Mechanisms

### 1. Backup Strategy
- Create backup branch before upgrade
- Snapshot current state
- Store upgrade plan for rollback

### 2. Incremental Execution
- Execute in small, reversible steps
- Validate after each step
- Commit incrementally

### 3. Conflict Detection
- Detect file conflicts before execution
- Warn about potential issues
- Require confirmation for risky operations

### 4. Rollback Mechanism
- Store original state
- Track all changes
- Provide rollback script

## Success Criteria

Upgrade is successful when:
1. ✅ Meta-framework structure created
2. ✅ Version tracking initialized
3. ✅ All existing code preserved
4. ✅ All tests pass
5. ✅ Configuration migrated
6. ✅ Documentation updated
7. ✅ Project still functions

## Next Steps

1. Implement project analyzer
2. Create structure mapper
3. Build upgrade executor
4. Add validation system
5. Create AI agent instructions
6. Test on example projects

