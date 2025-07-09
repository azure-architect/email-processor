#!/usr/bin/env python3
"""
Text-to-speech utilities for Claude Code hooks.
"""

import json
import os
import subprocess
import sys
from datetime import datetime

# Check for macOS for system-level text-to-speech
IS_MACOS = sys.platform == "darwin"

def say_text(text, voice="Daniel"):
    """
    Speak the provided text using system text-to-speech.
    Currently supports macOS using the 'say' command.
    
    Args:
        text: The text to speak
        voice: The voice to use (macOS only)
    """
    if IS_MACOS:
        try:
            subprocess.run(["say", "-v", voice, text], check=True)
            return True
        except Exception as e:
            print(f"Error using text-to-speech: {e}", file=sys.stderr)
            return False
    else:
        print(f"Text-to-speech is currently only supported on macOS", file=sys.stderr)
        print(f"Would speak: {text}", file=sys.stderr)
        return False

def generate_completion_message():
    """Generate a natural-sounding completion message."""
    messages = [
        "All set and ready for your next step.",
        "Task completed successfully.",
        "Finished processing your request.",
        "Operation completed.",
        "Command executed successfully.",
        "Task finished, ready for your next instruction.",
        "All done and ready for your next command.",
        "Processing complete.",
    ]
    
    # Use a simple approach - could be replaced with an actual LLM call
    # to generate more varied responses
    import random
    return random.choice(messages)

def log_event(event_type, data, log_dir=None):
    """
    Log an event to a JSON file in the logs directory.
    
    Args:
        event_type: Type of event (pre_tool, post_tool, etc.)
        data: The data to log
        log_dir: Optional custom log directory
    """
    if log_dir is None:
        # Default to .claude/logs relative to the script
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_dir = os.path.join(script_dir, "logs")
    
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Create a timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"{event_type}_{timestamp}.json")
    
    # Write the log
    with open(log_file, "w") as f:
        json.dump(data, f, indent=2)
    
    return log_file

def is_dangerous_command(tool_name, tool_input):
    """
    Check if a command is potentially dangerous.
    
    Args:
        tool_name: The name of the tool being used
        tool_input: The input to the tool
    
    Returns:
        (bool, str): Tuple of (is_dangerous, reason)
    """
    # Check for shell commands that could be destructive
    if tool_name == "shell":
        command = tool_input.get("command", "").strip().lower()
        
        # Check for rm commands
        if command.startswith("rm "):
            # Check for force flags
            if " -rf " in command or " -fr " in command or command.endswith(" -rf") or command.endswith(" -fr"):
                return True, "Blocked dangerous remove command with force flag"
            
            # Check for wildcards which could delete many files
            if "*" in command or "?" in command:
                return True, "Blocked dangerous remove command with wildcards"
        
        # Check for other potentially dangerous commands
        dangerous_commands = ["dd", "mkfs", "fdisk", "chown", "chmod 777", "> /dev/sda", ":(){ :|:& };:"]
        for dc in dangerous_commands:
            if dc in command:
                return True, f"Blocked potentially dangerous command: {dc}"
    
    # Not dangerous
    return False, ""

def is_protected_file_access(tool_name, tool_input):
    """
    Check if a command is accessing protected files.
    
    Args:
        tool_name: The name of the tool being used
        tool_input: The input to the tool
    
    Returns:
        (bool, str): Tuple of (is_protected, reason)
    """
    protected_patterns = [
        ".env",
        "config/secrets",
        "id_rsa",
        "credential",
        "password",
        "token",
        "secret",
        "key"
    ]
    
    # Check for file operations on protected files
    if tool_name in ["read_file", "write_file", "edit_file"]:
        path = tool_input.get("path", "").lower()
        
        for pattern in protected_patterns:
            if pattern in path:
                return True, f"Blocked access to protected file matching pattern: {pattern}"
    
    # Not protected
    return False, ""
