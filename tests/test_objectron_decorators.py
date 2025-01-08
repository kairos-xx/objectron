import unittest

from objectron.exceptions import TransformationError
from objectron.objectron import Objectron
from objectron_decorators.decorators import proxy_class


class TestDecorators(unittest.TestCase):
    def setUp(self):
        self.objectron = Objectron()

    def test_basic_proxy_class_decorator(self):
        @proxy_class(objectron=self.objectron)
        class SampleClass:
            def __init__(self, value: int):
                self.value = value

            def increment(self) -> int:
                self.value += 1
                return self.value

        obj = SampleClass(10)
        self.assertIsInstance(obj, SampleClass)
        self.assertEqual(obj.value, 10)
        self.assertEqual(obj.increment(), 11)
        self.assertTrue(hasattr(obj, "_proxy"))

    def test_dynamic_attribute_creation(self):
        from typing import Any

        @proxy_class()
        class DynamicClass:
            def __init__(self):
                self.__dict__: dict[str, Any] = {}

            def __setattr__(self, name: str, value: Any) -> None:
                self.__dict__[name] = value

            def __getattr__(self, name: str) -> Any:
                if name not in self.__dict__:
                    self.__dict__[name] = {}
                return self.__dict__[name]

        obj = DynamicClass()
        obj.name = "test"
        obj.data.nested = 42

        self.assertEqual(obj.name, "test")
        self.assertEqual(obj.data.nested, 42)

    def test_method_interception(self):
        calls = []

        @proxy_class()
        class Logger:
            def log(self, message: str) -> None:
                calls.append(message)

        logger = Logger()
        logger.log("test1")
        logger.log("test2")

        self.assertEqual(len(calls), 2)
        self.assertEqual(calls, ["test1", "test2"])

    def test_error_handling(self):
        @proxy_class()
        class SafeContainer:
            def add(self, item: int) -> None:
                if not isinstance(item, int):
                    raise TransformationError("Only integers allowed")

        container = SafeContainer()
        with self.assertRaises(TransformationError):
            container.add("string")  # pyright: ignore

    def test_custom_objectron(self):
        custom_objectron = Objectron()

        @proxy_class(objectron=custom_objectron)
        class Counter:
            def __init__(self):
                self.count = 0

            def increment(self) -> int:
                self.count += 1
                return self.count

        counter = Counter()
        self.assertEqual(counter.increment(), 1)
        self.assertEqual(counter.increment(), 2)


if __name__ == "__main__":
    unittest.main()
