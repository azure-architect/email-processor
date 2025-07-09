#!/usr/bin/env python3
"""
Claude Code session management script for finalizing sessions.
This script runs as a Stop hook when a session ends.
"""

import json
import os
import sys
from datetime import datetime
import re
import shutil

def get_latest_session_path():
    """Get the path to the latest session file."""
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

def get_chat_transcript(transcript_data):
    """Extract key information from chat transcript."""
    if not transcript_data or "messages" not in transcript_data:
        return []
    
    messages = transcript_data.get("messages", [])
    
    # Filter out system messages
    user_assistant_messages = [
        msg for msg in messages 
        if msg.get("role") in ["user", "assistant"]
    ]
    
    return user_assistant_messages

def extract_key_information(transcript, session_path):
    """Extract key discussions, decisions, and progress from transcript."""
    if not transcript:
        return None
    
    # Initialize results
    key_discussions = []
    decisions_made = []
    implementation_progress = []
    
    # Extract information from transcript
    for msg in transcript:
        content = msg.get("content", "")
        role = msg.get("role", "")
        
        # Look for decision indicators in assistant messages
        if role == "assistant":
            # Look for decisions
            decision_matches = re.findall(r"(?:I've decided|We should|Let's|I recommend|I suggest) ([^\.\n]+)", content)
            for match in decision_matches:
                if match and len(match) > 20:  # Avoid trivial matches
                    decisions_made.append(match.strip())
            
            # Look for implementation progress
            progress_matches = re.findall(r"(?:I've created|I've implemented|I've added|Created|Implemented|Added) ([^\.\n]+)", content)
            for match in progress_matches:
                if match and len(match) > 20:  # Avoid trivial matches
                    implementation_progress.append(match.strip())
    
    # Extract discussions from all messages (simplified approach)
    all_content = " ".join([msg.get("content", "") for msg in transcript])
    
    # Find topics that appear frequently
    topic_candidates = re.findall(r"(?:about|regarding|concerning|discuss) ([^\.\n,]+)", all_content)
    topic_count = {}
    for topic in topic_candidates:
        if len(topic) > 10:  # Avoid trivial matches
            topic_lower = topic.lower()
            topic_count[topic_lower] = topic_count.get(topic_lower, 0) + 1
    
    # Get top topics
    key_topics = sorted(topic_count.items(), key=lambda x: x[1], reverse=True)[:5]
    key_discussions = [f"Discussed {topic}" for topic, count in key_topics if count > 1]
    
    # Update session file with extracted information
    if session_path and os.path.exists(session_path):
        with open(session_path, "r") as f:
            session_content = f.read()
        
        # Update key discussions
        if key_discussions:
            discussions_section = "## Key Discussions\n"
            for discussion in key_discussions:
                discussions_section += f"- {discussion}\n"
            
            # Replace the discussions section
            session_content = re.sub(
                r"## Key Discussions\n.*?(?=\n##)",
                discussions_section,
                session_content,
                flags=re.DOTALL
            )
        
        # Update decisions made
        if decisions_made:
            decisions_section = "## Decisions Made\n"
            for decision in decisions_made:
                decisions_section += f"- {decision}\n"
            
            # Replace the decisions section
            session_content = re.sub(
                r"## Decisions Made\n.*?(?=\n##)",
                decisions_section,
                session_content,
                flags=re.DOTALL
            )
        
        # Update implementation progress
        if implementation_progress:
            progress_section = "## Implementation Progress\n"
            for progress in implementation_progress:
                progress_section += f"- {progress}\n"
            
            # Replace the progress section
            session_content = re.sub(
                r"## Implementation Progress\n.*?(?=\n##)",
                progress_section,
                session_content,
                flags=re.DOTALL
            )
        
        # Add end time
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Replace session information section to add end time
        session_info_pattern = r"## Session Information\n(.*?)(?=\n##)"
        session_info_match = re.search(session_info_pattern, session_content, re.DOTALL)
        
        if session_info_match:
            session_info = session_info_match.group(1)
            if "End Time:" not in session_info:
                updated_info = session_info + f"- **End Time:** {timestamp}\n"
                session_content = re.sub(
                    session_info_pattern,
                    f"## Session Information\n{updated_info}",
                    session_content,
                    flags=re.DOTALL
                )
        
        # Write updated session content
        with open(session_path, "w") as f:
            f.write(session_content)
    
    return {
        "key_discussions": key_discussions,
        "decisions_made": decisions_made,
        "implementation_progress": implementation_progress
    }

