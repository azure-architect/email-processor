#!/usr/bin/env python3
"""
Logger utilities for Claude Code hooks.
"""

import json
import os
import sys
from datetime import datetime

def get_log_dir():
    """Get the absolute path to the logs directory."""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(script_dir, "logs")

def log_json(data, prefix="log"):
    """
    Log data to a JSON file in the logs directory.
    
    Args:
        data: The data to log as JSON
        prefix: Prefix for the log filename
    
    Returns:
        str: Path to the log file
    """
    log_dir = get_log_dir()
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"{prefix}_{timestamp}.json")
    
    with open(log_file, "w") as f:
        json.dump(data, f, indent=2)
    
    return log_file

def append_to_transcript(message):
    """
    Append a message to the current transcript file.
    
    Args:
        message: The message to append
    """
    log_dir = get_log_dir()
    os.makedirs(log_dir, exist_ok=True)
    
    # Use today's date for the transcript file
    today = datetime.now().strftime("%Y-%m-%d")
    transcript_file = os.path.join(log_dir, f"transcript_{today}.jsonl")
    
    # Append the message as a JSON line
    with open(transcript_file, "a") as f:
        f.write(json.dumps(message) + "\n")
    
    return transcript_file

def get_chat_transcript(transcript_path):
    """
    Read a chat transcript file.
    
    Args:
        transcript_path: Path to the transcript file
    
    Returns:
        list: List of messages in the transcript
    """
    if not os.path.exists(transcript_path):
        return []
    
    messages = []
    with open(transcript_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    message = json.loads(line)
                    messages.append(message)
                except json.JSONDecodeError:
                    print(f"Error parsing transcript line: {line}", file=sys.stderr)
    
    return messages
