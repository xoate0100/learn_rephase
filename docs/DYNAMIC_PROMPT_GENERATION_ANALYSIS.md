# Dynamic Prompt Generation System - Analysis & Proposal

## Executive Summary

**Goal:** Implement a dynamic prompt generation system that consolidates meta-framework constraints, state, flags, and task context into a single AI-optimized document, automatically regenerated on state/flag changes to minimize human interaction.

**Status:** Analysis complete, implementation proposal ready

---

## 1. Critical Analysis of Previous System

### 1.1 What Worked (Pros)

✅ **Single Source of Truth for AI**
- Consolidated 7+ files into one document
- Eliminated constraint drift (AI forgetting rules mid-conversation)
- Token-efficient (sampling strategy: 15 rules, 12 invariants)

✅ **State Awareness**
- Included current state, task context, blocking issues
- Prevented AI from inferring state (violates invariant)
- Always current via dynamic generation

✅ **Authority Preservation**
- Generated document references authoritative sources
- Read-only generation (never modifies source files)
- Clear hierarchy: source files > generated document > chat context

✅ **AI-Optimized Structure**
- Markdown format (AI-friendly)
- Consistent structure every generation
- Sections ordered by importance

### 1.2 What Needs Improvement (Cons)

❌ **PowerShell-Specific**
- Not cross-platform (Windows-only)
- Our template needs Python (cross-platform)

❌ **Manual Regeneration Required**
- Human must run generator before chat
- Defeats "automated AI workflows" goal
- Easy to forget, causes stale constraints

❌ **Regex Parsing (Brittle)**
- YAML parsing uses regex fallback
- Markdown parsing uses regex
- Could break on format variations

❌ **Sampling Might Miss Critical Rules**
- First 15 rules shown, rest referenced
- Important rules might be #16-20
- AI might not check references

❌ **No Auto-Detection of Changes**
- No pre-commit hook integration
- No file watcher for state/flag changes
- Requires manual trigger

### 1.3 Template Adaptation Challenges

**File Structure Differences:**
- Previous: `control/FLAGS.yaml`, `control/STATE_POINTER.yaml`, `control/NEVER_RULES.md`
- Our template: `0_phase0_bootstrap/feature_flags.yml`, `6_ai_runtime_context/ACTIVE_PLAN.yaml`, `6_ai_runtime_context/ACTIVE_TASK_POINTER.yaml`, `0_phase0_bootstrap/AI_SANDBOX_RULES.md`

**Constraint Organization:**
- Previous: Separate files for never rules, invariants, intent anchors
- Our template: Constraints consolidated in `AI_SANDBOX_RULES.md` (simpler, but less structured)

**Enforcement Tools:**
- Previous: `scripts/framework/*.ps1`
- Our template: `3_bootstrap_scripts/*.py`

---

## 2. Proposed Solution for Our Template

### 2.1 Core Design Principles

