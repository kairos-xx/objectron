import unittest

from objectron.objectron import Objectron
from objectron.proxy import (
    ComplexProxy,
    DictProxy,
    FloatProxy,
    FrozensetProxy,
    IntProxy,
    ListProxy,
    StrProxy,
    TupleProxy,
)


class TestProxies(unittest.TestCase):
    # Class implementation remains unchanged
    """Test all proxy classes."""

    def setUp(self):
        self.objectron = Objectron()

    def test_int_proxy_operations(self):
        """Test integer proxy arithmetic operations."""
        num = IntProxy(5, self.objectron)
        self.assertEqual(num + 3, 8)
        self.assertEqual(num - 2, 3)
        self.assertEqual(num * 4, 20)
        num += 2
        self.assertEqual(num, 7)
        num -= 3
        self.assertEqual(num, 4)
        num *= 2
        self.assertEqual(num, 8)

    def test_float_proxy_operations(self):
        """Test float proxy arithmetic operations."""
        num = FloatProxy(5.5, self.objectron)
        self.assertEqual(round(num + 3.2, 1), 8.7)
        self.assertEqual(round(num - 2.1, 1), 3.4)
        self.assertEqual(round(num * 2.0, 1), 11.0)
        num += 1.1
        self.assertEqual(round(num, 1), 6.6)
        num -= 2.2
        self.assertEqual(round(num, 1), 4.4)
        num *= 2.0
        self.assertEqual(round(num, 1), 8.8)

    def test_string_proxy_operations(self):
        """Test string proxy operations."""
        text = StrProxy("Hello", self.objectron)
        self.assertEqual(text + " World", "Hello World")
        self.assertEqual(text * 2, "HelloHello")
        text += " There"
        self.assertEqual(text, "Hello There")
        text *= 2
        self.assertEqual(text, "Hello ThereHello There")

    def test_complex_proxy_operations(self):
        """Test complex proxy operations."""
        num = ComplexProxy(1 + 2j, self.objectron)
        self.assertEqual(num + (2 + 3j), 3 + 5j)
        self.assertEqual(num - (1 + 1j), 0 + 1j)
        self.assertEqual(num * (2 + 1j), 0 + 5j)
        num += 1 + 1j
        self.assertEqual(num, 2 + 3j)
        num -= 1 + 1j
        self.assertEqual(num, 1 + 2j)
        num *= 2 + 0j
        self.assertEqual(num, 2 + 4j)

    def test_list_proxy_operations(self):
        """Test list proxy operations."""
        lst = ListProxy([1, 2, 3], self.objectron)
        lst.append(4)
        self.assertEqual(len(lst), 4)
        lst.extend([5, 6])
        self.assertEqual(len(lst), 6)
        self.assertEqual(lst.pop(), 6)
        self.assertTrue(3 in lst)
        lst.pop()
        self.assertEqual(lst[0].get_original(), 1)

    def test_dict_proxy_path_access(self):
        """Test dictionary proxy path-based access."""
        d = DictProxy({"a": {"b": {"c": 1}}}, self.objectron)
        self.assertEqual(d["a.b.c"], 1)
        d["x.y.z"] = 2
        self.assertEqual(d["x.y.z"], 2)

    def test_frozenset_proxy_operations(self):
        """Test frozenset proxy operations."""
        fs1 = FrozensetProxy(frozenset([1, 2, 3]), self.objectron)
        fs2 = frozenset([3, 4, 5])
        self.assertEqual(fs1 | fs2, frozenset([1, 2, 3, 4, 5]))
        self.assertEqual(fs1 & fs2, frozenset([3]))
        fs1 |= fs2
        self.assertEqual(fs1, frozenset([1, 2, 3, 4, 5]))

    def test_tuple_proxy_operations(self):
        """Test tuple proxy operations."""
        tup = TupleProxy((1, 2, 3), self.objectron)
        self.assertEqual(tup + (4, 5), (1, 2, 3, 4, 5))
        self.assertEqual(tup * 2, (1, 2, 3, 1, 2, 3))


if __name__ == '__main__':
    unittest.main()
