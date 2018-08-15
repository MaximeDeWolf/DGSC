from containers.single_item import SingleItem
from tools.utils import loadYAML

LOADERS = None


class RuleHandler:

    def __init__(self, globals_, ruleFiles, config):
        self._globals = globals_
        self.ruleFiles = ruleFiles
        self.config = config
        global LOADERS
        LOADERS = config['PRODUCTION']['LOADERS']

    def _applyRule(self, rule):
        """Browse a rule and render its result according to the fields that the rule contains"""
        renderer = self.config['TEMPLATE']['BACKEND'].Renderer()
        renderer.initEnvironment('../res/templates/')

        rule['target'] = self._ensureIterableContainsContainer(rule['target'])
        for element in rule['target']:
            current = element
            data = self._extractDataInDict(rule['data'], current)

            templatePath = self._eval(rule['template'], current).extractData()
            renderer.loadTemplate(templatePath)
            renderer.loadData(data)

            outputPath = self._eval(rule['output'], current).extractData()
            output = open(outputPath, 'w')
            output.write(renderer.render())

    def _extractDataInDict(self, dataDict, current):
        """Evaluate the different data fields of the rule.

        We need this function in order to include information from the current treated element
        into the data fields.
        """
        keys = dataDict.keys()
        newDict = {}
        for key in keys:
            item = self._eval(dataDict[key], current)
            newDict[key] = item.extractData()
        return newDict

    def _eval(self, string, localValues=None):
        """Evaluate an expression stored as a string.

        This function is similar to the 'eval' function of python but takes care of
        using the right environment.
        """
        return eval(string, self._globals, {'current': localValues})

    def _ensureIterableContainsContainer(self, ruleField):
        if isinstance(ruleField, SingleItem):
            return [ruleField]
        else:
            return ruleField

    def processRules(self):
        for ruleFile in self.ruleFiles:
            rules = loadYAML(ruleFile)
            for rule in rules:
                rule['target'] = self._eval(rule['target'])
                self._applyRule(rule)
