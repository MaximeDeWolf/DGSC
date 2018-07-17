import argparse

from factoryengine.confighandler import ConfigHandler
from factoryengine.rulehandler import RuleHandler

CONFIG_FILE_NAME = 'config.yaml'

def parseCommandLine():
    """Extract the rule files paths passed from the command line."""
    parser = argparse.ArgumentParser(description="Process the rules contained in some Yaml files.")
    parser.add_argument('ruleFiles', metavar='F', type=str, nargs='+',
                        help='a file path or a regex pointing some Yaml files containing some rules')
    parser.add_argument('--conf', type=str, default=None,
                        help="modify the path to the configuration file (default: 'config.yaml') ")
    args = parser.parse_args()
    if args.conf is None:
        args.isConfProvided = False
        args.conf = CONFIG_FILE_NAME
    else:
        args.isConfProvided = True
    return args


if __name__ == '__main__':
    args = parseCommandLine()
    configHandler = ConfigHandler(args.conf, args.isConfProvided)
    globals_ = configHandler.computeGlobals()
    rulehandler = RuleHandler(globals_, args.ruleFiles, configHandler.config)
    rulehandler.processRules()
