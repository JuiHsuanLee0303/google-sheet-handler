import time
import logging
from functools import wraps
from typing import Callable, Any
from ..config.settings import settings

def retry_on_exception(
    exceptions: tuple = (Exception,),
    max_attempts: int = None,
    delay: float = None,
    backoff: float = None
) -> Callable:
    """Retry decorator with exponential backoff"""
    
    max_attempts = max_attempts or settings.retry_config['max_attempts']
    delay = delay or settings.retry_config['delay']
    backoff = backoff or settings.retry_config['backoff']
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempt = 1
            current_delay = delay
            
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    
                    logging.warning(
                        f"Attempt {attempt}/{max_attempts} failed: {str(e)}. "
                        f"Retrying in {current_delay} seconds..."
                    )
                    
                    time.sleep(current_delay)
                    current_delay *= backoff
                    attempt += 1
            
            return None
        return wrapper
    return decorator 