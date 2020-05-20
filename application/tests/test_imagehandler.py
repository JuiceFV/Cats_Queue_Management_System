"""The file contains the test which checks image handler.
"""
import sys
import os

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
import unittest
from sources.image_processing.img_handler import get_image_url


class TestImageProcessing(unittest.TestCase):
    """The simplest test for precise image retrieving.
    """

    def test_get_image_url(self):
        """The tests which checks """
        res = get_image_url()
        self.assertIn(res[-4:], ['.jpg', '.gif', '.png', '.svg'])
