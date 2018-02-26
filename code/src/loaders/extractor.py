from containers import many_items
from containers import single_item
import copy

SHORT_NAME = 'E'

@single_item.partialEval
@many_items.manyTimes
def fetch( container, toExtract,):
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

@single_item.partialEval
@single_item.singleToMany
@many_items.manyTimes
def listItems(singleItem):
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
        item.info['number'] = count
        count += 1
        itemList.append(item)
    return itemList
