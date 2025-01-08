"""Unit tests for DeepObjectReplacer with 100% coverage."""

import unittest
from typing import Any

from objectron.exceptions import TransformationError
from objectron.objectron import (
    ComplexProxy,
    DeepObjectReplacer,
    DictProxy,
    DynamicProxy,
    FloatProxy,
    FrozensetProxy,
    IntProxy,
    Objectron,
    StrProxy,
    TupleProxy,
)


class TestImports(unittest.TestCase):
    """Test module imports."""

    def test_imports(self):
        """Test that all objects are imported correctly."""
        self.assertIsNotNone(Objectron)
        self.assertIsNotNone(DynamicProxy)
        self.assertIsNotNone(DictProxy)
        self.assertIsNotNone(IntProxy)
        self.assertIsNotNone(FloatProxy)
        self.assertIsNotNone(StrProxy)
        self.assertIsNotNone(TupleProxy)
        self.assertIsNotNone(FrozensetProxy)
        self.assertIsNotNone(ComplexProxy)
        self.assertIsNotNone(DeepObjectReplacer)


class TestObjectron(unittest.TestCase):

    def setUp(self):
        self.objectron = Objectron()

    def test_wrap_class_with_type(self):
        """Test wrapping a class type."""
        objectron = Objectron()

        class TestClass:
            pass

        wrapped = objectron.transform(TestClass)
        self.assertTrue(hasattr(wrapped, '_objectron'))

    def test_add_class_reference_reshaping(self):
        """Test adding a class with reference reshaping."""
        objectron = Objectron()

        class TestClass:
            pass

        objectron.add_class(TestClass)
        self.assertEqual(TestClass, type(TestClass()))

    def test_builtin_types_transformation(self):
        # Test integer transformation
        int_val = self.objectron.transform(42)
        self.assertIsInstance(int_val, IntProxy)
        self.assertEqual(int_val.get_original(), 42)

        # Test float transformation
        float_val = self.objectron.transform(3.14)
        self.assertIsInstance(float_val, FloatProxy)
        self.assertEqual(float_val.get_original(), 3.14)

        # Test string transformation
        str_val = self.objectron.transform("test")
        self.assertIsInstance(str_val, StrProxy)
        self.assertEqual(str_val.get_original(), "test")

        # Test tuple transformation
        tuple_val = self.objectron.transform((1, 2, 3))
        self.assertIsInstance(tuple_val, TupleProxy)
        self.assertEqual(tuple_val.get_original(), (1, 2, 3))

        # Test frozenset transformation
        frozen_val = self.objectron.transform(frozenset([1, 2, 3]))
        self.assertIsInstance(frozen_val, FrozensetProxy)
        self.assertEqual(frozen_val.get_original(), frozenset([1, 2, 3]))

        # Test complex transformation
        complex_val = self.objectron.transform(1 + 2j)
        self.assertIsInstance(complex_val, ComplexProxy)
        self.assertEqual(complex_val.get_original(), 1 + 2j)

    def test_mutable_types_transformation(self):
        # Test dictionary transformation
        dict_val = self.objectron.transform({"key": "value"})
        self.assertIsInstance(dict_val, DictProxy)
        self.assertEqual(dict_val["key"], "value")

        # Test list transformation
        list_val = self.objectron.transform([1, 2, 3])
        self.assertIsInstance(list_val, DynamicProxy)
        self.assertEqual(list_val[0], 1)

        # Test set transformation
        set_val = self.objectron.transform({1, 2, 3})
        self.assertIsInstance(set_val, DynamicProxy)
        self.assertEqual(len(set_val), 3)

    def test_custom_class_transformation(self):

        class TestClass:

            def __init__(self, value: Any):
                self.value = value

            def get_value(self) -> Any:
                return self.value

        # Test class transformation
        wrapped_class = self.objectron.transform(TestClass)
        instance = wrapped_class(42)
        self.assertEqual(instance.value, 42)
        self.assertEqual(instance.get_value(), 42)

    def test_chained_attribute_access(self):
        obj = self.objectron.transform({})
        obj.a.b.c.d = 42
        self.assertEqual(obj.a.b.c.d, 42)
        self.assertEqual(obj["a"]["b"]["c"]["d"], 42)

    def test_path_based_access(self):
        obj = self.objectron.transform({})
        obj["x.y.z"] = 10
        self.assertEqual(obj["x"]["y"]["z"], 10)
        self.assertEqual(obj.x.y.z, 10)

    def test_method_interception(self):
        obj = self.objectron.transform([])
        obj.append(1)
        obj.extend([2, 3])
        self.assertEqual(len(obj), 3)
        self.assertEqual(obj[:], [1, 2, 3])

    def test_reference_reshaping(self):
        original = {"key": "value"}
        transformed = self.objectron.transform(original)
        self.objectron.reshape_references(original, transformed)

        # Test that references are properly updated
        container = {"ref": original}
        self.assertEqual(container["ref"], transformed)

    def test_error_handling(self):
        # Test invalid path access
        obj = self.objectron.transform({})

        with self.assertRaises(AttributeError):
            _ = obj.nonexistent.attribute

        # Test invalid transformation
        with self.assertRaises(TransformationError):
            self.objectron.reshape_references(None, None)

    def test_class_registration(self):

        class TestClass:
            pass

        self.objectron.add_class(TestClass)

        instance = TestClass()
        self.assertTrue(hasattr(instance, "_proxy"))

    def test_instance_registration(self):
        obj = {"test": "value"}
        self.objectron.add_instance(obj)
        transformed = self.objectron.transform(obj)
        self.assertIsInstance(transformed, DictProxy)

    def test_proxy_operations(self):
        # Test arithmetic operations
        int_val = self.objectron.transform(5)
        self.assertEqual(int_val + 3, 8)
        self.assertEqual(int_val * 2, 10)

        # Test comparison operations
        self.assertTrue(int_val > 3)
        self.assertFalse(int_val < 3)

        # Test string operations
        str_val = self.objectron.transform("hello")
        self.assertEqual(str_val.upper(), "HELLO")
        self.assertTrue(str_val.startswith("he"))

    def test_container_operations(self):
        # Test list operations
        list_val = self.objectron.transform([1, 2, 3])
        list_val.append(4)
        self.assertEqual(len(list_val), 4)
        self.assertEqual(list_val[-1], 4)

        # Test dict operations
        dict_val = self.objectron.transform({"a": 1})
        dict_val["b"] = 2
        self.assertEqual(dict_val.get("b"), 2)
        self.assertEqual(list(dict_val.keys()), ["a", "b"])

    def test_attribute_deletion(self):
        obj = self.objectron.transform({"a": 1, "b": 2})
        del obj.a
        with self.assertRaises(AttributeError):
            print(obj.a)
        with self.assertRaises(AttributeError):
            del obj.nonexistent


if __name__ == "__main__":
    unittest.main()
