# log_handler.py
import logging
import logging.handlers
import queue
from queue import Queue
import gzip
import shutil
import os

# Initialize a logger for this module
logger = logging.getLogger(__name__)

# Function for gzip compression
def gzip_compress(old_log_path, new_log_path):
    logger.info(f"Compressing {old_log_path} to {new_log_path}.")
    with open(old_log_path, 'rb') as f_in:
        with gzip.open(new_log_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    logger.info(f"Compression complete.")

# Create a log queue
log_queue = Queue(-1)

# Initialize logging
def initialize_logging():
    logger.info("log_handler - Initializing logging...")

    if not os.path.exists('log'):
        os.makedirs('log')
        logger.info("log_handler - Created 'log' directory.")

    logging.basicConfig(level=logging.INFO)
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    log_handler = logging.handlers.TimedRotatingFileHandler(
        'log/main.log', when='midnight', backupCount=7, utc=True, encoding='utf-8')
    log_handler.setFormatter(log_formatter)
    log_handler.suffix = '%Y-%m-%d'
    log_handler.extMatch = logging.handlers.re.compile(r"^\d{4}-\d{2}-\d{2}(\.gz)?$")
    log_handler.namer = lambda name: name + ".gz"
    log_handler.rotator = gzip_compress

    logger.info("log_handler - TimedRotatingFileHandler configured.")

    # Create QueueHandler and add to root logger
    global listener 
    queue_handler = logging.handlers.QueueHandler(log_queue)
    logging.getLogger().addHandler(queue_handler)

    # Create and start queue listener
    listener = logging.handlers.QueueListener(log_queue, log_handler)
    listener.start()
    
    logger.info("log_handler - QueueListener started.")

def stop_logging():
    listener.stop()
    logger.info("log_handler - Stopping logging...")
