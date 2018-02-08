import simplejson as json
from ruamel.yaml import YAML
import sys

def load(filepath):
    try:
        loader = __chooseLoaderFromExtension(filepath)
    except ValueError as e:
        print(e)
        sys.exit(1)
    return loader(filepath)

def __chooseLoaderFromExtension(filename):
    if filename[-5:] == '.json':
        return __loadJson
    elif filename[-5:] == '.yaml':
        return __loadYaml
    else:
        raise ValueError('The extension of the file \"{}\" is not handled by the loader.'.format(filename))

def __loadYaml(filepath):
    yamlFile = open(filepath)
    data = YAML(typ='safe')
    return data

def __loadJson():
    jsonFile = open(filepath)
    data = json.load(jsonFile)
    return data
