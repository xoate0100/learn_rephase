# Feedback Loop System Design

## Overview

A self-improving template system that collects AI feedback from all projects and uses it to automatically improve the template. Projects "phone home" with anonymized feedback that gets aggregated and processed to generate template improvements.

## Architecture

### 1. Feedback Collection (Client-Side)

**Location**: `3_bootstrap_scripts/feedback_collector.py`

**Responsibilities**:
- Read `ai_feedback_log.json` and other feedback sources
- Aggregate and anonymize feedback
- Send to template repository via GitHub Issues API
- Respect opt-in/opt-out settings

**Data Sources**:
- `6_ai_runtime_context/ai_feedback_log.json` - AI anomalies and failures
- Guardrail violations (from pre-commit hooks)
- Architecture check failures
- Template update issues
- Common patterns detected

**Anonymization**:
- Remove project-specific paths (replace with placeholders)
- Remove sensitive data (API keys, tokens, etc.)
- Hash project identifiers
- Keep only meta-framework relevant patterns

### 2. Feedback Submission

**Method**: GitHub Issues API

**Why GitHub Issues?**
- No infrastructure required
- Built-in aggregation (labels, search)
- Easy to process with GitHub Actions
- Already integrated with template repo
- Can auto-close duplicates

**Alternative**: Webhook endpoint (if custom infrastructure desired)

**Format**:
- Issue title: Pattern/issue summary
- Issue body: Aggregated feedback with metadata
- Labels: `feedback`, `auto-generated`, category tags
- Milestone: Template version

### 3. Feedback Processing (Server-Side)

**Location**: `.github/workflows/process_feedback.yml`

**Responsibilities**:
- Aggregate similar issues
- Detect patterns across projects
- Generate improvement suggestions
- Auto-create PRs for template improvements
- Track feedback metrics

**Processing Steps**:
1. Group similar issues by pattern
2. Analyze frequency and impact
3. Generate improvement proposals
4. Create PRs with fixes
5. Update template version

## Integration Points

### 1. Guardrail Violations
- **Location**: `3_bootstrap_scripts/guardrail_enforcement.py`
- **Trigger**: On guardrail failure
- **Data**: Violation type, files affected, context

### 2. AI Feedback Log
- **Location**: `6_ai_runtime_context/ai_feedback_log.json`
- **Trigger**: Periodic collection (pre-commit or scheduled)
- **Data**: Anomalies, failures, patterns

### 3. Architecture Checks
- **Location**: `3_bootstrap_scripts/architecture_check.py`
- **Trigger**: On architecture violation
- **Data**: SOLID violations, layer boundary issues

### 4. Template Updates
- **Location**: `3_bootstrap_scripts/template_update.py`
- **Trigger**: After update completion
- **Data**: Update success/failure, migration issues

### 5. AI Context Generation
- **Location**: `3_bootstrap_scripts/generate_ai_context.py`
- **Trigger**: On context generation
- **Data**: Missing context, unclear rules, drift issues

## Privacy & Security

### Opt-In/Opt-Out
- **Default**: Opt-in (enabled by default)
- **Configuration**: `0_phase0_bootstrap/feature_flags.yml`
  ```yaml
  feedback_collection:
    enabled: true
    frequency: "weekly"  # daily, weekly, monthly, on_event
    include_anonymized_logs: true
  ```

### Anonymization Rules
- Project paths → `[PROJECT_ROOT]/...`
- Repository URLs → `[TEMPLATE_REPO]`
- Sensitive patterns → `[REDACTED]`
- Project names → `[PROJECT_NAME]`

### Data Retention
- Feedback stored in GitHub Issues (public or private repo)
- No persistent storage of project-specific data
- Aggregated patterns only

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

## Auto-Improvement Workflow

1. **Feedback Collection**: Projects send anonymized feedback
2. **Pattern Detection**: GitHub Actions aggregates similar issues
3. **Improvement Generation**: AI analyzes patterns and generates fixes
4. **PR Creation**: Auto-create PRs with improvements
5. **Template Update**: Merge PRs and release new version
6. **Feedback Loop**: Projects update and send new feedback

## Benefits

1. **Self-Improving**: Template gets better with each project
2. **Lessons Learned**: All projects benefit from individual experiences
3. **Pattern Detection**: Identify common issues early
4. **Automated**: Minimal manual intervention
5. **Scalable**: Works with any number of projects

## Future Enhancements

- Real-time feedback dashboard
- Feedback analytics and metrics
- ML-based pattern detection
- Automated A/B testing of improvements
- Feedback prioritization (impact scoring)

