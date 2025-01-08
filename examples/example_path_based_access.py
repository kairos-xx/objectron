from objectron import Objectron


def example_path_based_access() -> None:
    objectron = Objectron()
    a = objectron.transform({})

    # Assign using path string
    a["x.y.z"] = 10
    print(a)  # Output: DictProxy({'x': {'y': {'z': 10}}}})

    # Access using path string
    value = a["x.y.z"]
    print(value)  # Output: 10

    # Modify using path string
    a["x.y.z"] += 5
    print(a["x.y.z"])  # Output: 15
    print(a)  # Output: DictProxy({'x': {'y': {'z': 15}}}})


if __name__ == "__main__":
    example_path_based_access()
