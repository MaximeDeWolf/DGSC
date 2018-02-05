import simplejson as json
from jinja2 import Environment, FileSystemLoader
import sys

def readJson(filepath):
    jsonFile = open(filepath, mode='r')
    data = json.load(jsonFile)
    return data

def renderJson(directory, data):
    env = Environment(loader=FileSystemLoader(directory), trim_blocks=True)
    template = env.get_template("template.j2")
    template.globals = data
    return template.render()

data = readJson(sys.argv[1])
content = renderJson("res/", data)
print(content)
