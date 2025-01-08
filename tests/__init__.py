"""Tests for the objectron package.

The test organization follows the module structure with dedicated
test files for each major component.
"""

import pytest


def run_tests():
    """
    Run all test suites in the proper order.
    """
    pytest.main([
        "tests/test_objectron.py",
        "tests/test_objectron_decorators.py",
        "tests/test_proxy.py",
        "tests/test_replace.py",
        "tests/test_wrappers.py",
    ])


if __name__ == "__main__":
    run_tests()
