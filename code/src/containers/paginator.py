from containers import many_items
from containers import page

class Paginator(many_items.ManyItems):

    def __init__(self, data, itemsPerPage, orphans=0):
        pages = self._groupPages(data, itemsPerPage, orphans)
        super().__init__(pages)
        self.paginatorInfo = {'count': len(data), 'num_pages': len(pages)}
        self._linkPages()

    def _groupPages(self, data, itemsPerPage, orphans):
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

    def _linkPages(self):
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

    def extractData(self):
        dataPage = super().extractData()
        return {'paginator': self.paginatorInfo, 'pages': dataPage}
