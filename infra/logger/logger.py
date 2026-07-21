import logging
from datetime import datetime
import os

LOG_FILE = f"{datetime.now().strftime('%m-%d-%Y-%H-%M-%S')}.log"
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(CURR_DIR, "logs")
os.makedirs(LOG_PATH, exist_ok = True)

LOG_FILE_PATH = os.path.join(LOG_PATH, LOG_FILE)

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO,
)

def log_result(result: dict):
    if result["passed"]:
        logging.info(f"[{result['suite']}] validation passed for {result['execution_date']}")
    else:
        logging.error(
            f"[{result['suite']}] validation FAILED at stage '{result['stage']}' "
            f"for {result['execution_date']}: {result['errors']}"
        )