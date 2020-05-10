"""The file contains tests which checks for correct token generation.
"""
import unittest
import __path_changing
from application.QMS import TokenGenerator


class TestQMS(unittest.TestCase):
    """Few tests for TokenGenerator
    """

    def test_get_first_token(self):
        """Test which checks first and second tokens obtaining.
        """
        t = TokenGenerator()
        self.assertEqual('A00', t.generate_new_token())
        self.assertEqual('A01', t.generate_new_token())

    def test_get_eleventh_token(self):
        """Tests which evaluates the second member (digit) it should fickle.
        """
        t = TokenGenerator()
        res = t.generate_new_token()
        for i in range(10):
            res = t.generate_new_token()

        self.assertEqual('A10', res)

    def test_get_hundredth_token(self):
        """Tests which evaluates the char member of token, it should fickle.
        """
        t = TokenGenerator()
        res = t.generate_new_token()
        for i in range(100):
            res = t.generate_new_token()

        self.assertEqual('B00', res)

    def test_get_token_with_used_tokens(self):
        """The test-case, when some of token has been popped.
        """
        t = TokenGenerator()
        self.assertEqual('A00', t.generate_new_token())
        self.assertEqual('A01', t.generate_new_token())

        # Pops the first token
        t.prepare_used_token('A00')
        self.assertEqual('A00', t.generate_new_token())
        self.assertEqual('A02', t.generate_new_token())
