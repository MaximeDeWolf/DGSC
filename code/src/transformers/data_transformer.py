
SHORT_NAME = 'DT'

def toUpper(dataPath):
    def rewriter(container):
        newData = container._accessData(dataPath).upper()
        container._modifyData(dataPath, newData)
        return container
    return rewriter
