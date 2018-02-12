import simplejson as json
from ruamel.yaml import YAML
import sys

def load(filepath):
    try:
        loader = _chooseLoaderFromExtension(filepath)
    except ValueError as e:
        print(e)
        sys.exit(1)
    return loader(filepath)

def _chooseLoaderFromExtension(filename):
    if filename[-5:] == '.json':
        return _loadJson
    elif filename[-5:] == '.yaml':
        return _loadYaml
    else:
        raise ValueError('The extension of the file \"{}\" is not handled by the loader.'.format(filename))

"""TODO:
Envelop data in a container object
"""
def _loadYaml(filepath):
    yamlFile = open(filepath)
    loader = YAML(typ='safe')
    data = loader.load(yamlFile)
    return data

def _loadJson(filepath):
    jsonFile = open(filepath)
    data = json.load(jsonFile)
    return data
