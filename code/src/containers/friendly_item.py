
class FriendlyItem:

    def __init__(self, item):
        self.item = item

    def __getattr__(self, name):
        try:
            return self.item.info[name]
        except KeyError:
            return self.item.__getattribute__(name)
