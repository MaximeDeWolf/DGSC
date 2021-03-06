import importlib.util
import os
from tools.utils import loadYAML
from schema import Optional, Schema, And, Use


def _importModules(modulesPath):
    """
    Import a list of modules via their filepath
    :param modulesPath: a list of filepath
    :return: the list of newly imported modules
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


def _mergeLists(defaultList, newList):
    baseSet = set(defaultList)
    newSet = set(newList)
    merged = baseSet | newSet
    print(merged)
    return list(merged)


def _recursiveMerge(priorityDico, defaultDico):
    if type(defaultDico) == dict:
        res = {}
        for key, value in defaultDico.items():
            try:
                res[key] = _recursiveMerge(priorityDico[key], value)
            except KeyError:
                res[key] = value
        return res
    elif type(defaultDico) == list:
        priorityDico.extend(defaultDico)
        return priorityDico
    else:
        return priorityDico


_DEFAULT_CONF = {
    'TEMPLATE': {
        'BACKEND': 'renderers/jinja_renderer.py',
        'DIR': ['.']
    },
    'PRODUCTION': {
        'MODULES': ['loaders/loader.py', 'loaders/lister.py', 'loaders/extractor.py',
                    'transformers/filename_transformer.py', 'transformers/meta_functions.py',
                    'transformers/data_transformer.py', 'transformers/wrapper.py', 'filters/selection_functions.py'],
        'LOADERS': ['loaders/json_loader.py', 'loaders/yaml_loader.py']
    }
}


_SCHEMA_CONF = Schema({
    Optional('TEMPLATE'): {
        Optional('BACKEND'): And(str, Use(_importModule)),
        Optional('DIR'): And(list, _isListOfStr)
    },
    Optional('PRODUCTION'): {
        Optional('MODULES'): And(list, _isListOfStr, Use(_importModules)),
        Optional('LOADERS'): And(list, _isListOfStr, Use(_importModules))
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
        """mergedConfig = { **_DEFAULT_CONF, **self.config}
        print(mergedConfig)
        mergedConfig['PRODUCTION']['MODULES'] = _mergeLists(_DEFAULT_CONF['PRODUCTION']['MODULES'],
                                                            mergedConfig['PRODUCTION']['MODULES'])
        mergedConfig['PRODUCTION']['LOADERS'] = _mergeLists(_DEFAULT_CONF['PRODUCTION']['LOADERS'],
                                                            mergedConfig['PRODUCTION']['LOADERS'])
        self.config = mergedConfig"""
        self.config = _recursiveMerge(self.config, _DEFAULT_CONF)

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
