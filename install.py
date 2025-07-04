#!/usr/bin/env python3
"""
Clean microservice template installation script.
Auto-configures framework based on project folder name.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, Optional

def detect_project_suffix(folder_path: Optional[Path] = None) -> Optional[str]:
    """Extract 2-digit suffix from folder name."""
    if folder_path is None:
        folder_path = Path.cwd()
    
    folder_name = folder_path.name
    print(f"Analyzing folder: {folder_name}")
    
    # Extract suffix from patterns like: my-project-03
    suffix_match = re.search(r'-(\d{2})$', folder_name)
    if suffix_match:
        suffix = suffix_match.group(1)
        print(f"Detected suffix: {suffix}")
        return suffix
    
    print(f"No suffix detected. Please rename folder to end with -XX")
    return None

def generate_ports(suffix: str) -> Dict[str, str]:
    """Generate ports based on suffix."""
    ports = {
        'fastapi': f'81{suffix}',
        'postgres': f'54{suffix}',
        'flower': f'55{suffix}',
        'adminer': f'80{suffix}'
    }
    
    print(f"Port configuration:")
    for service, port in ports.items():
        print(f"   - {service.capitalize()}: {port}")
    
    return ports

def main():
    """Main installation process."""
    print("Microservice Template Installation")
    print("=" * 40)
    
    # Detect project suffix
    suffix = detect_project_suffix()
    if not suffix:
        return 1
    
    # Generate configuration
    project_name = Path.cwd().name
    ports = generate_ports(suffix)
    
    print(f"\nConfiguration complete!")
    print(f"Project: {project_name}")
    print(f"Suffix: {suffix}")
    print(f"Next: docker-compose up -d")
    return 0

if __name__ == "__main__":
    sys.exit(main())
