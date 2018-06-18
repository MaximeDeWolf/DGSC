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
        You can specify several fields in the 'dataPath' by separating them by '|'.

        For example, if the data of a container is {a:{b:{c:'answer'}}} then, by following the
        datapath 'a|b|c' we obtain the string "answer".
        """
        keys = dataPath.split('|')
        newData = self.data
        for key in keys:
            newData = newData[key]
        return newData

    def _modifyData(self, dataPath, newValue):
        keys = dataPath.split('|')
        newData = self.data
        for key in keys[0:-1]:
            newData = newData[key]
        newData[keys[-1]] = newValue
