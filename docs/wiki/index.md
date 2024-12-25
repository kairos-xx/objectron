
# Objectron Documentation

## Overview
Objectron is a Python module designed for transforming and tracking Python objects. It provides powerful utilities for monitoring object behavior, debugging, and testing.

## Quick Start

```python
from Objectron.objectron import Objectron

# Create a objectron instance
objectron = Objectron()

# Transform a dictionary
data = objectron.transform({"name": "John", "age": 30})

# Access and modify using dot notation
data.email = "john@example.com"
print(data.name)  # Output: John
```

## Key Features

### 1. Object Transformation
- Transform any Python object into a trackable proxy
- Maintain original object behavior while adding monitoring capabilities
- Support for both built-in and custom types

### 2. Reference Tracking
- Track all references to transformed objects
- Automatic reference updating when objects change
- Comprehensive object graph management

### 3. Dynamic Access Patterns
- Dot notation for attribute access
- Path-based string access for nested structures
- Method interception and logging

### 4. Error Handling
- Clear error messages and exceptions
- Safe access patterns
- Comprehensive error tracking

## Installation
```bash
pip install Objectron
```

## Core Concepts

### 1. Transformation
Objects are transformed into proxies that maintain their original interface while adding monitoring capabilities.

### 2. Proxy Objects
Proxies wrap original objects and intercept access patterns for monitoring and control.

### 3. Reference Management
The objectron maintains a registry of transformed objects and their relationships.

## Best Practices

### 1. Object Creation
```python
# Recommended
objectron = Objectron()
proxy = objectron.transform(my_object)

# Not recommended
proxy = DynamicProxy(my_object, objectron)
```

### 2. Class Transformation
```python
# Using the decorator
@proxy_class()
class MyClass:
    pass

# Using direct transformation
transformed_class = objectron.wrap_class(MyClass)
```

### 3. Path Access
```python
# Accessing nested structures
data["users.0.details.name"] = "Alice"

# Equivalent dot notation
data.users[0].details.name = "Alice"
```

## Advanced Topics

### 1. Custom Proxy Types
Create specialized proxy classes for specific types:
```python
class CustomProxy(DynamicProxy):
    def __init__(self, obj, objectron):
        super().__init__(obj, objectron)
        self._custom_attr = None
```

### 2. Method Interception
Monitor method calls and their results:
```python
@proxy_class()
class Logger:
    def log(self, message):
        print(f"Logging: {message}")
```

### 3. Reference Reshaping
Handle complex object relationships:
```python
objectron.reshape_references(original_obj, transformed_obj)
```

## Examples
See the following examples for complete working demonstrations:
- [Nested Structures](/examples/example_nested_structures.py)
- [Error Handling](/examples/example_error_handling.py)
- [Method Interception](/examples/example_method_interception.py)
- [Path-based Access](/examples/example_path_based_access.py)
- [Combined Access](/examples/example_combined_access.py)
- [Safe Access](/examples/example_safe_access.py)
- [Logging](/examples/example_logging.py)
- [Chained Assignment](/examples/example_chained_assignment.py)

## API Reference
See [API Reference](api_reference.md) for detailed documentation of all classes and methods.
