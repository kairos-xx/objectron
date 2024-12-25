from Objectron.exceptions import TransformationError
from Objectron.objectron import Objectron


def example_error_handling():
    objectron = Objectron()
    a = objectron.transform({"numbers": [1, 2, 3]})

    # Attempt to access an invalid path
    try:
        print(a["numbers.10"])  # Index out of range
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error: {e}")

    # Attempt to set a value with an invalid type
    try:
        a["numbers"].append("four")  # Should work, but if type is restricted, may raise
    except TransformationError as e:
        print(f"Transformation Error: {e}")

    # Properly setting a value
    a["numbers"].append(4)
    print(a["numbers"])  # Output: [1, 2, 3, 4]


if __name__ == "__main__":
    example_error_handling()
