import sys
import containers.abstractItem
from containers import many_items
from containers import single_item
from factoryengine import rulehandler

SHORT_NAME = 'Lo'


@containers.abstractItem.partialEval
@many_items.manyTimes
@single_item.wrapString
def load(filepath):
    """Load the data contained in a file.
    """
    try:
        loader = _chooseLoaderFromExtension(filepath.data)
    except ValueError as e:
        print(e)
        sys.exit(1)
    loaded = loader(filepath)
    return loaded


def _chooseLoaderFromExtension(filename):
    """Select the appropriate loader based on the extension of the file.
    """
    for loader in rulehandler.LOADERS:
        if loader.canOpen(filename):
            return loader.loadfile
    raise ValueError('The extension of the file \"{}\" is not handled by the loaders.'.format(filename))


