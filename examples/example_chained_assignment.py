from Objectron.objectron import Objectron


def example_chained_assignment():
    objectron = Objectron()
    a = objectron.transform({})

    # Assigning a.b.c.d.e.f = 3
    a.b.c.d.e.f = 3

    print(a)  # Output: DictProxy({'b': {'c': {'d': {'e': {'f': 3}}}}}})
    print(a.b.c.d.e.f)  # Output: 3


if __name__ == "__main__":
    example_chained_assignment()
