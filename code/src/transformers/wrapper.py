from containers.single_item import SingleItem

SHORT_NAME = 'W'

def text(string):
    """
    Wrap a string in a SingleItem object
    :param string: The string to wrap
    :return: A SingleItem containing the "string"
    """
    return SingleItem(string)