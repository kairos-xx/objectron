
# ObjectronDecorators

**ObjectronDecorators** provides powerful decorators for seamless integration with the Objectron module. These decorators enable dynamic proxying, method interception, and enhanced object tracking with minimal code changes.

## Available Decorators

### @proxy_class
The primary decorator for enabling proxy functionality on classes.

```python
from objectron_decorators.decorators import proxy_class

@proxy_class()
class User:
    def __init__(self, name: str):
        self.name = name
        self.age = 0
    
    def set_age(self, age: int) -> None:
        self.age = age

# Usage
user = User("John")
user.set_age(25)  # Method call is intercepted and logged
user.new_field = "dynamic"  # Dynamic attribute creation
```

#### Parameters
- `objectron`: Optional custom Objectron instance (default: global instance)
- `track_methods`: Bool to enable/disable method call tracking (default: True)
- `track_attributes`: Bool to enable/disable attribute access tracking (default: True)

#### Features
1. **Dynamic Attribute Access**
   ```python
   @proxy_class()
   class Config:
       pass

   config = Config()
   config.database.host = "localhost"  # Creates nested structure
   ```

2. **Method Interception**
   ```python
   @proxy_class()
   class Calculator:
       def add(self, a: int, b: int) -> int:
           return a + b

   calc = Calculator()
   result = calc.add(5, 3)  # Method call is logged
   ```

3. **Path-based Access**
   ```python
   @proxy_class()
   class Settings:
       def __init__(self):
           self.data = {}

   settings = Settings()
   settings["database.host"] = "localhost"
   ```

### @method_wrapper
Decorator for individual method interception.

```python
from objectron_decorators.decorators import method_wrapper

class Service:
    @method_wrapper
    def process_data(self, data: dict) -> dict:
        return {"processed": data}
```

#### Parameters
- `log_level`: Logging level for method calls (default: INFO)
- `track_args`: Bool to log method arguments (default: True)

## Integration with Objectron

ObjectronDecorators works seamlessly with the main Objectron module:

```python
from Objectron.objectron import Objectron
from objectron_decorators.decorators import proxy_class

objectron = Objectron()

@proxy_class(objectron=objectron)
class MyClass:
    pass

instance = MyClass()
transformed = objectron.transform(instance)
```

## Error Handling

```python
from objectron_decorators.decorators import proxy_class
from Objectron.exceptions import TransformationError

@proxy_class()
class SafeContainer:
    def __init__(self):
        self.data = []

    def add(self, item: int):
        if not isinstance(item, int):
            raise TransformationError("Only integers allowed")
        self.data.append(item)

container = SafeContainer()
try:
    container.add("string")  # Raises TransformationError
except TransformationError as e:
    print(f"Error: {e}")
```

## Best Practices

1. **Selective Proxying**: Only proxy classes that need transformation tracking
2. **Error Handling**: Always catch TransformationError for robust code
3. **Custom Objectrons**: Use separate Objectron instances for different contexts
4. **Method Tracking**: Enable method tracking only when debugging is needed

For more information about the core transformation functionality, see the [Objectron API Reference](/docs/wiki/api_reference.md).
