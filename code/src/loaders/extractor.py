from containers import many_items
from containers import single_item
from containers import paginator
import copy

SHORT_NAME = 'E'

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

@single_item.partialEval
@many_items.manyToSingle
@many_items.manyTimes
def fetch( container, toExtract):
    """Browse the data structure of a loaded file and wrap the value of the field in a SingleItem.
    You can specify several fields by separating them by '|'.
    """
    newData = container._accessData(toExtract)
    container.info['datapath'] = toExtract
    container.data = newData
    return container


@single_item.partialEval
def paginate(items, itemsPerPage, orphans=0):
    """Creates a Paginator in terms of the arguments received."""
    data = _listItems(items)
    return paginator.Paginator(data, itemsPerPage, orphans)
