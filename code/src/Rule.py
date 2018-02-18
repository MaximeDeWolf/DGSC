import sys
from loaders import loader
from loaders import lister
from renderers import jinja_renderer

""" Prototype of rule syntax
"""
R= {
    'target': lister.listFiles('../res/*.json'),
    'data': {'json': loader.load(lister.listFiles('../res/players.json')),
           'yaml': loader.load(lister.listFiles('../res/players.yaml'))
           },
    'template': 'mixedTemplate.j2',
    'output': '../out/mixed.txt'
}

def applyRule(rule):
    renderer = jinja_renderer.jinjaRenderer()
    renderer.initEnvironment('../res/')
    renderer.loadTemplate(rule['template'])
    extractDataInDico(rule['data'])
    for element in rule['target']:
        print(element)
        renderer.loadData(rule['data'])
        output = open(rule['output'], 'w')
        output.write(renderer.render())

def extractDataInDico(dico):
    keys = dico.keys()
    for key in keys:
        dico[key] = dico[key].extractData()

if __name__ == '__main__':
    applyRule(R)
