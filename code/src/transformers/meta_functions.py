from functools import reduce

import containers.abstractItem
import containers.many_items
from containers import many_items
from containers import single_item
import copy

from containers.many_items import flattenContainers

SHORT_NAME = 'MF'


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


@containers.abstractItem.partialEval
@containers.many_items.singleToMany
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

@containers.abstractItem.partialEval
@containers.many_items.singleToMany
@copyInfo
@flattenContainers
def map_(container, function):
    """
    Applies the function to each item of the container and return the result in a new one.
    """
    newItems = list(map(function, container))
    newContainer = many_items.ManyItems(newItems)
    return newContainer

@containers.abstractItem.partialEval
@containers.many_items.singleToMany
@copyInfo
@flattenContainers
def reduce_(container, function, initializer=None):
    """
    Aggregate all the items of the container in a new item by applying the function
    cumulatively to each item of the container. The resulting item is wrapped in a
    container and returned. The function takes exactly 2 arguments.
    """
    item = reduce(function, container)
    return item
