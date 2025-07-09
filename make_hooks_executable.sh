#!/bin/bash
# Make all Python hook scripts executable

# Change to the script directory
cd "$(dirname "$0")"

# Make all Python scripts in hooks directory executable
chmod +x .claude/hooks/*.py
chmod +x .claude/hooks/utils/*.py

echo "All hook scripts are now executable."
