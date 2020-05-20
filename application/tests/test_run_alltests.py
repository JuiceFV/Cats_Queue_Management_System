"""The module which contains the runner of all unit tests.
"""
import unittest


def start_tests():
    """Running all tests at one time.
    """
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
