import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logger(name: str = None, log_file: str = None) -> logging.Logger:
    """Configure logger with file and console handlers"""
    
    logger = logging.getLogger(name or __name__)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

logger = setup_logger(
    'google_sheet_handler',
    f'logs/sheet_operations_{datetime.now():%Y%m%d}.log'
) 