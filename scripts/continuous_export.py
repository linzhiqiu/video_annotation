#!/usr/bin/env python3

import os
import sys
import time
import logging
import subprocess
from datetime import datetime
import signal
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'logs/continuous_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

def run_script(script_name: str) -> bool:
    """
    Run a Python script and return True if successful, False otherwise.
    Shows output in real-time. Ensures completion before returning.
    
    Args:
        script_name: Name of the script to run
        
    Returns:
        bool: True if script ran successfully, False otherwise
    """
    process = None
    try:
        logging.info(f"Starting {script_name}")
        logging.info("-" * 30)
        start_time = time.time()
        
        # Run the script using Popen to get real-time output
        process = subprocess.Popen(
            [sys.executable, f"scripts/{script_name}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered
            universal_newlines=True
        )
        
        # Function to handle output in real-time
        def handle_output(pipe, prefix):
            try:
                for line in pipe:
                    line = line.strip()
                    if line:
                        logging.info(f"{prefix}{line}")
            except Exception as e:
                logging.error(f"Error in output handling: {str(e)}")
        
        # Create threads to handle stdout and stderr in real-time
        import threading
        stdout_thread = threading.Thread(
            target=handle_output, 
            args=(process.stdout, "")
        )
        stderr_thread = threading.Thread(
            target=handle_output, 
            args=(process.stderr, "ERROR: ")
        )
        
        # Start threads and make them daemon threads
        stdout_thread.daemon = True
        stderr_thread.daemon = True
        stdout_thread.start()
        stderr_thread.start()
        
        # Wait for the process to complete with timeout
        try:
            return_code = process.wait(timeout=7200)  # 2 hour timeout
        except subprocess.TimeoutExpired:
            logging.error(f"{script_name} timed out after 2 hours")
            process.kill()
            return False
        
        # Wait for output threads to complete with timeout
        stdout_thread.join(timeout=30)
        stderr_thread.join(timeout=30)
        
        # Close pipes
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()
        
        duration = time.time() - start_time
        logging.info("-" * 30)
        logging.info(f"Completed {script_name} in {duration:.2f} seconds")
        logging.info(f"Return code: {return_code}")
        
        if return_code != 0:
            logging.error(f"{script_name} failed with return code {return_code}")
            return False
            
        return True
        
    except Exception as e:
        logging.error(f"Unexpected error running {script_name}: {str(e)}")
        logging.error(traceback.format_exc())
        if process:
            try:
                process.kill()
            except:
                pass
        return False
    finally:
        # Ensure process is terminated in all cases
        if process:
            try:
                process.kill()
            except:
                pass

def run_export_cycle():
    """Run all export scripts in sequence, ensuring no overlap."""
    scripts = [
        "export_labelbox_data.py",
        "export_pretests_labelbox_data.py",
        "export_and_update_sheets.py",
        "process_pretest_labelbox_data.py"
    ]
    
    for i, script in enumerate(scripts, 1):
        logging.info(f"\nExecuting script {i} of {len(scripts)}: {script}")
        if not run_script(script):
            logging.error(f"Failed to run {script}, continuing with next cycle after delay")
            return False
        logging.info(f"Successfully completed script {i} of {len(scripts)}")
    return True

def handle_signal(signum, frame):
    """Handle termination signals gracefully."""
    logging.info("Received termination signal. Shutting down...")
    sys.exit(0)

def main():
    """Main function to run continuous export cycle."""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    logging.info("Starting continuous export process")
    
    cycle_count = 0
    delay_minutes = 360
    
    try:
        while True:
            cycle_count += 1
            cycle_start = datetime.now()
            
            logging.info(f"\nStarting cycle {cycle_count} at {cycle_start}")
            logging.info("-" * 50)
            
            success = run_export_cycle()
            
            cycle_end = datetime.now()
            cycle_duration = (cycle_end - cycle_start).total_seconds()
            
            logging.info(f"Cycle {cycle_count} {'completed successfully' if success else 'completed with errors'}")
            logging.info(f"Cycle duration: {cycle_duration:.2f} seconds")
            
            next_run = cycle_end.timestamp() + (delay_minutes * 60)
            next_run_str = datetime.fromtimestamp(next_run).strftime('%Y-%m-%d %H:%M:%S')
            
            logging.info(f"Waiting {delay_minutes} minutes before next cycle")
            logging.info(f"Next cycle will start at: {next_run_str}")
            logging.info("-" * 50)
            
            time.sleep(delay_minutes * 60)
            
    except Exception as e:
        logging.error(f"Fatal error in main loop: {str(e)}")
        logging.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main() 