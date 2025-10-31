#!/usr/bin/env python3
"""
Run the Flask Web Interface for AI Mental Health Support Agent

This script automatically uses the venv Python where dependencies are installed.
"""

import sys
import os

# Check if we're running in the project's venv
def check_and_use_venv():
    """Ensure we're using the project venv with all dependencies."""
    # Path to local venv Python
    venv_python = os.path.join(os.path.dirname(__file__), 'venv', 'bin', 'python')
    
    # Check if we're already running from the venv
    if sys.executable == venv_python:
        # Already using venv, we're good!
        return
    
    # If venv exists but we're not using it, switch to it
    if os.path.exists(venv_python):
        print("🔄 Switching to project virtual environment...")
        print(f"   Using: {venv_python}\n")
        # Re-run this script with venv Python
        os.execv(venv_python, [venv_python] + sys.argv)
    else:
        # No venv found - show setup instructions
        print("❌ Virtual environment not found!")
        print("\n📋 Setup Instructions:")
        print("   1. Create venv: python3 -m venv venv")
        print("   2. Activate it: source venv/bin/activate")
        print("   3. Install deps: pip install -r requirements.txt")
        print("   4. Run app: python run_web.py\n")
        sys.exit(1)

# Check environment and switch to venv if needed
check_and_use_venv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the Flask app
from interface.web.app import app

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )
