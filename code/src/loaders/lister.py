import glob
from containers import single_item
from containers import many_items

def listFiles(regex, filterFunction=lambda x : True):
    """Return a list of the files found by a regular expression and filtered by a function.

    If there are more than 1 file, there are contained in a ManyItems.
    Else, it is contained in SingleItem.
    """
    fileNames = glob.glob(regex, recursive=True)
    fileNames = list(filter(filterFunction, fileNames))
    items = []
    if len(fileNames) == 1:
        return single_item.SingleItem(fileNames[0])
    else:
        for fileName in fileNames:
            item = single_item.SingleItem(fileName)
            item.info['filepath'] = fileName
            items.append(item)
        itemGroup = many_items.ManyItems(items)
        return itemGroup
