# Legacy Project Upgrade - AI Agent Prompt

## Instructions for AI Agent

You are tasked with upgrading a legacy project (with no AI/meta-framework structure) to the **project_initializer** format. This project provides a comprehensive meta-framework for AI-assisted development.

### Your Mission

Upgrade this project to use the project_initializer template format by:
1. Discovering the upgrade system in the project_initializer repository
2. Following the upgrade workflow autonomously
3. Preserving all existing functionality
4. Adding the meta-framework structure alongside existing code

### Reference Repository

**Repository**: https://github.com/xoate0100/project_initializer

**Key Files to Discover**:
- `3_bootstrap_scripts/upgrade_legacy_project.py` - Main upgrade script
- `docs/LEGACY_UPGRADE_GUIDE.md` - Complete upgrade guide
- `6_ai_runtime_context/LEGACY_UPGRADE_AI_INSTRUCTIONS.md` - AI agent instructions
- `docs/LEGACY_UPGRADE_EXAMPLE_PROJECTS.md` - Example project strategies

### Discovery Process

1. **Examine the Repository**:
   - Read the project_initializer repository structure
   - Locate the upgrade system documentation
   - Understand the upgrade workflow (analyze → plan → execute → validate)

2. **Review Upgrade Instructions**:
   - Read `6_ai_runtime_context/LEGACY_UPGRADE_AI_INSTRUCTIONS.md` for agent constraints
   - Review `docs/LEGACY_UPGRADE_GUIDE.md` for the complete workflow
   - Check `docs/LEGACY_UPGRADE_EXAMPLE_PROJECTS.md` for similar project strategies

3. **Understand the Template Structure**:
   - Review what the project_initializer format requires
   - Understand meta-framework directories (0_phase0_bootstrap/, 1_global_standards/, etc.)
   - Learn about MVP_SPECIFICATION.yaml and feature_flags.yml

### Upgrade Workflow

Follow these phases **autonomously**:

#### Phase 1: Analysis
```bash
python3 3_bootstrap_scripts/upgrade_legacy_project.py --analyze
```
- Analyzes project structure, framework, dependencies
- Detects edge cases
- Generates: `6_ai_runtime_context/UPGRADE_ANALYSIS.yaml`

**Your Actions**:
- Run the analysis command
- Review the analysis report
- Note any edge cases or conflicts

#### Phase 2: Planning
```bash
python3 3_bootstrap_scripts/upgrade_legacy_project.py --plan
```
- Generates upgrade plan based on analysis
- Maps existing structure to template structure
- Plans edge case handling
- Generates: `6_ai_runtime_context/UPGRADE_PLAN.yaml`

**Your Actions**:
- Run the planning command
- Review the upgrade plan carefully
- Verify structure mappings are correct
- Adjust plan if needed (edit YAML file)

#### Phase 3: Execution
```bash
python3 3_bootstrap_scripts/upgrade_legacy_project.py --execute --template-repo https://github.com/xoate0100/project_initializer.git
```
- Creates backup branch automatically
- Creates meta-framework directories
- Generates MVP_SPECIFICATION.yaml
- Initializes version tracking
- Copies template files

**Your Actions**:
- Review plan one more time
- Confirm execution (answer "yes" when prompted)
- Monitor execution progress
- Handle any errors immediately
- Commit changes incrementally

#### Phase 4: Validation
```bash
python3 3_bootstrap_scripts/upgrade_legacy_project.py --validate
```
- Verifies meta-framework structure
- Validates configuration files
- Ensures version tracking initialized

**Your Actions**:
- Run validation command
- Review validation results
- Fix any issues found
- Re-run validation until all checks pass

### Critical Constraints

**NEVER**:
- ❌ Delete any existing files or directories
- ❌ Modify existing code files
- ❌ Force structure into frontend/backend/shared if it doesn't fit
- ❌ Overwrite existing CI/CD workflows
- ❌ Move files referenced by build system
- ❌ Change import paths without updating all references

