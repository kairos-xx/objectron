import logging
from functools import wraps
from typing import Callable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def method_wrapper(method: Callable) -> Callable:
    """
    A decorator to wrap methods for logging or other purposes.

    Args:
        method (Callable): The method to wrap.

    Returns:
        Callable: The wrapped method.
    """

    @wraps(method)
    def wrapped(*args, **kwargs):
        logger.info(f"Executing method: {method.__name__}")
        result = method(*args, **kwargs)
        logger.info(f"Method {method.__name__} executed successfully.")
        return result

    return wrapped
