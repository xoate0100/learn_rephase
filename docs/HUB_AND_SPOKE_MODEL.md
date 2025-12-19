# Hub-and-Spoke Model: project_initializer as Central Hub

## Overview

The `project_initializer` template implements a **hub-and-spoke architecture** where:

- **Hub**: `project_initializer` repository (upstream template)
- **Spokes**: Child projects initialized from the template (downstream projects)

This model enables:
1. **Centralized Maintenance**: Template improvements benefit all child projects
2. **Standardized Feedback**: Child projects report issues/patterns to the hub
3. **Automated Updates**: Child projects automatically pull improvements
4. **Continuous Improvement**: Feedback loop drives template evolution

## Architecture

```
┌─────────────────────────────────────┐
│   project_initializer (Hub)         │
│   - Template files                  │
│   - Meta-framework                  │
│   - Version tracking                │
│   - Feedback processing             │
└──────────────┬──────────────────────┘
               │
               │ (initializes)
               │
    ┌──────────┴──────────┐
    │                      │
┌───▼────┐          ┌──────▼───┐
│ Child  │          │  Child  │
│Project │          │ Project │
│   A    │          │    B    │
└───┬────┘          └────┬─────┘
    │                    │
    │ (feedback)         │ (feedback)
    │                    │
    └──────────┬──────────┘
               │
               │ (submits issues)
               │
    ┌──────────▼──────────┐
    │   Hub Processes      │
    │   - Aggregates       │
    │   - Generates PRs    │
    │   - Releases updates │
    └──────────────────────┘
```

## Standardized Feedback Reporting

### Pre-Configured Module

Every child project inherits `3_bootstrap_scripts/standardized_feedback.py` which provides:

1. **Templated Issue Formats**: Standardized templates for common error types
2. **Automatic Categorization**: Feedback automatically categorized
3. **Anonymization**: Project-specific data anonymized before submission
4. **Easy Integration**: Simple function calls throughout codebase

### Feedback Types

The standardized feedback module supports:

- `GUARDRAIL_VIOLATION` - Guardrail enforcement failures
- `ARCHITECTURE_VIOLATION` - SOLID/layer boundary violations
- `TEMPLATE_DRIFT` - Configuration mismatches
- `UPDATE_ISSUE` - Template update problems
- `PERFORMANCE_ISSUE` - Performance degradation
- `SCHEMA_MISMATCH` - Schema validation failures
- `DOCUMENTATION_GAP` - Missing documentation
- `OPERATIONAL_ERROR` - Runtime errors

### Usage in Child Projects

```python
from standardized_feedback import (
    report_guardrail_violation,
    report_architecture_violation,
    report_performance_issue,
    auto_report_from_exception,
)

# Report guardrail violation
report_guardrail_violation(
    guardrail_name="enforce_task_scope",
    component="frontend",
    files=["src/components/Button.tsx"],
    details="File modified outside active task scope",
)

# Report performance issue
report_performance_issue(
    metric="build_time",
    component="backend",
    threshold="30s",
    actual="45s",
    recommendation="Optimize dependency resolution",
)

# Auto-report exceptions
try:
    risky_operation()
except Exception as e:
    auto_report_from_exception(e, component="shared")
```

### Automatic Submission

Feedback is automatically collected and submitted via:

1. **Pre-commit hooks**: Guardrails log violations automatically
2. **Validation scripts**: Schema/architecture checks log issues
3. **Update process**: Template updates log problems
4. **Manual submission**: `python3 3_bootstrap_scripts/cli.py submit-feedback`

## Automated Downstream Updates

### Update Enforcement

Child projects are **compelled** to check for and apply updates through:

1. **Pre-commit Hook**: Checks for updates on every commit
2. **Feature Flags**: Configurable update behavior
3. **Version Tracking**: Tracks current template version
4. **Automatic Updates**: Optional auto-update mode

### Update Configuration

In `feature_flags.yml`:

```yaml
template_updates:
  check_on_commit: true      # Check for updates on every commit
  auto_update: false         # Auto-apply updates (optional)
  check_frequency: "on_commit"  # on_commit, daily, weekly, manual
  warn_only: true            # Warn but don't block commits
```

