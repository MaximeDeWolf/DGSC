import simplejson as json
from jinja2 import Environment, FileSystemLoader
import sys

def readJson(filepath):
    jsonFile = open(filepath, mode='r')
    data = json.load(jsonFile)
    return data

def renderContent(directory, data, templatePath):
    env = Environment(loader=FileSystemLoader(directory), trim_blocks=True)
    template = env.get_template(templatePath)
    template.globals = data
    return template.render()

if __name__ == '__main__':
    data = readJson(sys.argv[1])
    content = renderContent("res/", data, "template.j2")
    print(content)
