#!/usr/bin/env python3
"""
Claude Code pre_tool_use hook for blocking dangerous commands.
"""

import json
import sys
import os

# Add the parent directory to sys.path to allow importing utils
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hooks.utils.speech import is_dangerous_command, is_protected_file_access
from hooks.utils.logger import log_json

def main():
    # Read input from stdin (Claude Code passes JSON)
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Error: Could not parse input as JSON", file=sys.stderr)
        sys.exit(1)
    
    # Log the input for debugging and observability
    log_json(input_data, prefix="pre_tool_use")
    
    # Get tool information
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    
    # Check for dangerous commands
    is_dangerous, reason = is_dangerous_command(tool_name, tool_input)
    if is_dangerous:
        print(f"Command blocked: {reason}", file=sys.stderr)
        # Return a non-zero exit code to indicate the tool should be blocked
        sys.exit(1)
    
    # Check for protected file access
    is_protected, reason = is_protected_file_access(tool_name, tool_input)
    if is_protected:
        print(f"File access blocked: {reason}", file=sys.stderr)
        # Return a non-zero exit code to indicate the tool should be blocked
        sys.exit(1)
    
    # Everything is safe, allow the command to proceed
    sys.exit(0)

if __name__ == "__main__":
    main()
