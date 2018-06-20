import containers.abstractItem
from containers import many_items
from containers import single_item
from containers import paginator
import copy

SHORT_NAME = 'E'

@containers.abstractItem.partialEval
@many_items.manyToSingle
@many_items.manyTimes
def fetch( container, toExtract):
    """Browse the data structure of a loaded file and wrap the value of the field in a SingleItem.
    You can specify several fields by separating them by '.'.
    """
    newData = container._accessData(toExtract)
    container.info['datapath'] = toExtract
    container.data = newData
    return container


@containers.abstractItem.partialEval
@many_items.flattenContainers
def paginate(items, itemsPerPage, orphans=0):
    """Creates a Paginator in terms of the arguments received."""
    return paginator.Paginator(items, itemsPerPage, orphans)
