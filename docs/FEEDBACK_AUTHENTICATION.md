# Feedback System Authentication Guide

## Overview

The feedback system requires GitHub authentication to submit feedback as issues to the template repository. This guide explains authentication requirements and best practices.

## Authentication Requirements

### Token Requirements

Each project initialized from the template needs its own GitHub Personal Access Token to submit feedback.

**Required Scopes:**
- **Public Repos**: `public_repo` scope
- **Private Repos**: `repo` scope

**Permissions Needed:**
- Create issues in the template repository
- Read repository metadata

### Why Each Project Needs Its Own Token

1. **Security**: Sharing tokens is a security risk
2. **Accountability**: Each project's feedback is traceable to its owner
3. **Rate Limits**: Tokens have individual rate limits
4. **Revocation**: Tokens can be revoked independently

## Creating a GitHub Token

### Step 1: Generate Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name: "Template Feedback - [Project Name]"
4. Select expiration (recommended: 90 days or 1 year)
5. Select scopes:
   - For **public template repos**: Check `public_repo`
   - For **private template repos**: Check `repo`
6. Click "Generate token"
7. **Copy the token immediately** (you won't see it again!)

### Step 2: Store Token Securely

**Option A: Environment Variable (Recommended)**
```bash
# Linux/Mac
export GITHUB_TOKEN=ghp_your_token_here

# Windows (PowerShell)
$env:GITHUB_TOKEN="ghp_your_token_here"

# Windows (CMD)
set GITHUB_TOKEN=ghp_your_token_here
```

**Option B: Use CLI Argument**
```bash
python3 3_bootstrap_scripts/cli.py submit-feedback --github-token ghp_your_token_here
```

**Option C: GitHub Secrets (for CI/CD)**
If running in CI/CD, store token as a secret:
- GitHub Actions: Repository secrets
- GitLab CI: CI/CD variables
- Other: Use your platform's secret management

### Step 3: Verify Token Works

```bash
# Test with dry-run first
python3 3_bootstrap_scripts/cli.py submit-feedback --dry-run

# Then submit (if token is set)
python3 3_bootstrap_scripts/cli.py submit-feedback
```

## Common Authentication Issues

### Issue: "Authentication failed" (401)

**Causes:**
- Token expired
- Token invalid
- Token revoked

**Solutions:**
1. Generate a new token
2. Verify token is copied correctly (no extra spaces)
3. Check token hasn't expired

### Issue: "Permission denied" (403)

**Causes:**
- Token doesn't have required scope
- Token doesn't have access to repository
- Repository is private and token only has `public_repo` scope

**Solutions:**
1. For private repos: Use `repo` scope (not `public_repo`)
2. For public repos: Use `public_repo` scope
3. Verify token has access to the template repository

### Issue: "Repository not found" (404)

**Causes:**
- Template repository URL incorrect
- Repository doesn't exist
- Repository is private and token doesn't have access

**Solutions:**
1. Verify template repository URL in `META_FRAMEWORK_VERSION.yaml`
2. Check repository exists and is accessible
3. For private repos: Ensure token has `repo` scope

### Issue: "Network error"

**Causes:**
- No internet connectivity
- GitHub API is down
- Firewall blocking requests

**Solutions:**
1. Check internet connectivity
2. Verify GitHub status: https://www.githubstatus.com/
3. Check firewall/proxy settings

## Security Best Practices

### ✅ DO

- **Use environment variables** for tokens (not hardcoded)
- **Use minimal scopes** (`public_repo` for public repos)
- **Set token expiration** (90 days recommended)
- **Revoke unused tokens** regularly
- **Use different tokens** for different projects
- **Store tokens securely** (use secret management tools)

### ❌ DON'T

- **Don't commit tokens** to git repositories
- **Don't share tokens** between projects
- **Don't use overly broad scopes** (like `repo` for public repos)
- **Don't hardcode tokens** in scripts
- **Don't log tokens** in output or logs

## Alternative Approaches

### Option 1: GitHub App (Future Enhancement)

A GitHub App could be created that projects install, providing:
- Better security (scoped permissions)
- No token management per project
- Centralized authentication

**Status**: Not yet implemented, but planned for future

### Option 2: Webhook Endpoint

Instead of GitHub Issues API, projects could POST to a webhook:
- No GitHub token needed
- Requires webhook infrastructure
- More control over processing

**Status**: Not yet implemented, but can be added

### Option 3: Email/Form Submission

Projects could submit feedback via email or form:
- No authentication needed
- Requires processing infrastructure
- Less automated

**Status**: Not yet implemented

### Option 4: Optional Feedback (Current)

Feedback collection is **opt-in** and **graceful**:
- If no token: Feedback is logged locally but not submitted
- Projects can disable: `feedback_collection.enabled: false`
- No blocking: Missing token doesn't break workflows

## Token Lifecycle

1. **Create**: Generate token with appropriate scope
2. **Store**: Save securely (environment variable, secrets manager)
3. **Use**: Submit feedback periodically
4. **Rotate**: Regenerate token before expiration
5. **Revoke**: Delete token when no longer needed

## FAQ

### Q: Can I use the template owner's token?

**A:** No. Each project should have its own token for security and accountability.

### Q: What if I don't want to submit feedback?

**A:** You can disable feedback collection:
```yaml
# feature_flags.yml
feedback_collection:
  enabled: false
```

### Q: Can I submit feedback without a token?

**A:** No, but feedback is still logged locally. You can review it in `6_ai_runtime_context/ai_feedback_log.json`.

### Q: What happens if my token expires?

**A:** Feedback submission will fail with authentication error. Generate a new token and update `GITHUB_TOKEN`.

### Q: Is feedback submission required?

**A:** No, it's completely optional. The template works fine without feedback submission.

## Troubleshooting

### Check Token Permissions

```bash
# Test token with GitHub API
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
```

### Verify Repository Access

```bash
# Check if token can access repository
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/OWNER/REPO
```

### Test Issue Creation

```bash
# Test creating an issue (will create a test issue)
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/OWNER/REPO/issues \
  -d '{"title":"Test Issue","body":"This is a test"}'
```

## Summary

- Each project needs its own GitHub token
- Token needs `public_repo` (public) or `repo` (private) scope
- Store tokens securely (environment variables, secrets)
- Feedback submission is optional and graceful
- Alternative approaches (GitHub App, webhook) can be implemented