### Update Workflow

1. **Check**: Pre-commit hook checks for new template version
2. **Notify**: Warns if update available (or blocks if `warn_only: false`)
3. **Update**: Child project runs `update-template` command
4. **Validate**: Post-update validation ensures compatibility
5. **Report**: Any update issues automatically reported to hub

### Compelling Updates

Updates are made compelling through:

- **Security Fixes**: Critical security patches highlighted
- **Performance**: Performance improvements emphasized
- **New Features**: Feature additions clearly documented
- **Bug Fixes**: Bug fixes aggregated and prioritized
- **Breaking Changes**: Major updates require explicit confirmation

## Feedback Loop

### Collection

1. **Child projects** log feedback using standardized templates
2. **Feedback aggregated** locally in `ai_feedback_log.json`
3. **Periodic submission** to hub (weekly by default, configurable)

### Processing (Hub)

1. **GitHub Issues**: Feedback submitted as structured GitHub issues
2. **Aggregation**: Similar issues grouped and analyzed
3. **Pattern Detection**: Recurring patterns identified
4. **Improvement Generation**: AI generates improvement suggestions
5. **PR Creation**: Auto-create PRs for high-priority improvements

### Distribution

1. **Version Bump**: Template version incremented
2. **Tag Creation**: Git tag created for new version
3. **Child Notification**: Child projects notified on next commit
4. **Update Available**: Child projects can pull updates

## Benefits

### For Hub (Template Maintainer)

- **Centralized Maintenance**: Fix once, benefit all projects
- **Pattern Recognition**: Identify common issues across projects
- **Continuous Improvement**: Data-driven template evolution
- **Quality Assurance**: Feedback validates template quality

### For Spokes (Child Projects)

- **Automatic Improvements**: Receive bug fixes and features automatically
- **Standardized Reporting**: Easy issue reporting with templates
- **Consistency**: All projects benefit from lessons learned
- **Reduced Maintenance**: Template handles meta-framework updates

## Configuration

### Enabling Feedback (Child Project)

```yaml
# feature_flags.yml
feedback_collection:
  enabled: true
  frequency: "weekly"  # weekly, daily, on_commit
  include_anonymized_logs: true
  auto_submit: false  # Set to true for automatic submission
```

### Enabling Updates (Child Project)

```yaml
# feature_flags.yml
template_updates:
  check_on_commit: true
  auto_update: false  # Set to true for automatic updates
  warn_only: true    # Set to false to block commits if update available
```

## Best Practices

### For Hub Maintainers

1. **Version Bumping**: Always bump version when making template changes
2. **Tag Creation**: Create git tags for each version release
3. **Migration Scripts**: Provide migrations for breaking changes
4. **Documentation**: Document new features and changes
5. **Feedback Processing**: Regularly review and process feedback

### For Child Project Maintainers

1. **Feedback Reporting**: Use standardized feedback functions
2. **Update Regularly**: Pull template updates regularly
3. **Test Updates**: Validate updates in development first
4. **Report Issues**: Report update problems to hub
5. **Stay Current**: Keep template version up-to-date

## Migration Path

### Existing Projects

Projects created before the hub-and-spoke model can be upgraded:

1. **Legacy Upgrade**: Use `upgrade-legacy` command
2. **Pre-Versioned Upgrade**: Use `update-template --init-versioning`
3. **Force Upgrade**: Use force upgrade prompt for AI agents

See:
- `docs/LEGACY_UPGRADE_GUIDE.md` - For projects with no AI structure
- `docs/PRE_VERSIONED_UPGRADE_PROMPT.md` - For pre-versioned projects
- `docs/FORCE_UPGRADE_PROMPT.md` - For automatic upgrades

## Summary

The hub-and-spoke model ensures:

✅ **Standardized Feedback**: All projects use same reporting format  
✅ **Automated Updates**: Projects automatically receive improvements  
✅ **Centralized Maintenance**: Template fixes benefit all projects  
✅ **Continuous Improvement**: Feedback drives template evolution  
✅ **Consistency**: All projects stay aligned with best practices  

---

**The hub-and-spoke model transforms project_initializer from a static template into a living, evolving system that improves continuously based on real-world usage.**

