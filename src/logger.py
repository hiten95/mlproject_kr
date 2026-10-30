import logging
import os 
from datetime import datetime

logging.basicConfig(level=logging.INFO)

logfile= f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_path = os.path.join(os.getcwd(), "logs", logfile)

os.makedirs(os.path.dirname(log_path), exist_ok=True)   

log_file_path = os.path.join(log_path)

format="%(asctime)s: %(levelname)s: %(message)s"

logging.basicConfig(format=format, datefmt='%m/%d/%Y %I:%M:%S %p')

if __name__ == "__main__":
    logging.info("Logging has started.")
    logging.info(f"Log file path: {log_file_path}")

