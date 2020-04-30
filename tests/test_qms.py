import unittest
from random import randrange
from application.QMS.tokengenerator import TokenGenerator


class TestQueryManagementSystem(unittest.TestCase):

    def test_first_obtaining(self):
        t = TokenGenerator()

        # Testing the case with empty usage history
        self.assertEqual(t.generate_new_token(), 'A00')

    def test_next_obtaining(self):
        t = TokenGenerator()

        # The case when tokens were picked at least once
        answers = ['A00', 'A01', 'A02', 'A03']

        for i in range(0, 4):
            self.assertEqual(t.generate_new_token(), answers[i])

    def test_spare_tokens(self):
        t = TokenGenerator()

        # The case when some of the tokens were used and prepared for reuse
        t.prepare_used_token('A00')
        self.assertEqual(t.generate_new_token(), 'A00')

        t.prepare_used_token('A01')
        t.prepare_used_token('A02')
        t.prepare_used_token('A03')
        t.prepare_used_token('A00')
        self.assertEqual(t.generate_new_token(), 'A00')
        self.assertEqual(t.generate_new_token(), 'A01')
        self.assertEqual(t.generate_new_token(), 'A02')
        self.assertEqual(t.generate_new_token(), 'A03')
