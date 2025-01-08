from objectron import Objectron


def example_safe_access():
    objectron = Objectron()
    a = objectron.transform({})

    try:
        print(a.b.c.d.e)
    except AttributeError as e:
        print(
            f"Caught an AttributeError: {e}"
        )  # Expected: Caught an AttributeError

    print(a)  # Output remains unchanged: DictProxy({})


if __name__ == "__main__":
    example_safe_access()
