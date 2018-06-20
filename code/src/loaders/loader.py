import sys
import simplejson as json
from ruamel.yaml import YAML

import containers.abstractItem
from containers import many_items
from containers import single_item

SHORT_NAME = 'Lo'

@containers.abstractItem.partialEval
@many_items.manyTimes
@single_item.wrapString
def load(filepath):
    """Load the data contained in a file.
    """
    try:
        loader = _chooseLoaderFromExtension(filepath.data)
    except ValueError as e:
        print(e)
        sys.exit(1)
    loaded = loader(filepath)
    return loaded

def _chooseLoaderFromExtension(filename):
    """Select the appropriate loader based on the extension of the file.
    """
    if filename[-5:] == '.json':
        return _loadJson
    elif filename[-5:] == '.yaml' or filename[-4:] == '.yml':
        return _loadYaml
    else:
        raise ValueError('The extension of the file \"{}\" is not handled by the loader.'.format(filename))

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
