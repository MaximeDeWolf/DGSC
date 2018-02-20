from containers import single_item

class ManyItems(single_item.SingleItem):

    def __init__(self, data):
        super().__init__(data)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __str__(self):
        string = str(self.info)+'\n\n'
        for data in self.data:
            string += str(data)+'\n\n'
        return string

    def extractData(self):
        """Unwrap the data of all wrapped items and return it as a list of value.
        """
        extractedData = [elem.extractData() for elem in self.data]
        return extractedData


def manyTimes(function):
    """Execute a function several times and envelop its return values in a ManyItems object.

    The function passed in argument must at least takes a ManyItems or a SingleItem
    object as first argument. The function will be execute for each objects contains
    in the ManyItems argument or a single time in the case of a SingleItem.
    """
    def wrapped(dataWrapper, *args, **kwargs):
        if type(dataWrapper) == single_item.SingleItem:
            return function(dataWrapper, *args, **kwargs)
        elif type(dataWrapper) == ManyItems:
            items = []
            for data in dataWrapper:
                items.append(function(data, *args, **kwargs))
            return ManyItems(items)
        else:
            return function(dataWrapper, *args, **kwargs)
    return wrapped
