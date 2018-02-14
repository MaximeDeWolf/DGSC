from containers import single_item

class ManyItems(single_item.SingleItem):

    def __init__(self, data):
        super().__init__(data)

    def __iter__(self):
        return iter(self.data)

    """
    def __getitem__(self, key):
        for field in self.data:
    """
