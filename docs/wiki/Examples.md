
# Examples

## Basic Usage
```python
from objectron import Objectron

objectron = Objectron()
config = objectron.transform({})

# Dynamic attributes
config.server.host = "0.0.0.0"
config.server.port = 8080

# Path access
config["database.url"] = "postgres://localhost:5432"
```

## Class Transformation
```python 
@proxy_class()
class User:
    def __init__(self, name: str):
        self.name = name

user = User("Alice")
user.profile.age = 25
```

## Method Interception
```python
@proxy_class()
class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b

calc = Calculator()
result = calc.add(5, 3)  # Method call is logged
```

## Reference Management
```python
original = {"data": [1, 2, 3]}
transformed = objectron.transform(original)
objectron.reshape_references(original, transformed)
```
