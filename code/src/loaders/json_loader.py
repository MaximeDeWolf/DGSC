import simplejson as json

from containers import single_item


def canOpen(filename):
    return filename[-5:] == '.json'


@single_item.hookInfo('type', 'json')
@single_item.openContainer
def loadfile(filepath):
    jsonFile = open(filepath)
    data = json.load(jsonFile)
    return data