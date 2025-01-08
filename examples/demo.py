"""Comprehensive demonstration of the Objectron package features.

This module provides complete examples of:
1. Nested configuration management
2. Complex data structures
3. Dynamic method creation
4. Attribute validation
5. Custom type handling

Each example demonstrates practical usage patterns for
different package components.

Usage:
    Run directly:
    $ python examples/demo.py
"""

from objectron import Objectron


def demonstrate_nested_config():
    """Demonstrate nested configuration management."""
    print("\n=== Nested Configuration ===")
    objectron = Objectron()
    config = objectron.transform({})

    # Create nested structure
    config.server.host = "0.0.0.0"
    config.server.ports.http = 80
    config.server.ports.https = 443
    config.server.settings.timeout = 30
    config.server.settings.max_connections = 1000

    print(f"Server config: {config.server}")
    print(f"HTTPS port: {config.server.ports.https}")


def demonstrate_complex_data():
    """Demonstrate handling of complex data structures."""
    print("\n=== Complex Data Structures ===")
    objectron = Objectron()
    data = objectron.transform(
        {"users": [{
            "id": 1,
            "roles": ["admin", "user"]
        }]})

    # Array and nested object manipulation
    data.users[0].permissions = {"read": True, "write": True}
    data.users[0].roles.append("moderator")
    print(f"User data: {data.users[0]}")


def demonstrate_dynamic_methods():
    """Demonstrate dynamic method creation and interception."""
    print("\n=== Dynamic Methods ===")

    class Service:

        def process(self, data: dict) -> dict:
            return {"processed": data}

        def __setattr__(self, name, value):
            super().__setattr__(name,
                                value)  # Standard attribute setting behavior

        def __getattr__(self, name):
            return object.__getattribute__(self, name)

    objectron = Objectron()
    service = Service()
    objectron.transform(service)

    # Add dynamic method
    def validate(data: dict) -> bool:
        return bool(data)

    service.validate = validate
    # Allow the instance to accept any new attribute without pyright errors
    result = service.validate({"test": True})
    print(f"Validation result: {result}")


def demonstrate_attribute_validation():
    """Demonstrate attribute validation capabilities."""
    print("\n=== Attribute Validation ===")

    class Temperature:

        def __init__(self):
            self.celsius = 0

    objectron = Objectron()
    temp = objectron.transform(Temperature())

    # Valid value
    temp.celsius = 25
    print(f"Temperature: {temp.celsius}°C")

    # Invalid value handling
    try:
        temp.celsius = "invalid"
    except TypeError as e:
        print(f"Error: {e}")


def demonstrate_custom_types():
    """Demonstrate handling of custom types."""
    print("\n=== Custom Types ===")

    class Vector:

        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y

        def __repr__(self):
            return f"Vector({self.x}, {self.y})"

    objectron = Objectron()
    vectors = objectron.transform([])

    # Add custom objects
    vectors.append(Vector(1.0, 2.0))
    vectors.append(Vector(3.0, 4.0))
    print(f"Vectors: {vectors}")


def run_demo():
    """Run all Objectron demonstrations."""
    print("=== Objectron Package Demo ===")
    demonstrate_nested_config()
    demonstrate_complex_data()
    demonstrate_dynamic_methods()
    demonstrate_attribute_validation()
    demonstrate_custom_types()


if __name__ == "__main__":
    run_demo()
