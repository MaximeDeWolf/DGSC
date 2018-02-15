import simplejson as json
from ruamel.yaml import YAML
from containers import many_items
from containers import single_item
import sys

@many_items.manyTimes
def load(filepath):
    try:
        loader = _chooseLoaderFromExtension(filepath.data)
    except ValueError as e:
        print(e)
        sys.exit(1)
    return loader(filepath)

def _chooseLoaderFromExtension(filename):
    if filename[-5:] == '.json':
        return _loadJson
    elif filename[-5:] == '.yaml' or filename[-4:] == '.yml':
        return _loadYaml
    else:
        raise ValueError('The extension of the file \"{}\" is not handled by the loader.'.format(filename))

"""TODO:
Envelop data in a container object
"""
@single_item.hookInfo('type', 'yaml')
@single_item.openContainer
def _loadYaml(filepath):
    yamlFile = open(filepath)
    loader = YAML(typ='safe')
    data = loader.load(yamlFile)
    return data

@single_item.hookInfo('type', 'json')
@single_item.openContainer
def _loadJson(filepath):
    jsonFile = open(filepath)
    data = json.load(jsonFile)
    return data
