# Schema & Template Analysis Report

## Executive Summary

**Critical Issues Found:**
1. ❌ **MVP_SPECIFICATION.yaml structure completely mismatches schema** - Template uses simple structure, schema expects complex nested structure
2. ⚠️ **feature_flags.yml has fields not in schema** - Extensions need schema update or removal
3. ⚠️ **Many schema-defined features unused in codebase** - Need implementation or removal
4. ⚠️ **Schema expects features not in template** - Need template updates or schema simplification

---

## 1. Feature Flags Analysis

### Schema Requirements vs Template

| Field | Schema | Template | Status | Action Required |
|-------|--------|----------|--------|-----------------|
| `mode` | ✅ Required | ✅ Present | ✅ OK | - |
| `permissions` | ✅ Required | ✅ Present | ✅ OK | - |
| `components` | ✅ Required | ✅ Present | ✅ OK | - |
| `gates` | ✅ Required | ✅ Present | ✅ OK | - |
| `thresholds` | ⚪ Optional | ✅ Present | ✅ OK | - |
| `ai_guardrails` | ⚪ Optional | ✅ Present | ✅ OK | - |
| `meta` | ⚪ Optional | ❌ Missing | ⚠️ **MISSING** | Add to template or remove from schema |

### Template Extensions (Not in Schema)

1. **`mode.human_review_required_for_merge`** (line 6)
   - Not in schema
   - Used in: ❓ Unknown (need to check)
   - **Action**: Add to schema OR remove from template

2. **`components.*.package_manager: "auto"`** (line 25)
   - Schema allows string, but "auto" not documented
   - Used in: ❓ Unknown
   - **Action**: Document "auto" as valid enum value OR remove

3. **`ai_guardrails.require_commit_plan_tags`** (line 59)
   - Not in schema
   - Used in: `ai_behavior_validation.py` (indirectly)
   - **Action**: Add to schema OR remove from template

### Schema Features Not Used in Code

1. **`meta.schema_version`** - Not validated or used
2. **`meta.last_updated`** - Not validated or used  
3. **`meta.author`** - Not validated or used
4. **`gates.warn_on_performance_regression`** - Defined but no enforcement script
5. **`gates.warn_on_mutation_drop`** - Defined but no enforcement script
6. **`thresholds.coverage`** - Not used (component-specific used instead)
7. **`thresholds.mutation_kill`** - Defined but no mutation testing script
8. **`thresholds.perf_regression_pct`** - Defined but no performance testing
9. **`thresholds.max_complexity`** - Not used (component-specific used instead)
10. **`ai_guardrails.enforce_task_scope`** - Defined but not enforced
11. **`ai_guardrails.forbid_folder_creation_outside_scope`** - Defined but not enforced

---

## 2. MVP Specification Analysis

### CRITICAL: Structure Mismatch

**Schema Expects:**
```yaml
Project: "string"
Maturity: "L2" | "L2.5" | "L3"
Architecture: "string"
Repo_Type: "frontend" | "backend" | ...
Execution_Mode: "Human Directed" | ...
GOALS_AND_PRINCIPLES:
  goals: [...]
  principles: [...]
TECH_STACK:
  frontend: { framework: "nextjs" | ..., language: ..., styling: [...] }
  backend: { framework: "fastapi" | ..., language: ..., orm: ... }
  shared: { language: ... }
  integrations: [...]
  optional_libs: [...]
MONOREPO_LAYOUT:
  root: {...}
  apps: {...}
  scripts: [...]
  shared: {...}
ENVIRONMENT_AND_CONFIG: {...}
ROUTING_MODEL: {...}
SCHEMA_DEFINITION: {...}
BRAND_MODULE: {...}
ANALYTICS_AND_EVENTS: {...}
INTEGRATIONS: {...}
SEO_AND_JSONLD: {...}
AI_UI_GENERATION: {...}
AUTOMATION_SCRIPTS: {...}
INTERACTIVE_PATTERNS: {...}
QA_CHECKLIST: [...]
DEPLOYMENT: {...}
MIGRATION_PATH: {...}
FIRST_RUN_PLAYBOOK: {...}
POST_MVP_FEATURES: [...]
DELIVERABLES_DAY1: {...}
ACTIVE_PLAN_TEMPLATE: {...}
FEATURE_FLAGS_REFERENCE: {...}
SUMMARY_FOR_INITIALIZER: {...}
```

**Template Has:**
```yaml
project_name: "string"
project_description: "string"
tech_stack:
  frontend: { framework: "react", language: "typescript", package_manager: "npm" }
  backend: { framework: "fastapi", language: "python", package_manager: "pip" }
  shared: { language: "typescript" }
MONOREPO_LAYOUT: [array of strings]
ACTIVE_PLAN_TEMPLATE: {...}
initial_config: {...}
```

**Impact**: ❌ **Schema validation will FAIL** on current template!

### Schema Fields Not in Template (Required)

