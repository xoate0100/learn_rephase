# Feedback System Usage Guide

## Overview

The feedback system enables projects to "phone home" with anonymized AI feedback, which is then aggregated and used to automatically improve the template. This creates a self-improving system where all projects benefit from lessons learned.

## Quick Start

### Enable Feedback Collection

Feedback collection is **enabled by default**. To disable:

```yaml
# 0_phase0_bootstrap/feature_flags.yml
feedback_collection:
  enabled: false
```

### Submit Feedback

```bash
# Preview what would be submitted
python3 3_bootstrap_scripts/cli.py submit-feedback --dry-run

# Submit feedback (requires GITHUB_TOKEN)
export GITHUB_TOKEN=your_token_here
python3 3_bootstrap_scripts/cli.py submit-feedback
```

## How It Works

### 1. Feedback Collection

Feedback is automatically logged throughout the meta-framework:

- **Guardrail Violations**: Logged when guardrails fail
- **Architecture Violations**: Logged when SOLID/layer rules are violated
- **Template Drift**: Logged when configuration drift is detected
- **AI Anomalies**: Logged when AI agents encounter issues
- **Schema Mismatches**: Logged when validation fails

All feedback is stored in `6_ai_runtime_context/ai_feedback_log.json`.

### 2. Feedback Submission

Projects submit feedback to the template repository via GitHub Issues API:

- Feedback is anonymized (project paths, names, etc. removed)
- Grouped by category and pattern
- Submitted as GitHub issues with `feedback` label

### 3. Feedback Processing

The template repository processes feedback:

- **Aggregation**: Groups similar issues by pattern
- **Pattern Detection**: Identifies recurring problems
- **Improvement Generation**: Creates improvement suggestions
- **PR Creation**: Auto-generates PRs for high-priority improvements

## Configuration

### Feature Flags

```yaml
feedback_collection:
  enabled: true                    # Enable/disable feedback collection
  frequency: "weekly"               # Collection frequency: daily, weekly, monthly, on_event
  include_anonymized_logs: true    # Include anonymized log entries
  auto_submit: false               # Auto-submit on events (future feature)
```

### GitHub Token

**Important**: Each project needs its own GitHub Personal Access Token. You cannot use the template owner's token.

Set `GITHUB_TOKEN` environment variable or use `--github-token`:

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

To create a token:
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with descriptive name: "Template Feedback - [Your Project]"
3. Select scope:
   - **Public template repos**: `public_repo` scope
   - **Private template repos**: `repo` scope
4. Set expiration (recommended: 90 days or 1 year)
5. Generate and copy token immediately
6. Store securely (environment variable, secrets manager)

**See `docs/FEEDBACK_AUTHENTICATION.md` for detailed authentication guide.**

**Note**: If no token is provided, feedback is logged locally but not submitted. This is graceful and doesn't break workflows.

## Manual Feedback Logging

You can manually log feedback using the feedback logger:

```python
from feedback_logger import log_feedback, log_guardrail_violation

# Log general feedback
log_feedback(
    issue="Common pattern detected",
    category="PATTERN_DETECTED",
    context="Additional context",
    files=["path/to/file"],
)

# Log guardrail violation
log_guardrail_violation(
    guardrail_name="enforce_task_scope",
    violation_details="Files outside task scope",
    files=["file1.py", "file2.ts"],
)
```

## Privacy & Security

### Anonymization

All feedback is automatically anonymized:

- Project paths → `[PROJECT_ROOT]/...`
- Repository URLs → `[TEMPLATE_REPO]`
- Sensitive data → `[REDACTED]`
- Project identifiers → Hashed (for pattern tracking only)

### What's Sent

- **Included**: Issue descriptions, categories, patterns, file paths (anonymized)
- **Excluded**: Project names, repository URLs, sensitive data, code content

### Opt-Out

To disable feedback collection:

```yaml
# 0_phase0_bootstrap/feature_flags.yml
feedback_collection:
  enabled: false
```

## Feedback Categories

1. **GUARDRAIL_VIOLATION** - Guardrail enforcement failures
2. **ARCHITECTURE_VIOLATION** - SOLID/layer boundary issues
3. **TEMPLATE_DRIFT** - Configuration drift detected
4. **UPDATE_ISSUE** - Template update problems
5. **AI_ANOMALY** - AI agent failures/confusion
6. **SCHEMA_MISMATCH** - Schema validation issues
7. **PERFORMANCE_ISSUE** - Performance regressions
8. **DOCUMENTATION_GAP** - Missing or unclear docs
9. **FEATURE_REQUEST** - Suggested improvements
10. **PATTERN_DETECTED** - Common patterns across projects

## Integration Points

### Pre-Commit Hooks

Feedback is automatically logged when:
- Guardrails fail (`guardrail_enforcement.py`)
- Architecture checks fail (`architecture_check.py`)
- Schema validation fails (`schema_enforcement.py`)

### Template Updates

After template updates, feedback is logged for:
- Update success/failure
- Migration issues
- Version compatibility problems

### AI Context Generation

During AI context generation, feedback is logged for:
- Missing context
- Unclear rules
- Configuration drift

## Best Practices

1. **Regular Submission**: Submit feedback weekly or after significant issues
2. **Review Before Submit**: Use `--dry-run` to preview feedback
3. **Token Security**: Store GitHub token securely (use environment variables)
4. **Feedback Quality**: Ensure feedback is actionable and specific

## Troubleshooting

### "No GitHub token provided"

Set `GITHUB_TOKEN` environment variable or use `--github-token` argument.

### "Feedback collection is disabled"

Enable in `feature_flags.yml`:
```yaml
feedback_collection:
  enabled: true
```

### "No feedback entries found"

Feedback is only collected when issues occur. If no guardrail violations or anomalies occur, there's no feedback to submit.

### "Failed to create issue"

Check:
- GitHub token has correct permissions
- Template repository URL is correct
- Network connectivity

## Future Enhancements

- Real-time feedback dashboard
- Feedback analytics and metrics
- ML-based pattern detection
- Automated A/B testing of improvements
- Feedback prioritization (impact scoring)
- Webhook endpoint (alternative to GitHub Issues)

