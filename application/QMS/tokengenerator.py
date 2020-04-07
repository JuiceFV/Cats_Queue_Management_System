"""


"""


class TokenGenerator:
    """The token-generator class generates an unique token

    Methods:
    generate_new_token -- generates new unique token.
    prepare_used_token -- prepares already used token for the reuse.

    """

    def __init__(self):
        """Constructor for the token-generator.

        It's just zeroing each field, specifically the token and the list of the prepared tokens.

        """
        self.token = None
        self.tokens_ready_to_present = []

    def generate_new_token(self):
        """Generate an unique token.

        A token contains three characters:
        1) A letter [A-Z]
        2) A digit [0-9]
        3) A digit [0-9]
        Therefore there is 26*10*10 = 2600 different options (tokens).
        Tokens are counted in the direction of increase, as following:
        A00, A01, A02, A03 ... Z99
        It is also possible to reuse the used token.

        returns the token as a string. For instance 'A00'.

        """
        if self.tokens_ready_to_present:
            self.token = self.tokens_ready_to_present.pop(0)
        elif self.token is None:
            self.token = ['A', '0', '0']
        elif self.token[2] < '9':
            self.token[2] = chr(ord(self.token[2]) + 1)
        elif self.token[1] < '9':
            self.token[2] = '0'
            self.token[1] = chr(ord(self.token[1]) + 1)
        elif self.token[0] < 'Z':
            self.token[2] = self.token[1] = '0'
            self.token[0] = chr(ord(self.token[0]) + 1)
        return ''.join(self.token)

    def prepare_used_token(self, token: str):
        """The method prepares the tokens already used.
        And we can use them again.

        Keywords arguments:
        token -- it's a three-character string which is a token used before and now available for reuse.

        Append the token as a list into the another list "ready to present"

        """
        self.tokens_ready_to_present.append(list(token))
        self.tokens_ready_to_present.sort()