1. **`Project`** - Required, missing
2. **`Maturity`** - Required, missing
3. **`Architecture`** - Required, missing
4. **`Execution_Mode`** - Required, missing
5. **`GOALS_AND_PRINCIPLES`** - Required, missing
6. **`SUMMARY_FOR_INITIALIZER`** - Required, missing

### Schema Fields Not in Template (Optional but Defined)

1. `Repo_Type`
2. `ENVIRONMENT_AND_CONFIG`
3. `ROUTING_MODEL`
4. `SCHEMA_DEFINITION`
5. `BRAND_MODULE`
6. `ANALYTICS_AND_EVENTS`
7. `INTEGRATIONS`
8. `SEO_AND_JSONLD`
9. `AI_UI_GENERATION`
10. `AUTOMATION_SCRIPTS`
11. `INTERACTIVE_PATTERNS`
12. `QA_CHECKLIST`
13. `DEPLOYMENT`
14. `MIGRATION_PATH`
15. `FIRST_RUN_PLAYBOOK`
16. `POST_MVP_FEATURES`
17. `DELIVERABLES_DAY1`
18. `FEATURE_FLAGS_REFERENCE`

### Template Fields Not in Schema

1. **`project_name`** - Not in schema (should be `Project`)
2. **`project_description`** - Not in schema
3. **`initial_config`** - Not in schema

### Code Usage Analysis

**init_project.py usage:**
- ✅ Uses: `MONOREPO_LAYOUT` (expects array, schema expects object)
- ✅ Uses: `ACTIVE_PLAN_TEMPLATE`
- ❌ Does NOT use: `tech_stack`, `project_name`, `project_description`

**Impact**: Code expects array, schema expects object structure!

---

## 3. Required Actions

### Priority 1: CRITICAL (Breaks Functionality)

1. **Fix MVP_SPECIFICATION.yaml Template**
   - Option A: Update template to match schema (complex, full-featured)
   - Option B: Simplify schema to match template (recommended for template repo)
   - **Recommendation**: Option B - simplify schema for template use

2. **Fix MONOREPO_LAYOUT Structure**
   - Code expects: `array of strings`
   - Schema expects: `object with root/apps/scripts/shared`
   - **Action**: Align one to the other

3. **Fix Required Fields**
   - Add missing required fields to template OR
   - Make them optional in schema

### Priority 2: HIGH (Features Not Working)

4. **Implement Missing Feature Flag Features**
   - Add `meta` section to template (or remove from schema)
   - Implement mutation testing enforcement
   - Implement performance regression checking
   - Implement task scope enforcement
   - Implement folder creation restrictions

5. **Add Missing Schema Fields to Template**
   - Add `meta` section to feature_flags.yml
   - Document all optional fields

6. **Update Schema or Remove Unused Features**
   - Remove `meta` from schema if not used
   - Remove unused gate flags if not implementing
   - Remove unused thresholds if not implementing

### Priority 3: MEDIUM (Clarity & Completeness)

7. **Document Template Extensions**
   - Add `human_review_required_for_merge` to schema
   - Add `require_commit_plan_tags` to schema
   - Document `package_manager: "auto"` as valid

8. **Implement Guardrails**
   - `enforce_task_scope` - Check files match ACTIVE_PLAN.yaml task
   - `forbid_folder_creation_outside_scope` - Validate new directories

9. **Add MVP Spec Optional Fields**
   - Consider which optional fields are useful for template
   - Add them to template or document why excluded

---

## 4. Recommended Solution

### Option A: Simplify Schema for Template Use (RECOMMENDED)

**Rationale**: Template repo should be simple and generic. Complex schema is for specific projects.

**Actions**:
1. Create simplified `mvp_specification.schema.json` for template
2. Keep full schema for reference/documentation
3. Update template to match simplified schema
4. Update validation to use simplified schema

### Option B: Update Template to Match Full Schema

**Rationale**: Support full feature set from start.

**Actions**:
1. Rewrite `MVP_SPECIFICATION.yaml` to match full schema
2. Add all required fields
3. Update `init_project.py` to handle new structure
4. Document all optional fields

**Recommendation**: **Option A** - Template should be minimal, projects can expand.

---

## 5. Implementation Checklist

### Immediate Fixes (Before Next Use)

- [ ] Align MONOREPO_LAYOUT structure (code vs schema)
- [ ] Add missing required MVP fields OR make optional
- [ ] Fix schema validation to not fail on template

### Short-term (Feature Completeness)

- [ ] Add `meta` section to feature_flags.yml OR remove from schema
- [ ] Document/add template extensions to schema
- [ ] Implement at least one guardrail enforcement
- [ ] Add mutation testing script if threshold defined
- [ ] Add performance regression check if threshold defined

### Long-term (Full Feature Support)

- [ ] Implement all guardrails
- [ ] Support all optional MVP spec fields
- [ ] Create comprehensive template examples
- [ ] Document schema evolution

