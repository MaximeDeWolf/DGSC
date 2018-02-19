class SingleItem:

    def __init__(self, data):
        self.data = data
        self.info = {}

    def __iter__(self):
        return iter([self.data])

    def __str__(self):
        string = str(self.info)+'\n'+str(self.data)
        return string

    def __getitem__(self, key):
        """This method allows the user to easily access the info dict
        stored in the "info" variable. We don't implement the analog method
        "__setitem__" because we don't wan't the user to modify this data structure
        """
        return self.info[key]

    def extractData(self):
        return self.data

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

def wrapString(f):
    def wrapped(string, *args, **kwargs):
        if type(string) == str:
            item = SingleItem(string)
            item.info['filepath'] = string
            return f(item, *args, **kwargs)
        else:
            return f(string, *args, **kwargs)
    return wrapped
