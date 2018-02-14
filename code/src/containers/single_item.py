class SingleItem:

    def __init__(self, data):
        self.data = data
        self.info = {}

    """This method allows the user to easily access the data structure
    stored in the "data" variable. We don't implement the analog method
    "__setitem__" because we don't wan't the user to modify this data structure
    """
    def __getitem__(self, key):
        return self.data[key]
