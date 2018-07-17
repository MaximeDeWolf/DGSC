from functools import partial

from glom import glom

from tools.utils import partial


class AbstractItem:

    def __init__(self, data):
        self.data = data
        self.info = {}

    def __rshift__(self, other):
        return other(self)

    def __getattr__(self, name):
        """Permit access to the 'info' dict by a dot notation.
        ex: Let F be a AbstractItem, F.info[name] <==> F.name

        If 'name' is not a key of the 'info' dict, this method will return the value
        of the field 'name' if it exist.
        """
        try:
            return self.info[name]
        except KeyError:
            return self.__getattribute__(name)

    def _accessData(self, dataPath):
        """
        Browse the data of the container by following the 'dataPath' and return the final value found.
        You can specify several fields in the 'dataPath' by separating them by '.'.

        For example, if the data of a container is {a:{b:{c:'answer'}}} then, by following the
        datapath 'a.b.c' we obtain the string "answer".
        """
        return glom(self.data, dataPath)

    def _modifyData(self, dataPath, newValue):
        """
        Follow the 'dataPath' to access the data and replace it by 'newValue'.
        You can specify several fields in the 'dataPath' by separating them by '.'.
        """
        lastID = str.split(dataPath, '.')[-1]
        pathWithoutTerminus = '.'.join(str.split(dataPath, '.')[0:-1])
        if len(pathWithoutTerminus) == 0:
            toChange = self.data
        else:
            toChange = glom(self.data, pathWithoutTerminus)
        toChange[lastID] = newValue


def partialEval(f):
    """
    Stop the evaluation of a function until it has all the arguments it requires
    """
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except TypeError as e:
            return partial(f, *args, **kwargs)
    return wrapped