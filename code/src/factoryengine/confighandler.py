import importlib.util
import os
from tools.utils import loadYAML
from schema import Optional, Schema, And, Use


def _importModules(modulesPath):
    """
    Import a list of modules via their filepath
    :param modulesPath: a list of filepath
    :return: the list of newly immported modules
    """
    modules = []
    for module in modulesPath:
        modules.append(_importModule(module))
    return modules


def _isListOfStr(list_):
    """
    Check if a list contains only str objects
    :param list_: the list to check
    :return: True iif the list contains only str, False otherwise
    """
    for e in list_:
        if type(e) != str:
            return False
    return True


def _importModule(modulePath):
    """
    Import a single module via its filepath
    :param modulePath: the filepath of the module
    :return: the imported module
    """
    moduleName = modulePath.split(os.sep)[-1].split('.')[0]
    spec = importlib.util.spec_from_file_location(moduleName, modulePath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_DEFAULT_CONF = {
    'TEMPLATE': {
        'BACKEND': 'renderers/jinja_renderer.py',
        'DIR': '.'
    },
    'PRODUCTION': {
        'WORKING_DIR': '.',
        'MODULES': ['loaders/loader.py', 'loaders/lister.py', 'loaders/extractor.py',
                    'transformers/filename_transformer.py', 'transformers/meta_functions.py',
                    'transformers/data_transformer.py', 'transformers/wrapper.py', 'filters/selection_functions.py']
    }
}


_SCHEMA_CONF = Schema({
    Optional('TEMPLATE'): {
        Optional('BACKEND'): And(str, Use(_importModule)),
        Optional('DIR'): str
    },
    Optional('PRODUCTION'): {
        Optional('WORKING_DIR'): str,
        Optional('MODULES'): And(list, _isListOfStr, Use(_importModules))
    }
})


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
        self._validateConfigSchema()

    def _mergeConfigs(self):
        """
        Merge the _DEFAULT_CONF with the configuration provided by the user
        """
        mergedConfig = {**self.config, **_DEFAULT_CONF}
        baseModules = set(_DEFAULT_CONF['PRODUCTION']['MODULES'])
        newModules = set(mergedConfig['PRODUCTION']['MODULES'])
        modules = baseModules | newModules
        mergedConfig['PRODUCTION']['MODULES'] = list(modules)
        self.config = mergedConfig

    def computeGlobals(self):
        """Compute all the modules usable within a rule and store it in the _globals dictionnary.
        This dictionary is then used in the _eval function.
        """
        _globals = {}
        for module in self.config['PRODUCTION']['MODULES']:
            _globals[module.SHORT_NAME] = module
        return _globals

    def _validateConfigSchema(self):
        """
        Check if the configuration is correctly formatted
        """
        self.config = _SCHEMA_CONF.validate(self.config)
