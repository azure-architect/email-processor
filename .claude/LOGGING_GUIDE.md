# Claude Code Logging System

## Overview

The Claude Code hooks system implements comprehensive logging to provide observability into Claude's actions and decisions. This document explains how the logging system works and what information is captured.

## Log Types and Location

All logs are stored in the `.claude/logs/` directory and are organized by type:

### Hook Event Logs

- **`pre_tool_use_*.json`** - Logs of tool execution attempts
  - Captured before a tool runs
  - Contains tool name and parameters
  - Records any blocked commands

- **`post_tool_use_*.json`** - Logs of completed tool executions
  - Captured after a tool runs
  - Contains tool name, parameters, and results
  - Records execution time and success status

- **`stop_*.json`** - Logs of session completions
  - Captured when a Claude Code session ends
  - Contains session duration and completion status
  - May include references to the transcript

- **`notification_*.json`** - Logs of user notifications
  - Captured when Claude needs user input
  - Contains notification message and type

### Transcript Logs

- **`chat_transcript_*.json`** - Complete chat transcripts
  - Contains the full conversation history
  - Includes all messages from user and Claude
  - Captured at the end of a session

- **`transcript_*.jsonl`** - Running transcript log
  - Append-only log of all messages
  - Each line is a JSON object representing a message
  - Organized by date

## Log File Naming

Log files follow a consistent naming pattern:

```
{log_type}_{timestamp}.json
```

For example:
- `pre_tool_use_2025-07-09_15-30-45.json`
- `post_tool_use_2025-07-09_15-31-12.json`
- `chat_transcript_2025-07-09_16-00-00.json`

## When Logs Are Generated

Logs are generated automatically by Claude Code hooks:

1. **Tool Usage**: When Claude uses a tool (like running a shell command)
2. **Session End**: When a Claude Code session completes
3. **User Input**: When Claude needs input from the user
4. **Subagent Completion**: When a subagent task completes

Logs are not generated during normal conversation turns unless they involve tool use.

## Log Content

Each log type contains specific information:

### Pre-Tool Use Logs

```json
{
  "timestamp": "2025-07-09T15:30:45.123456",
  "tool_name": "shell",
  "tool_input": {
    "command": "ls -la"
  }
}
```

### Post-Tool Use Logs

```json
{
  "timestamp": "2025-07-09T15:31:12.654321",
  "tool_name": "shell",
  "tool_input": {
    "command": "ls -la"
  },
  "tool_response": {
    "stdout": "total 32\ndrwxr-xr-x  5 user  group  160 Jul  9 15:30 .\n...",
    "stderr": "",
    "returncode": 0
  },
  "execution_time": 0.25
}
```

### Chat Transcript Logs

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Let's implement a database connection."
    },
    {
      "role": "assistant",
      "content": "I'll help you implement a database connection..."
    }
  ]
}
```

## Using Logs for Analysis

The logs can be used for:

1. **Auditing**: Review all commands executed by Claude
2. **Debugging**: Identify issues in Claude's execution
3. **Security**: Monitor for potentially dangerous operations
4. **Performance**: Track tool execution times
5. **Context Reconstruction**: Rebuild the context of a session

## Log Retention

Logs are retained indefinitely by default. If you want to implement log rotation or cleanup:

1. Create a simple script that:
   - Finds logs older than a certain date
   - Archives or deletes them based on your retention policy
   - Runs periodically (daily or weekly)

2. Example log cleanup script:
   ```python
   import os
   import glob
   from datetime import datetime, timedelta

   # Set retention period (e.g., 30 days)
   retention_days = 30
   cutoff_date = datetime.now() - timedelta(days=retention_days)

   # Find log files
   log_files = glob.glob(".claude/logs/*.json")

   for log_file in log_files:
       # Extract date from filename (format: type_YYYY-MM-DD_HH-MM-SS.json)
       try:
           filename = os.path.basename(log_file)
           date_part = filename.split('_', 1)[1].split('.')[0]
           file_date = datetime.strptime(date_part, "%Y-%m-%d_%H-%M-%S")
           
           # Check if file is older than retention period
           if file_date < cutoff_date:
               # Archive or delete the file
               os.remove(log_file)
               print(f"Removed old log file: {log_file}")
       except Exception as e:
           print(f"Error processing {log_file}: {e}")
   ```

## Analyzing Logs

You can use standard JSON processing tools to analyze logs:

1. **jq** for command-line analysis:
   ```bash
   # Find all shell commands run
   jq 'select(.tool_name == "shell") | .tool_input.command' .claude/logs/post_tool_use_*.json
   ```

2. **Python** for more complex analysis:
   ```python
   import glob
   import json

   # Load all post-tool-use logs
   logs = []
   for log_file in glob.glob(".claude/logs/post_tool_use_*.json"):
       with open(log_file, 'r') as f:
           logs.append(json.load(f))
   
   # Analyze tool usage
   tool_counts = {}
   for log in logs:
       tool_name = log.get("tool_name", "unknown")
       tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
   
   print("Tool usage statistics:")
   for tool, count in sorted(tool_counts.items(), key=lambda x: x[1], reverse=True):
       print(f"  {tool}: {count}")
   ```

## Conclusion

The logging system provides comprehensive visibility into Claude Code's actions and decisions. By analyzing these logs, you can better understand how Claude is working with your codebase and identify opportunities for improvement.
