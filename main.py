from Objectron.objectron import Objectron


def test_chained_attribute_access_creation():
    objectron = Objectron()
    original = {}
    ref = objectron.transform(original)
    ref.a.b.c.d.e.f = 3
    ref.a.b.c.d.e.f += 3
    print(ref)  # Will print: DictProxy({'a': {'b': {'c': {'d': {'e': {'f': 3}}}}}})


if __name__ == "__main__":
    test_chained_attribute_access_creation()
