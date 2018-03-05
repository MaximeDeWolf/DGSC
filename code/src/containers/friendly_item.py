
class FriendlyItem:
    """The aim of this class is only to wrap an object and to modify
    the syntax to access it. It should be totally transparent for the user.
    """

    def __init__(self, item):
        self.item = item

    def __getattr__(self, name):
        """Permit to the 'info' dict of the 'item' field by a dot notation.
        ex: Let F be a FriendlyItem, F.item.info[name] <==> F.name

        If 'name' is not a key of the 'info' dict, this method will return the value
        of the 'item' object's 'name' field.
        """
        try:
            return self.item.info[name]
        except KeyError:
            return self.item.__getattribute__(name)

    def __setattr__(self, name, value):
        """Permit to access the contained object as if it was the FriendlyItem itself.

        The only exception is if we want to access the 'item' filed of the FriendlyItem.
        """
        if name == 'item':
            super(FriendlyItem, self).__setattr__(name, value)
        else:
            self.item.__setattr__(name, value)
