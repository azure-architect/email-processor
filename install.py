#!/usr/bin/env python3
"""
Clean microservice template installation script.
Auto-configures framework based on project folder name.
"""

import os
import re
import sys
import subprocess
import venv
from pathlib import Path
from typing import Dict, Optional

def create_virtual_environment():
    """Create and activate virtual environment."""
    venv_path = Path.cwd() / "venv"
    
    if venv_path.exists():
        print(f"✅ Virtual environment already exists")
        return venv_path
    
    print(f"🔧 Creating virtual environment...")
    venv.create(venv_path, with_pip=True)
    print(f"✅ Virtual environment created at: {venv_path}")
    
    return venv_path

def install_dependencies(venv_path: Path):
    """Install dependencies in virtual environment."""
    if sys.platform == "win32":
        pip_path = venv_path / "Scripts" / "pip"
        python_path = venv_path / "Scripts" / "python"
    else:
        pip_path = venv_path / "bin" / "pip"
        python_path = venv_path / "bin" / "python"
    
    print(f"📦 Installing dependencies...")
    try:
        result = subprocess.run([
            str(pip_path), "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)
        print(f"✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def detect_project_suffix(folder_path: Optional[Path] = None) -> Optional[str]:
    """Extract 2-digit suffix from folder name."""
    if folder_path is None:
        folder_path = Path.cwd()
    
    folder_name = folder_path.name
    print(f"🔍 Analyzing folder: {folder_name}")
    
    # Extract suffix from patterns like: my-project-03
    suffix_match = re.search(r'-(\d{2})$', folder_name)
    if suffix_match:
        suffix = suffix_match.group(1)
        print(f"✅ Detected suffix: {suffix}")
        return suffix
    
    print(f"❌ No suffix detected. Please rename folder to end with -XX")
    return None

def generate_ports(suffix: str) -> Dict[str, str]:
    """Generate ports based on suffix."""
    ports = {
        'fastapi': f'81{suffix}',
        'postgres': f'54{suffix}',
        'flower': f'55{suffix}',
        'adminer': f'80{suffix}'
    }
    
    print(f"🔧 Port configuration:")
    for service, port in ports.items():
        print(f"   - {service.capitalize()}: {port}")
    
    return ports

def main():
    """Main installation process."""
    print("🚀 Microservice Template Installation")
    print("=" * 50)
    
    # Create virtual environment
    venv_path = create_virtual_environment()
    
    # Install dependencies
    if not install_dependencies(venv_path):
        return 1
    
    # Detect project suffix
    suffix = detect_project_suffix()
    if not suffix:
        return 1
    
    # Generate configuration
    project_name = Path.cwd().name
    ports = generate_ports(suffix)
    
    print(f"\n✅ Installation complete!")
    print(f"📁 Project: {project_name}")
    print(f"🔢 Suffix: {suffix}")
    print(f"🐍 Virtual environment: ./venv")
    print(f"\n🌐 Service URLs:")
    print(f"   - API: http://localhost:{ports['fastapi']}")
    print(f"   - Database: localhost:{ports['postgres']}")
    print(f"   - Monitoring: http://localhost:{ports['flower']}")
    print(f"   - DB Admin: http://localhost:{ports['adminer']}")
    
    # Show activation instructions
    if sys.platform == "win32":
        activate_cmd = ".\\venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    print(f"\n🚀 Next steps:")
    print(f"   1. Activate virtual environment: {activate_cmd}")
    print(f"   2. Start services: docker-compose up -d")
    print(f"   3. Test health: curl http://localhost:{ports['fastapi']}/health")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
