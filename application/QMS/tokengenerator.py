class TokenGenerator:
    def __init__(self):
        self.token = None

    def generate_new_token(self):
        if self.token is None:
            self.token = ['A', 'A', '0', '0']
        elif self.token[3] < '9':
            self.token[3] = chr(ord(self.token[3]) + 1)
        elif self.token[2] < '9':
            self.token[3] = '0'
            self.token[2] = chr(ord(self.token[2]) + 1)
        elif self.token[1] < 'Z':
            self.token[3] = self.token[2] = '0'
            self.token[1] = chr(ord(self.token[1]) + 1)
        elif self.token[0] < 'Z':
            self.token[3] = self.token[2] = '0'
            self.token[1] = 'A'
            self.token[0] = chr(ord(self.token[0]) + 1)
        return ''.join(self.token)
