class C1Code:

    def __init__(self):
        self.c1Code = str()
        self.c1CoordX = str()
        self.c1CoordY = str()
        self.c1NameKR = str()

    def set_c1code(self, c1code):
        self.c1Code = c1code['value']
        self.c1CoordX = c1code['xcrdn']
        self.c1CoordY = c1code['ycrdn']
        self.c1NameKR = c1code.text

    def print_c1code(self):
        print(self.c1Code, self.c1NameKR)

    class Builder:
        def __init__(self):
            self.c1Code = C1Code()

        def set_c1code(self, arg):
            self.c1Code.c1Code = arg
            return self

        def set_c1coord(self, arg1, arg2):
            self.c1Code.c1CoordX = arg1
            self.c1Code.c1CoordY = arg2
            return self

        def set_c1namekr(self, arg):
            self.c1Code.c1NameKR = arg
            return self

        def build(self):
            return self.c1Code

class C2Code(C1Code):
    def __init__(self):

        self.c2Code = 'test'
        self.c2NameKR = 'test'
        super(C2Code, self).__init__()

    def set_c2code(self, c2code):
        self.c2Code = 'test'
        self.c2NameKR = 'test'
