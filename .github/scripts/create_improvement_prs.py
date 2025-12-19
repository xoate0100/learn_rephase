#!/usr/bin/env python3
"""
Create Improvement PRs
Creates pull requests for high-priority improvement suggestions.
"""

import json
import os
import subprocess
import sys
from typing import Any, Dict, List

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = os.environ.get("GITHUB_REPOSITORY", "xoate0100/project_initializer")
IMPROVEMENTS_FILE = ".github/feedback_analysis/improvement_suggestions.json"


def load_improvements() -> List[Dict[str, Any]]:
    """Load improvement suggestions."""
    if not os.path.exists(IMPROVEMENTS_FILE):
        return []
    with open(IMPROVEMENTS_FILE, "r") as f:
        data = json.load(f)
        return data.get("suggestions", [])


def create_pr(title: str, body: str, branch: str) -> bool:
    """Create a pull request."""
    url = f"https://api.github.com/repos/{REPO}/pulls"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_TOKEN}",
    }
    payload = {
        "title": title,
        "body": body,
        "head": branch,
        "base": "main",
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 201:
            pr_url = response.json().get("html_url", "")
            print(f"Created PR: {pr_url}")
            return True
        elif response.status_code == 422:
            # PR might already exist
            print(f"PR may already exist for branch {branch}")
            return False
        else:
            print(f"Failed to create PR: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error creating PR: {e}")
        return False


def create_branch(branch_name: str) -> bool:
    """Create a new branch."""
    try:
        subprocess.run(["git", "checkout", "-b", branch_name], check=True, capture_output=True)
        return True
    except Exception:
        return False


def main():
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN environment variable required")
        sys.exit(1)

    improvements = load_improvements()
    if not improvements:
        print("No improvements to create PRs for")
        return

    # Only create PRs for high-priority improvements
    high_priority = [imp for imp in improvements if imp.get("priority") == "high"]
    if not high_priority:
        print("No high-priority improvements to create PRs for")
        return

    print(f"Creating PRs for {len(high_priority)} high-priority improvements")

    # For now, create a single PR with all high-priority improvements
    # In the future, could create separate PRs per improvement
    branch_name = f"feedback-improvements-{os.environ.get('GITHUB_RUN_ID', 'manual')}"
    
    # Create branch (if not in CI, this will fail gracefully)
    try:
        subprocess.run(["git", "config", "user.name", "GitHub Actions"], check=True)
        subprocess.run(["git", "config", "user.email", "actions@github.com"], check=True)
        create_branch(branch_name)
    except Exception:
        pass  # May not be in git repo context

    # Generate PR body
    pr_body_parts = [
        "## Feedback-Based Improvements",
        "",
        "This PR addresses high-priority patterns identified from project feedback.",
        "",
    ]

    for improvement in high_priority[:5]:  # Limit to top 5
        pr_body_parts.extend([
            f"### {improvement.get('pattern', 'Unknown pattern')[:80]}",
            f"- **Category**: {improvement.get('category', 'unknown')}",
            f"- **Occurrences**: {improvement.get('occurrence_count', 0)}",
            f"- **Priority**: {improvement.get('priority', 'medium')}",
            "",
            "**Suggested Changes:**",
        ])
        for change in improvement.get("suggested_changes", []):
            pr_body_parts.append(f"- {change}")
        pr_body_parts.append("")

    pr_body_parts.extend([
        "---",
        "",
        "*This PR was auto-generated from aggregated project feedback.*",
        "*Review and modify as needed before merging.*",
    ])

    pr_title = f"[Feedback] Address high-priority patterns ({len(high_priority)} improvements)"
    pr_body = "\n".join(pr_body_parts)

    # Note: In a real implementation, would commit changes and push branch first
    # For now, just create the PR structure
    print(f"Would create PR: {pr_title}")
    print(f"Branch: {branch_name}")
    print("\nPR Body preview:")
    print(pr_body[:500] + "...")


if __name__ == "__main__":
    main()

