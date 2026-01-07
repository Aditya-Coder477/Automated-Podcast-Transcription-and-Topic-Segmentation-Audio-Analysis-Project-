import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name):
    """
    Creates a logger that writes to both a file and the console.
    """
    # 1. Define Log Directory
    # Goes up 3 levels to project root (src/utils/ -> src/ -> root)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_dir = os.path.join(base_dir, 'logs')
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 2. Configure Format (Time | Module | Level | Message)
    log_formatter = logging.Formatter('%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s')
    
    # 3. File Handler (Writes to logs/app.log)
    # RotatingFileHandler: Keeps file size manageable (max 5MB, keeps last 3 files)
    log_file = os.path.join(log_dir, 'app.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    # 4. Console Handler (Prints to Terminal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    # 5. Setup Logger Object
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate logs if handler already exists
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger