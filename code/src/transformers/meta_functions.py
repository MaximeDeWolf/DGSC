from functools import reduce
from containers import many_items
from containers import single_item
import copy

SHORT_NAME = 'MF'

def dataExtractor(f):
    def extractData(container, *args, **kwargs):
        return f(container.extractData, *args, **kwargs)
    return extractData

def copyInfo(f):
    """
    Copy the info of the old container and store it in the new container
    """
    def copier(container, *args, **kwargs):
        if not isinstance(container, many_items.ManyItems):
            raise TypeError
        else:
            info = copy.copy(container.info)
            newContainer = f(container, *args, **kwargs)
            newContainer.info = info
            return newContainer
    return copier

@single_item.singleToMany
@many_items.manyTimes
def _listItems(singleItem):
    """Transform a list of data in a list of SingleItem. This function ensure that
    every SingleItem created stay at the same wrapping level than the others.

    If "data" is a SingleItem, then it will be transformed in a ManyItems containing
    the list of newly created SingleItem.
    Else, "data" is supposed to be a ManyItems. Then this ManyItems will contain all SingleItem
    that has been created from the previous ones.
    """
    itemList = []
    count = 0
    for data in singleItem.data:
        item = single_item.SingleItem(data)
        item.info = copy.copy(singleItem.info)
        itemList.append(item)
    return itemList

def flattenContainers(f):
    def flattener(container, *args, **kwargs):
        return f(_listItems(container), *args, **kwargs)
    return flattener

@single_item.partialEval
@single_item.singleToMany
@copyInfo
@many_items.manyTimes
def filter_(container, function):
    """
    Returns a new container that only contains items that were present in the old
    container and match the function.
    """
    flatContainer = _listItems(container)
    matchedItems = list(filter(function, flatContainer))
    newContainer = many_items.ManyItems(matchedItems)
    return newContainer

@single_item.partialEval
@single_item.singleToMany
@copyInfo
@flattenContainers
def map_(container, function):
    """
    Applies the function to each item of the container and return the result in a new one.
    """
    newItems = list(map(function, container))
    newContainer = many_items.ManyItems(newItems)
    return newContainer

@single_item.partialEval
@single_item.singleToMany
@copyInfo
@dataExtractor
def reduce_(container, function, initializer=0):
    """
    Aggregate all the items of the container in a new item by applying the function
    cumulatively to each item of the container. The resulting item is wrapped in a
    container and returned. The function takes exactly 2 arguments.

    Does this function make any sense in our context ?
    """
    item = reduce(function, container, initializer=initializer)
    return single_item.SingleItem(item)
