"""
Objectron: Advanced Python Object Transformation System

A framework for transforming Python objects with comprehensive
monitoring capabilities.
Provides dynamic object proxying, path-based access, and reference management.

Key Features:
- Transparent object proxying and method interception
- Path-based nested object access (e.g., obj['a.b.c'])
- Reference tracking and circular reference handling
- Support for both mutable and immutable types
- Dynamic attribute creation and monitoring
"""

from typing import Any, Type, TypeVar

from .proxy import (
    ComplexProxy,
    DictProxy,
    DynamicProxy,
    FloatProxy,
    FrozensetProxy,
    IntProxy,
    ListProxy,
    ReferenceObjectron,
    StrProxy,
    TupleProxy,
)
from .replace import DeepObjectReplacer

T = TypeVar("T")
TransformedObject = Any


class Objectron(ReferenceObjectron):
    """Central class for object transformation and monitoring.

    Manages the transformation of Python objects into proxy objects that enable
    tracking, monitoring, and enhanced access patterns while maintaining the
    original object's interface.

    Example:
        objectron = Objectron()
        config = objectron.transform({})
        config.database.host = "0.0.0.0"  # Dynamic attribute creation
        print(config["database.host"])     # Path-based access
    """

    def __init__(self) -> None:
        """Initialize with an empty registry for transformed objects."""
        self._instances: dict[int, Any] = {}

    def transform(self, value: object) -> TransformedObject:
        """Transform an object into its corresponding proxy.

        Creates appropriate proxy objects based on the input type while
        maintaining type-specific behavior and adding monitoring capabilities.

        Args:
            value: Object to transform (any Python type)

        Returns:
            A proxy object wrapping the input value
        """
        if isinstance(value, int):
            return IntProxy(value, self)
        elif isinstance(value, float):
            return FloatProxy(value, self)
        elif isinstance(value, str):
            return StrProxy(value, self)
        elif isinstance(value, tuple):
            return TupleProxy(value, self)
        elif isinstance(value, frozenset):
            return FrozensetProxy(value, self)
        elif isinstance(value, complex):
            return ComplexProxy(value, self)
        elif isinstance(value, dict):
            return DictProxy(value, self)
        elif isinstance(value, list):
            return ListProxy(value, self)
        elif isinstance(value, set):
            return DynamicProxy(set(value), self)
        elif isinstance(value, type):
            return self.wrap_class(value)
        else:
            return DynamicProxy(value, self)

    def wrap_class(self, cls: type[Any]) -> type[Any]:
        """
        Create a proxy subclass that wraps the given class.

        This method creates a new class that inherits from the original class
        and adds proxy functionality. All instances of the wrapped class will
        automatically be proxied.

        Args:
            cls (Type[T]): The class to wrap with proxy functionality.

        Returns:
            Type[T]: A new class that inherits from the original and includes
                    proxy capabilities.

        Example:
            >>> @objectron.wrap_class
            >>> class MyClass:
            >>>     def __init__(self):
            >>>         self.value = 42
        """

        class WrappedClass(cls):
            """
            A proxy subclass that wraps the original class.

            This class intercepts attribute access and method calls to provide
            tracking and monitoring capabilities while maintaining the original
            class's interface.
            """

            _objectron = self

            def __init__(self, *args, **kwargs):
                """
                Initialize the wrapped class instance.

                Creates a DynamicProxy for the instance after calling the
                original class's __init__ method.
                """
                object.__setattr__(
                    self, "_proxy", DynamicProxy(self, self._objectron)
                )

                super().__init__(*args, **kwargs)

            def __getattribute__(self, name: str) -> Any:
                """
                Intercept attribute access to provide proxy functionality.

                Special attributes (starting with '_') are accessed directly,
                while other attributes are accessed through the proxy.
                """

                if name in {"_proxy", "_objectron"} or name.startswith("_"):
                    return super().__getattribute__(name)
                try:
                    return super().__getattribute__(name)

                except Exception:
                    return self._proxy.__getattr__(name)

            def __setattr__(self, name: str, value: Any) -> None:
                """
                Intercept attribute assignment to maintain proxy consistency.

                Special attributes are set directly, while other attributes are
                set through the proxy to maintain consistent transformation.
                """

                if name in {"_proxy", "_objectron"} or name.startswith("_"):
                    super().__setattr__(name, value)
                else:
                    self._proxy.__setattr__(name, value)

            def get_original(self) -> Any:
                """
                Retrieve the original unwrapped instance.

                Returns:
                    T: The original instance without proxy wrapping.
                """
                return self._proxy.get_original()

        WrappedClass.__name__ = f"Wrapped{cls.__name__}"
        WrappedClass.__doc__ = f"Proxy subclass of {cls.__name__}"

        return WrappedClass

    def reshape_references(
        self,
        original: object,
        transformed: Any,
    ) -> None:
        """
        Update all references to the original object with transformed version.

        This method scans the entire object graph to find references to the
        original object and replaces them with references to the transformed
        proxy object.

        Args:
            original (T): The original object to update references for
            transformed (Any): The proxy object to replace references with

        Raises:
            TransformationError: If an error occurs during reference reshaping.
        """
        DeepObjectReplacer(original, transformed)

    def add_class(self, cls: Type[T]) -> None:
        """
        Register a class for transformation tracking.

        This method wraps the class and makes it available globally for
        transformation.

        Args:
            cls (Type[T]): The class to add to the transformation registry.
        """
        wrapped_cls = self.wrap_class(cls)
        self.reshape_references(cls, wrapped_cls)

    def add_instance(self, instance: object) -> None:
        """
        Register an instance for transformation tracking.

        This method transforms the instance and adds it to the transformation
        registry.

        Args:
            instance (object): The instance to add to the transformation
            registry.
        """
        self.transform(instance)
