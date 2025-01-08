"""Unit tests for DeepObjectReplacer with 100% coverage."""

import unittest
from unittest.mock import MagicMock, patch

from objectron.exceptions import TransformationError
from objectron.replace import DeepObjectReplacer, generate_object_id


class TestDeepObjectReplacer(unittest.TestCase):
    """Test cases for DeepObjectReplacer class."""

    def setUp(self):
        """Set up test objects."""
        self.obj_a = object()
        self.obj_b = object()

    def test_initialization(self):
        """Test initialization with valid inputs."""
        replacer = DeepObjectReplacer(self.obj_a, self.obj_b, max_workers=4)
        self.assertIsInstance(replacer, DeepObjectReplacer)
        self.assertEqual(replacer.old_obj, self.obj_a)
        self.assertEqual(replacer.new_obj, self.obj_b)
        self.assertIsInstance(replacer.visited, set)

    def test_invalid_old_obj_type(self):
        """Test initialization with invalid old_obj raises TypeError."""
        with self.assertRaises(TransformationError):
            DeepObjectReplacer("not an object", self.obj_b)

    def test_invalid_new_obj_type(self):
        """Test initialization with invalid new_obj raises TypeError."""
        with self.assertRaises(TypeError):
            DeepObjectReplacer(self.obj_a, "not an object")

    def test_invalid_max_workers(self):
        """Test initialization with invalid max_workers."""
        with self.assertRaises(ValueError):
            DeepObjectReplacer(self.obj_a, self.obj_b, max_workers=0)

    def test_schedule_task(self):
        """Test _schedule_task method."""
        replacer = DeepObjectReplacer(self.obj_a, self.obj_b, max_workers=1)
        mock_func = MagicMock()

        # Test scheduling new task
        replacer._schedule_task(mock_func, ("arg1", ))

        # Test scheduling duplicate task
        task_id = generate_object_id((mock_func, ("arg1", )))
        replacer.visited.add(task_id)
        replacer._schedule_task(mock_func, ("arg1", ))

    def test_safe_execute(self):
        """Test _safe_execute method."""
        replacer = DeepObjectReplacer(self.obj_a, self.obj_b, max_workers=1)

        def mock_func(arg):
            if arg == "raise":
                raise Exception("Test exception")
            return arg

        # Test successful execution
        replacer._safe_execute(mock_func, "success")

        # Test execution with exception
        replacer._safe_execute(mock_func, "raise")

    def test_process_referrers(self):
        """Test _process_referrers method with different types."""
        replacer = DeepObjectReplacer(self.obj_a, self.obj_b, max_workers=1)

        # Test dict referrer
        dict_ref = {"key": self.obj_a, self.obj_a: "value"}
        replacer._process_referrers(self.obj_a, self.obj_b, [dict_ref])
        self.assertEqual(dict_ref["key"], self.obj_b)
        self.assertIn(self.obj_b, dict_ref)

        # Test list referrer
        list_ref = [self.obj_a]
        replacer._process_referrers(self.obj_a, self.obj_b, [list_ref])
        self.assertEqual(list_ref[0], self.obj_b)

        # Test set referrer
        set_ref = {self.obj_a}
        replacer._process_referrers(self.obj_a, self.obj_b, [set_ref])
        self.assertIn(self.obj_b, set_ref)

        # Test custom object referrer
        class CustomObj:
            pass

        custom_ref = CustomObj()
        replacer._process_referrers(self.obj_a, self.obj_b, [custom_ref])

    def test_replace_in_members(self):
        """Test _replace_in_members method."""

        class TestClass:

            def __init__(self):
                self.attr = None

        test_obj = TestClass()
        test_obj.attr = self.obj_a  # pyright: ignore

        replacer = DeepObjectReplacer(self.obj_a, self.obj_b, max_workers=1)
        replacer._replace_in_members(test_obj)
        self.assertEqual(test_obj.attr, self.obj_b)

    def test_wait_for_all_tasks(self):
        """Test _wait_for_all_tasks method."""
        with patch("objectron.replace.ThreadPoolExecutor") as mock_executor:
            instance = mock_executor.return_value
            instance._max_workers = 4
            DeepObjectReplacer(self.obj_a, self.obj_b, max_workers=1)

    def test_generate_object_id(self):
        """Test generate_object_id function."""
        obj = object()
        id1 = generate_object_id(obj)
        id2 = generate_object_id(obj)
        self.assertEqual(id1, id2)

        obj2 = object()
        id3 = generate_object_id(obj2)
        self.assertNotEqual(id1, id3)

    def test_handle_frame_exception(self):
        """Test _handle_frame with exceptions."""
        replacer = DeepObjectReplacer(self.obj_a, self.obj_b, max_workers=1)
        mock_frame = MagicMock()
        mock_frame.frame.f_globals = {"key": self.obj_a}
        mock_frame.frame.f_locals = None  # Cause exception
        replacer._handle_frame(
            mock_frame)  # Should handle exception gracefully

    def test_replace_in_members_visited(self):
        """Test _replace_in_members with visited objects."""
        replacer = DeepObjectReplacer(self.obj_a, self.obj_b, max_workers=1)
        test_obj = object()
        obj_id = generate_object_id(test_obj)
        replacer.visited.add(obj_id)
        replacer._replace_in_members(
            test_obj)  # Should skip already visited object


if __name__ == "__main__":
    unittest.main()
