
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
