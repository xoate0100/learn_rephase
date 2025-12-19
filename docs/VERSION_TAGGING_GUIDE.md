# Version Tagging Guide

## Overview

The project_initializer template uses **git tags** to mark version releases. Tags enable projects to:
- Check for available updates
- Reference specific template versions
- Track template evolution

## Version Detection Methods

The template update system uses **two methods** to detect the latest version (in order):

1. **GitHub API** (Primary) - Reads `META_FRAMEWORK_VERSION.yaml` from the repository
2. **Git Tags** (Fallback) - Parses git tags from the remote repository

### Why Both Methods?

- **GitHub API**: Works even if tags aren't created, always reflects the actual version in the manifest
- **Git Tags**: Works as a fallback if API is unavailable, and provides semantic versioning

## Creating Tags

### Automatic Tagging (Recommended)

After updating `META_FRAMEWORK_VERSION.yaml` and committing:

**Linux/macOS:**
```bash
# Setup automatic tagging (one-time)
bash scripts/setup_version_tagging.sh
```

**Windows (PowerShell):**
```powershell
# Setup automatic tagging (one-time)
.\scripts\setup_version_tagging.ps1
```

**Now, every commit that updates the version file will create a tag**

The post-commit hook will:
- Detect when `META_FRAMEWORK_VERSION.yaml` is updated
- Automatically create a git tag (e.g., `v1.3.0`)
- Remind you to push the tag

### Manual Tagging

If you prefer manual control:

```bash
# After updating version and committing
python3 scripts/create_version_tag.py

# Or manually
VERSION=$(python3 -c "import yaml; print(yaml.safe_load(open('0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml'))['template_version'])")
git tag -a "v$VERSION" -m "Template version $VERSION"
git push origin "v$VERSION"
```

## Tag Format

Tags follow semantic versioning with a `v` prefix:
- `v1.0.0` - Major version
- `v1.1.0` - Minor version (new features)
- `v1.1.1` - Patch version (bug fixes)

## Workflow

### When Updating the Template

1. **Update version** in `0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml`
2. **Commit changes** (pre-commit hook will verify version bump)
3. **Tag is created** automatically (if post-commit hook installed)
4. **Push commit and tag**:
   ```bash
   git push origin main
   git push origin $(git describe --tags --abbrev=0)  # Push latest tag
   ```

### Version Bump Reminder

The `check_version_bump.py` pre-commit hook will remind you to create a tag:

```
OK: Version bumped from 1.2.0 to 1.3.0

NOTE: After committing, create a git tag for this version:
  python3 scripts/create_version_tag.py
  Or manually: git tag -a v1.3.0 -m 'Template version 1.3.0' && git push origin v1.3.0
```

## Scripts

### `scripts/create_version_tag.py`

Creates and optionally pushes a git tag for the current version.

**Usage**:
```bash
# Create tag locally (don't push)
python3 scripts/create_version_tag.py --no-push

# Create and push tag
python3 scripts/create_version_tag.py
```

**Features**:
- Reads version from `META_FRAMEWORK_VERSION.yaml`
- Formats tag as `v{version}` (e.g., `v1.3.0`)
- Skips if tag already exists
- Creates annotated tag with message

### `scripts/setup_version_tagging.sh`

Installs a post-commit hook for automatic tagging.

**Usage**:
```bash
bash scripts/setup_version_tagging.sh
```

**What it does**:
- Creates `.git/hooks/post-commit`
- Hook detects version file changes
- Automatically creates tag (local only, doesn't push)

## Troubleshooting

### Tag Already Exists

If you try to create a tag that already exists:
```
Tag v1.3.0 already exists. Skipping tag creation.
```

**Solution**: Either:
- Use a new version number
- Delete the old tag: `git tag -d v1.3.0 && git push origin :refs/tags/v1.3.0`

### Tag Not Found by Update Scripts

If projects can't find the latest version:

1. **Check tag exists**: `git tag -l`
2. **Check tag pushed**: `git ls-remote --tags origin`
3. **Verify version manifest**: Check `META_FRAMEWORK_VERSION.yaml` in the repository

**Note**: The update scripts will fall back to reading from the GitHub API if tags aren't available.

### Post-Commit Hook Not Running

If automatic tagging isn't working:

1. **Check hook exists**: `ls -la .git/hooks/post-commit`
2. **Check hook is executable**: `chmod +x .git/hooks/post-commit`
3. **Run setup script**: `bash scripts/setup_version_tagging.sh`

## Best Practices

1. **Always tag after version bump** - Enables proper version detection
2. **Push tags immediately** - So projects can find the latest version
3. **Use semantic versioning** - Follow MAJOR.MINOR.PATCH format
4. **Tag message** - Include brief description of changes

## Integration with Update System

Projects using the template will:

1. **Check for updates** using `check_template_updates.py`
2. **Read version** from GitHub API (primary) or git tags (fallback)
3. **Compare versions** to determine if update is available
4. **Apply updates** using `template_update.py`

Both methods ensure projects can always find the latest version, even if tags aren't created.

---

**Summary**: Create git tags when updating the template version. Use automatic tagging (post-commit hook) or manual tagging. Tags enable version detection but aren't strictly required (GitHub API fallback exists).

