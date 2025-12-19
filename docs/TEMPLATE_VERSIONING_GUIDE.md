# Template Versioning and Update System

## Overview

The template versioning system enables projects initialized from this template to receive updates, bug fixes, and new features from the template repository. This ensures all projects benefit from "lessons learned" and improvements made to the meta-framework.

## Key Features

- **Version Tracking**: Each project tracks its template version in `0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml`
- **Safe Updates**: Protected files (like `MVP_SPECIFICATION.yaml`) are never overwritten
- **Migration System**: Automatic migrations handle breaking changes between versions
- **AI-Assisted**: Pre-versioned projects can be migrated with AI assistance
- **Dry Run**: Preview updates before applying them

## Version Manifest

The version manifest (`META_FRAMEWORK_VERSION.yaml`) tracks:

- Current template version
- Template repository URL
- Installation and update timestamps
- Update history
- Available features
- Protected files and directories

### Example Version Manifest

```yaml
template_version: "1.0.0"
template_repo: "https://github.com/xoate0100/project_initializer.git"
installed_at: "2024-01-15T10:30:00Z"
last_updated_at: null

update_history: []

features:
  dynamic_layout_adaptation: true
  guided_initialization: true
  dynamic_ai_context: true
  template_versioning: true
  drift_detection: true

template_directories:
  - "0_phase0_bootstrap/"
  - "1_global_standards/"
  - "2_framework_templates/"
  - "3_bootstrap_scripts/"
  - "5_reference_architectures/"
  - "7_schemas/"
  - "8_ci/"

protected_files:
  - "0_phase0_bootstrap/MVP_SPECIFICATION.yaml"
  - "0_phase0_bootstrap/feature_flags.yml"

project_directories:
  - "4_docs_index/"
  - "6_ai_runtime_context/"
  - "frontend/"
  - "backend/"
  - "shared/"
```

## Usage

### Checking for Updates

```bash
python3 3_bootstrap_scripts/cli.py update-template --dry-run
```

This shows what would be updated without making changes.

### Updating to Latest Version

```bash
python3 3_bootstrap_scripts/cli.py update-template
```

### Updating to Specific Version

```bash
python3 3_bootstrap_scripts/cli.py update-template --version 1.2.0
```

### Initializing Versioning for Pre-Versioned Projects

If your project was created before versioning was added:

```bash
python3 3_bootstrap_scripts/cli.py update-template --init-versioning --template-repo <your-template-repo-url>
```

The system will:
1. Detect your template source (or prompt for it)
2. Create a version manifest
3. Detect available features
4. Initialize update tracking

## Update Process

When you run `update-template`, the system:

1. **Checks Current Version**: Reads `META_FRAMEWORK_VERSION.yaml`
2. **Fetches Latest**: Queries template repository for available versions
3. **Clones Template**: Temporarily clones the template repository
4. **Copies Files**: Updates template directories while respecting protected files
5. **Applies Migrations**: Runs migration scripts for version transitions
6. **Updates Manifest**: Records the update in version history

### Protected Files

These files are **never overwritten** during updates:

- `0_phase0_bootstrap/MVP_SPECIFICATION.yaml` - Project-specific configuration
- `0_phase0_bootstrap/feature_flags.yml` - May have project customizations
- All files in `project_directories` (frontend/, backend/, shared/, etc.)

### Template Directories

These directories are updated from the template:

- `0_phase0_bootstrap/` (except protected files)
- `1_global_standards/`
- `2_framework_templates/`
- `3_bootstrap_scripts/`
- `5_reference_architectures/`
- `7_schemas/`
- `8_ci/`

## Migration System

Migrations handle breaking changes and feature additions between versions. They are defined in `3_bootstrap_scripts/migrations/`.

### Example Migration

```python
# migrations/migration_1_2_0.py
def migrate_to_1_2_0(project_root: pathlib.Path) -> Tuple[bool, str]:
    """Migrate to version 1.2.0: New feature flags schema"""
    # Update feature flags if needed
    # Transform deprecated configurations
    # Add new required files
    return True, "Updated feature flags schema"
```

Migrations are automatically applied when updating between versions that require them.

## Best Practices

### Before Updating

1. **Commit Your Changes**: Ensure all work is committed
2. **Review Protected Files**: Check if you've customized any template files
3. **Backup**: Consider creating a branch before major updates
4. **Dry Run**: Always run `--dry-run` first to preview changes

### After Updating

1. **Review Changes**: Check what files were updated
2. **Test**: Run validation and tests
3. **Check Migrations**: Review migration notes for breaking changes
4. **Update Documentation**: Document any manual steps required

### Handling Conflicts

If you've customized a template file that gets updated:

1. The update will skip protected files automatically
2. Review the new version in the template repository
3. Manually merge changes if needed
4. Consider contributing improvements back to the template

## AI-Assisted Migration

For projects created before versioning existed, the system provides AI-assisted migration:

1. Detects missing version manifest
2. Analyzes project structure
3. Detects available features
4. Initializes version tracking
5. Provides migration path to current version

This ensures all projects can benefit from template improvements, regardless of when they were created.

## Versioning Strategy

The template uses [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes (require migrations)
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Version Tags

The template repository uses Git tags for versions:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Projects can update to specific versions or always pull the latest.

## Troubleshooting

### "Template repository URL required"

Set the template repo in your version manifest or use `--template-repo`:

```bash
python3 3_bootstrap_scripts/cli.py update-template --template-repo https://github.com/your-org/template.git
```

### "Already at latest version"

Your project is up to date. Use `--force` to re-apply updates:

```bash
python3 3_bootstrap_scripts/cli.py update-template --force
```

### "Failed to clone template"

Check network connectivity and repository access. The update system needs read access to the template repository.

### Migration Failures

If a migration fails:

1. Check migration notes for details
2. Review the migration script in `3_bootstrap_scripts/migrations/`
3. Manually apply required changes
4. Report issues to the template maintainers

## Contributing Improvements

When you improve the meta-framework:

1. Update the template version in `META_FRAMEWORK_VERSION.yaml`
2. Create migration scripts if breaking changes are introduced
3. Document changes in migration notes
4. Tag the release in the template repository
5. Projects can then pull the updates

This creates a virtuous cycle where improvements benefit all projects using the template.

