# Claude Code Hooks Documentation

This document explains the advanced Claude Code hooks implemented in this project, which provide safety controls, observability, notifications, parallel processing capabilities, and state management for session continuity.

## Features Implemented

- **Blocking dangerous commands** (like `rm -rf`) for safety
- **Logging all agent actions** for better observability
- **Creating voice notifications** when tasks complete
- **Capturing entire chat transcripts** for analysis
- **Parallel processing** with subagents for complex tasks
- **State management** for preserving context between sessions

## Directory Structure

```
.claude/
├── hooks/              # Hook implementation scripts
│   ├── pre_tool_use.py       # Blocks dangerous commands
│   ├── post_tool_use.py      # Logs tool executions
│   ├── notification.py       # Speaks notifications
│   ├── stop.py               # Speaks task completions
│   ├── sub_agent_stop.py     # Speaks subagent completions
│   ├── session_init.py       # Initializes new sessions with state
│   ├── session_end.py        # Finalizes sessions and updates state
│   ├── parallel_tasks.py     # Runs tasks in parallel
│   └── utils/                # Utility functions
│       ├── speech.py         # Text-to-speech utilities
│       └── logger.py         # Logging utilities
├── logs/               # Generated logs directory
│   ├── pre_tool_use_*.json   # Logs of tool attempts
│   ├── post_tool_use_*.json  # Logs of tool executions
│   ├── chat_transcript_*.json # Complete chat transcripts
│   └── transcript_*.jsonl    # Running transcript of messages
├── state/              # State management
│   ├── current.md            # Current project state
│   ├── index.md              # Reference index to resources
│   └── history/              # Historical state snapshots
│       └── YYYY-MM-DD-HHMMSS-state.md
├── sessions/           # Session records
│   └── YYYY-MM-DD-N.md       # Session files with context
└── hooks.toml          # Hook configuration
```

## Hook Types

### Safety Hooks

The `pre_tool_use.py` hook runs before any tool execution and blocks:

- Dangerous shell commands like `rm -rf`
- Access to sensitive files (containing keywords like "env", "secret", "credential")

### Observability Hooks

The `post_tool_use.py` hook logs every tool execution to `.claude/logs/` for analysis:

- Captures command parameters
- Records timestamps
- Preserves output and errors

### Notification Hooks

Voice notification hooks provide audio feedback:

- `notification.py` - Speaks when Claude needs user input
- `stop.py` - Announces when a task is complete
- `sub_agent_stop.py` - Announces when a subagent task completes

### Transcript Capture

The `stop.py` hook also captures complete chat transcripts:

- Stores entire conversations in `.claude/logs/chat_transcript_*.json`
- Maintains a running transcript in `.claude/logs/transcript_*.jsonl`

### State Management

The state management hooks provide context continuity between sessions:

- `session_init.py` - Initializes new sessions with previous state context
- `session_end.py` - Finalizes sessions and updates the state document

The state system maintains:
- A current state document with project status and context
- Historical state snapshots for reference
- Session records with detailed context
- A reference index to relevant resources

### Parallel Processing

The `parallel_tasks.py` script enables running multiple Claude Code tasks in parallel:

- Executes multiple independent tasks concurrently
- Uses subagents to process tasks in parallel
- Aggregates results from all tasks

## Using These Hooks

### Voice Notifications

Voice notifications are automatic. When Claude:
- Completes a task
- Needs your input
- Finishes a subagent task

You'll hear a spoken notification.

### Analyzing Logs

To review logs of Claude's actions:

1. Look in the `.claude/logs/` directory
2. Review files by timestamp
3. Use the `post_tool_use_*.json` files to see what commands were run
4. Check `chat_transcript_*.json` files for complete conversations

### Using State Management

To maintain context between sessions:

1. **Start a new session** with the command: `SESSION_INIT`
   - This loads the current state and creates a new session record
   - Claude will provide a summary of the current project state

2. **End a session naturally**
   - The session_end hook automatically captures key information
   - Updates the state document with progress and decisions
   - Creates a state snapshot for historical reference

3. **Review session history** by looking at files in the `.claude/sessions/` directory
   - Each session file contains the initial state, goals, discussions, and outcomes

4. **Check current state** by viewing `.claude/state/current.md`
   - This shows the current project status, focus, and next actions

### Running Parallel Tasks

To run multiple tasks in parallel:

1. Use the `PARALLEL` keyword followed by tasks separated by semicolons:

```
PARALLEL Analyze this code file; Create unit tests for this function; Document this API
```

2. Claude will split these into separate subagent tasks and execute them concurrently
3. Results will be combined and presented together

## Requirements

- Python 3.6+ for hook scripts
- macOS for built-in text-to-speech (optional)
- Claude Code CLI (`cl` command)
- Astral UV for running hook scripts

## Customization

You can customize the hooks by editing:

- `.claude/hooks.toml` - Hook configuration
- `.claude/hooks/utils/speech.py` - Text-to-speech settings
- `.claude/hooks/pre_tool_use.py` - Dangerous command patterns
- `.claude/state/current.md` - Current project state

## Setup

To set up the hooks:

1. Ensure all scripts are executable:
   ```
   chmod +x .claude/hooks/*.py
   chmod +x .claude/hooks/utils/*.py
   ```
   
   Or run the provided script:
   ```
   ./make_hooks_executable.sh
   ```

2. Test a hook:
   ```
   echo '{"tool_name": "shell", "tool_input": {"command": "ls"}}' | python .claude/hooks/pre_tool_use.py
   ```

3. Initialize a session:
   ```
   cl
   > SESSION_INIT
   ```

4. Start using Claude Code with these hooks enabled!
