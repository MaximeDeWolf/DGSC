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
    for element in rule['target']:
        renderer.loadData(rule['data'])
        output = open(rule['output'], 'w')
        output.write(renderer.render())


if __name__ == '__main__':
    applyRule(R)
