# AI Execution Constraints Prompting System
## Comprehensive Documentation & Justification

**Version:** 1.0  
**Date:** 2025-12-18  
**Purpose:** Template documentation for project initializer - AI constraint system  
**Audience:** AI agents, human operators, project template consumers

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement & Rationale](#2-problem-statement--rationale)
3. [System Architecture](#3-system-architecture)
4. [Dynamic Prompt Generation Mechanism](#4-dynamic-prompt-generation-mechanism)
5. [Use Cases & Scenarios](#5-use-cases--scenarios)
6. [Usage Patterns](#6-usage-patterns)
7. [Implementation Details](#7-implementation-details)
8. [Examples & Pseudo Code](#8-examples--pseudo-code)
9. [Integration Points](#9-integration-points)
10. [Justification & Design Decisions](#10-justification--design-decisions)
11. [Template Adaptation Guide](#11-template-adaptation-guide)

---

## 1. Executive Summary

### 1.1 What Is This System?

The **AI Execution Constraints Prompting System** is a dynamic document generation framework that consolidates all project constraints, state information, permissions, and enforcement tools into a single, context-aware reference document (`AI_EXECUTION_CONSTRAINTS.md`). This document serves as the **primary constraint context** for AI chat sessions, ensuring consistent behavior and preventing constraint drift.

### 1.2 Core Value Proposition

**Problem Solved:** AI agents in chat sessions suffer from:
- **Constraint drift:** Forgetting or misinterpreting rules over long conversations
- **State blindness:** Not knowing current project state or permissions
- **Context fragmentation:** Constraints scattered across multiple files
- **Stale context:** Using outdated constraint information

**Solution Provided:**
- **Single source of truth:** All constraints in one document
- **Dynamic generation:** Always reflects current state and flags
- **Context-aware:** Includes current state, permissions, and task context
- **AI-optimized:** Structured for immediate AI comprehension

### 1.3 Key Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Read-Only Generation** | Generator only reads source files, never modifies them |
| **Dynamic Content** | Reflects current state, flags, and context at generation time |
| **Authority Preservation** | Generated document references authoritative sources |
| **AI-First Design** | Structured for optimal AI ingestion and comprehension |
| **Template-Ready** | Designed for extraction into project initializer templates |

---

## 2. Problem Statement & Rationale

### 2.1 The Constraint Drift Problem

**Symptom:** AI agents in chat sessions gradually forget or misinterpret constraints as conversations progress.

**Root Causes:**
1. **Token limits:** Long conversations push early context out of window
2. **Context decay:** Important constraints mentioned early become less prominent
3. **State changes:** Project state changes mid-conversation without AI awareness
4. **Flag changes:** Permission flags change without AI knowledge
5. **File fragmentation:** Constraints spread across 7+ source files

**Impact:**
- AI violates invariants that were established earlier
- AI attempts operations blocked by current flags
- AI works on wrong state/task context
- Inconsistent behavior across chat sessions

### 2.2 The State Awareness Problem

**Symptom:** AI agents don't know current project state, permissions, or task context.

**Root Causes:**
1. **No state pointer:** AI must infer state from context (violates invariant)
2. **Flag opacity:** AI doesn't know which permissions are enabled
3. **Task blindness:** AI doesn't know current task or blocking issues
4. **Tool ignorance:** AI doesn't know available enforcement tools

**Impact:**
- AI infers state (violates absolute invariant #1)
- AI attempts blocked operations
- AI works on wrong tasks
- AI doesn't use available validation tools

### 2.3 The Context Fragmentation Problem

**Symptom:** Critical constraints exist in multiple files, making it hard for AI to maintain complete awareness.

**Source Files:**
1. `AI_ORCHESTRATION_META_FRAMEWORK.md` - Absolute invariants
2. `control/FLAGS.yaml` - Feature flags and permissions
3. `control/STATE_POINTER.yaml` - Current state and progress
4. `control/NEVER_RULES.md` - Critical never rules
5. `control/INVARIANTS.md` - Regression protection rules
6. `control/INTENT_ANCHORS.md` - Architectural constraints
7. `control/ACTIVE_PLAN.md` - Current task context

**Impact:**
- AI must read 7+ files to understand constraints
- Incomplete constraint awareness leads to violations
- No single reference point for constraint checking

### 2.4 Solution Rationale

**Why Dynamic Generation?**
- **State changes:** Project state changes require updated context
- **Flag changes:** Permission changes affect what AI can do
- **Task progression:** Task context changes as work progresses
- **Freshness:** Generated document includes timestamp for staleness detection

**Why Single Document?**
- **Token efficiency:** One document vs. reading 7+ files
- **Completeness:** All constraints in one place
- **Consistency:** Same structure every time
- **AI optimization:** Structured for immediate comprehension

**Why Read-Only Generation?**
- **Authority preservation:** Source files remain authoritative
- **Non-destructive:** Generator never modifies source files
- **Reversibility:** Can regenerate from source at any time
- **Safety:** No risk of corrupting source files

---

## 3. System Architecture

### 3.1 Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Source Files (Read-Only)                 │
├─────────────────────────────────────────────────────────────┤
│  • AI_ORCHESTRATION_META_FRAMEWORK.md                       │
│  • control/FLAGS.yaml                                       │
│  • control/STATE_POINTER.yaml                               │
│  • control/NEVER_RULES.md                                   │
│  • control/INVARIANTS.md                                   │
│  • control/INTENT_ANCHORS.md                               │
│  • control/ACTIVE_PLAN.md                                  │
│  • scripts/framework/*.ps1 (tool discovery)                │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│          Generator Script                                   │
│  scripts/framework/generate_prompt_constraints.ps1          │
│                                                             │
│  Functions:                                                 │
│  • Extract-AbsoluteInvariants()                            │
│  • Parse-Flags()                                            │
│  • Parse-StatePointer()                                     │
│  • Extract-NeverRules()                                     │
│  • Extract-KeyInvariants()                                  │
│  • Extract-IntentAnchors()                                 │
│  • Get-FrameworkTools()                                     │
│  • Generate-ConstraintDocument()                           │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│          Generated Document                                 │
│  AI_EXECUTION_CONSTRAINTS.md                                │
│                                                             │
│  Sections:                                                  │
│  • Current State Context                                    │
│  • Absolute Invariants                                      │
│  • Current Flag States                                      │
│  • Never Rules (sampled)                                    │
│  • Key Invariants (sampled)                                 │
│  • Intent Anchors                                           │
│  • Enforcement Tools Available                              │
│  • Current Task Context                                     │
│  • Reference Documents                                      │
│  • Usage Instructions                                       │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│          AI Chat Session                                    │
│  • Loads AI_EXECUTION_CONSTRAINTS.md first                  │
│  • References authoritative sources for details              │
│  • Uses enforcement tools listed                             │
│  • Regenerates if state/flags change                        │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Data Flow

```
1. Human Operator / CI/CD triggers generation
   ↓
2. Generator reads all source files (read-only)
   ↓
3. Extraction functions parse and extract data:
   - Regex patterns extract invariants from meta framework
   - YAML parser extracts flags and state
   - Markdown parsers extract rules and anchors
   - File system scan discovers framework tools
   ↓
4. Data structures assembled:
   - Arrays of invariants, rules, anchors
   - Hash tables of flags (enabled/disabled)
   - State object with current/next/blocking
   - Tool list with descriptions
   ↓
5. Markdown template populated with data
   ↓
6. Generated document written to project root
   ↓
7. AI chat session loads document
   ↓
8. AI uses document as constraint reference
```

### 3.3 Authority Hierarchy

```
Level 1 (Highest): AI_ORCHESTRATION_META_FRAMEWORK.md
  └─ Absolute invariants (non-negotiable)

Level 2: Control Files (control/*)
  ├─ FLAGS.yaml (permissions)
  ├─ STATE_POINTER.yaml (state)
  ├─ NEVER_RULES.md (critical constraints)
  ├─ INVARIANTS.md (regression protection)
  ├─ INTENT_ANCHORS.md (architectural constraints)
  └─ ACTIVE_PLAN.md (task context)

Level 3: Generated Document
  └─ AI_EXECUTION_CONSTRAINTS.md (consolidated reference)

Level 4 (Lowest): Chat Conversation
  └─ Transient context, not authoritative
```

**Rule:** Generated document is a **summary and convenience reference**. If conflict exists, authoritative sources win.

---

## 4. Dynamic Prompt Generation Mechanism

### 4.1 Generation Triggers

**Manual Triggers:**
- Human operator runs script before new chat session
- Human operator runs script after state/flag changes
- CI/CD pipeline includes generation step

**Automatic Triggers (Future):**
- Pre-commit hook detects state/flag changes
- State transition scripts auto-regenerate
- Flag modification scripts auto-regenerate

### 4.2 Extraction Mechanisms

#### 4.2.1 Absolute Invariants Extraction

**Source:** `AI_ORCHESTRATION_META_FRAMEWORK.md` Section 2

**Method:** Regex pattern matching

**Pattern:**
```regex
## 2\. ABSOLUTE INVARIANTS.*?## 3\.
```

**Extraction:**
```regex
^\d+\.\s+AI\s+\*\*may not\s+(.+?)\*\*
```

**Result:** Array of invariant descriptions (e.g., "infer state", "execute commands")

**Rationale:**
- Invariants are numbered list items
- Consistent format enables reliable extraction
- Section boundaries prevent false matches

#### 4.2.2 Flag State Parsing

**Source:** `control/FLAGS.yaml`

**Method:** YAML parsing with regex fallback

**Pattern:**
```regex
^\s+([A-Z_]+):\s*(true|false)
```

**Result:** Hash table mapping flag names to boolean values

**Categorization:**
- **Active Permissions:** Flags where value = true
- **Blocked Permissions:** Flags where value = false

**Rationale:**
- YAML structure is predictable
- Boolean values enable clear categorization
- Flag names are uppercase with underscores (consistent)

#### 4.2.3 State Context Parsing

**Source:** `control/STATE_POINTER.yaml`

**Method:** Line-by-line parsing with indentation awareness

**Patterns:**
```regex
^state:\s*(\d+)(\s|$|#)           # Top-level only
^subtask:\s*([\d.]+)(\s|$|#)      # Top-level only
^last_verified:\s*([\d.]+)(\s|$|#) # Top-level only
^next:\s*([\d.]+)(\s|$|#)         # Top-level only
blocking_issues:\s*\[(.*?)\]      # Array parsing
```

**Result:** State object with:
- `State`: Current state number
- `Subtask`: Current subtask (e.g., "6.2")
- `LastVerified`: Last verified subtask
- `Next`: Next task to execute
- `BlockingIssues`: Array of blocking issue descriptions

**Rationale:**
- Indentation awareness prevents matching nested values
- State history section explicitly skipped
- Array parsing handles comma-separated values

#### 4.2.4 Never Rules Extraction

**Source:** `control/NEVER_RULES.md`

**Method:** Category-based section extraction

**Pattern:**
```regex
## (.+?) Never Rules\s*\n(.*?)(?=\n##|\Z)
```

**Rule Extraction:**
```regex
^\s*-\s*\*\*(.+?)\*\*
```

**Result:** Array of rules with category prefix (e.g., "Security: Never expose management services")

**Sampling:** First 15 rules shown, remainder referenced

**Rationale:**
- Category organization enables structured extraction
- Sampling prevents document bloat
- Category prefix provides context

#### 4.2.5 Key Invariants Extraction

**Source:** `control/INVARIANTS.md`

**Method:** Category-based section extraction (same as never rules)

**Pattern:**
```regex
## (.+?) Invariants\s*\n(.*?)(?=\n##|\Z)
```

**Invariant Extraction:**
```regex
^\s*-\s*\*\*(.+?)\*\*
```

**Result:** Array of invariants with category prefix

**Sampling:** First 12 invariants shown, remainder referenced

**Rationale:**
- Same structure as never rules enables reuse
- Category prefix provides context
- Sampling balances completeness with brevity

#### 4.2.6 Intent Anchors Extraction

**Source:** `control/INTENT_ANCHORS.md`

**Method:** Section-based extraction with content aggregation

**Pattern:**
```regex
## (.+? Intent)\s*\n(.*?)(?=\n##|\Z)
```

**Content Extraction:**
```regex
^\s*-\s*\*\*(.+?)\*\*
```

**Result:** Array of anchor objects with:
- `Title`: Section title (e.g., "DNS Architecture Intent")
- `Content`: Semicolon-separated list of intent points

**Rationale:**
- Intent anchors are architectural constraints
- Aggregation provides concise representation
- Section titles provide context

#### 4.2.7 Framework Tools Discovery

**Source:** `scripts/framework/` directory

**Method:** File system scan with description extraction

**Process:**
1. Scan directory for `*.ps1` files
2. Read first 5 lines of each file
3. Extract description from first comment line (non-encoding)
4. Build tool list with name and description

**Pattern:**
```regex
#\s+(.+)
```

**Result:** Array of tool objects with:
- `Name`: Script filename
- `Description`: Extracted description or default

**Rationale:**
- Framework tools are enforcement mechanisms
- Description extraction provides context
- File system scan is reliable and fast

### 4.3 Document Assembly

**Template Structure:**
```markdown
# AI Execution Constraints - Auto-Generated

**Generated:** {timestamp}
**Authority:** AI_ORCHESTRATION_META_FRAMEWORK.md
**Purpose:** Consolidated constraint context for AI chat sessions

## Current State Context
{state information}

## Absolute Invariants (Non-Negotiable)
{numbered list of invariants}

## Current Flag States
{enabled flags}
{disabled flags}

## Never Rules (Critical Constraints)
{sampled rules with reference}

## Key Invariants
{sampled invariants with reference}

## Intent Anchors (Architectural Constraints)
{anchor sections}

## Enforcement Tools Available
{tool list}

## Current Task Context
{active plan excerpt}

## Reference Documents
{authoritative source list}

## Usage Instructions
{usage guidance}
```

**Assembly Process:**
1. Generate timestamp
2. Populate state context section
3. Format absolute invariants as numbered list
4. Categorize and format flags (enabled/disabled)
5. Sample and format never rules (first 15)
6. Sample and format key invariants (first 12)
7. Format intent anchors by section
8. List framework tools with descriptions
9. Extract and format active plan context
10. Add reference document list
11. Add usage instructions

**Rationale:**
- Consistent structure enables AI pattern recognition
- Sections ordered by importance (state → invariants → rules → tools)
- Sampling prevents token bloat while maintaining completeness
- References point to authoritative sources

---

## 5. Use Cases & Scenarios

### 5.1 Use Case: New Chat Session Initialization

**Scenario:** Human operator starts new AI chat session

**Workflow:**
1. Operator runs: `.\scripts\framework\generate_prompt_constraints.ps1`
2. Generator creates/updates `AI_EXECUTION_CONSTRAINTS.md`
3. Operator includes in prompt: "Please read AI_EXECUTION_CONSTRAINTS.md first, then [task]"
4. AI loads document and understands:
   - Current state (6.2)
   - Enabled permissions (autonomous execution, etc.)
   - Blocked permissions (meta-framework edits, etc.)
   - Critical constraints (never rules, invariants)
   - Available enforcement tools
   - Current task context

**Benefits:**
- AI starts with complete constraint awareness
- No need to read 7+ source files
- Consistent behavior across sessions
- State-aware from session start

### 5.2 Use Case: State Transition

**Scenario:** Task completed, state advances from 6.2 → 6.3

**Workflow:**
1. State transition script updates `control/STATE_POINTER.yaml`
2. Operator (or script) regenerates constraints: `.\scripts\framework\generate_prompt_constraints.ps1`
3. Generated document reflects new state (6.3)
4. Next chat session uses updated state context
5. AI knows:
   - Current state is 6.3 (not stale 6.2)
   - Next task is 6.4
   - Blocking issues (if any)

**Benefits:**
- AI always has current state
- No state inference required (invariant compliance)
- Task context always accurate

### 5.3 Use Case: Flag Permission Change

**Scenario:** Human enables `ALLOW_EDIT_META_FRAMEWORK` for framework update

**Workflow:**
1. Human edits `control/FLAGS.yaml`: `ALLOW_EDIT_META_FRAMEWORK: true`
2. Human regenerates constraints: `.\scripts\framework\generate_prompt_constraints.ps1`
3. Generated document shows flag as "Enabled" in Active Permissions
4. AI sees permission is enabled
5. AI can proceed with meta-framework edit (with ADR, etc.)
6. After edit, human disables flag and regenerates

**Benefits:**
- AI knows current permissions without reading FLAGS.yaml
- Permission changes immediately reflected
- Clear visibility into what's allowed/blocked

### 5.4 Use Case: Constraint Reference During Chat

**Scenario:** AI needs to check if operation is allowed

**Workflow:**
1. AI considers operation (e.g., skip verification step)
2. AI checks `AI_EXECUTION_CONSTRAINTS.md`:
   - Sees "Never Rules: Never remove verification gates"
   - Sees "ALLOW_TASK_SKIP: Disabled"
   - Sees "Absolute Invariants: AI may not skip steps"
3. AI determines operation is blocked
4. AI explains why operation cannot proceed

**Benefits:**
- Single reference point for constraint checking
- No need to search multiple files
- Fast constraint validation

### 5.5 Use Case: Enforcement Tool Discovery

**Scenario:** AI needs to validate a change before proceeding

**Workflow:**
1. AI checks "Enforcement Tools Available" section
2. AI sees: `validate_framework.ps1: Framework Validator`
3. AI runs: `.\scripts\framework\validate_framework.ps1`
4. Tool validates change against constraints
5. AI proceeds or blocks based on validation result

**Benefits:**
- AI discovers available tools automatically
- Tool descriptions provide context
- No manual tool discovery required

### 5.6 Use Case: Long-Running Chat Session

**Scenario:** Chat session spans multiple hours, state changes mid-session

**Workflow:**
1. Chat session starts with state 6.2
2. AI loads `AI_EXECUTION_CONSTRAINTS.md` (state 6.2)
3. Mid-session, human completes task, advances to 6.3
4. Human regenerates constraints
5. AI detects state change (or human notifies)
6. AI reloads `AI_EXECUTION_CONSTRAINTS.md` (state 6.3)
7. AI continues with updated context

**Benefits:**
- AI can refresh context mid-session
- No need to restart chat
- State changes don't cause constraint violations

---

## 6. Usage Patterns

### 6.1 Human Operator Pattern

**Before New Chat:**
```powershell
# Generate fresh constraints
.\scripts\framework\generate_prompt_constraints.ps1

# Start chat with constraint reference
# Prompt: "Please read AI_EXECUTION_CONSTRAINTS.md first, then [task]"
```

**After State Change:**
```powershell
# Update state (via state manager or manual edit)
# Then regenerate constraints
.\scripts\framework\generate_prompt_constraints.ps1
```

**After Flag Change:**
```powershell
# Edit control/FLAGS.yaml
# Then regenerate constraints
.\scripts\framework\generate_prompt_constraints.ps1
```

### 6.2 AI Agent Pattern

**Session Initialization:**
```
1. Load AI_EXECUTION_CONSTRAINTS.md
2. Parse current state context
3. Understand enabled/disabled permissions
4. Note critical constraints (never rules, invariants)
5. Identify available enforcement tools
6. Review current task context
```

**During Session:**
```
1. Reference constraints before operations
2. Check flag states before attempting operations
3. Use enforcement tools for validation
4. Regenerate constraints if state/flags change
5. Reference authoritative sources for details
```

**Constraint Checking:**
```
IF operation_considered:
    CHECK AI_EXECUTION_CONSTRAINTS.md:
        IF violates_absolute_invariant:
            BLOCK operation
            EXPLAIN violation
        ELIF violates_never_rule:
            BLOCK operation
            EXPLAIN violation
        ELIF blocked_by_flag:
            BLOCK operation
            EXPLAIN flag state
        ELIF conflicts_with_intent_anchor:
            FLAG conflict
            REQUIRE ADR
        ELSE:
            PROCEED with operation
```

### 6.3 CI/CD Integration Pattern

**Pre-Commit Hook:**
```powershell
# Check if constraints are stale
$constraintsFile = "AI_EXECUTION_CONSTRAINTS.md"
$stateFile = "control/STATE_POINTER.yaml"

$constraintsTime = (Get-Item $constraintsFile).LastWriteTime
$stateTime = (Get-Item $stateFile).LastWriteTime

IF ($stateTime -gt $constraintsTime):
    WARN "Constraints may be stale, regenerate before commit"
    OPTIONALLY: Auto-regenerate
```

**CI Pipeline:**
```yaml
steps:
  - name: Generate Constraints
    run: .\scripts\framework\generate_prompt_constraints.ps1

  - name: Validate Constraints
    run: .\scripts\framework\validate_framework.ps1
```

---

## 7. Implementation Details

### 7.1 Generator Script Structure

**File:** `scripts/framework/generate_prompt_constraints.ps1`

**Key Functions:**

```powershell
# File reading with error handling
function Read-FileContent {
    param([string]$Path, [string]$Description)
    # Returns file content or null with warning
}

# Invariant extraction from meta framework
function Extract-AbsoluteInvariants {
    param([string]$MetaFrameworkContent)
    # Returns array of invariant descriptions
}

# Flag parsing from YAML
function Parse-Flags {
    param([string]$FlagsContent)
    # Returns hash table of flag states
}

# State parsing from YAML
function Parse-StatePointer {
    param([string]$StateContent)
    # Returns state object with current/next/blocking
}

# Rule extraction from markdown
function Extract-NeverRules {
    param([string]$NeverRulesContent)
    # Returns array of categorized rules
}

# Invariant extraction from markdown
function Extract-KeyInvariants {
    param([string]$InvariantsContent)
    # Returns array of categorized invariants
}

# Intent anchor extraction
function Extract-IntentAnchors {
    param([string]$IntentContent)
    # Returns array of anchor objects
}

# Tool discovery
function Get-FrameworkTools {
    param([string]$FrameworkDir)
    # Returns array of tool objects
}

# Main generation function
function Generate-ConstraintDocument {
    # Orchestrates all extraction and assembly
    # Returns generation result
}
```

### 7.2 Error Handling

**Missing Files:**
- Generator warns but continues
- Missing sections result in empty arrays/objects
- Generated document indicates missing sources

**Parse Failures:**
- Regex failures result in empty extractions
- YAML parse failures use regex fallback
- Errors logged but don't stop generation

**Rationale:**
- Graceful degradation prevents generation failure
- Missing data is better than no document
- Warnings alert to configuration issues

### 7.3 Output Formatting

**Markdown Structure:**
- Consistent heading hierarchy
- Bullet lists for rules/invariants
- Code blocks for references
- Bold for emphasis
- Horizontal rules for section separation

**Sampling Strategy:**
- Never rules: First 15 shown
- Key invariants: First 12 shown
- Remainder referenced with count
- Prevents document bloat while maintaining completeness

**Timestamp:**
- ISO format: `yyyy-MM-dd HH:mm:ss`
- Enables staleness detection
- Provides generation audit trail

---

## 8. Examples & Pseudo Code

### 8.1 Complete Generation Pseudo Code

```pseudocode
FUNCTION Generate-ConstraintDocument():
    // Initialize
    timestamp = GetCurrentTimestamp()
    rootDir = GetProjectRoot()
    controlDir = JoinPath(rootDir, "control")
    frameworkDir = JoinPath(rootDir, "scripts/framework")
    outputPath = JoinPath(rootDir, "AI_EXECUTION_CONSTRAINTS.md")

    // Read source files
    metaFramework = ReadFile(JoinPath(rootDir, "AI_ORCHESTRATION_META_FRAMEWORK.md"))
    flagsContent = ReadFile(JoinPath(controlDir, "FLAGS.yaml"))
    stateContent = ReadFile(JoinPath(controlDir, "STATE_POINTER.yaml"))
    neverRulesContent = ReadFile(JoinPath(controlDir, "NEVER_RULES.md"))
    invariantsContent = ReadFile(JoinPath(controlDir, "INVARIANTS.md"))
    intentContent = ReadFile(JoinPath(controlDir, "INTENT_ANCHORS.md"))
    activePlanContent = ReadFile(JoinPath(controlDir, "ACTIVE_PLAN.md"))

    // Extract data
    absoluteInvariants = Extract-AbsoluteInvariants(metaFramework)
    flagStates = Parse-Flags(flagsContent)
    currentState = Parse-StatePointer(stateContent)
    neverRules = Extract-NeverRules(neverRulesContent)
    keyInvariants = Extract-KeyInvariants(invariantsContent)
    intentAnchors = Extract-IntentAnchors(intentContent)
    frameworkTools = Get-FrameworkTools(frameworkDir)

    // Generate markdown
    document = BuildMarkdownTemplate({
        timestamp: timestamp,
        state: currentState,
        invariants: absoluteInvariants,
        flags: flagStates,
        neverRules: Sample(neverRules, 15),
        invariants: Sample(keyInvariants, 12),
        anchors: intentAnchors,
        tools: frameworkTools,
        activePlan: ExtractActivePlanContext(activePlanContent)
    })

    // Write output
    WriteFile(outputPath, document)

    RETURN {
        success: true,
        outputPath: outputPath,
        timestamp: timestamp
    }
END FUNCTION
```

### 8.2 Invariant Extraction Pseudo Code

```pseudocode
FUNCTION Extract-AbsoluteInvariants(metaFrameworkContent):
    invariants = []

    // Match section 2
    IF metaFrameworkContent MATCHES "## 2\. ABSOLUTE INVARIANTS.*?## 3\.":
        invariantSection = MATCH[0]
        lines = SplitLines(invariantSection)

        FOR EACH line IN lines:
            // Match: "1. AI **may not infer state**"
            IF line MATCHES "^\d+\.\s+AI\s+\*\*may not\s+(.+?)\*\*":
                invariantText = MATCH[1]  // "infer state"
                invariants.APPEND(invariantText)
            END IF
        END FOR
    END IF

    RETURN invariants
END FUNCTION
```

### 8.3 Flag Parsing Pseudo Code

```pseudocode
FUNCTION Parse-Flags(flagsContent):
    flags = {}

    IF flagsContent IS NOT NULL:
        lines = SplitLines(flagsContent)

        FOR EACH line IN lines:
            // Match: "  ALLOW_AUTONOMOUS_EXECUTION: true"
            IF line MATCHES "^\s+([A-Z_]+):\s*(true|false)":
                flagName = MATCH[1]      // "ALLOW_AUTONOMOUS_EXECUTION"
                flagValue = MATCH[2]     // "true"
                flags[flagName] = (flagValue == "true")
            END IF
        END FOR
    END IF

    RETURN flags
END FUNCTION
```

### 8.4 State Parsing Pseudo Code

```pseudocode
FUNCTION Parse-StatePointer(stateContent):
    state = {
        State: "",
        Subtask: "",
        LastVerified: "",
        Next: "",
        BlockingIssues: []
    }

    IF stateContent IS NOT NULL:
        lines = SplitLines(stateContent)
        inStateHistory = false

        FOR EACH line IN lines:
            originalLine = line
            trimmed = Trim(line)

            // Skip state_history section
            IF trimmed MATCHES "^state_history:":
                inStateHistory = true
                CONTINUE
            END IF

            IF inStateHistory AND trimmed MATCHES "^\w+:":
                inStateHistory = false
            END IF

            IF inStateHistory:
                CONTINUE
            END IF

            // Match top-level keys only (not indented)
            IF NOT StartsWith(originalLine, "  ") AND NOT StartsWith(originalLine, "    "):
                IF trimmed MATCHES "^state:\s*(\d+)(\s|$|#)":
                    IF state.State == "":
                        state.State = MATCH[1]
                    END IF
                ELIF trimmed MATCHES "^subtask:\s*([\d.]+)(\s|$|#)":
                    IF state.Subtask == "":
                        state.Subtask = MATCH[1]
                    END IF
                ELIF trimmed MATCHES "^last_verified:\s*([\d.]+)(\s|$|#)":
                    IF state.LastVerified == "":
                        state.LastVerified = MATCH[1]
                    END IF
                ELIF trimmed MATCHES "^next:\s*([\d.]+)(\s|$|#)":
                    IF state.Next == "":
                        state.Next = MATCH[1]
                    END IF
                END IF
            END IF
        END FOR

        // Parse blocking issues array
        IF stateContent MATCHES "blocking_issues:\s*\[(.*?)\]":
            issuesString = MATCH[1]
            issues = Split(issuesString, ",")
            state.BlockingIssues = Filter(Trim(issues), NOT EMPTY)
        END IF
    END IF

    RETURN state
END FUNCTION
```

### 8.5 Document Assembly Pseudo Code

```pseudocode
FUNCTION BuildMarkdownTemplate(data):
    document = ""

    // Header
    document += "# AI Execution Constraints - Auto-Generated\n\n"
    document += "**Generated:** " + data.timestamp + "\n"
    document += "**Authority:** `AI_ORCHESTRATION_META_FRAMEWORK.md`\n"
    document += "**Purpose:** Consolidated constraint context for AI chat sessions\n\n"

    // State Context
    document += "## Current State Context\n\n"
    document += "**Current State:** " + data.state.State + "." + data.state.Subtask + "\n"
    document += "**Last Verified:** " + data.state.LastVerified + "\n"
    document += "**Next Task:** " + data.state.Next + "\n\n"

    IF data.state.BlockingIssues.COUNT > 0:
        document += "**Blocking Issues:** " + Join(data.state.BlockingIssues, ", ") + "\n"
    ELSE:
        document += "**Blocking Issues:** None\n"
    END IF

    document += "\n---\n\n"

    // Absolute Invariants
    document += "## Absolute Invariants (Non-Negotiable)\n\n"
    document += "These rules **may not be removed, weakened, or bypassed**. Violation → **hard stop**.\n\n"

    index = 1
    FOR EACH invariant IN data.invariants:
        document += index + ". AI **may not " + invariant + "**\n"
        index++
    END FOR

    document += "\n**Reference:** Section 2 of `AI_ORCHESTRATION_META_FRAMEWORK.md`\n\n---\n\n"

    // Flag States
    document += "## Current Flag States\n\n"
    document += "**Active Permissions:**\n\n"

    FOR EACH flag IN data.flags WHERE flag.Value == true:
        document += "- **" + flag.Key + "**: Enabled\n"
    END FOR

    document += "\n**Blocked Permissions:**\n\n"

    FOR EACH flag IN data.flags WHERE flag.Value == false:
        document += "- **" + flag.Key + "**: Disabled\n"
    END FOR

    document += "\n**Reference:** `control/FLAGS.yaml`\n\n---\n\n"

    // Never Rules (sampled)
    document += "## Never Rules (Critical Constraints)\n\n"
    document += "These constraints apply **even in sandbox mode**.\n\n"

    sampledRules = data.neverRules.TAKE(15)
    FOR EACH rule IN sampledRules:
        document += "- " + rule + "\n"
    END FOR

    IF data.neverRules.COUNT > 15:
        remaining = data.neverRules.COUNT - 15
        document += "\n*... and " + remaining + " more (see `control/NEVER_RULES.md` for complete list)*\n"
    END IF

    document += "\n**Reference:** `control/NEVER_RULES.md`\n\n---\n\n"

    // Key Invariants (sampled)
    document += "## Key Invariants\n\n"
    document += "Regression protection rules that must always be true.\n\n"

    sampledInvariants = data.invariants.TAKE(12)
    FOR EACH invariant IN sampledInvariants:
        document += "- " + invariant + "\n"
    END FOR

    IF data.invariants.COUNT > 12:
        remaining = data.invariants.COUNT - 12
        document += "\n*... and " + remaining + " more (see `control/INVARIANTS.md` for complete list)*\n"
    END IF

    document += "\n**Reference:** `control/INVARIANTS.md`\n\n---\n\n"

    // Intent Anchors
    document += "## Intent Anchors (Architectural Constraints)\n\n"
    document += "If a change conflicts with an intent anchor, AI must:\n"
    document += "1. Explicitly flag the conflict\n"
    document += "2. Require ADR (Architecture Decision Record)\n"
    document += "3. Cannot proceed silently\n\n"

    FOR EACH anchor IN data.anchors:
        document += "### " + anchor.Title + "\n"
        document += anchor.Content + "\n\n"
    END FOR

    document += "**Reference:** `control/INTENT_ANCHORS.md`\n\n---\n\n"

    // Enforcement Tools
    document += "## Enforcement Tools Available\n\n"
    document += "Framework scripts available for validation and enforcement:\n\n"

    FOR EACH tool IN data.tools:
        document += "- **" + tool.Name + "**: " + tool.Description + "\n"
    END FOR

    document += "\n**Location:** `scripts/framework/`\n\n"
    document += "**Usage:** Run scripts with `-Verbose` for detailed output, or `-Help` for usage information.\n\n---\n\n"

    // Task Context
    document += "## Current Task Context\n\n"
    document += data.activePlan + "\n\n"
    document += "**Reference:** `control/ACTIVE_PLAN.md`\n\n---\n\n"

    // Reference Documents
    document += "## Reference Documents\n\n"
    document += "For complete details, see:\n\n"
    document += "1. **`AI_ORCHESTRATION_META_FRAMEWORK.md`** - Root authority, all rules and philosophy\n"
    document += "2. **`control/FLAGS.yaml`** - Current feature flags and permissions\n"
    document += "3. **`control/STATE_POINTER.yaml`** - Current state and progress\n"
    document += "4. **`control/NEVER_RULES.md`** - Complete list of never rules\n"
    document += "5. **`control/INVARIANTS.md`** - Complete list of invariants\n"
    document += "6. **`control/INTENT_ANCHORS.md`** - Complete architectural intents\n"
    document += "7. **`control/ACTIVE_PLAN.md`** - Current task plan and status\n"
    document += "8. **`control/WORKFLOW_RULES.yaml`** - Workflow enforcement rules\n\n---\n\n"

    // Usage Instructions
    document += "## Usage Instructions\n\n"
    document += "**For AI Agents:**\n"
    document += "1. Load this document first in new chat sessions\n"
    document += "2. Reference authoritative documents for complete details\n"
    document += "3. Use enforcement tools listed above for validation\n"
    document += "4. Regenerate this document if state/flags change during session\n\n"
    document += "**For Human Operators:**\n"
    document += "- Regenerate before starting new chat: `.\scripts\framework\generate_prompt_constraints.ps1`\n"
    document += "- Regenerate after state transitions or flag changes\n"
    document += "- Include in prompt: \"Please read AI_EXECUTION_CONSTRAINTS.md first, then [task]\"\n\n---\n\n"

    // Footer
    document += "**Last Generated:** " + data.timestamp + "\n"
    document += "**Generator:** `scripts/framework/generate_prompt_constraints.ps1`\n"

    RETURN document
END FUNCTION
```

### 8.6 AI Usage Pattern Pseudo Code

```pseudocode
FUNCTION AI-ChatSession-Initialize():
    // Load constraint document
    constraints = ReadFile("AI_EXECUTION_CONSTRAINTS.md")

    // Parse key information
    currentState = ParseState(constraints)
    enabledFlags = ParseEnabledFlags(constraints)
    disabledFlags = ParseDisabledFlags(constraints)
    absoluteInvariants = ParseAbsoluteInvariants(constraints)
    neverRules = ParseNeverRules(constraints)
    availableTools = ParseEnforcementTools(constraints)

    // Store in session context
    SessionContext = {
        state: currentState,
        enabledFlags: enabledFlags,
        disabledFlags: disabledFlags,
        invariants: absoluteInvariants,
        neverRules: neverRules,
        tools: availableTools
    }

    RETURN SessionContext
END FUNCTION

FUNCTION AI-CheckOperation(operation):
    // Check against constraints

    // 1. Check absolute invariants
    FOR EACH invariant IN SessionContext.invariants:
        IF operation.Violates(invariant):
            RETURN {
                allowed: false,
                reason: "Violates absolute invariant: " + invariant,
                severity: "HARD_STOP"
            }
        END IF
    END FOR

    // 2. Check never rules
    FOR EACH rule IN SessionContext.neverRules:
        IF operation.Violates(rule):
            RETURN {
                allowed: false,
                reason: "Violates never rule: " + rule,
                severity: "HARD_STOP"
            }
        END IF
    END FOR

    // 3. Check flag permissions
    requiredFlags = operation.RequiredFlags()
    FOR EACH flag IN requiredFlags:
        IF flag NOT IN SessionContext.enabledFlags:
            RETURN {
                allowed: false,
                reason: "Operation requires flag: " + flag + " (currently disabled)",
                severity: "BLOCKED"
            }
        END IF
    END FOR

    // 4. Check state context
    IF operation.RequiresState() AND operation.State != SessionContext.state.State:
        RETURN {
            allowed: false,
            reason: "Operation requires state " + operation.State + " (current: " + SessionContext.state.State + ")",
            severity: "BLOCKED"
        }
    END IF

    // 5. All checks passed
    RETURN {
        allowed: true,
        reason: "Operation complies with all constraints",
        severity: "ALLOWED"
    }
END FUNCTION
```

---

## 9. Integration Points

### 9.1 Framework Integration

**Status Check Integration:**
- `framework_status.ps1` includes constraint freshness check
- Warns if constraints are stale relative to state file

**Validation Integration:**
- `validate_framework.ps1` can validate generated document
- Ensures all sections present and properly formatted

**State Management Integration:**
- State transition scripts can auto-regenerate constraints
- Ensures constraints always reflect current state

### 9.2 Pre-Commit Hook Integration

**Staleness Detection:**
```powershell
# Check if constraints are stale
$constraintsFile = "AI_EXECUTION_CONSTRAINTS.md"
$stateFile = "control/STATE_POINTER.yaml"

IF (Test-Path $constraintsFile) AND (Test-Path $stateFile):
    $constraintsTime = (Get-Item $constraintsFile).LastWriteTime
    $stateTime = (Get-Item $stateFile).LastWriteTime

    IF $stateTime -gt $constraintsTime:
        Write-Warning "Constraints may be stale. Regenerate: .\scripts\framework\generate_prompt_constraints.ps1"
    END IF
END IF
```

### 9.3 CI/CD Integration

**Pipeline Step:**
```yaml
- name: Generate AI Constraints
  run: |
    pwsh -File ./scripts/framework/generate_prompt_constraints.ps1

- name: Validate Constraints
  run: |
    pwsh -File ./scripts/framework/validate_framework.ps1
    -ConstraintDocument
```

### 9.4 Documentation Integration

**Workflow Documentation:**
- `docs/PROMPT_CONSTRAINT_WORKFLOW.md` provides usage guide
- Referenced from main meta framework
- Part of project documentation index

---

## 10. Justification & Design Decisions

### 10.1 Why Dynamic Generation vs. Static Document?

**Decision:** Generate document dynamically from source files

**Rationale:**
1. **State Changes:** Project state changes require updated context
2. **Flag Changes:** Permission changes affect what AI can do
3. **Freshness:** Timestamp enables staleness detection
4. **Consistency:** Always reflects current project state
5. **Maintainability:** Single source of truth (source files), not generated document

**Alternative Considered:** Static document manually maintained
- **Rejected:** Prone to drift, requires manual updates, easy to forget

### 10.2 Why Read-Only Generation?

**Decision:** Generator only reads source files, never modifies them

**Rationale:**
1. **Authority Preservation:** Source files remain authoritative
2. **Non-Destructive:** No risk of corrupting source files
3. **Reversibility:** Can regenerate from source at any time
4. **Safety:** Generator failures don't affect source files
5. **Separation of Concerns:** Generation is transformation, not modification

**Alternative Considered:** Generator updates source files
- **Rejected:** Risk of corruption, violates separation of concerns

### 10.3 Why Single Document vs. Multiple Documents?

**Decision:** Consolidate all constraints into single document

**Rationale:**
1. **Token Efficiency:** One document vs. reading 7+ files
2. **Completeness:** All constraints in one place
3. **Consistency:** Same structure every time
4. **AI Optimization:** Structured for immediate comprehension
5. **Convenience:** Single reference point for constraint checking

**Alternative Considered:** Keep constraints in separate files
- **Rejected:** Requires reading multiple files, incomplete awareness risk

### 10.4 Why Sampling vs. Complete Lists?

**Decision:** Sample never rules (15) and invariants (12), reference remainder

**Rationale:**
1. **Token Efficiency:** Prevents document bloat
2. **Completeness:** Most important rules shown
3. **Reference:** Points to authoritative sources for complete lists
4. **Balance:** Completeness vs. token usage

**Alternative Considered:** Include all rules/invariants
- **Rejected:** Document becomes too large, token inefficient

**Alternative Considered:** Include no rules/invariants, only references
- **Rejected:** Defeats purpose of consolidated reference

### 10.5 Why Markdown Format?

**Decision:** Generate markdown document

**Rationale:**
1. **AI Compatibility:** Markdown is well-understood by AI
2. **Human Readable:** Humans can also read and understand
3. **Structured:** Headings, lists, code blocks provide structure
4. **Version Control:** Markdown works well with Git
5. **Tooling:** Wide support for markdown processing

**Alternative Considered:** JSON format
- **Rejected:** Less human-readable, harder for AI to parse naturally

**Alternative Considered:** YAML format
- **Rejected:** Less suitable for narrative text, harder to read

### 10.6 Why Regex Parsing vs. Structured Parsers?

**Decision:** Use regex patterns for extraction where possible

**Rationale:**
1. **Lightweight:** No external dependencies
2. **Fast:** Regex is fast for simple patterns
3. **Portable:** Works across PowerShell versions
4. **Sufficient:** Patterns are predictable and consistent

**Limitations:**
- YAML parsing uses regex fallback (not full YAML parser)
- Markdown parsing uses regex (not full markdown parser)

**Trade-off:** Simplicity and portability vs. robustness

**Alternative Considered:** Full YAML/Markdown parsers
- **Rejected:** Adds dependencies, complexity, but considered for future enhancement

### 10.7 Why Tool Discovery vs. Static List?

**Decision:** Discover framework tools by scanning directory

**Rationale:**
1. **Automatic:** No manual maintenance required
2. **Complete:** Always includes all tools
3. **Descriptive:** Extracts descriptions from script headers
4. **Dynamic:** New tools automatically included

**Alternative Considered:** Static tool list in configuration
- **Rejected:** Requires manual updates, prone to drift

### 10.8 Why Authority References?

**Decision:** Generated document references authoritative sources

**Rationale:**
1. **Clarity:** Makes authority hierarchy explicit
2. **Completeness:** Points to full details in source files
3. **Trust:** AI knows where to find authoritative information
4. **Traceability:** Links generated content to sources

**Implementation:**
- Each section includes "Reference:" pointing to source file
- Document header states authority
- Usage instructions emphasize authoritative sources

---

## 11. Template Adaptation Guide

### 11.1 Core Components to Extract

**For Project Initializer Template:**

1. **Generator Script:**
   - `scripts/framework/generate_prompt_constraints.ps1`
   - Adapt extraction functions to project structure
   - Modify source file paths as needed

2. **Source File Structure:**
   - Meta framework document (or equivalent)
   - Control directory with constraint files
   - State tracking file
   - Flag/permission file

3. **Generated Document Template:**
   - Markdown template structure
   - Section organization
   - Reference format

### 11.2 Adaptation Steps

**Step 1: Identify Constraint Sources**
```
1. List all files containing constraints
2. Categorize by type (invariants, rules, flags, state)
3. Document file formats (YAML, Markdown, etc.)
4. Identify extraction patterns needed
```

**Step 2: Adapt Extraction Functions**
```
1. Modify regex patterns for project-specific formats
2. Adapt YAML parsing for project structure
3. Update file paths and directory structure
4. Test extraction on sample files
```

**Step 3: Customize Document Template**
```
1. Adapt section structure to project needs
2. Modify sampling thresholds (15 rules, 12 invariants)
3. Update reference document list
4. Customize usage instructions
```

**Step 4: Integration Points**
```
1. Identify state management system
2. Find flag/permission management
3. Locate enforcement tools
4. Set up pre-commit hooks (optional)
5. Configure CI/CD integration (optional)
```

### 11.3 Minimal Viable Template

**Required Components:**
- Generator script (adapted)
- At least one constraint source file
- State tracking file (or equivalent)
- Generated document output location

**Optional Components:**
- Multiple constraint source files
- Flag/permission system
- Enforcement tools discovery
- Pre-commit hook integration
- CI/CD integration

### 11.4 Template Customization Points

**File Paths:**
```powershell
# Adapt these paths to project structure
$script:RootDir = Join-Path $PSScriptRoot "..\.."
$script:ControlDir = Join-Path $script:RootDir "control"
$script:FrameworkDir = $script:FrameworkDir
$script:OutputPath = Join-Path $script:RootDir "AI_EXECUTION_CONSTRAINTS.md"
```

**Extraction Patterns:**
```powershell
# Adapt regex patterns to project-specific formats
# Example: If invariants use different format, update pattern
if ($line -match "^\d+\.\s+AI\s+\*\*may not\s+(.+?)\*\*") {
    # Project-specific extraction logic
}
```

**Document Sections:**
```markdown
# Adapt sections to project needs
# Add/remove sections as needed
# Modify sampling thresholds
# Update reference document list
```

### 11.5 Testing Template Adaptation

**Test Cases:**
1. **Generation:** Run generator, verify output created
2. **Extraction:** Verify all constraint sources extracted correctly
3. **State:** Verify state context reflects current state
4. **Flags:** Verify flag states correctly categorized
5. **Sampling:** Verify sampling works (if applicable)
6. **References:** Verify all references point to correct files
7. **Staleness:** Test staleness detection (if implemented)

**Validation:**
```powershell
# Validate generated document
.\scripts\framework\validate_framework.ps1 -ConstraintDocument

# Check for missing sections
# Verify all references valid
# Test AI comprehension (manual review)
```

---

## 12. Conclusion

### 12.1 Key Takeaways

1. **Dynamic Generation:** Constraint document generated from source files, always current
2. **Single Reference:** All constraints in one document for AI chat sessions
3. **State Awareness:** Includes current state, permissions, and task context
4. **Authority Preservation:** Generated document references authoritative sources
5. **AI-Optimized:** Structured for immediate AI comprehension
6. **Template-Ready:** Designed for extraction into project initializer templates

### 12.2 Success Metrics

**Effectiveness Indicators:**
- Reduced constraint violations in AI chat sessions
- Faster AI constraint checking (single document vs. multiple files)
- Consistent behavior across chat sessions
- Current state awareness from session start
- Reduced need for constraint clarification

### 12.3 Future Enhancements

**Potential Improvements:**
1. **Auto-Regeneration:** Automatic regeneration on state/flag changes
2. **Incremental Updates:** Update only changed sections
3. **Validation Integration:** Automated validation of generated document
4. **Staleness Enforcement:** Pre-commit hook enforcement of freshness
5. **Structured Parsers:** Full YAML/Markdown parsers for robustness
6. **Customization:** Configuration file for template customization
7. **Multi-Format Output:** Support JSON/YAML output formats
8. **Diff Generation:** Show what changed since last generation

### 12.4 Final Notes

This system represents a **proven approach** to managing AI constraint awareness in complex projects. The dynamic generation mechanism ensures constraints are always current, while the consolidated format provides efficient reference for AI agents.

**For AI Agents Reading This:**
- This document explains the constraint system you use
- Understand the generation mechanism
- Know when to regenerate constraints
- Reference authoritative sources for details
- Use this as template for other projects

**For Human Operators:**
- Regenerate constraints before new chat sessions
- Regenerate after state/flag changes
- Include constraint document in chat prompts
- Monitor for staleness
- Adapt this system to other projects as needed

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-18  
**Author:** AI Execution Constraints System Documentation  
**Status:** Complete and Ready for Template Extraction
