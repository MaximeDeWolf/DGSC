import sys
from loaders import loader
from loaders import lister
from loaders import extractor
from renderers import jinja_renderer
from transformers import filename_transformer

""" Prototype of rule syntax
"""
R= {
    'target': extractor.listItems(extractor.fetch(loader.load(lister.listFiles('../res/datas/*')), 'players')),
    'data': {'current': 'extractor.listItems(extractor.fetch(loader.load(current[\'filepath\']), current[\'datapath\'])).data[current[\'number\']]'
           },
    'template': 'single.j2',
    'output': '\'../res/out/\'+extractor.fetch(current, \'name\').data+\'.txt\''
}

def applyRule(rule):
    renderer = jinja_renderer.jinjaRenderer()
    renderer.initEnvironment('../res/templates/')
    renderer.loadTemplate(rule['template'])
    global current
    for element in rule['target']:
        current = element
        data = extractDataInDict(rule['data'])
        renderer.loadData(data)
        outputPath = computeOutput(rule['output'])
        output = open(outputPath, 'w')
        output.write(renderer.render())

def extractDataInDict(dataDict):
    keys = dataDict.keys()
    newDict = {}
    for key in keys:
        newDict[key] = eval(dataDict[key], globals()).extractData()
    return newDict

def computeOutput(output):
    return eval(output, globals())

if __name__ == '__main__':
    applyRule(R)
