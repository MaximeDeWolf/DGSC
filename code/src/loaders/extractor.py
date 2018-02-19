from containers import many_items
from containers import single_item
import copy

@many_items.manyTimes
def fetch(container, toExtract):
    keys = toExtract.split('|')
    newData = container.data
    for key in keys:
        newData = newData[key]
    container.info['datapath'] = toExtract
    container.data = newData
    return container


def listItems(container):
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
    items = []
    count = 0
    for data in singleItem.data:
        item = single_item.SingleItem(data)
        item.info = copy.copy(singleItem.info)
        item.info['number'] = count
        count += 1
        items.append(item)
    return items