1. **Automated Regeneration** (Priority #1)
   - Auto-regenerate on state/flag file changes
   - Pre-commit hook detects staleness
   - CI/CD includes generation step

2. **Python-Based** (Cross-Platform)
   - Use Python (not PowerShell)
   - Leverage existing `3_bootstrap_scripts/` structure
   - Use proper YAML/Markdown parsers (not regex)

3. **Template-Generic**
   - Works with our file structure
   - Adaptable to different project types
   - Minimal assumptions about constraint organization

4. **Minimal Human Interaction**
   - Auto-regenerate on changes
   - Pre-commit warns if stale
   - CI/CD validates freshness

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Source Files (Read-Only)                       │
├─────────────────────────────────────────────────────────────┤
│  • 0_phase0_bootstrap/AI_SANDBOX_RULES.md                  │
│  • 0_phase0_bootstrap/feature_flags.yml                    │
│  • 0_phase0_bootstrap/AI_EXECUTION_CONSTRAINTS.md           │
│  • 6_ai_runtime_context/ACTIVE_PLAN.yaml                   │
│  • 6_ai_runtime_context/ACTIVE_TASK_POINTER.yaml           │
│  • 5_reference_architectures/LAYER_RULES.yaml              │
│  • 3_bootstrap_scripts/*.py (tool discovery)               │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│          Generator Script (Python)                          │
│  3_bootstrap_scripts/generate_ai_context.py                │
│                                                             │
│  Functions:                                                 │
│  • extract_sandbox_rules()                                 │
│  • parse_feature_flags()                                   │
│  • parse_active_plan()                                     │
│  • parse_task_pointer()                                    │
│  • discover_enforcement_tools()                            │
│  • generate_context_document()                              │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│          Generated Document                                  │
│  6_ai_runtime_context/AI_CONTEXT.md                        │
│                                                             │
│  Sections:                                                  │
│  • Current State Context                                    │
│  • Sandbox Rules (Allowed/Forbidden/Required)              │
│  • Feature Flags (Enabled/Disabled)                        │
│  • Current Task Context                                     │
│  • Enforcement Tools Available                             │
│  • Architecture Rules                                       │
│  • Reference Documents                                      │
│  • Usage Instructions                                       │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│          Auto-Regeneration Triggers                         │
│  • Pre-commit hook (staleness check)                       │
│  • File watcher (optional, for dev)                         │
│  • CI/CD pipeline (always regenerate)                      │
│  • Manual: python 3_bootstrap_scripts/generate_ai_context.py│
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Document Structure (Proposed)

```markdown
# AI Execution Context - Auto-Generated

**Generated:** 2025-01-XX XX:XX:XX
**Authority:** `0_phase0_bootstrap/AI_SANDBOX_RULES.md`
**Purpose:** Consolidated constraint context for AI chat sessions

## Current State Context

**Plan:** {plan_id}
**Component:** {component}
**Current Task:** {task_id} - {task_name}
**Status:** {status}
**Next Task:** {next_task_id}

**Blocking Issues:** {blocking_issues or "None"}

---

## Sandbox Rules

### Allowed
{extracted from AI_SANDBOX_RULES.md "## Allowed" section}

### Required (MANDATORY - BLOCKING)
{extracted from AI_SANDBOX_RULES.md "## Required" section}

### Forbidden
{extracted from AI_SANDBOX_RULES.md "## Forbidden" section}

**Reference:** `0_phase0_bootstrap/AI_SANDBOX_RULES.md`

---

## Feature Flags

### Enabled Permissions
{flags where value = true, formatted as list}

### Disabled Permissions
{flags where value = false, formatted as list}

**Reference:** `0_phase0_bootstrap/feature_flags.yml`

---

## Current Task Context

**Task {task_id}:** {task_name}
**Outputs:** {task_outputs}
**Status:** {task_status}

**Full Plan:** See `6_ai_runtime_context/ACTIVE_PLAN.yaml`

---

## Enforcement Tools Available

{discovered tools from 3_bootstrap_scripts/ with descriptions}

**Location:** `3_bootstrap_scripts/`

---

## Architecture Rules

{extracted from LAYER_RULES.yaml - component boundaries, layer rules}

**Reference:** `5_reference_architectures/LAYER_RULES.yaml`

---

## Reference Documents

1. **`0_phase0_bootstrap/AI_SANDBOX_RULES.md`** - Sandbox execution rules
2. **`0_phase0_bootstrap/feature_flags.yml`** - Feature flags and permissions
3. **`6_ai_runtime_context/ACTIVE_PLAN.yaml`** - Current plan and tasks
4. **`6_ai_runtime_context/ACTIVE_TASK_POINTER.yaml`** - Current task pointer
5. **`5_reference_architectures/LAYER_RULES.yaml`** - Architecture boundaries
6. **`1_global_standards/`** - Code standards (TDD, SOLID, etc.)

---

## Usage Instructions

**For AI Agents:**
1. Load this document first in new chat sessions
2. Reference authoritative documents for complete details
3. Use enforcement tools listed above for validation
4. Regenerate if state/flags change during session

**For Human Operators:**
- Auto-regenerates on state/flag changes
- Pre-commit hook warns if stale
- Manual: `python 3_bootstrap_scripts/generate_ai_context.py`

---

**Last Generated:** {timestamp}
**Generator:** `3_bootstrap_scripts/generate_ai_context.py`
```

### 2.4 Key Improvements Over Previous System

✅ **Automated Regeneration**
- Pre-commit hook detects staleness
- Auto-regenerate on file changes (optional file watcher)
- CI/CD always regenerates

✅ **Proper Parsing**
- Use `pyyaml` for YAML (not regex)
- Use markdown parser or structured extraction for markdown
- More robust than regex fallback

✅ **Cross-Platform**
- Python (works on Windows/macOS/Linux)
- No PowerShell dependency

✅ **Template-Adapted**
- Works with our file structure
- Extracts from `AI_SANDBOX_RULES.md` (not separate never rules/invariants files)
- Discovers tools from `3_bootstrap_scripts/`

✅ **Minimal Human Interaction**
- Auto-regenerates on changes
- Pre-commit warns (doesn't block, but alerts)
- CI/CD validates freshness

---

## 3. Implementation Plan

### Phase 1: Core Generator (Python)
- [ ] Create `3_bootstrap_scripts/generate_ai_context.py`
- [ ] Implement extraction functions:
  - [ ] `extract_sandbox_rules()` - Parse AI_SANDBOX_RULES.md sections
  - [ ] `parse_feature_flags()` - Read feature_flags.yml with pyyaml
  - [ ] `parse_active_plan()` - Read ACTIVE_PLAN.yaml
  - [ ] `parse_task_pointer()` - Read ACTIVE_TASK_POINTER.yaml
  - [ ] `discover_enforcement_tools()` - Scan 3_bootstrap_scripts/*.py
- [ ] Implement document generation
- [ ] Write to `6_ai_runtime_context/AI_CONTEXT.md`

### Phase 2: Auto-Regeneration
- [ ] Pre-commit hook: Check staleness (compare file mtimes)
- [ ] Auto-regenerate if source files newer than generated doc
- [ ] CI/CD: Always regenerate in pipeline

### Phase 3: Integration
- [ ] Update `init_project.py` to generate on initialization
- [ ] Update documentation (INITIALIZATION_GUIDE.md, etc.)
- [ ] Add to CLI: `python 3_bootstrap_scripts/cli.py generate-context`

### Phase 4: Validation (Optional)
- [ ] Validate generated document structure
- [ ] Check all references exist
- [ ] Verify no missing sections

---

## 4. Pros/Cons Analysis

### Pros ✅

1. **Solves Constraint Drift**
   - AI always has current constraints
   - Single document vs. reading 5+ files
   - Token-efficient

2. **State Awareness**
   - AI knows current task, plan, blocking issues
   - No state inference required
   - Always current

3. **Automated Workflows**
   - Auto-regenerates on changes
   - Pre-commit warns if stale
   - Minimal human interaction

4. **Template-Generic**
   - Works with our file structure
   - Adaptable to different projects
   - Cross-platform (Python)

5. **Authority Preservation**
   - References authoritative sources
   - Read-only generation
   - Clear hierarchy

### Cons ⚠️

1. **Additional File to Maintain**
   - Generated file in repo (or .gitignore?)
   - Need to decide: commit generated file or generate on-demand?

2. **Parsing Complexity**
   - Markdown extraction can be brittle
   - Need robust error handling
   - May need to update if source format changes

3. **Staleness Risk**
   - If auto-regeneration fails, document can be stale
   - Pre-commit hook helps but not foolproof
   - CI/CD validation helps

4. **Token Usage**
   - Generated document adds to context
   - But still more efficient than reading 5+ files
   - Can optimize with sampling if needed

---

## 5. Decision: Commit Generated File or Generate On-Demand?

### Option A: Commit Generated File (Recommended)
**Pros:**
- AI can immediately load document
- No generation step required
- Version controlled (can see history)

**Cons:**
- Merge conflicts possible
- Need to ensure auto-regeneration works
- File in repo (but it's generated, not source)

**Implementation:**
- Pre-commit hook auto-regenerates if stale
- CI/CD validates freshness
- Document clearly marked as "Auto-Generated"

### Option B: Generate On-Demand
**Pros:**
- No generated file in repo
- Always fresh (generated when needed)

**Cons:**
- Requires generation step before chat
- Human interaction required (defeats automation goal)
- Not available immediately

**Recommendation:** **Option A** (commit generated file) - aligns with automated workflows goal

---

## 6. Next Steps

1. **Implement Core Generator** (`generate_ai_context.py`)
2. **Add Pre-Commit Hook** (staleness check + auto-regenerate)
3. **Update Documentation** (usage instructions)
4. **Test End-to-End** (generation → AI usage → regeneration)
5. **CI/CD Integration** (always regenerate in pipeline)

---

## 7. Success Metrics

- ✅ AI constraint violations reduced
- ✅ Faster constraint checking (single doc vs. multiple files)
- ✅ Consistent behavior across chat sessions
- ✅ Current state awareness from session start
- ✅ Zero manual regeneration required (fully automated)

---

**Status:** Ready for Implementation
**Priority:** High (enables automated AI workflows)
**Estimated Effort:** 2-3 hours for core implementation
