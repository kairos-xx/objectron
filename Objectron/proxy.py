import inspect
import re
from functools import wraps
from typing import Any, Callable, Generic, List, TypeVar

T = TypeVar("T")


class ReferenceObjectron:
    """Forward declaration for type hinting."""

    def transform(self, value: Any) -> Any:
        pass  # Placeholder for actual implementation


class DynamicProxy(Generic[T]):
    """A versatile proxy class for attribute and item access.

    Provides dynamic attribute access, method interception, reference tracking,
    and path-based object traversal for both mutable and immutable types.

    Attributes:
        _obj: Wrapped object
        _objectron: Objectron instance
        _attributes: Dynamic attributes store
        _initialized: Initialization flag
    """

    _registry = {}

    def __new__(cls, obj: T, objectron: ReferenceObjectron) -> "DynamicProxy[T]":
        obj_id = id(obj)
        if obj_id in cls._registry:
            proxy = cls._registry[obj_id]
            # Update objectron if different
            object.__setattr__(proxy, "_objectron", objectron)
            return proxy
        instance = super(DynamicProxy, cls).__new__(cls)
        cls._registry[obj_id] = instance
        return instance

    def __init__(self, obj: T, objectron: ReferenceObjectron) -> None:
        # Use __dict__ directly to avoid recursion
        if "_initialized" in self.__dict__:
            return
        object.__setattr__(self, "_obj", obj)
        object.__setattr__(self, "_objectron", objectron)
        object.__setattr__(self, "_attributes", {})  # For dynamic attributes
        object.__setattr__(self, "_initialized", True)

    def __getattr__(self, name: str) -> Any:
        # Handle dynamic attributes first
        if name in self._attributes:
            return self._attributes[name]

        # Check if __getattr__ is called as part of __setattr__
        if self._is_being_set():
            # If setting, create a new DictProxy
            new_dict = self._objectron.transform({})
            self._obj[name] = new_dict
            return new_dict
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            # Internal attributes
            object.__setattr__(self, name, value)
        elif isinstance(self._obj, dict):
            self._obj[name] = self._objectron.transform(value)
        else:
            # For immutable types, store in _attributes
            self._attributes[name] = self._objectron.transform(value)

    def __getitem__(self, key: Any) -> Any:
        if isinstance(key, str) and self._is_path_string(key):
            path_steps = self._parse_path(key)
            return self._resolve_path(path_steps)
        # Regular item access
        item = self._obj[key]
        return self._objectron.transform(item)

    def __setitem__(self, key: Any, value: Any) -> None:
        if isinstance(key, str) and self._is_path_string(key):
            path_steps = self._parse_path(key)
            try:
                self._resolve_path(path_steps[:-1], create=True)
                parent = self._resolve_path(path_steps[:-1])
                last_step = path_steps[-1]
                if isinstance(parent, DictProxy):
                    parent[last_step] = self._objectron.transform(value)
                elif isinstance(parent, DynamicProxy) and isinstance(parent._obj, list):
                    if isinstance(last_step, int):
                        parent[last_step] = self._objectron.transform(value)
                    else:
                        raise KeyError(f"Invalid list index: {last_step}")
                else:
                    raise TypeError("Unsupported parent type for setting value.")
            except Exception as e:
                # Optionally handle or log the exception
                raise e
            return
        # Regular item access
        self._obj[key] = self._objectron.transform(value)

    def _is_path_string(self, path: str) -> bool:
        # Simple heuristic: contains dots or brackets
        return "." in path or "[" in path

    def _parse_path(self, path: str) -> List[Any]:
        """
        Parses a complex path string into a list of steps.
        Example: "b.c.0['d']" -> ['b', 'c', 0, 'd']
        """
        tokens = []
        regex = re.compile(
            r"""
            (?:\.|^)                # Start of string or dot
            ([a-zA-Z_]\w*)          # Attribute name
            |                       # OR
            \[                      # Opening bracket
                (?:
                    '([^']+)'       # Single-quoted key
                    |               # OR
                    "([^"]+)"       # Double-quoted key
                    |               # OR
                    (\d+)            # Integer index
                )
            \]                      # Closing bracket
            """,
            re.VERBOSE,
        )
        pos = 0
        while pos < len(path):
            match = regex.match(path, pos)
            if not match:
                raise ValueError(f"Invalid path syntax at position {pos}: {path[pos:]}")
            attr, single_quote, double_quote, index = match.groups()
            if attr:
                tokens.append(attr)
            elif single_quote:
                tokens.append(single_quote)
            elif double_quote:
                tokens.append(double_quote)
            elif index:
                tokens.append(int(index))
            pos = match.end()
        return tokens

    def _resolve_path(self, steps: List[Any], create: bool = False) -> Any:
        """
        Traverses the proxy based on the list of steps.
        If 'create' is True, it will create proxies along the path if they don't exist.
        """
        current = self
        for step in steps:
            if isinstance(step, str):
                if isinstance(current, DictProxy):
                    if step not in current._obj:
                        if create:
                            current._obj[step] = {}
                        else:
                            raise KeyError(f"Key '{step}' not found.")
                    current = current[step]
                else:
                    current = getattr(current, step)
            elif isinstance(step, int):
                if isinstance(current, DynamicProxy) and isinstance(current._obj, list):
                    if step >= len(current._obj):
                        if create:
                            # Extend the list with None to accommodate the index
                            while len(current._obj) <= step:
                                current._obj.append(None)
                        else:
                            raise IndexError(f"List index out of range: {step}")
                    current = current[step]
                else:
                    raise TypeError(
                        "Cannot index into object of type",
                        f"{type(current._obj).__name__}",
                    )
            else:
                raise TypeError(f"Invalid step type: {type(step).__name__}")
        return current

    def _is_being_set(self) -> bool:
        # Check the call stack to see if __getattr__ is being called from __setattr__
        stack = inspect.stack()
        return any(frame.function == "__setattr__" for frame in stack[2:])

    def _wrap_method(self, method: Callable, name: str) -> Callable:
        @wraps(method)
        def wrapped(*args, **kwargs):
            print(f"[ReferenceTracker] Calling method: {name}")
            result = method(*args, **kwargs)
            print(f"[ReferenceTracker] Method {name} called successfully.")
            return self._objectron.transform(result)

        return wrapped

    def get_original(self) -> object:
        """Retrieve the original object."""
        return self._obj

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._obj)})"

    def __str__(self) -> str:
        return str(self._obj)

    # Implement additional magic methods as needed


