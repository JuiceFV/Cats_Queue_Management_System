import unittest
from application.QMS.tokengenerator import TokenGenerator


class TestQueryManagementSystem(unittest.TestCase):

    t = TokenGenerator()

    def testFirstObtaining(self):

        # Testing the case with empty usage history
        self.assertEqual(self.t.generate_new_token(), 'A00')

    def test_next_obtaining(self):

        # The case when tokens were picked at least once
        answers = ['A01', 'A02', 'A03']

        for i in range(0, 3):
            self.assertEqual(self.t.generate_new_token(), answers[i])

    def test_spare_tokens(self):

        # The case when some of the tokens were used and prepared for reuse
        self.t.prepare_used_token('A00')
        self.assertEqual(self.t.generate_new_token(), 'A00')

        self.t.prepare_used_token('A01')
        self.t.prepare_used_token('A02')
        self.t.prepare_used_token('A03')
        self.t.prepare_used_token('A00')
        self.assertEqual(self.t.generate_new_token(), 'A00')
        self.assertEqual(self.t.generate_new_token(), 'A01')
        self.assertEqual(self.t.generate_new_token(), 'A02')
        self.assertEqual(self.t.generate_new_token(), 'A03')