def update_state_document(extracted_info):
    """Update the state document with information from the session."""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    state_path = os.path.join(script_dir, "state", "current.md")
    
    if not os.path.exists(state_path):
        return False
    
    with open(state_path, "r") as f:
        state_content = f.read()
    
    # Update last updated timestamp
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    state_content = re.sub(
        r"## Last Updated\n.*?\n",
        f"## Last Updated\n{timestamp} by Claude\n\n",
        state_content
    )
    
    # Update recent progress with implementation progress
    if extracted_info and "implementation_progress" in extracted_info:
        progress = extracted_info["implementation_progress"]
        if progress:
            progress_section = "## Recent Progress\n"
            for p in progress[:5]:  # Limit to top 5
                progress_section += f"- {p} ({timestamp})\n"
            
            # Replace the recent progress section
            state_content = re.sub(
                r"## Recent Progress\n.*?(?=\n##)",
                progress_section,
                state_content,
                flags=re.DOTALL
            )
    
    # Add new decisions to implementation decisions
    if extracted_info and "decisions_made" in extracted_info:
        decisions = extracted_info["decisions_made"]
        if decisions:
            # Find the implementation decisions section
            decisions_match = re.search(r"## Implementation Decisions\n(.*?)(?=\n##|$)", state_content, re.DOTALL)
            if decisions_match:
                current_decisions = decisions_match.group(1)
                updated_decisions = current_decisions
                
                for decision in decisions[:3]:  # Limit to top 3
                    if decision not in current_decisions:
                        updated_decisions += f"- {decision} ({timestamp})\n"
                
                state_content = state_content.replace(
                    decisions_match.group(0),
                    f"## Implementation Decisions\n{updated_decisions}\n\n"
                )
    
    # Write updated state content
    with open(state_path, "w") as f:
        f.write(state_content)
    
    # Create state snapshot
    history_dir = os.path.join(script_dir, "state", "history")
    os.makedirs(history_dir, exist_ok=True)
    
    snapshot_path = os.path.join(history_dir, f"{now.strftime('%Y-%m-%d-%H%M%S')}-state.md")
    shutil.copy2(state_path, snapshot_path)
    
    return True

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
    
    # Use a simple approach - random selection
    import random
    return random.choice(messages)

def say_text(text, voice="Daniel"):
    """
    Speak the provided text using system text-to-speech.
    Currently supports macOS using the 'say' command.
    
    Args:
        text: The text to speak
        voice: The voice to use (macOS only)
    """
    # Check for macOS for system-level text-to-speech
    if sys.platform == "darwin":
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

def log_json(data, prefix="log"):
    """
    Log data to a JSON file in the logs directory.
    
    Args:
        data: The data to log as JSON
        prefix: Prefix for the log filename
    
    Returns:
        str: Path to the log file
    """
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(script_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"{prefix}_{timestamp}.json")
    
    with open(log_file, "w") as f:
        json.dump(data, f, indent=2)
    
    return log_file

def main():
    """Main function."""
    # Read input from stdin (Claude Code passes JSON)
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Error: Could not parse input as JSON", file=sys.stderr)
        sys.exit(1)
    
    # Get transcript if available
    transcript = input_data.get("transcript", {})
    
    # Extract chat transcript
    chat_transcript = get_chat_transcript(transcript)
    
    # Get the latest session
    session_path = get_latest_session_path()
    
    # Extract key information from transcript
    extracted_info = None
    if chat_transcript:
        extracted_info = extract_key_information(chat_transcript, session_path)
    
    # Update state document
    if extracted_info:
        update_state_document(extracted_info)
    
    # Log the stop event
    log_json(input_data, prefix="stop")
    
    # Announce completion
    completion_message = generate_completion_message()
    say_text(completion_message)
    
    # Exit successfully
    sys.exit(0)

if __name__ == "__main__":
    main()
