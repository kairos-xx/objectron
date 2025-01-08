import unittest

from objectron.wrappers import method_wrapper


class TestWrappers(unittest.TestCase):
    """Test wrapper functionality."""

    def test_method_wrapper(self):
        """Test method wrapper decorator."""

        @method_wrapper
        def test_method(x: int, y: int) -> int:
            return x + y

        result = test_method(2, 3)
        self.assertEqual(result, 5)


if __name__ == '__main__':
    unittest.main()
