#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run wrapper for generating-articles-from-docs skill scripts.

Usage:
    python scripts/run.py <script_name> [args]

Examples:
    python scripts/run.py upload.py --source ./docs
    python scripts/run.py planner.py --source "知识库" --count 3
    python scripts/run.py workflow.py --source ./docs --count 3
"""

import sys
import os
import subprocess
from pathlib import Path

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <script_name> [args]")
        print("\nAvailable scripts:")
        print("  upload.py    - Upload documents to data directory")
        print("  planner.py   - Generate article plan from NotebookLM analysis")
        print("  generate.py  - Generate article content")
        print("  workflow.py  - Run complete workflow")
        sys.exit(1)

    script_name = sys.argv[1]
    script_path = SCRIPT_DIR / script_name

    if not script_path.exists():
        print(f"Error: Script not found: {script_name}")
        print(f"Looking in: {SCRIPT_DIR}")
        sys.exit(1)

    # Run the script with remaining arguments
    args = [sys.executable, str(script_path)] + sys.argv[2:]

    result = subprocess.run(args, cwd=SCRIPT_DIR.parent)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
