
SHORT_NAME = 'SF'

def selectItems(dataPath, toMatch):
    """
    Returns a function that follows the 'dataPath' into a container and return
    true iff this data is equal to 'toMatch'
    """
    def selector(container):
        data = container._accessData(dataPath)
        return data == toMatch
    return selector

def deleteItems(dataPath, toMatch):
    """
    Returns a function that follows the 'dataPath' into a container and return
    true iff this data is different from 'toMatch'
    """
    def eraser(container):
        data = container._accessData(dataPath)
        return not (data == toMatch)
    return eraser
