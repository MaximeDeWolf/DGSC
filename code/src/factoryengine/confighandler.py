import copy
import importlib
from tools.utils import loadYAML
from schema import Optional, Schema, And, Use

_DEFAULT_CONF = {
    'TEMPLATE': {
        'BACKEND': 'renderers.jinja_renderer',
        'DIR': '.'
    },
    'PRODUCTION': {
        'WORKING_DIR': '.',
        'MODULES': ['loaders.loader', 'loaders.lister', 'loaders.extractor', 'transformers.filename_transformer',
                    'transformers.meta_functions', 'filters.selection_functions',
                    'transformers.data_transformer', 'transformers.wrapper']
    }
}


_SCHEMA_CONF = Schema({
    Optional('TEMPLATE'): {
        Optional('BACKEND'): str,
        Optional('DIR'): str
    },
    Optional('PRODUCTION'): {
        Optional('WORKING_DIR'): str,
        Optional('MODULES'): list
    }
})


def _importModules(toImport):
    modules = []
    for module in toImport:
        modules.append(importlib.import_module(module))
    return modules


def _importBackend(toImport):
    backend = importlib.import_module(toImport)
    return backend


def _isListOfStr(list_):
    for e in list_:
        if type(e) != str:
            return False
    return True

class ConfigHandler:

    def __init__(self, configFile, configPathProvided=False):
        if configPathProvided:
            self.config = loadYAML(configFile)
        else:
            try:
                self.config = loadYAML(configFile)
            except ValueError:
                self.config = _DEFAULT_CONF
        self._mergeConfigs()
        print(self.config)
        #self._validateConfigSchema()
        self._importModules()
        self._importBackend()

    def _mergeConfigs(self):
        mergedConfig = {**self.config, **_DEFAULT_CONF}
        baseModules = set(_DEFAULT_CONF['PRODUCTION']['MODULES'])
        newModules = set(mergedConfig['PRODUCTION']['MODULES'])
        modules = baseModules | newModules
        mergedConfig['PRODUCTION']['MODULES'] = list(modules)
        self.config = mergedConfig

    def _importModules(self):
        toImport = self.config['PRODUCTION']['MODULES']
        modules = []
        for module in toImport:
            modules.append(importlib.import_module(module))
        self.config['PRODUCTION']['MODULES'] = modules

    def _importBackend(self):
        toImport = self.config['TEMPLATE']['BACKEND']
        backend = importlib.import_module(toImport)
        self.config['TEMPLATE']['BACKEND'] = backend

    def computeGlobals(self):
        """Compute all the modules usable within a rule and store it in the _globals dictionnary.
        This dictionary is then used in the _eval function.
        """
        _globals = {}
        for module in self.config['PRODUCTION']['MODULES']:
            _globals[module.SHORT_NAME] = module
        return _globals

    def _validateConfigSchema(self):
        self.config = _SCHEMA_CONF.validate(self.config)
