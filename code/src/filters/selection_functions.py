
SHORT_NAME = 'SF'

def selectItems(dataPath, toMatch):
    def selector(container):
        data = container._accessData(dataPath)
        return data == toMatch
    return selector

def deleteItems(dataPath, toMatch):
    def eraser(container):
        data = container._accessData(dataPath)
        return not (data == toMatch)
    return eraser
