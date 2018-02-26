class AbstractItem:

    def __init__(self, data):
        self.data = data
        self.info = {}

    def __rshift__(self, other):
        return other(self)
