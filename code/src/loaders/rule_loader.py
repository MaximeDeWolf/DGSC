from ruamel.yaml import YAML

def loadRulesIn(filepath):
    yamlFile = open(filepath)
    loader = YAML(typ='safe')
    data = loader.load(yamlFile)
    return data
