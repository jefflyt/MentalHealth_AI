#!/usr/bin/env python3
"""
Run the Flask Web Interface for AI Mental Health Support Agent

This script automatically activates the conda environment and runs the app.
Usage: python run_web.py
"""

import sys
import os
import subprocess
import signal

# Try to activate conda environment and run app
if __name__ == '__main__':
    # Check if we're already in the right environment
    current_env = os.environ.get('CONDA_DEFAULT_ENV')
    
    if current_env == 'mentalhealth_py311':
        # Already in correct environment, run directly
        sys.path.insert(0, os.path.dirname(__file__))
        
        from interface.web.app import app
        
        print("🌟 AI Mental Health Support Agent starting...")
        print("🌐 Open http://localhost:5001 in your browser")
        print("⏹️  Press Ctrl+C to stop")
        print("")
        
        try:
            app.run(
                host='0.0.0.0',
                port=5001,
                debug=True
            )
        except KeyboardInterrupt:
            print("\n\n⏹️  Server stopped gracefully. Goodbye!")
            sys.exit(0)
    else:
        # Not in correct environment - attempt to run with conda activation
        print("🔄 Conda environment not active, attempting to activate and run...")
        print("")
        
        # Get conda base path
        conda_exe = os.environ.get('CONDA_EXE', 'conda')
        conda_base = os.path.dirname(os.path.dirname(conda_exe)) if conda_exe != 'conda' else None
        
        # Build command to activate environment and run app
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Use bash to source conda and activate environment
        if conda_base:
            activate_script = os.path.join(conda_base, 'etc', 'profile.d', 'conda.sh')
            cmd = f"""
            source "{activate_script}" && \
            conda activate mentalhealth_py311 && \
            cd "{script_dir}" && \
            python "{os.path.join(script_dir, 'interface', 'web', 'app.py')}"
            """
        else:
            # Fallback: try using conda directly
            cmd = f"""
            eval "$(conda shell.bash hook)" && \
            conda activate mentalhealth_py311 && \
            cd "{script_dir}" && \
            python "{os.path.join(script_dir, 'interface', 'web', 'app.py')}"
            """
        
        try:
            # Run the command in a bash shell with proper signal handling
            process = subprocess.Popen(
                ['bash', '-c', cmd],
                stdout=sys.stdout,
                stderr=sys.stderr
            )
            
            # Wait for process and handle Ctrl+C gracefully
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n\n⏹️  Stopping server...")
                # Send SIGTERM to the process group
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                print("⏹️  Server stopped gracefully. Goodbye!")
                sys.exit(0)
            
            sys.exit(process.returncode)
            
        except Exception as e:
            print(f"❌ Failed to activate environment automatically: {e}")
            print("\n💡 Please activate the environment manually:")
            print("\n   Method 1: Use the activation script")
            print("   $ source activate_env.sh")
            print("   $ python run_web.py")
            print("\n   Method 2: Manual activation")
            print("   $ conda activate mentalhealth_py311")
            print("   $ python run_web.py")
            print("\n   Method 3: Direct launch (recommended)")
            print("   $ conda run -n mentalhealth_py311 python interface/web/app.py")
            sys.exit(1)
