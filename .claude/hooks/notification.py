#!/usr/bin/env python3
"""
Claude Code notification hook for speaking notifications.
"""

import json
import sys
import os

# Add the parent directory to sys.path to allow importing utils
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hooks.utils.speech import say_text
from hooks.utils.logger import log_json

def main():
    # Read input from stdin (Claude Code passes JSON)
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Error: Could not parse input as JSON", file=sys.stderr)
        sys.exit(1)
    
    # Log the notification
    log_json(input_data, prefix="notification")
    
    # Get the notification message
    message = input_data.get("message", "Your agent needs your input.")
    
    # Speak the notification
    say_text(message)
    
    # Exit successfully
    sys.exit(0)

if __name__ == "__main__":
    main()
