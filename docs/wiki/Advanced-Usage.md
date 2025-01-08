
# Advanced Usage

## Path-Based Access
```python
objectron = Objectron()
data = objectron.transform({})

# Nested path creation
data["users.0.profile.name"] = "Alice"
data["users[0].settings.theme"] = "dark"
```

## Method Interception
```python
class Service:
    def process(self, data):
        return {"processed": data}

service = objectron.transform(Service())
# Methods are automatically intercepted and monitored
result = service.process({"input": "data"})
```

## Custom Type Handling
```python
@objectron.wrap_class
class CustomType:
    def __init__(self):
        self.value = None
    
    def set_value(self, value):
        self.value = value

obj = CustomType()
obj.dynamic_field = "New field"  # Dynamic attribute creation
```

## Reference Tracking
```python
# Original object
original = {"value": 42}
# Transform and track
proxy = objectron.transform(original)
proxy.value = 100
# All references are updated
print(original["value"])  # Output: 100
```

## Attribute Validation
```python
class Temperature:
    def __init__(self):
        self._celsius = 0
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Temperature must be a number")
        self._celsius = value

temp = objectron.transform(Temperature())
temp.celsius = 25  # Works
temp.celsius = "invalid"  # Raises TypeError
```
