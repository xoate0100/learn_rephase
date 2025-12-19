#!/usr/bin/env python3
"""
Setup GitHub Labels for Feedback System
Creates all required labels for the feedback reporting system.
"""

import argparse
import os
import re
import sys
from typing import Dict, List, Optional

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)


# Label definitions with colors and descriptions
LABELS = {
    # Base labels
    "feedback": {
        "color": "1f77b4",  # Blue
        "description": "Feedback from child projects",
    },
    "auto-generated": {
        "color": "ff7f0e",  # Orange
        "description": "Auto-generated issue from feedback system",
    },
    # Category labels (from feedback_collector.py and standardized_feedback.py)
    "guardrail-violation": {
        "color": "d62728",  # Red
        "description": "Guardrail enforcement violation",
    },
    "architecture-violation": {
        "color": "9467bd",  # Purple
        "description": "Architecture or SOLID principle violation",
    },
    "template-drift": {
        "color": "8c564b",  # Brown
        "description": "Template configuration drift detected",
    },
    "update-issue": {
        "color": "e377c2",  # Pink
        "description": "Template update or migration issue",
    },
    "schema-mismatch": {
        "color": "7f7f7f",  # Gray
        "description": "Schema validation mismatch",
    },
    "performance-issue": {
        "color": "bcbd22",  # Yellow-green
        "description": "Performance degradation detected",
    },
    "documentation-gap": {
        "color": "17becf",  # Cyan
        "description": "Missing or incomplete documentation",
    },
    "operational-error": {
        "color": "ff9896",  # Light red
        "description": "Runtime operational error",
    },
    "ai-anomaly": {
        "color": "c5b0d5",  # Light purple
        "description": "AI agent anomaly detected",
    },
    "pattern-detected": {
        "color": "c49c94",  # Light brown
        "description": "Recurring pattern detected in feedback",
    },
}


def get_repo_info(repo_url: str) -> tuple[Optional[str], Optional[str]]:
    """Extract owner and repo from GitHub URL."""
    match = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", repo_url)
    if not match:
        return None, None
    return match.groups()


def create_label(
    owner: str,
    repo: str,
    label_name: str,
    color: str,
    description: str,
    token: str,
) -> bool:
    """Create or update a GitHub label."""
    api_url = f"https://api.github.com/repos/{owner}/{repo}/labels/{label_name}"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}",
    }
    
    payload = {
        "name": label_name,
        "color": color,
        "description": description,
    }
    
    # Try to create label
    response = requests.post(
        f"https://api.github.com/repos/{owner}/{repo}/labels",
        json=payload,
        headers=headers,
        timeout=10,
    )
    
    if response.status_code == 201:
        print(f"  ✓ Created label: {label_name}")
        return True
    elif response.status_code == 401:
        # Authentication failed
        error_data = response.json() if response.text else {}
        error_msg = error_data.get("message", "Bad credentials")
        print(f"  ✗ Authentication failed for {label_name}: {error_msg}")
        print(f"    Check that your token is valid and has 'repo' scope")
        return False
    elif response.status_code == 422:
        # Label already exists, try to update it
        response = requests.patch(
            api_url,
            json=payload,
            headers=headers,
            timeout=10,
        )
        if response.status_code == 200:
            print(f"  ✓ Updated label: {label_name}")
            return True
        else:
            print(f"  ✗ Failed to update label {label_name}: {response.status_code}")
            return False
    else:
        print(f"  ✗ Failed to create label {label_name}: {response.status_code}")
        if response.text:
            try:
                error_data = response.json()
                error_msg = error_data.get("message", response.text[:200])
                print(f"    Error: {error_msg}")
            except:
                print(f"    Error: {response.text[:200]}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="setup_github_labels.py",
        description="Create GitHub labels for feedback system",
    )
    parser.add_argument(
        "--repo",
        default="",
        help="Repository URL (default: from META_FRAMEWORK_VERSION.yaml)",
    )
    parser.add_argument(
        "--github-token",
        default="",
        help="GitHub token (or set GITHUB_TOKEN env var)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without creating",
    )
    
    args = parser.parse_args()
    
    # Get repository URL
    repo_url = args.repo
    if not repo_url:
        # Try to read from version manifest
        try:
            import pathlib
            import yaml
            
            version_file = pathlib.Path("0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml")
            if version_file.exists():
                with open(version_file, "r", encoding="utf-8") as f:
                    manifest = yaml.safe_load(f)
                    repo_url = manifest.get("template_repo", "")
        except Exception:
            pass
    
    if not repo_url:
        print("ERROR: Repository URL required")
        print("Specify --repo or set template_repo in META_FRAMEWORK_VERSION.yaml")
        return 1
    
    owner, repo = get_repo_info(repo_url)
    if not owner or not repo:
        print(f"ERROR: Could not parse repository URL: {repo_url}")
        return 1
    
    print(f"Repository: {owner}/{repo}")
    print(f"Labels to create: {len(LABELS)}")
    print()
    
    # Get GitHub token
    github_token = args.github_token or os.environ.get("GITHUB_TOKEN", "")
    if not github_token:
        print("ERROR: GitHub token required")
        print("Specify --github-token or set GITHUB_TOKEN environment variable")
        print()
        print("To create a token:")
        print("1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)")
        print("2. Generate new token (classic) with 'repo' scope")
        print("3. Use token with --github-token or export GITHUB_TOKEN=your_token")
        print()
        print("Note: Token must have 'repo' scope to create labels")
        return 1
    
    # Validate token by checking if we can access the repo
    print("Validating token...")
    test_url = f"https://api.github.com/repos/{owner}/{repo}"
    test_headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {github_token}",
    }
    test_response = requests.get(test_url, headers=test_headers, timeout=10)
    if test_response.status_code == 401:
        print("ERROR: Token authentication failed")
        print("Possible issues:")
        print("  - Token is expired or invalid")
        print("  - Token doesn't have 'repo' scope")
        print("  - Token was revoked")
        print()
        print("To fix:")
        print("1. Go to GitHub Settings → Developer settings → Personal access tokens")
        print("2. Check if your token exists and has 'repo' scope")
        print("3. If not, create a new token with 'repo' scope")
        return 1
    elif test_response.status_code == 404:
        print("ERROR: Repository not found or not accessible")
        print(f"  Repository: {owner}/{repo}")
        print("  Check that the repository exists and you have access")
        return 1
    elif test_response.status_code != 200:
        print(f"WARN: Token validation returned {test_response.status_code}")
        print("  Continuing anyway...")
    else:
        print("✓ Token validated successfully")
    print()
    
    if args.dry_run:
        print("=== DRY RUN: Would create the following labels ===")
        for label_name, label_info in LABELS.items():
            print(f"  {label_name}")
            print(f"    Color: #{label_info['color']}")
            print(f"    Description: {label_info['description']}")
        return 0
    
    # Create labels
    print("Creating labels...")
    success_count = 0
    for label_name, label_info in LABELS.items():
        if create_label(
            owner,
            repo,
            label_name,
            label_info["color"],
            label_info["description"],
            github_token,
        ):
            success_count += 1
    
    print()
    print(f"Created/updated {success_count}/{len(LABELS)} labels")
    
    if success_count == len(LABELS):
        print("✓ All labels created successfully!")
        return 0
    else:
        print("⚠ Some labels failed to create. Check errors above.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