**ALWAYS**:
- ✅ Preserve everything that exists
- ✅ Use `adopt_existing` mode for structure
- ✅ Add meta-framework alongside existing structure
- ✅ Document custom structures in MVP_SPECIFICATION.yaml
- ✅ Test after each major change
- ✅ Commit incrementally

### Edge Cases to Handle

Based on the project_initializer documentation, handle these edge cases:

1. **Monorepo**: If `apps/` or `packages/` exist, preserve structure
2. **Mixed Languages**: If both Node.js and Python, create both frontend/ and backend/
3. **Next.js**: Preserve App Router or Pages Router structure
4. **CLI Tools**: Map to backend/ component
5. **Existing CI/CD**: Preserve workflows, add template CI alongside
6. **Database Migrations**: Preserve migration structure
7. **Environment Configs**: Preserve .env files, document in MVP_SPECIFICATION.yaml
8. **Documentation**: Preserve docs/, add 4_docs_index/ for meta-framework

### Safety Mechanisms

1. **Backup**: Backup branch created automatically (`backup-before-upgrade`)
2. **Rollback**: If upgrade fails, switch to backup: `git checkout backup-before-upgrade`
3. **Incremental**: Execute in small, reversible steps
4. **Validation**: Validate after each major step

### Success Criteria

Upgrade is successful when:
- ✅ Meta-framework structure exists
- ✅ MVP_SPECIFICATION.yaml generated and valid
- ✅ Version tracking initialized
- ✅ All existing code preserved
- ✅ All tests pass (if available)
- ✅ Project builds and runs
- ✅ Configuration valid

### Getting the Upgrade Script

If the upgrade script doesn't exist in this project:

1. **Clone or Reference**: Get the upgrade script from project_initializer repository
2. **Copy Script**: Copy `3_bootstrap_scripts/upgrade_legacy_project.py` to this project
3. **Install Dependencies**: Ensure PyYAML is installed (`pip install pyyaml`)
4. **Run Workflow**: Execute the upgrade workflow phases

### Template Files

To get template files (if needed):

1. **Clone Template**: Clone https://github.com/xoate0100/project_initializer.git
2. **Copy Files**: Copy meta-framework directories:
   - `0_phase0_bootstrap/` (except MVP_SPECIFICATION.yaml - will be generated)
   - `1_global_standards/`
   - `2_framework_templates/`
   - `3_bootstrap_scripts/` (including upgrade_legacy_project.py)
   - `5_reference_architectures/`
   - `7_schemas/`
   - `8_ci/`
3. **Or Use Execute**: The `--execute` phase can copy template files automatically if `--template-repo` is provided

### Post-Upgrade Steps

After successful upgrade:

1. **Review Changes**: `git diff backup-before-upgrade`
2. **Test Thoroughly**: Ensure everything works
3. **Run Initialization**: `python3 3_bootstrap_scripts/cli.py init`
4. **Update Documentation**: Document any customizations
5. **Commit Incrementally**: Commit changes in logical groups

### Autonomous Execution

You should:
- **Discover** the upgrade system from the project_initializer repository
- **Analyze** the current project structure
- **Plan** the upgrade based on analysis
- **Execute** the upgrade safely
- **Validate** the upgrade success
- **Test** that everything still works
- **Document** any customizations or issues

### Questions to Answer

Before starting, discover answers to:
1. What is the project_initializer format?
2. What are the upgrade phases?
3. What constraints must I follow?
4. How do I handle edge cases?
5. What is the rollback procedure?

### Start Here

1. **Examine project_initializer repository**: https://github.com/xoate0100/project_initializer
2. **Read upgrade documentation**: Find and read the upgrade guides
3. **Understand the workflow**: Analyze → Plan → Execute → Validate
4. **Begin upgrade**: Start with Phase 1 (Analysis)

---

**Remember**: Your goal is to add the meta-framework structure to this project while preserving all existing functionality. When in doubt, preserve existing structure and document it.

Good luck! 🚀

