class singleItem:

    def __init__(self, data):
        self.data = data
        self._info = {}

    def __getitem__(self, key):
        return self._info[key]

    def __setitem__(self, key, value):
        self._info[key] = value

    def __len__(self):
        return len(self._info)
