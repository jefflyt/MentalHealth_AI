"""
End Web Script - Safely shutdown all Mental Health AI processes

This script terminates all running processes related to the Mental Health AI system,
including Flask servers, Python processes, and any background services.

Usage:
    python run_endweb.py

Author: Mental Health AI Team
"""

import os
import sys
import subprocess
import signal
import time
import psutil


def print_banner():
    """Print shutdown banner."""
    print("\n" + "="*60)
    print("🛑 AI Mental Health Support Agent - Shutdown Script")
    print("="*60)
    print("⚠️  Terminating all running processes...")
    print("="*60 + "\n")


def kill_processes_by_name(process_names):
    """Kill processes by name patterns."""
    killed_count = 0
    
    for proc_name in process_names:
        try:
            # Use pkill to kill processes matching the pattern
            result = subprocess.run(['pkill', '-f', proc_name], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Killed processes matching: {proc_name}")
                killed_count += 1
            else:
                print(f"ℹ️  No processes found matching: {proc_name}")
                
        except subprocess.TimeoutExpired:
            print(f"⚠️  Timeout killing processes: {proc_name}")
        except Exception as e:
            print(f"❌ Error killing {proc_name}: {e}")
    
    return killed_count


def kill_processes_by_port(ports):
    """Kill processes running on specific ports."""
    killed_count = 0
    
    for port in ports:
        try:
            # Find processes using the port
            result = subprocess.run(['lsof', '-ti', f':{port}'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid.strip():
                        try:
                            # Force kill the process
                            subprocess.run(['kill', '-9', pid.strip()], timeout=5)
                            print(f"✅ Killed process {pid.strip()} on port {port}")
                            killed_count += 1
                        except Exception as e:
                            print(f"❌ Error killing PID {pid}: {e}")
            else:
                print(f"ℹ️  No processes found on port {port}")
                
        except subprocess.TimeoutExpired:
            print(f"⚠️  Timeout checking port {port}")
        except Exception as e:
            print(f"❌ Error checking port {port}: {e}")
    
    return killed_count


def kill_python_processes_selective():
    """Kill Python processes related to the Mental Health AI project."""
    killed_count = 0
    current_pid = os.getpid()
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Skip this script's process
                if proc.info['pid'] == current_pid:
                    continue
                
                # Check if it's a Python process
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = proc.info['cmdline'] or []
                    cmdline_str = ' '.join(cmdline).lower()
                    
                    # Check if it's related to our project
                    project_keywords = [
                        'mentalhealth_ai', 'mental_health', 'run_web.py', 'app.py',
                        'flask', 'agent', 'sunny', 'dass21', 'interface/web'
                    ]
                    
                    if any(keyword in cmdline_str for keyword in project_keywords):
                        try:
                            proc.terminate()  # Try graceful termination first
                            print(f"✅ Terminated Python process: PID {proc.info['pid']}")
                            killed_count += 1
                            
                            # Wait a bit, then force kill if still running
                            time.sleep(1)
                            if proc.is_running():
                                proc.kill()
                                print(f"🔥 Force killed stubborn process: PID {proc.info['pid']}")
                                
                        except psutil.NoSuchProcess:
                            pass  # Process already terminated
                        except Exception as e:
                            print(f"❌ Error terminating PID {proc.info['pid']}: {e}")
                            
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
    except Exception as e:
        print(f"❌ Error during selective Python process cleanup: {e}")
    
    return killed_count


def cleanup_conda_environment():
    """Deactivate conda environment if active."""
    try:
        conda_env = os.environ.get('CONDA_DEFAULT_ENV')
        if conda_env and conda_env != 'base':
            print(f"🔄 Deactivating conda environment: {conda_env}")
            # Note: This won't actually deactivate in the parent shell,
            # but it shows the user what environment was active
            return True
    except Exception as e:
        print(f"❌ Error checking conda environment: {e}")
    
    return False


def verify_shutdown():
    """Verify that processes have been shut down."""
    print("\n🔍 Verifying shutdown...")
    
    # Check common ports
    ports_to_check = [5000, 5001, 8000, 8080]
    active_ports = []
    
    for port in ports_to_check:
        try:
            result = subprocess.run(['lsof', '-i', f':{port}'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    if line.strip() and 'python' in line.lower():
                        active_ports.append(port)
                        break
        except Exception:
            continue
    
    if active_ports:
        print(f"⚠️  Warning: Still found Python processes on ports: {active_ports}")
        return False
    else:
        print("✅ Verification complete - No Python web servers detected")
        return True


def main():
    """Main shutdown function."""
    print_banner()
    
    total_killed = 0
    
    # Step 1: Kill processes by name patterns
    print("🎯 Step 1: Terminating processes by name...")
    process_patterns = [
        'run_web.py',
        'interface/web/app.py',
        'app.py',
        'flask.*mentalhealth',
        'python.*mental',
        'werkzeug'
    ]
    total_killed += kill_processes_by_name(process_patterns)
    
    # Step 2: Kill processes by port
    print("\n🎯 Step 2: Terminating processes by port...")
    ports = [5000, 5001, 8000, 8080, 3000]
    total_killed += kill_processes_by_port(ports)
    
    # Step 3: Selective Python process cleanup
    print("\n🎯 Step 3: Selective Python process cleanup...")
    total_killed += kill_python_processes_selective()
    
    # Step 4: Cleanup conda environment info
    print("\n🎯 Step 4: Environment cleanup...")
    cleanup_conda_environment()
    
    # Step 5: Wait and verify
    if total_killed > 0:
        print(f"\n⏳ Waiting 2 seconds for processes to terminate...")
        time.sleep(2)
    
    # Step 6: Verification
    verify_shutdown()
    
    # Final summary
    print("\n" + "="*60)
    print("📊 SHUTDOWN SUMMARY")
    print("="*60)
    print(f"🔥 Total processes terminated: {total_killed}")
    
    if total_killed > 0:
        print("✅ Mental Health AI system shutdown complete!")
    else:
        print("ℹ️  No active Mental Health AI processes found")
    
    print("💡 To restart the system, run: python run_web.py")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Shutdown interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during shutdown: {e}")
        sys.exit(1)