class AbstractItem:

    def __init__(self, data):
        self.data = data
        self.info = {}

    def __gt__(self, other):
        print("Other.args = {}".format(type(other.args)))
        other.args = (self,) + other.args
