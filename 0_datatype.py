class c1code:

    def __init__(self):
        self.c1Code = 'test'
        self.c1CoordX = ''
        self.c1CoordY = ''
        self.c1NameKR = ''

    def set_c1code(self, c1code):
        self.c1Code = c1code['value']
        self.c1CoordX = c1code['xcrdn']
        self.c1CoordY = c1code['ycrdn']
        self.c1NameKR = c1code.text

    def print_c1code(self):
        print(self.c1Code, self.c1NameKR)

class c2code(c1code):
    def __init__(self):

        self.c2Code = 'test'
        self.c2NameKR = 'test'
        super(c2code, self).__init__()

    def set_c2code(self, c2code):
        self.c2Code = 'test'
        self.c2NameKR = 'test'
