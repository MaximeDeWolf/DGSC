from containers.friendly_item import FriendlyItem

class AbstractItem:

    def __init__(self, data):
        self.data = data
        self.info = {}

    def __rshift__(self, other):
        return other(self)

    def __instancecheck__(self, instance):
        print("__instancecheck__")
        if isinstance(instance, FriendlyItem):
            return instance.__instancecheck__(self)
        else:
            return super().__instancecheck__(instance)
