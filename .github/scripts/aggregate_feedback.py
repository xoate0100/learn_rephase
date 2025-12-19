#!/usr/bin/env python3
"""
Aggregate Feedback Issues
Groups similar feedback issues and tracks patterns.
"""

import json
import os
import re
import sys
from collections import defaultdict
from typing import Any, Dict, List

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = os.environ.get("GITHUB_REPOSITORY", "xoate0100/project_initializer")


def get_feedback_issues() -> List[Dict[str, Any]]:
    """Get all issues with 'feedback' label."""
    url = f"https://api.github.com/repos/{REPO}/issues"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_TOKEN}",
    }
    params = {
        "labels": "feedback",
        "state": "open",
        "per_page": 100,
    }

    issues = []
    page = 1
    while True:
        params["page"] = page
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code != 200:
            break
        page_issues = response.json()
        if not page_issues:
            break
        issues.extend(page_issues)
        page += 1
        if len(page_issues) < 100:
            break

    return issues


def extract_pattern(issue_body: str) -> str:
    """Extract pattern key from issue body."""
    # Look for "Pattern:" or "Issue:" in body
    pattern_match = re.search(r"(?:Pattern|Issue):\s*(.+?)(?:\n|$)", issue_body, re.IGNORECASE)
    if pattern_match:
        pattern = pattern_match.group(1).strip()
        # Normalize: lowercase, remove extra whitespace
        pattern = " ".join(pattern.lower().split()[:10])  # First 10 words
        return pattern
    return "unknown"


def group_issues_by_pattern(issues: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group issues by pattern."""
    grouped = defaultdict(list)
    for issue in issues:
        pattern = extract_pattern(issue.get("body", ""))
        category = None
        for label in issue.get("labels", []):
            if label["name"] not in ["feedback", "auto-generated"]:
                category = label["name"]
                break
        grouped[(pattern, category)].append(issue)
    return grouped


def main():
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN environment variable required")
        sys.exit(1)

    print("Fetching feedback issues...")
    issues = get_feedback_issues()
    print(f"Found {len(issues)} feedback issues")

    grouped = group_issues_by_pattern(issues)
    print(f"Grouped into {len(grouped)} patterns")

    # Save aggregation results
    aggregation = {
        "total_issues": len(issues),
        "patterns": len(grouped),
        "groups": [],
    }

    for (pattern, category), group_issues in grouped.items():
        if len(group_issues) >= 2:  # Only track patterns with 2+ occurrences
            aggregation["groups"].append({
                "pattern": pattern,
                "category": category or "unknown",
                "count": len(group_issues),
                "issue_numbers": [issue["number"] for issue in group_issues],
                "sample_title": group_issues[0].get("title", ""),
            })

    # Save to file for next step
    os.makedirs(".github/feedback_analysis", exist_ok=True)
    with open(".github/feedback_analysis/aggregated_patterns.json", "w") as f:
        json.dump(aggregation, f, indent=2)

    print(f"Identified {len(aggregation['groups'])} patterns with 2+ occurrences")
    print("Aggregation complete. Results saved to .github/feedback_analysis/aggregated_patterns.json")


if __name__ == "__main__":
    main()

