from containers import many_items
from containers import page

class Paginator(many_items.ManyItems):

    def __init__(self, data, itemsPerPage, orphans=0):
        pages = self._groupPages(data, itemsPerPage, orphans)
        super().__init__(pages)
        self.paginatorInfo = {'count': len(data), 'num_pages': len(pages)}
        self.hookInfoOnChild('paginator', self.paginatorInfo)
        self._linkPages()

    def _groupPages(self, data, itemsPerPage, orphans):
        """Creates a list of Page object.

        Each Page is meant to contain exactly 'itemsPerPage' elements
        except for the last one.

        The number of elements in the last Page depends on the 'orphans' argument.

        Let R = number of total elements % 'itemsPerPage',
            If R > orphans then:
                The last Page will contain R elements.
            Else then:
                The last Page will contain R + 'itemsPerPage' elements
        """
        countPerPage = 0
        currentPage = []
        pages = []
        for item, nonTreatedItems in zip(data, range(len(data), 0, -1)):
            currentPage.append(item)
            countPerPage += 1
            if countPerPage >= itemsPerPage:
                if not (0 < nonTreatedItems <= orphans):
                    newPage = page.Page(currentPage, len(pages)+1)
                    pages.append(newPage)
                    countPerPage = 0
                    currentPage = []
        return pages

    def __getattr__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self.paginatorInfo[name]

    def _linkPages(self):
        """Add information to each Page created according to their relative "position"
        in the Paginator.
        """
        pages = self.data
        for page in pages:
            pageNumber = page.pageInfo['pageNum']
            hasPrevious = True
            hasNext = True
            if pageNumber == 1:
                hasPrevious = False
            if pageNumber == len(pages):
                hasNext = False
            if hasPrevious:
                page.pageInfo['prevPageNumber'] = pageNumber-1
            page.pageInfo['hasPrevious'] = hasPrevious
            if hasNext:
                page.pageInfo['nextPageNumber'] = pageNumber+1
            page.pageInfo['hasNext'] = hasNext


    def hookInfoOnChild(self, key, info):
        """Add the same information to each Page of the Paginator."""
        for child in self:
            child.pageInfo[key] = info

    def extractData(self):
        """Override the method of the same name from the ManyItems class.

        This allows the Page object to store additional informations.
        """
        dataPage = super().extractData()
        return {'paginator': self.paginatorInfo, 'pages': dataPage}
