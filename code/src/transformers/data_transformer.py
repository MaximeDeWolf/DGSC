from containers import single_item

SHORT_NAME = 'DT'

def toUpper(dataPath):
    """
    Returns a function that follows the 'dataPath' into a container and replace it
    by the same data but written in capital letters
    """
    def rewriter(container):
        newData = container._accessData(dataPath).upper()
        container._modifyData(dataPath, newData)
        return container
    return rewriter

def concatData(firstItem, secondItem):
    newData = {}
    for key in firstItem.data:
        newData[key] = firstItem.data[key] + secondItem.data[key]
    newItem = single_item.SingleItem(newData)
    newItem.info = firstItem.info
    return newItem