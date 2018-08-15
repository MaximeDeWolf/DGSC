from containers import single_item
import os

def canOpen(filename):
    return os.path.isfile(filename)


@single_item.hookInfo('type', 'other')
@single_item.openContainer
def loadfile(filepath):
    text = open(filepath)
    return text
