# State Reference Index

## Technical Documentation
- [CLAUDE.md](/CLAUDE.md) - Claude Code guidelines and best practices
- [HOOKS_DOCUMENTATION.md](/.claude/HOOKS_DOCUMENTATION.md) - Documentation for Claude Code hooks
- [PLANNING.md](/project/PLANNING.md) - Project architecture and planning

## Implementation
- [.claude/hooks/pre_tool_use.py](/.claude/hooks/pre_tool_use.py) - Hook for blocking dangerous commands
- [.claude/hooks/post_tool_use.py](/.claude/hooks/post_tool_use.py) - Hook for logging tool executions
- [.claude/hooks/stop.py](/.claude/hooks/stop.py) - Hook for session completion and transcript capture
- [.claude/hooks.toml](/.claude/hooks.toml) - Hook configuration file

## Key Decisions
- Hook Implementation Approach (2025-07-09) - Use Python scripts with UV for dependency management
- State Management Strategy (2025-07-09) - Implement dual-nature state system with event logs and snapshots
- Safety Controls (2025-07-09) - Block dangerous commands like rm -rf

## Conceptual Framework
- [State Management](/Volumes/Samsung/mo/docs/ideas/concepts/21-state-management.md) - Framework for maintaining continuity of context
- [Dual-Nature State System](/Volumes/Samsung/mo/docs/ideas/concepts/23-dual-nature-state-system.md) - Event streams and state snapshots

## External Resources
- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks) - Official documentation for Claude Code hooks
- [Astral UV Documentation](https://docs.astral.sh/uv/getting-started/installation/) - Documentation for UV package manager