class DictProxy(DynamicProxy[dict]):
    """
    A specialized proxy class for dictionaries that allows attribute-style access.
    For example, {"a": {"b": {"c": 1}}} can be accessed as a.b.c
    """

    def __getattr__(self, name: str) -> Any:
        try:
            value = self._obj[name]
            return self._objectron.transform(value)
        except KeyError:
            # Create a new empty dict for attribute chaining
            self._obj[name] = {}
            return self._objectron.transform(self._obj[name])

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            # Internal attributes
            object.__setattr__(self, name, value)
        else:
            self._obj[name] = self._objectron.transform(value)

    def __init__(self, obj: object, objectron: ReferenceObjectron) -> None:
        # Use __dict__ directly to avoid recursion
        if "_initialized" in self.__dict__:
            return
        object.__setattr__(self, "_obj", obj)
        object.__setattr__(self, "_objectron", objectron)
        object.__setattr__(self, "_attributes", {})  # For dynamic attributes
        object.__setattr__(self, "_initialized", True)

    def __repr__(self) -> str:
        return f"DictProxy({repr(self._obj)})"


class IntProxy(int, DynamicProxy[int]):
    def __new__(cls, value: int, objectron: ReferenceObjectron):
        obj = int.__new__(cls, value)
        DynamicProxy.__init__(obj, obj, objectron)
        return obj

    def __add__(self, other):
        result = super().__add__(other)
        print(f"[ReferenceTracker] Adding {self} + {other}")
        return self._objectron.transform(result)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        result = super().__sub__(other)
        print(f"[ReferenceTracker] Subtracting {self} - {other}")
        return self._objectron.transform(result)

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        result = super().__mul__(other)
        print(f"[ReferenceTracker] Multiplying {self} * {other}")
        return self._objectron.transform(result)

    def __imul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return f"IntProxy({int(self)})"

    def __str__(self):
        return str(int(self))

    def get_original(self) -> int:
        return int(self)


