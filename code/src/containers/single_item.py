from containers import many_items
from containers import abstractItem


class SingleItem(abstractItem.AbstractItem):

    def __init__(self, data):
        super().__init__(data)

    def __iter__(self):
        return iter([self.data])

    def __str__(self):
        string = "SingleItem:\n-Info: {}\n-Data: {}\n".format(str(self.info), str(self.data))
        return string

    def __getitem__(self, key):
        """This method allows the user to easily access the info dict
        stored in the "info" variable. We don't implement the analog method
        "__setitem__" because we don't wan't the user to modify this data structure
        """
        return self.info[key]

    def __add__(self, other):
        """
        This method concatenate data contained in 2 SingleItem objects
        :param other: A SingleItem
        :return: A new SinleItem containing the concatenated data
        """
        newData = str(self.data) + str(other.data)
        return SingleItem(newData)

    def extractData(self):
        """Return the data contained in this item.
        """
        return self.data

def openContainer(f):
    """Apply a function to the data of an item then wrapp the return
    value in SingleItem object.
    """
    def wrapped(container, *args, **kwargs):
        data = f(container.data, *args, **kwargs)
        container.data = data
        return container
    return wrapped

def hookInfo(key, value):
    """Hook some information to a SingleItem returned by the function
    passed as argument. Designed to be used as a decorator.
    """
    def realDecorator(f):
        def wrapped(*args, **kwargs):
            contained = f(*args, **kwargs)
            contained.info[key] = value
            return contained
        return wrapped
    return realDecorator

def wrapString(f):
    """Ensure that string argument passed to a function is wrapped in a SingleItem.
    """
    def wrapped(string, *args, **kwargs):
        if type(string) == str:
            item = SingleItem(string)
            item.info['filepath'] = string
            return f(item, *args, **kwargs)
        else:
            return f(string, *args, **kwargs)
    return wrapped

def singleToMany(f):
    """
    Transform a SingleItem into a ManyItems
    """
    def wrapped(dataWrapper, *args, **kwargs):
        if isinstance(dataWrapper, SingleItem):
            newContainer = many_items.ManyItems([dataWrapper])
        else:
            newContainer = dataWrapper
        return f(newContainer, *args, **kwargs)
    return wrapped


