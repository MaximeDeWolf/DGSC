from containers import many_items
from containers import single_item
import copy

@many_items.manyTimes
def fetch(container, toExtract):
    """Browse the data structure of a loaded file and wrap the value of the field in a SingleItem.
    You can specify several fields by separating them by '|'.
    """
    keys = toExtract.split('|')
    newData = container.data
    for key in keys:
        newData = newData[key]
    container.info['datapath'] = toExtract
    container.data = newData
    return container


def listItems(container):
    """Transform a list of data in a list of SingleItem. This function ensure that
    every SingleItem created stay at the same wrapping level than the others.

    If "container" is a SingleItem, then it will be transformed in a ManyItems containing
    the list of newly created SingleItem.
    Else, "container" is supposed to be a ManyItems. Then this ManyItems will contain all SingleItem
    that has been created from the previous ones.
    """
    if type(container) == single_item.SingleItem:
        items = _expandSingleItem(container)
        container = many_items.ManyItems(items)
        return container
    else:
        items = []
        for singleItem in container:
            item = _expandSingleItem(singleItem)
            items.extend(item)
        newContainer = many_items.ManyItems(items)
        newContainer.info = container.info
        return newContainer


def _expandSingleItem(singleItem):
    """Wrapp each element of list of data in a SingleItem.
    """
    items = []
    count = 0
    for data in singleItem.data:
        item = single_item.SingleItem(data)
        item.info = copy.copy(singleItem.info)
        item.info['number'] = count
        #hook the index of this data in order to retrieve it easily
        count += 1
        items.append(item)
    return items
