from jinja2 import Environment, FileSystemLoader, contextfilter

@contextfilter
def relative_url(context, targetpath):
    basepath = context['page']
    basedir = os.path.dirname(basepath)
    targetdir = os.path.dirname(os.path.join('.', targetpath))
    diff = os.path.relpath(targetdir, basedir)
    return os.path.join(diff, os.path.basename(targetpath))


class Renderer:
    """Represents the configuration of a Jinja2 template engine
    """

    def initEnvironment(self, workingDirectory):
        self._environment =  Environment(loader=FileSystemLoader(workingDirectory), trim_blocks=True)
        self._environment.filters.update({
            'relative': relative_url,
        })

    def loadTemplate(self, templatePath):
        self._template = self._environment.get_template(templatePath)

    def loadData(self, data):
        self._template.globals = data

    def render(self):
        return self._template.render()
