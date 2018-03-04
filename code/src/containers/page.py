from containers import many_items

class Page(many_items.ManyItems):

    def __init__(self, data, pageNumber):
        super().__init__(data)
        self.pageInfo = {'pageNum': pageNumber}

    def extractData(self):
        data = super().extractData()
        return {'page': self.pageInfo, 'dataList': data}
