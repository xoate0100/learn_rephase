# Project Structure Analysis Report

## ✅ Working Correctly

1. **Pre-commit hooks → Scripts**: All hooks correctly reference scripts in `3_bootstrap_scripts/`
2. **Scripts → Config files**: All scripts correctly reference:
   - `0_phase0_bootstrap/feature_flags.yml` ✓
   - `5_reference_architectures/LAYER_RULES.yaml` ✓
   - `6_ai_runtime_context/ACTIVE_PLAN.yaml` ✓
   - `4_docs_index/DOCUMENTATION_INDEX.md` ✓
3. **CI workflows**: Both workflows reference correct script paths
4. **Directory structure**: All required directories exist
5. **Schemas**: JSON schemas properly validate plan structure

## ⚠️ Issues Found

### 1. **Permission Mismatch** (CRITICAL)
**Issue**: `feature_flags.yml` allows writes to `tests/` and `scripts/` but these directories don't exist in the template.
**Location**: `0_phase0_bootstrap/feature_flags.yml` lines 13-15
**Impact**: AI behavior validation will allow writes to non-existent paths
**Fix**: Either create `.gitkeep` files or update permissions to match actual structure

### 2. **Architecture Check Glob Pattern** (CRITICAL)
**Issue**: Line 14 in `architecture_check.py` has broken glob pattern
```python
for p in root.rglob("*.{ts,tsx,js,py,java,cs}".replace("{","").replace("}","").split(",")):
```
This creates invalid patterns like `*.ts`, `*.tsx` which won't match files.
**Location**: `3_bootstrap_scripts/architecture_check.py:14`
**Fix**: Use proper extension matching with tuple/list

### 3. **Duplicate CI Workflows**
**Issue**: Both `8_ci/pr_checks.yml` and `.github/workflows/pr_checks.yml` exist with identical content
**Location**: Both files
**Impact**: Confusion about which workflow is used
**Fix**: Remove one or clarify purpose (8_ci/ is template, .github/workflows/ is active)

### 4. **Missing Python Dependencies**
**Issue**: Scripts use `yaml` module but no requirements.txt exists
**Location**: Multiple scripts import `yaml`
**Impact**: Scripts will fail if PyYAML not installed
**Fix**: Add requirements.txt or handle missing dependencies gracefully

### 5. **Docs Sync References Non-Existent Directory**
**Issue**: `docs_sync.py` creates index referencing `docs/` directory that doesn't exist
**Location**: `3_bootstrap_scripts/docs_sync.py:7`
**Impact**: Index will reference non-existent directory
**Fix**: Update to reference actual component directories only

### 6. **Layer Rules Structure Mismatch**
**Issue**: `LAYER_RULES.yaml` defines layers as array, but `architecture_check.py` expects dict structure
**Location**: `5_reference_architectures/LAYER_RULES.yaml` vs `3_bootstrap_scripts/architecture_check.py:24-27`
**Impact**: Layer rule checking may not work correctly
**Fix**: Align data structure expectations

### 7. **Missing .gitkeep in Scripts Directory**
**Issue**: If `scripts/` directory is expected to exist (per permissions), it should have `.gitkeep`
**Location**: Root directory
**Fix**: Create `scripts/.gitkeep` or remove from permissions

## 🔧 Recommended Fixes

1. Fix architecture check glob pattern
2. Resolve duplicate CI workflows
3. Update permissions to match actual structure
4. Fix layer rules structure alignment
5. Update docs sync to match actual directories
6. Add requirements.txt for Python dependencies

