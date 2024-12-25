from typing import Any, Callable, Optional, Type

from Objectron.objectron import Objectron

# Initialize a global Objectron instance or allow users to provide one
_global_objectron = Objectron()


def proxy_class(objectron: Optional[Objectron] = None) -> Callable:
    """Class decorator for automatic proxy transformation.

    Enables transparent proxying with attribute tracking, method interception,
    and reference monitoring.

    Args:
        objectron: Optional custom objectron instance

    Returns:
        Decorated class with proxy capabilities
    """

    def decorator(cls: Type[Any]) -> Type[Any]:
        if objectron is None:
            objectron_instance = _global_objectron
        else:
            objectron_instance = objectron

        # Create proxy wrapper
        class ProxyWrapper(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._proxy = objectron_instance.transform(self)

        return ProxyWrapper

    return decorator