class FloatProxy(float, DynamicProxy[float]):
    def __new__(cls, value: float, objectron: ReferenceObjectron):
        obj = float.__new__(cls, value)
        DynamicProxy.__init__(obj, obj, objectron)
        return obj

    def __add__(self, other):
        result = super().__add__(other)
        print(f"[ReferenceTracker] Adding {self} + {other}")
        return self._objectron.transform(result)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        result = super().__sub__(other)
        print(f"[ReferenceTracker] Subtracting {self} - {other}")
        return self._objectron.transform(result)

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        result = super().__mul__(other)
        print(f"[ReferenceTracker] Multiplying {self} * {other}")
        return self._objectron.transform(result)

    def __imul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return f"FloatProxy({float(self)})"

    def __str__(self):
        return str(float(self))

    def get_original(self) -> float:
        return float(self)


class StrProxy(str, DynamicProxy[str]):
    def __new__(cls, value: str, objectron: ReferenceObjectron):
        obj = str.__new__(cls, value)
        DynamicProxy.__init__(obj, obj, objectron)
        return obj

    def __add__(self, other):
        result = super().__add__(other)
        print(f"[ReferenceTracker] Adding '{self}' + '{other}'")
        return self._objectron.transform(result)

    def __iadd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        result = super().__mul__(other)
        print(f"[ReferenceTracker] Multiplying '{self}' * {other}")
        return self._objectron.transform(result)

    def __imul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return f"StrProxy({str(self)!r})"

    def __str__(self):
        return str(self)

    def get_original(self) -> str:
        return str(self)


class TupleProxy(tuple, DynamicProxy[tuple]):
    def __new__(cls, value: tuple, objectron: ReferenceObjectron):
        obj = tuple.__new__(cls, value)
        DynamicProxy.__init__(obj, obj, objectron)
        return obj

    def __add__(self, other):
        result = super().__add__(other)
        print(f"[ReferenceTracker] Adding {self} + {other}")
        return self._objectron.transform(result)

    def __iadd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        result = super().__mul__(other)
        print(f"[ReferenceTracker] Multiplying {self} * {other}")
        return self._objectron.transform(result)

    def __imul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return f"TupleProxy({tuple(self)!r})"

    def __str__(self):
        return str(self)

    def get_original(self) -> tuple:
        return tuple(self)


class FrozensetProxy(frozenset, DynamicProxy[frozenset]):
    def __new__(cls, value: frozenset, objectron: ReferenceObjectron):
        obj = frozenset.__new__(cls, value)
        DynamicProxy.__init__(obj, obj, objectron)
        return obj

    def __or__(self, other):
        result = super().__or__(other)
        print(f"[ReferenceTracker] Union {self} | {other}")
        return self._objectron.transform(result)

    def __ior__(self, other):
        return self.__or__(other)

    def __and__(self, other):
        result = super().__and__(other)
        print(f"[ReferenceTracker] Intersection {self} & {other}")
        return self._objectron.transform(result)

    def __iand__(self, other):
        return self.__and__(other)

    def __repr__(self):
        return f"FrozensetProxy({frozenset(self)!r})"

    def __str__(self):
        return str(self)

    def get_original(self) -> frozenset:
        return frozenset(self)


class ComplexProxy(complex, DynamicProxy[complex]):
    def __new__(cls, value: complex, objectron: ReferenceObjectron):
        obj = complex.__new__(cls, value)
        DynamicProxy.__init__(obj, obj, objectron)
        return obj

    def __add__(self, other):
        result = super().__add__(other)
        print(f"[ReferenceTracker] Adding {self} + {other}")
        return self._objectron.transform(result)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        result = super().__sub__(other)
        print(f"[ReferenceTracker] Subtracting {self} - {other}")
        return self._objectron.transform(result)

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        result = super().__mul__(other)
        print(f"[ReferenceTracker] Multiplying {self} * {other}")
        return self._objectron.transform(result)

    def __imul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return f"ComplexProxy({complex(self)})"

    def __str__(self):
        return str(self)

    def get_original(self) -> complex:
        return complex(self)
