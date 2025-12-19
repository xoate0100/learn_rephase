#!/usr/bin/env python3
"""
Generate Improvement Suggestions
Analyzes aggregated feedback patterns and generates improvement suggestions.
"""

import json
import os
import sys
from typing import Any, Dict, List

AGGREGATION_FILE = ".github/feedback_analysis/aggregated_patterns.json"
IMPROVEMENTS_FILE = ".github/feedback_analysis/improvement_suggestions.json"


def load_aggregation() -> Dict[str, Any]:
    """Load aggregated patterns."""
    if not os.path.exists(AGGREGATION_FILE):
        return {"groups": []}
    with open(AGGREGATION_FILE, "r") as f:
        return json.load(f)


def generate_improvement_suggestion(pattern_group: Dict[str, Any]) -> Dict[str, Any]:
    """Generate improvement suggestion from pattern group."""
    pattern = pattern_group.get("pattern", "")
    category = pattern_group.get("category", "unknown")
    count = pattern_group.get("count", 0)

    # Map categories to improvement types
    improvement_type = "enhancement"
    if "violation" in category.lower():
        improvement_type = "fix"
    elif "drift" in category.lower() or "mismatch" in category.lower():
        improvement_type = "fix"
    elif "gap" in category.lower():
        improvement_type = "documentation"

    suggestion = {
        "pattern": pattern,
        "category": category,
        "occurrence_count": count,
        "improvement_type": improvement_type,
        "priority": "high" if count >= 5 else "medium" if count >= 3 else "low",
        "description": f"Address pattern: {pattern} (reported {count} times)",
        "affected_files": [],
        "suggested_changes": [],
    }

    # Generate specific suggestions based on category
    if "guardrail" in category.lower():
        suggestion["suggested_changes"].append(
            "Review guardrail enforcement logic in 3_bootstrap_scripts/guardrail_enforcement.py"
        )
        suggestion["affected_files"].append("3_bootstrap_scripts/guardrail_enforcement.py")
    elif "architecture" in category.lower():
        suggestion["suggested_changes"].append(
            "Review architecture check rules in 3_bootstrap_scripts/architecture_check.py"
        )
        suggestion["affected_files"].append("3_bootstrap_scripts/architecture_check.py")
    elif "drift" in category.lower():
        suggestion["suggested_changes"].append(
            "Update drift detection in scripts/meta_framework_drift_check.py"
        )
        suggestion["affected_files"].append("scripts/meta_framework_drift_check.py")
    elif "documentation" in category.lower():
        suggestion["suggested_changes"].append(
            "Improve documentation clarity in relevant guide files"
        )

    return suggestion


def main():
    aggregation = load_aggregation()
    groups = aggregation.get("groups", [])

    if not groups:
        print("No patterns to generate improvements for")
        return

    improvements = []
    for group in groups:
        if group.get("count", 0) >= 2:  # Only suggest improvements for patterns with 2+ occurrences
            suggestion = generate_improvement_suggestion(group)
            improvements.append(suggestion)

    # Sort by priority and count
    improvements.sort(key=lambda x: (x["priority"] == "high", x["occurrence_count"]), reverse=True)

    result = {
        "generated_at": os.environ.get("GITHUB_SHA", "unknown"),
        "total_suggestions": len(improvements),
        "suggestions": improvements,
    }

    os.makedirs(".github/feedback_analysis", exist_ok=True)
    with open(IMPROVEMENTS_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Generated {len(improvements)} improvement suggestions")
    print(f"Results saved to {IMPROVEMENTS_FILE}")


if __name__ == "__main__":
    main()

