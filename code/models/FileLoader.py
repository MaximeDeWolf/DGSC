import simplejson as json
from ruamel.yaml import YAML

def jsonLoader(filepath):
    jsonFile = open(filepath, mode='r')
    data = json.load(jsonFile)
    return data

def yamlLoader(filepath):
    yamlFile = open(filepath)
    yaml = YAML(typ = 'safe')
    return yaml.load(yamlFile)

if __name__ == '__main__':
    print(jsonLoader('res/players.json'))
    print(yamlLoader('res/players.yaml'))
