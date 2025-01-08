# Objectron API Reference

## Core Classes

### Objectron
Main transformation engine

```python
class Objectron:
    def transform(self, value: Any) -> TransformedObject
    def wrap_class(self, cls: Type[T]) -> Type[T]
    def reshape_references(self, original: object, transformed: Any) -> None
```

### DynamicProxy 
Base proxy implementation

```python
class DynamicProxy(Generic[T]):
    def __getattr__(self, name: str) -> Any
    def __setattr__(self, name: str, value: Any) -> None
    def get_original(self) -> T
```

### Specialized Proxies
- DictProxy - Dictionary with path access
- ListProxy - List operations
- IntProxy - Integer operations  
- FloatProxy - Float operations
- StrProxy - String operations
- TupleProxy - Tuple operations
- ComplexProxy - Complex number operations
- FrozensetProxy - Frozenset operations

## Decorators
```python
@proxy_class(objectron: Optional[Objectron] = None)
def my_class(): ...

@method_wrapper
def my_method(): ...
```

## Exceptions
- TransformationError - Base transformation exception
- ReferenceError - Reference tracking error