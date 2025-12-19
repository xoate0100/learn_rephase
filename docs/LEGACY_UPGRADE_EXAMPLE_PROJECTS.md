# Legacy Upgrade - Example Projects Analysis

## Overview

This document provides specific upgrade strategies for the example projects provided. Each project has unique characteristics that require tailored handling.

## Example Projects

1. **google-form-generator-cli** - CLI tool
2. **crypto-trading-bot** - Trading bot (Python)
3. **CutRatesLMS** - Learning Management System (full-stack)
4. **AutoBlogAssist** - Blog automation tool

## Project 1: google-form-generator-cli

### Expected Structure

```
google-form-generator-cli/
├── src/ or lib/          # Source code
├── package.json          # Node.js CLI
├── bin/                  # CLI entry point
├── README.md
└── tests/
```

### Upgrade Strategy

**Analysis Phase**:
- Framework: Node.js CLI tool
- Structure: Standard CLI structure
- Language: JavaScript/TypeScript

**Mapping**:
- `src/` or root → `backend/` (CLI is backend-like)
- `bin/` → Preserve (CLI entry point)
- `tests/` → `tests/` (preserved)

**MVP_SPECIFICATION.yaml**:
```yaml
Project: google-form-generator-cli
Architecture: cli
TECH_STACK:
  backend:
    framework: nodejs
    language: typescript  # or javascript
PROJECT_LAYOUT:
  adaptation:
    mode: adopt_existing
  components:
    backend:
      directories: ["src"]  # or ["."] if root-level
```

**Edge Cases**:
- CLI-specific structure (not web app)
- May have custom build/package scripts
- Entry point in `bin/` or `package.json` scripts

**Handling**:
- Map to `backend/` component (CLI tools are backend-like)
- Preserve `bin/` directory
- Preserve package.json scripts
- Document CLI structure in MVP_SPECIFICATION.yaml

## Project 2: crypto-trading-bot

### Expected Structure

```
crypto-trading-bot/
├── src/ or bot/          # Trading logic
├── requirements.txt      # Python dependencies
├── config/               # Trading configuration
├── strategies/           # Trading strategies
├── api/                  # Exchange API clients
└── tests/
```

### Upgrade Strategy

**Analysis Phase**:
- Framework: Python (likely FastAPI or pure Python)
- Structure: Trading bot structure
- Language: Python

**Mapping**:
- `src/` or root → `backend/`
- `strategies/` → Preserve in `backend/`
- `api/` → Preserve in `backend/`
- `config/` → Preserve, document in ENVIRONMENT_AND_CONFIG

**MVP_SPECIFICATION.yaml**:
```yaml
Project: crypto-trading-bot
Architecture: trading-bot
TECH_STACK:
  backend:
    framework: python
    language: python
PROJECT_LAYOUT:
  adaptation:
    mode: adopt_existing
  components:
    backend:
      directories: ["src"]  # or ["."] if root-level
ENVIRONMENT_AND_CONFIG:
  trading_config: "config/"
  api_keys: ".env"
```

**Edge Cases**:
- Trading-specific structure
- API keys and secrets (sensitive)
- Real-time trading logic
- Database for trade history

**Handling**:
- Preserve all trading logic
- Document trading structure
- Keep config/ directory
- Add `.env` to `.gitignore` if not already
- Document API integrations

## Project 3: CutRatesLMS

### Expected Structure

```
CutRatesLMS/
├── frontend/ or client/  # Frontend code
├── backend/ or server/   # Backend API
├── database/            # Database migrations
├── shared/              # Shared types/utilities
├── docs/                # Documentation
└── docker-compose.yml   # Docker setup
```

### Upgrade Strategy

**Analysis Phase**:
- Framework: Full-stack (likely React + Node.js/Python)
- Structure: Monorepo or separate repos
- Language: TypeScript/JavaScript + Python/Node.js

**Mapping**:
- `frontend/` → `frontend/` (perfect match)
- `backend/` → `backend/` (perfect match)
- `shared/` → `shared/` (perfect match)
- `database/` → Preserve, document migrations

**MVP_SPECIFICATION.yaml**:
```yaml
Project: CutRatesLMS
Architecture: full-stack
TECH_STACK:
  frontend:
    framework: react  # or detected framework
    language: typescript
  backend:
    framework: fastapi  # or detected
    language: python
PROJECT_LAYOUT:
  adaptation:
    mode: adopt_existing
  components:
    frontend:
      directories: ["frontend"]
    backend:
      directories: ["backend"]
    shared:
      directories: ["shared"]
```

