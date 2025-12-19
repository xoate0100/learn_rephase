# Standardized Feedback Reporting Guide

## Overview

The `standardized_feedback.py` module provides **pre-configured, templated issue reporting** for child projects. This ensures all feedback submitted to the hub (project_initializer) follows a consistent format and structure.

## Quick Start

```python
from standardized_feedback import report_guardrail_violation

# Report a guardrail violation
report_guardrail_violation(
    guardrail_name="enforce_task_scope",
    component="frontend",
    files=["src/components/Button.tsx"],
    details="File modified outside active task scope",
)
```

## Available Reporting Functions

### 1. Guardrail Violations

```python
from standardized_feedback import report_guardrail_violation

report_guardrail_violation(
    guardrail_name="enforce_tdd_cycle",
    component="backend",
    files=["api/users.py"],
    context="Code modified without tests",
    details="User API modified but no test updates",
    requires_intervention=True,
)
```

### 2. Architecture Violations

```python
from standardized_feedback import report_architecture_violation

report_architecture_violation(
    violation_type="SRP violation",
    component="shared",
    principle="Single Responsibility Principle",
    files=["utils/helpers.ts"],
    details="Helper module has multiple responsibilities",
    expected="Single responsibility per module",
    actual="Module handles validation, formatting, and API calls",
)
```

### 3. Template Drift

```python
from standardized_feedback import report_template_drift

report_template_drift(
    drift_type="Write path mismatch",
    location="feature_flags.yml",
    expected="frontend/, backend/",
    actual="src/, lib/",
    impact="Guardrails may not enforce correctly",
    recommendation="Align write paths with template",
)
```

### 4. Update Issues

```python
from standardized_feedback import report_update_issue

report_update_issue(
    issue_type="Migration failure",
    from_version="1.2.0",
    to_version="1.3.0",
    migration_applied=False,
    details="Migration script failed during update",
    error="Permission denied: cannot write to protected file",
    resolution="Manual migration required",
)
```

### 5. Performance Issues

```python
from standardized_feedback import report_performance_issue

report_performance_issue(
    metric="build_time",
    component="frontend",
    threshold="30s",
    actual="45s",
    files=["package.json", "next.config.js"],
    impact="CI/CD pipeline slowed down",
    recommendation="Optimize dependency resolution",
)
```

### 6. Schema Mismatches

```python
from standardized_feedback import report_schema_mismatch

report_schema_mismatch(
    schema_file="7_schemas/mvp_specification.schema.json",
    validated_file="0_phase0_bootstrap/MVP_SPECIFICATION.yaml",
    errors=[
        "Missing required field: GOALS_AND_PRINCIPLES",
        "Invalid value for Maturity: 'L3' (expected: 'L2' or 'L2.5')",
    ],
    details="MVP specification does not match schema",
    fix_required="Update MVP_SPECIFICATION.yaml to match schema",
)
```

### 7. Documentation Gaps

```python
from standardized_feedback import report_documentation_gap

report_documentation_gap(
    component="backend",
    missing="API endpoint documentation",
    files=["api/users.py", "api/posts.py"],
    impact="Developers unclear on API usage",
    recommendation="Add OpenAPI/Swagger documentation",
)
```

### 8. Operational Errors

```python
from standardized_feedback import report_operational_error, auto_report_from_exception

# Manual reporting
report_operational_error(
    error_type="DatabaseConnectionError",
    component="backend",
    error="Connection timeout after 30s",
    context="Failed to connect to PostgreSQL database",
    files=["db/connection.py"],
    resolution="Check database credentials and network",
)

# Automatic exception reporting
try:
    risky_operation()
except Exception as e:
    auto_report_from_exception(
        e,
        component="shared",
        context="Exception during data processing",
        files=["utils/processor.py"],
    )
```

## Universal Reporting Function

For dynamic feedback types:

```python
from standardized_feedback import report_feedback

report_feedback(
    feedback_type="GUARDRAIL_VIOLATION",
    guardrail_name="enforce_task_scope",
    component="frontend",
    files=["src/components/Button.tsx"],
    details="File modified outside active task scope",
    requires_intervention=True,
)
```

## Integration Examples

### In Guardrail Enforcement

```python
# 3_bootstrap_scripts/guardrail_enforcement.py
from standardized_feedback import report_guardrail_violation

def enforce_task_scope(guardrails, staged_files):
    # ... validation logic ...
    if violation_detected:
        report_guardrail_violation(
            guardrail_name="enforce_task_scope",
            component="shared",
            files=staged_files,
            details="Files modified outside active task scope",
        )
        return False
    return True
```

### In Architecture Checks

```python
# 3_bootstrap_scripts/architecture_check.py
from standardized_feedback import report_architecture_violation

def check_srp_violation(file_path):
    # ... SRP check logic ...
    if violation:
        report_architecture_violation(
            violation_type="SRP violation",
            component="shared",
            principle="Single Responsibility Principle",
            files=[file_path],
            details="Module has multiple responsibilities",
        )
```

### In Update Process

```python
# 3_bootstrap_scripts/template_update.py
from standardized_feedback import report_update_issue

def apply_migration(from_version, to_version):
    try:
        # ... migration logic ...
    except Exception as e:
        report_update_issue(
            issue_type="Migration failure",
            from_version=from_version,
            to_version=to_version,
            migration_applied=False,
            error=str(e),
        )
```

## Feedback Submission

Feedback is automatically collected in `6_ai_runtime_context/ai_feedback_log.json` and can be submitted to the hub:

```bash
# Manual submission
python3 3_bootstrap_scripts/cli.py submit-feedback

# Automatic submission (if auto_submit: true in feature_flags.yml)
# Runs automatically based on frequency setting
```

## Template Structure

Each feedback type uses a standardized template:

```markdown
## [Category] Title

**Field**: Value
**Field**: Value

**Details**:
Description

**Recommendation**: Action
```

This ensures consistent formatting when issues are submitted to the hub.

## Best Practices

1. **Use Appropriate Type**: Choose the correct feedback type for the issue
2. **Provide Context**: Include relevant context and details
3. **List Files**: Always include affected files when available
4. **Be Specific**: Provide specific details, not generic messages
5. **Include Recommendations**: Suggest fixes or improvements when possible

## Configuration

Feedback collection is controlled by `feature_flags.yml`:

```yaml
feedback_collection:
  enabled: true
  frequency: "weekly"  # weekly, daily, on_commit
  include_anonymized_logs: true
  auto_submit: false
```

## Summary

The standardized feedback module provides:

✅ **Templated Formats**: Consistent issue structure  
✅ **Easy Integration**: Simple function calls  
✅ **Automatic Categorization**: Issues properly categorized  
✅ **Anonymization**: Project data anonymized before submission  
✅ **Hub Compatibility**: Works seamlessly with hub processing  

---

**Use standardized feedback functions throughout your project to ensure consistent, high-quality feedback to the hub.**

