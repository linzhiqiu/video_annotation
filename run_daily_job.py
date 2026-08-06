#!/usr/bin/env python3
"""
Repeating Job Runner - Execute commands with configurable intervals

Usage:
    python run_daily_job.py --command "python script.py --arg value" --interval 3600
"""

import argparse
import subprocess
import sys
import time
from datetime import datetime

def run_command(command: str):
    """Execute a command and show output in real-time"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Starting command: {command}")
    print("-" * 80)
    sys.stdout.flush()
    
    try:
        # Force Python to be unbuffered and show all output
        if command.strip().startswith('python '):
            command = command.replace('python ', 'python -u ', 1)
        
        # Run command directly without capturing output
        # This lets the subprocess write directly to our terminal
        result = subprocess.run(
            command,
            shell=True,
            timeout=14400  # 4 hour timeout
        )
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("-" * 80)
        if result.returncode == 0:
            print(f"[{timestamp}] Command completed successfully")
        else:
            print(f"[{timestamp}] Command failed with exit code: {result.returncode}")
        
        return result.returncode
        
    except subprocess.TimeoutExpired:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Command timed out after 4 hours")
        return 124
    except KeyboardInterrupt:
        print("\nCommand interrupted by user")
        return 130
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Error executing command: {str(e)}")
        return 1

def main():
    parser = argparse.ArgumentParser(description="Run commands repeatedly with configurable intervals")
    parser.add_argument("--command", required=True, help="Command to execute")
    parser.add_argument("--interval", type=int, default=86400, 
                       help="Seconds between reruns (default: 86400 = 24 hours)")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    
    args = parser.parse_args()
    
    if args.once:
        # Run once and exit
        exit_code = run_command(args.command)
        sys.exit(exit_code)
    else:
        # Run repeatedly
        print(f"Running command every {args.interval} seconds ({args.interval/3600:.1f} hours)")
        print("Press Ctrl+C to stop")
        print("=" * 80)
        
        try:
            while True:
                run_command(args.command)
                
                next_run = datetime.now().timestamp() + args.interval
                next_run_str = datetime.fromtimestamp(next_run).strftime("%Y-%m-%d %H:%M:%S")
                print(f"\nWaiting {args.interval} seconds until next run (at {next_run_str})...")
                print("=" * 80)
                
                time.sleep(args.interval)
                
        except KeyboardInterrupt:
            print("\nStopped by user")
            sys.exit(0)

if __name__ == "__main__":
    main()