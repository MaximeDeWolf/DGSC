import glob
from containers import single_item
from containers import many_items

def listFiles(regex, filterFunction = lambda x : True):
    fileNames = glob.glob(regex, recursive=True)
    fileNames = _filter(fileNames, filterFunction)
    items = []
    for fileName in fileNames:
        item = single_item.SingleItem(fileName)
        item.info['filepath'] = fileName
        items.append(item)
    itemGroup = many_items.ManyItems(items)
    return itemGroup

def _filter(collection, filterFunction):
    newList = []
    for elem in collection:
        if filterFunction(elem):
            newList.append(elem)
    return newList
