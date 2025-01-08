"""Main demonstration module for the Objectron package.

This module demonstrates the core features of Objectron including:
- Object transformation
- Dynamic attribute access
- Path-based traversal
- Reference tracking
- Method interception
"""

from objectron.objectron import Objectron


def demonstrate_basic_transformation():
    """Demonstrate basic object transformation."""
    print("\n=== Basic Transformation ===")
    objectron = Objectron()
    config = objectron.transform({})

    # Dynamic attribute creation
    config.database.host = "0.0.0.0"
    config.database.port = 5432
    print(f"Database config: {config.database}")


def demonstrate_path_access():
    """Demonstrate path-based access patterns."""
    print("\n=== Path Access ===")
    objectron = Objectron()
    data = objectron.transform({"users": [{"name": "", "age": ""}]})

    # Path-based access
    data["users.0.name"] = "Alice"
    data["users[0].age"] = 25
    print(f"User data: {data}")


def demonstrate_method_interception():
    """Demonstrate method call interception."""
    print("\n=== Method Interception ===")

    class Calculator:

        def add(self, a: int, b: int) -> int:
            self.z = 1
            return a + b

    objectron = Objectron()
    calc = objectron.transform(Calculator())
    result = calc.add(5, 3)
    print(f"Calculation result: {result}")


def demonstrate_reference_tracking():
    """Demonstrate reference tracking capabilities."""
    print("\n=== Reference Tracking ===")
    objectron = Objectron()
    original = {"value": 42}
    transformed = objectron.transform(original)
    transformed.value = 100
    print(f"Original value: {original['value']}")
    print(f"Transformed value: {transformed.value}")


def demonstrate_class_transformation():
    """Demonstrate class transformation."""
    print("\n=== Class Transformation ===")

    class User:

        def __init__(self, name: str):
            self.name = name

    objectron = Objectron()
    TransformedUser = objectron.wrap_class(User)
    user = TransformedUser("Bob")
    user.age = 30  # Dynamic attribute
    print(f"User name: {user.name}")
    print(f"User age: {user.age}")


def main():
    """Run all demonstrations."""
    print("Objectron Demonstration\n")
    demonstrate_basic_transformation()
    demonstrate_path_access()
    demonstrate_method_interception()
    demonstrate_reference_tracking()
    demonstrate_class_transformation()


if __name__ == "__main__":
    main()
