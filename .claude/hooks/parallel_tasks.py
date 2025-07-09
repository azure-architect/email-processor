#!/usr/bin/env python3
"""
Claude Code parallel processing script for executing tasks in parallel.

Example usage:
    python parallel_tasks.py "First task description" "Second task description" "Third task description"
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def run_claude_task(task_description):
    """
    Run a Claude Code task with the given description.
    
    Args:
        task_description: The task to execute
    
    Returns:
        dict: The result of the task
    """
    # Create a temporary file for the task input
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        tmp.write(task_description)
        tmp_path = tmp.name
    
    try:
        # Run Claude Code in programmable mode with the task
        result = subprocess.run(
            ["cl", "-p", f"@{tmp_path}"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Return the result
        return {
            "task": task_description,
            "success": True,
            "output": result.stdout,
            "error": result.stderr
        }
    except subprocess.CalledProcessError as e:
        return {
            "task": task_description,
            "success": False,
            "output": e.stdout if hasattr(e, 'stdout') else "",
            "error": e.stderr if hasattr(e, 'stderr') else str(e)
        }
    finally:
        # Clean up the temporary file
        try:
            os.unlink(tmp_path)
        except:
            pass

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run Claude Code tasks in parallel')
    parser.add_argument('tasks', nargs='+', help='Task descriptions to run in parallel')
    parser.add_argument('--max-workers', type=int, default=4, help='Maximum number of parallel workers')
    parser.add_argument('--output', '-o', help='Output file for results (JSON format)')
    args = parser.parse_args()
    
    # Run tasks in parallel
    results = []
    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = [executor.submit(run_claude_task, task) for task in args.tasks]
        for future in futures:
            results.append(future.result())
    
    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
    else:
        print(json.dumps(results, indent=2))
    
    # Exit with success if all tasks succeeded
    sys.exit(0 if all(r["success"] for r in results) else 1)

if __name__ == "__main__":
    main()
