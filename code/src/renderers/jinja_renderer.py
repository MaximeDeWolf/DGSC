from jinja2 import Environment, FileSystemLoader

class jinjaRenderer:
    """Represents the configuration of a Jinja2 template engine
    """

    def initEnvironment(self, workingDirectory):
        self._environment =  Environment(loader=FileSystemLoader(workingDirectory), trim_blocks=True)

    def loadTemplate(self, templatePath):
        self._template = self._environment.get_template(templatePath)

    def loadData(self, data):
        self._template.globals = data

    def render(self):
        return self._template.render()
