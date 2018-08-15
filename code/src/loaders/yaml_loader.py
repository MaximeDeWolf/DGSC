from ruamel.yaml import YAML

from containers import single_item


def canOpen(filename):
    return filename[-5:] == '.yaml' or filename[-4:] == '.yml'


@single_item.hookInfo('type', 'yaml')
@single_item.openContainer
def loadfile(filepath):
    yamlFile = open(filepath)
    loader = YAML(typ='safe')
    data = loader.load(yamlFile)
    return data