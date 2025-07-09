#!/usr/bin/env python3
"""
Claude Code session management script for initializing new sessions.
This script runs as a MessageReceived hook when a new session starts.
"""

import json
import os
import sys
from datetime import datetime
import shutil

def get_current_state_path():
    """Get the path to the current state document."""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(script_dir, "state", "current.md")

def get_latest_session():
    """Get the most recent session file."""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sessions_dir = os.path.join(script_dir, "sessions")
    
    # Ensure sessions directory exists
    if not os.path.exists(sessions_dir):
        return None
    
    # Get the most recent session file
    session_files = [f for f in os.listdir(sessions_dir) if f.endswith(".md")]
    if not session_files:
        return None
    
    session_files.sort(reverse=True)  # Sort in descending order
    latest_session = os.path.join(sessions_dir, session_files[0])
    return latest_session

def create_new_session():
    """Create a new session file."""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sessions_dir = os.path.join(script_dir, "sessions")
    
    # Ensure sessions directory exists
    os.makedirs(sessions_dir, exist_ok=True)
    
    # Generate timestamps
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Count sessions today
    session_count = len([f for f in os.listdir(sessions_dir) if f.startswith(date)])
    session_num = session_count + 1
    session_id = f"{date}-{session_num}"
    
    # Create session file path
    session_file = os.path.join(sessions_dir, f"{session_id}.md")
    
    # Get current state
    current_state_path = get_current_state_path()
    current_state = ""
    if os.path.exists(current_state_path):
        with open(current_state_path, "r") as f:
            current_state = f.read()
    
    # Create session file
    with open(session_file, "w") as f:
        f.write(f"# Session: {session_id}\n\n")
        f.write(f"## Session Information\n")
        f.write(f"- **Start Time:** {timestamp}\n")
        f.write(f"- **Participants:** Developer, Claude\n\n")
        
        f.write(f"## Initial State\n")
        f.write(f"See current state document below.\n\n")
        
        f.write(f"## Session Goals\n")
        f.write(f"- [To be filled during session]\n\n")
        
        f.write(f"## Key Discussions\n")
        f.write(f"- [To be filled during session]\n\n")
        
        f.write(f"## Decisions Made\n")
        f.write(f"- [To be filled during session]\n\n")
        
        f.write(f"## Implementation Progress\n")
        f.write(f"- [To be filled during session]\n\n")
        
        f.write(f"## Current State Document\n")
        f.write(f"```markdown\n{current_state}\n```\n\n")
        
        f.write(f"## Next Session\n")
        f.write(f"- **Planned Focus:** [To be filled at end of session]\n")
    
    return session_file

def take_state_snapshot():
    """Take a snapshot of the current state."""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    state_dir = os.path.join(script_dir, "state")
    history_dir = os.path.join(state_dir, "history")
    
    # Ensure directories exist
    os.makedirs(history_dir, exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    
    # Get current state path
    current_state_path = os.path.join(state_dir, "current.md")
    if not os.path.exists(current_state_path):
        return None
    
    # Create snapshot path
    snapshot_path = os.path.join(history_dir, f"{timestamp}-state.md")
    
    # Copy current state to snapshot
    shutil.copy2(current_state_path, snapshot_path)
    
    return snapshot_path

def main():
    """Main function."""
    # Take snapshot of current state
    snapshot_path = take_state_snapshot()
    
    # Create new session
    session_file = create_new_session()
    
    # Generate response for Claude
    response = {
        "message": f"""
This is a new Claude Code session. I'm loading the project state to maintain continuity.

# Project State Summary

I see that you're working on implementing Claude Code hooks with state management.

## Recent Progress
- Comprehensive hook system implementation
- Safety controls for dangerous commands
- Observability logging for agent actions
- Voice notifications for events
- Transcript capture for analysis
- State management for session continuity

## Next Actions
- Test hooks with real development tasks
- Fine-tune dangerous command detection
- Enhance session management
- Document the state management system
- Integrate with CI/CD pipeline

Would you like to continue working on any of these tasks, or would you prefer to focus on something else?
"""
    }
    
    # Output response
    print(json.dumps(response))
    sys.exit(0)

if __name__ == "__main__":
    main()
