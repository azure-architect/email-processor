#!/bin/bash
# Script to move Claude hook changes to a separate branch

# Get the current branch name
current_branch=$(git branch --show-current)
echo "Current branch: $current_branch"

# Create a new branch for the Claude hook changes
git checkout -b claude-hooks-implementation

# Add the changes to the new branch
git add .claude/

# Commit the changes
git commit -m "Add Claude Code hooks for IADPVEC automation"

# Push the new branch to remote (if desired)
# git push -u origin claude-hooks-implementation

# Return to the original branch
git checkout $current_branch

# Remove the .claude directory from the original branch
rm -rf .claude/

echo "Changes have been moved to the 'claude-hooks-implementation' branch."
echo "You can review them there without affecting your main workflow."
echo "The .claude directory has been removed from your current branch."
