from objectron import Objectron


def example_combined_access():
    objectron = Objectron()
    a = objectron.transform({})

    # Assign using attribute chaining
    a.b.c.d.e.f = 3
    print(a)  # Output: DictProxy({'b': {'c': {'d': {'e': {'f': 3}}}}}})

    # Assign using path string
    a["b.c.d.e.g"] = 4
    print(
        a
    )  # Output: DictProxy({'b': {'c': {'d': {'e': {'f': 3, 'g': 4}}}}}})

    # Access using both methods
    print(a.b.c.d.e.f)  # Output: 3
    print(a["b.c.d.e.g"])  # Output: 4

    # Safe access that doesn't alter the structure
    try:
        print(a.b.c.x)
    except AttributeError as e:
        print(f"Caught an AttributeError: {e}")

    print(a)  # Output remains unchanged


if __name__ == "__main__":
    example_combined_access()
