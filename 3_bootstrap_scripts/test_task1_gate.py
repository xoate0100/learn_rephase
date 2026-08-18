#!/usr/bin/env python3
"""Test Task 1 completion gate without Unicode issues."""

import json
import pathlib
import subprocess
import yaml

# Get staged files
result = subprocess.run(
    ["git", "diff", "--cached", "--name-only"],
    capture_output=True,
    text=True,
    encoding="utf-8"
)
staged_files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]

print("Staged files:", staged_files)

# Load plan
plan = yaml.safe_load(open("6_ai_runtime_context/ACTIVE_PLAN.yaml"))
task1 = [t for t in plan["tasks"] if t["id"] == 1][0]
expected_outputs = task1["outputs"]

print("Task 1 expected outputs:", expected_outputs)

# Check each staged file
for file_path in staged_files:
    if file_path.startswith("6_ai_runtime_context/"):
        print(f"OK: {file_path} (runtime file, allowed)")
        continue
    
    if file_path in expected_outputs:
        print(f"OK: {file_path} (in expected outputs)")
    else:
        print(f"FAIL: {file_path} (not in expected outputs)")

# Check if outputs exist
print("\nChecking outputs exist:")
for output in expected_outputs:
    exists = pathlib.Path(output).exists()
    print(f"{'OK' if exists else 'MISSING'}: {output}")
