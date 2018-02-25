
class FriendlyItem:

    def __init__(self, item):
        self.data = item.data
        self.info = item.info

    def __getattr__(self, name):
        return self.info[name]
