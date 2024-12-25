
# Objectron API Reference

## Table of Contents
- [Objectron Class](#objectron-class)
- [Proxy System](#proxy-system)
- [Decorators](#decorators)
- [Exceptions](#exceptions)

## Objectron Class
The main entry point for object transformation and reference tracking.

### Methods
#### `transform(value: T) -> TransformedObject`
Transforms a Python object into its corresponding proxy object.
```python
objectron = Objectron()
proxy = objectron.transform({"key": "value"})
```

#### `wrap_class(cls: Type[T]) -> Type[T]`
Creates a proxy subclass that wraps a given class.
```python
@objectron.wrap_class
class MyClass:
    pass
```

#### `reshape_references(original: T, transformed: Any) -> None`
Updates all references to the original object with the transformed version.
```python
objectron.reshape_references(original_obj, transformed_obj)
```

## Proxy System

### DynamicProxy
Base proxy class providing dynamic attribute and item access.

#### Key Methods
- `__getattr__(name: str) -> Any`: Dynamic attribute access
- `__setattr__(name: str, value: Any) -> None`: Attribute assignment
- `__getitem__(key: Any) -> Any`: Item access with path support
- `__setitem__(key: Any, value: Any) -> None`: Item assignment
- `get_original() -> T`: Retrieve original object

### Specialized Proxies
Each proxy type inherits from both its native type and DynamicProxy.

#### Built-in Type Proxies
- **IntProxy**: Integer operations
- **FloatProxy**: Floating-point operations
- **StrProxy**: String operations
- **TupleProxy**: Immutable sequence operations
- **FrozensetProxy**: Immutable set operations
- **ComplexProxy**: Complex number operations
- **DictProxy**: Dictionary operations with path access

```python
# Dictionary proxy example
proxy = objectron.transform({})
proxy.nested.value = 42  # Creates nested structure
proxy["nested.other"] = 24  # Path-based access
```

## Decorators

See the [ObjectronDecorators documentation](/ObjectronDecorators/objectron_decorators/README.md) for detailed information about available decorators and their usage.

## Exceptions

### TransformationError
Base exception for transformation failures.
```python
try:
    result = objectron.transform(obj)
except TransformationError as e:
    print(f"Transform failed: {e}")
```

### ReferenceError
Raised when reference tracking encounters issues.
```python
try:
    objectron.reshape_references(old, new)
except ReferenceError as e:
    print(f"Reference update failed: {e}")
```
