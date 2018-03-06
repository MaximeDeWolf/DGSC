class AbstractItem:

    def __init__(self, data):
        self.data = data
        self.info = {}

    def __rshift__(self, other):
        return other(self)

    def __getattr__(self, name):
        """Permit access to the 'info' dict by a dot notation.
        ex: Let F be a AbstractItem, F.info[name] <==> F.name

        If 'name' is not a key of the 'info' dict, this method will return the value
        of the field 'name' if it exist.
        """
        try:
            return self.info[name]
        except KeyError:
            return self.__getattribute__(name)
