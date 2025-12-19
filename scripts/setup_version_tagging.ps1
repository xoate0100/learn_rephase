# Setup Version Tagging (PowerShell)
# Installs a post-commit hook to automatically create git tags when version is updated

$HookFile = ".git\hooks\post-commit"

if (-not (Test-Path ".git")) {
    Write-Host "ERROR: Not in a git repository" -ForegroundColor Red
    exit 1
}

$HookContent = @'
#!/bin/bash
# Post-commit hook: Create version tag if version was updated
# This hook runs after a successful commit

# Check if META_FRAMEWORK_VERSION.yaml was changed in this commit
if git diff-tree --no-commit-id --name-only -r HEAD | grep -q "0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml"; then
    # Version file was changed, check if we should create a tag
    if [ -f "scripts/create_version_tag.py" ]; then
        # Run tag creation script (non-blocking, don't fail commit if tag fails)
        python3 scripts/create_version_tag.py --no-push 2>/dev/null || true
        echo ""
        echo "NOTE: Version updated. To push the tag, run:"
        echo "  git push origin \$(git describe --tags --abbrev=0)"
    fi
fi
'@

# Create hooks directory if it doesn't exist
$HooksDir = ".git\hooks"
if (-not (Test-Path $HooksDir)) {
    New-Item -ItemType Directory -Path $HooksDir -Force | Out-Null
}

# Write hook file
Set-Content -Path $HookFile -Value $HookContent -Encoding UTF8

# Make executable (if on Unix-like system, this will work; on Windows, git handles it)
if ($IsLinux -or $IsMacOS) {
    chmod +x $HookFile
}

Write-Host "Post-commit hook installed: $HookFile" -ForegroundColor Green
Write-Host "This hook will automatically create git tags when META_FRAMEWORK_VERSION.yaml is updated." -ForegroundColor Green

