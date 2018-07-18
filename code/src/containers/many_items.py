import copy
from containers import abstractItem, single_item
from containers.single_item import SingleItem


class ManyItems(abstractItem.AbstractItem):

    def __init__(self, data):
        super().__init__(data)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __str__(self):
        string = "ManyItems:\n-Info: {}\n\n-Data:\n".format(str(self.info))
        for data in self.data:
            string += "{}\n\n".format(str(data))
        return string

    def __getitem__(self, item):
        return self.data[item]

    def extractData(self):
        """Unwrap the data of all wrapped items and return it as a list of value."""
        extractedData = [elem.extractData() for elem in self.data]
        return extractedData


def manyTimes(function):
    """Execute a function several times and envelop its return values in a ManyItems object.

    The function passed in argument must at least takes a ManyItems or a SingleItem
    object as first argument. The function will be executed for each objects contained
    in the ManyItems argument or a single time in the case of a SingleItem.
    """
    def wrapped(dataWrapper, *args, **kwargs):
        if isinstance(dataWrapper, single_item.SingleItem):
            return function(dataWrapper, *args, **kwargs)
        elif isinstance(dataWrapper, ManyItems):
            items = []
            for data in dataWrapper:
                res = function(data, *args, **kwargs)
                if isinstance(res, list):
                    items.extend(res)
                else:
                    items.append(res)
            dataWrapper.data = items
            return dataWrapper
        else:
            return function(dataWrapper, *args, **kwargs)
    return wrapped

def manyToSingle(f):
    """Looks if the ManyItems returned by the function 'f' contains only one SingleItem.

    If it does, this SingleItem is returned instead of the ManyItems.
    """
    def wrapped(*args, **kwargs):
        res = f(*args, **kwargs)
        if isinstance(res, ManyItems):
            if len(res) == 1:
                res = res.data[0]
            return res
        else:
            return res
    return wrapped


def singleToMany(f):
    """
    Transform a SingleItem into a ManyItems
    """
    def wrapped(dataWrapper, *args, **kwargs):
        if isinstance(dataWrapper, SingleItem):
            newContainer = ManyItems([dataWrapper])
        else:
            newContainer = dataWrapper
        return f(newContainer, *args, **kwargs)
    return wrapped


@singleToMany
@manyTimes
def _listItems(singleItem):
    """Transform a list of data in a list of SingleItem. This function ensure that
    every SingleItem created stay at the same wrapping level than the others.

    If "data" is a SingleItem, then it will be transformed in a ManyItems containing
    the list of newly created SingleItem.
    Else, "data" is supposed to be a ManyItems. Then this ManyItems will contain all SingleItem
    that has been created from the previous ones.
    """
    try:
        itemList = []
        if isinstance(singleItem.data, list):
            for data in singleItem.data:
                if isinstance(data, single_item.SingleItem):
                    itemList.append(data)
                else:
                    item = single_item.SingleItem(data)
                    item.info = copy.copy(singleItem.info)
                    itemList.append(item)
        else:
            itemList.append(singleItem)
        return itemList
    except AttributeError as e:
        raise TypeError

def flattenContainers(f):
    def flattener(container, *args, **kwargs):
        return f(_listItems(container), *args, **kwargs)
    return flattener