from containers import many_items

class Page(many_items.ManyItems):

    def __init__(self, data, pageNumber):
        super().__init__(data)
        self.pageInfo = {'pageNum': pageNumber}

    def extractData(self):
        """Override the method of the same name from the ManyItems class.

        This allows the Page object to store additional informations.
        """
        data = super().extractData()
        return {'page': self.pageInfo, 'dataList': data}

    def __getattr__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self.pageInfo[name]
