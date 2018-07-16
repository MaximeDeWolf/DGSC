import argparse

from factoryengine.confighandler import ConfigHandler
from factoryengine.rulehandler import RuleHandler

CONFIG_FILE_NAME = 'config.yaml'

def _getRuleFiles():
    """Extract the rule files paths passed from the command line."""
    parser = argparse.ArgumentParser(description="Process the rules contained in some Yaml files.")
    parser.add_argument('ruleFiles', metavar='F', type=str, nargs='+',
                        help='a file path or a regex pointing some Yaml files containing some rules')
    args = parser.parse_args()
    return args.ruleFiles


if __name__ == '__main__':
    configHandler = ConfigHandler(CONFIG_FILE_NAME)
    globals = configHandler.computeGlobals()
    rulehandler = RuleHandler(globals, _getRuleFiles())
    rulehandler.processRules()
