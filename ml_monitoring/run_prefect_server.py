import subprocess
import sys
import logging
import time
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def run_prefect_server():
    """Start the Prefect server."""
    logger.info("Starting Prefect server")
    
    try:
        # Start Prefect server
        server_process = subprocess.Popen(
            ["prefect", "server", "start"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give the server some time to start
        time.sleep(5)
        
        # Check if server started successfully
        if server_process.poll() is not None:
            stdout, stderr = server_process.communicate()
            logger.error(f"Failed to start Prefect server: {stderr}")
            return False
        
        logger.info("Prefect server started successfully")
        
        # Print server URL
        logger.info("Prefect server UI available at: http://localhost:4200")
        
        # Keep the server running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down Prefect server")
            server_process.terminate()
            server_process.wait()
    
    except Exception as e:
        logger.error(f"Error running Prefect server: {e}")
        return False
    
    return True

def main():
    """Main function."""
    run_prefect_server()

if __name__ == "__main__":
    main()