**Edge Cases**:
- DATABASE_MIGRATIONS: Database migration files
- EXISTING_DOCS: Documentation directory
- DOCKER: Docker configuration
- Full-stack structure (already matches template)

**Handling**:
- Structure already matches template (easy upgrade)
- Preserve database migrations
- Preserve docs/, add 4_docs_index/ for meta-framework
- Preserve Docker setup
- Document in MVP_SPECIFICATION.yaml

## Project 4: AutoBlogAssist

### Expected Structure

```
AutoBlogAssist/
├── app/ or src/          # Application code
├── components/           # React components (if Next.js)
├── pages/ or app/        # Next.js pages/app
├── api/                  # API routes
├── lib/                  # Utilities
└── public/               # Static assets
```

### Upgrade Strategy

**Analysis Phase**:
- Framework: Next.js (likely) or React
- Structure: Next.js App Router or Pages Router
- Language: TypeScript

**Mapping**:
- `app/` or `pages/` → `frontend/` (Next.js root)
- `components/` → Preserve in `frontend/`
- `api/` → Preserve (Next.js API routes)
- `lib/` → Map to `shared/` or preserve in `frontend/`

**MVP_SPECIFICATION.yaml**:
```yaml
Project: AutoBlogAssist
Architecture: nextjs
TECH_STACK:
  frontend:
    framework: nextjs
    language: typescript
PROJECT_LAYOUT:
  adaptation:
    mode: adopt_existing
  components:
    frontend:
      directories: ["."]  # Next.js root structure
```

**Edge Cases**:
- Next.js App Router or Pages Router
- API routes in `app/api/` or `pages/api/`
- Static assets in `public/`
- May have blog-specific structure

**Handling**:
- Preserve Next.js structure (don't force frontend/backend split)
- Use `adaptation.mode: adopt_existing`
- Map root to `frontend/` component
- Preserve API routes
- Document Next.js-specific structure

## Common Patterns

### Pattern 1: CLI Tools

**Detection**: `bin/` directory, CLI entry in package.json

**Strategy**:
- Map to `backend/` component
- Preserve CLI structure
- Document as CLI tool

### Pattern 2: Next.js Projects

**Detection**: `next.config.js`, `app/` or `pages/` directory

**Strategy**:
- Use `adaptation.mode: adopt_existing`
- Map root to `frontend/`
- Preserve Next.js structure
- Don't force frontend/backend split

### Pattern 3: Python Backends

**Detection**: `requirements.txt`, `main.py` or `app.py`

**Strategy**:
- Map to `backend/`
- Preserve Python structure
- Keep requirements.txt
- Document framework (FastAPI, Django, etc.)

### Pattern 4: Full-Stack (Already Structured)

**Detection**: `frontend/` and `backend/` already exist

**Strategy**:
- Perfect match! Easy upgrade
- Use existing structure
- Just add meta-framework

## Upgrade Checklist

For each project:

- [ ] Run analysis phase
- [ ] Review framework detection
- [ ] Verify structure mapping
- [ ] Check edge cases
- [ ] Review upgrade plan
- [ ] Execute upgrade
- [ ] Validate upgrade
- [ ] Test project still works
- [ ] Commit changes

## AI Agent Workflow

1. **Clone project** (if not already)
2. **Run analysis**: `upgrade-legacy --analyze`
3. **Review analysis**: Check `UPGRADE_ANALYSIS.yaml`
4. **Generate plan**: `upgrade-legacy --plan`
5. **Review plan**: Check `UPGRADE_PLAN.yaml`, adjust if needed
6. **Execute**: `upgrade-legacy --execute --template-repo <url>`
7. **Validate**: `upgrade-legacy --validate`
8. **Test**: Ensure project builds and runs
9. **Commit**: Commit changes incrementally

## Notes

- **Preserve everything**: Never delete existing files
- **Document customizations**: Note any unusual structures
- **Test thoroughly**: Ensure functionality preserved
- **Incremental commits**: Commit in logical groups
- **Rollback ready**: Backup branch created automatically

## Summary

Each project requires:
1. **Analysis**: Understand structure and framework
2. **Mapping**: Map to template structure (preserve existing)
3. **Execution**: Add meta-framework alongside
4. **Validation**: Ensure everything works
5. **Documentation**: Document any customizations

The upgrade system handles all edge cases automatically, but review is always recommended.

