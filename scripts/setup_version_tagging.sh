#!/bin/bash
# Setup Version Tagging
# Installs a post-commit hook to automatically create git tags when version is updated

HOOK_FILE=".git/hooks/post-commit"

if [ ! -d ".git" ]; then
    echo "ERROR: Not in a git repository"
    exit 1
fi

cat > "$HOOK_FILE" << 'EOF'
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
EOF

chmod +x "$HOOK_FILE"
echo "Post-commit hook installed: $HOOK_FILE"
echo "This hook will automatically create git tags when META_FRAMEWORK_VERSION.yaml is updated."

