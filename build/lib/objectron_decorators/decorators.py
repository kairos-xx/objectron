from typing import Any, Callable, Optional, Type

from objectron import Objectron

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

        objectron_instance = (_global_objectron
                              if objectron is None else objectron)

        # Create proxy wrapper
        class ProxyWrapper(cls):

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._proxy = objectron_instance.transform(self)

            def __getattr__(self, name):
                if name not in self.__dict__:
                    self.__dict__[name] = objectron_instance.transform({})
                return self.__dict__[name]

        return ProxyWrapper

    return decorator
