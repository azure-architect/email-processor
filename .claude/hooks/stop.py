#!/usr/bin/env python3
"""
Claude Code stop hook for speaking completion notifications and capturing transcripts.
"""

import json
import sys
import os

# Add the parent directory to sys.path to allow importing utils
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from hooks.utils.speech import say_text, generate_completion_message
from hooks.utils.logger import log_json, append_to_transcript

def main():
    # Read input from stdin (Claude Code passes JSON)
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Error: Could not parse input as JSON", file=sys.stderr)
        sys.exit(1)
    
    # Log the stop event
    log_json(input_data, prefix="stop")
    
    # Get the transcript path if available
    if "transcript" in input_data:
        # Log the full transcript
        transcript = input_data.get("transcript", {})
        log_json(transcript, prefix="chat_transcript")
        
        # Add the last message to our running transcript
        if "messages" in transcript:
            messages = transcript.get("messages", [])
            if messages:
                last_message = messages[-1]
                append_to_transcript(last_message)
    
    # Announce completion
    completion_message = generate_completion_message()
    say_text(completion_message)
    
    # Exit successfully
    sys.exit(0)

if __name__ == "__main__":
    main()
