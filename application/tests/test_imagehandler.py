"""The file contains the test which checks image handler.
"""
import __path_changing
import unittest
from sources.image_processing.img_handler import get_image_url


class TestImageProcessing(unittest.TestCase):
    """The simplest test for precise image retrieving.
    """

    def test_get_image_url(self):
        """The tests which checks """
        res = get_image_url()
        self.assertIn(res[-4:], ['.jpg', '.gif'])
