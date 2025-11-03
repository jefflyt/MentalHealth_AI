#!/usr/bin/env python3
"""
Run the Flask Web Interface for AI Mental Health Support Agent

This script automatically activates the conda environment and runs the app.
Usage: python run_web.py
"""

import sys
import os
import subprocess

def activate_conda_and_run():
    """Automatically activate conda environment and run the Flask app."""
    # Check if we're already in the correct conda environment
    current_env = os.environ.get('CONDA_DEFAULT_ENV')
    
    if current_env == 'mentalhealth_py311':
        # Already using correct environment, continue with normal startup
        print("✅ Already in mentalhealth_py311 environment")
        return True
    
    # Try to activate conda environment and re-run this script
    try:
        print("🔄 Activating mentalhealth_py311 conda environment...")
        
        # Find conda initialization script
        conda_base = subprocess.check_output(['conda', 'info', '--base'], text=True).strip()
        conda_sh = os.path.join(conda_base, 'etc', 'profile.d', 'conda.sh')
        
        # Create command to activate environment and run the Flask app
        cmd = f"""
source {conda_sh}
conda activate mentalhealth_py311
echo "✅ Environment activated successfully"
echo "🚀 Starting Flask application..."
python -c "
import sys
sys.path.insert(0, '{os.path.dirname(__file__)}')
from interface.web.app import app
print('🌟 AI Mental Health Support Agent starting...')
print('📱 Open http://localhost:5001 in your browser')
print('⏹️  Press Ctrl+C to stop')
app.run(host='0.0.0.0', port=5001, debug=True)
"
"""
        
        # Execute the command using bash
        result = subprocess.run(['bash', '-c', cmd], cwd=os.path.dirname(__file__))
        sys.exit(result.returncode)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error activating conda environment: {e}")
        print("\n📋 Manual Setup Instructions:")
        print("   1. conda activate mentalhealth_py311")
        print("   2. python run_web.py")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Conda not found!")
        print("\n📋 Setup Instructions:")
        print("   1. Install Miniconda/Anaconda")
        print("   2. Create env: conda create -n mentalhealth_py311 python=3.11")
        print("   3. Activate it: conda activate mentalhealth_py311")
        print("   4. Install deps: pip install -r requirements.txt")
        print("   5. Run app: python run_web.py")
        sys.exit(1)

# Try to activate conda environment and run app
if __name__ == '__main__':
    # If we're already in the right environment, run directly
    current_env = os.environ.get('CONDA_DEFAULT_ENV')
    if current_env == 'mentalhealth_py311':
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(__file__))
        
        # Import and run the Flask app
        from interface.web.app import app
        
        print("🌟 AI Mental Health Support Agent starting...")
        print("📱 Open http://localhost:5001 in your browser")
        print("⏹️  Press Ctrl+C to stop")
        
        app.run(
            host='0.0.0.0',
            port=5001,
            debug=True
        )
    else:
        # Activate environment and run
        activate_conda_and_run()

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
