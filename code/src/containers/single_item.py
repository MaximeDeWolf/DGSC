class SingleItem:

    def __init__(self, data):
        self.data = data
        self.info = {}


    def __getitem__(self, key):
        """This method allows the user to easily access the data structure
        stored in the "data" variable. We don't implement the analog method
        "__setitem__" because we don't wan't the user to modify this data structure
        """
        return self.data[key]

def openContainer(f):
    def wrapped(container, *args, **kwargs):
        data = f(container.data, *args, **kwargs)
        container.data = data
        return container
    return wrapped

def hookInfo(key, value):
    def realDecorator(f):
        def wrapped(*args, **kwargs):
            contained = f(*args, **kwargs)
            contained.info[key] = value
            return contained
        return wrapped
    return realDecorator
