#!/usr/bin/env python3
"""
Claude Code post_tool_use hook for logging tool execution.
"""

import json
import sys
import os

# Add the parent directory to sys.path to allow importing utils
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hooks.utils.logger import log_json

def main():
    # Read input from stdin (Claude Code passes JSON)
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Error: Could not parse input as JSON", file=sys.stderr)
        sys.exit(1)
    
    # Log the tool execution for observability
    log_file = log_json(input_data, prefix="post_tool_use")
    print(f"Tool execution logged to {log_file}", file=sys.stderr)
    
    # Always exit with success
    sys.exit(0)

if __name__ == "__main__":
    main()
