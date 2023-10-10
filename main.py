#main.py
import logging
import threading
from log_handler import initialize_logging, stop_logging #defines the logging defind in the log_handler script used to unify logging of all scripts being controlled
initialize_logging()
logger = logging.getLogger(__name__)
logger.info("Initialized logging in main.py")
from configparser import ConfigParser
import time
from example1 import run_example1 #imports the other script and what function to use
from example2 import run_example2
from example3 import run_example3


# Initialize config parser and read config.ini
config = ConfigParser()
config.read('config.ini')

# Get loop times from config
example1_loop_time = int(config['example1']['loop_time_seconds']) #in the config.ini, define the loop_time_seconds for each script so that the main script can call on it continuesly
example2_loop_time = int(config['example2']['loop_time_seconds'])
example3_loop_time = int(config['example3']['loop_time_seconds'])

# Define example1 thread
def example1_thread():
    while True:
        run_example1() #replace with the running function in the other script
        time.sleep(example1_loop_time)

# Define example2 thread
def example2_thread():
    while True:
        run_example2()
        time.sleep(example2_loop_time)

def example3_thread():
    while True:
        run_example3()
        time.sleep(example3_loop_time)

if __name__ == "__main__":
    logger.info("Executing script main.py")
    
    # Start example1 thread
    logger.info("Starting thread 1 example1")
    t1 = threading.Thread(target=example1_thread)
    t1.start()

    # Start example2 thread
    logger.info("Starting thread 2, example2")
    t2 = threading.Thread(target=example2_thread)
    t2.start()

    # Start example3 thread
    logger.info("Starting thread 3, example3_thread")
    t3 = threading.Thread(target=example_thread)
    t3.start()

    # Let the main thread know that it should wait for the spawned threads to complete
    t1.join()
    t2.join()
    t3.join()
    
    stop_logging()


