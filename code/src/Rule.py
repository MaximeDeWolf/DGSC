import sys
import argparse
from loaders import loader
from loaders import lister
from loaders import extractor
from renderers import jinja_renderer
from transformers import filename_transformer
from loaders.rule_loader import loadRulesIn
from containers.friendly_item import FriendlyItem

_modules = [loader, lister, extractor, filename_transformer]

_globals = {}

def _computeGlobals():
    for module in _modules:
        _globals[module.SHORT_NAME] = module

def _applyRule(rule):
    renderer = jinja_renderer.jinjaRenderer()
    renderer.initEnvironment('../res/templates/')
    renderer.loadTemplate(rule['template'])
    for element in rule['target']:
        current = FriendlyItem(element)
        #print(element)
        data = _extractDataInDict(rule['data'], current)
        renderer.loadData(data)
        outputPath = _eval(rule['output'], current)
        output = open(outputPath, 'w')
        output.write(renderer.render())

def _extractDataInDict(dataDict, current):
    """Evaluate the different data fields of the rule.

    We need this function in order to include information from the current treated element
    into the data fields.
    """
    keys = dataDict.keys()
    newDict = {}
    for key in keys:
        newDict[key] = _eval(dataDict[key], current).extractData()
    return newDict

def _eval(string, localValues=None):
    """Evaluate an expression stored as a string.

    This function is similar to the 'eval' function of python but takes care of
    using the right environment.
    """
    return eval(string, _globals, {'current': localValues})

def _getRuleFiles():
    parser = argparse.ArgumentParser(description="Process the rules contained in some Yaml files.")
    parser.add_argument('ruleFiles', metavar='F', type=str, nargs='+',
                        help='a file path to a Yaml file containing some rules')
    args = parser.parse_args()
    return args.ruleFiles

if __name__ == '__main__':
    _computeGlobals()
    ruleFiles = _getRuleFiles()
    for ruleFile in ruleFiles:
        rules = loadRulesIn(ruleFile)
        for rule in rules:
            rule['target'] = _eval(rule['target'])
            _applyRule(rule)
