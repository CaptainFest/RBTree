class Color(object):    # subclass color of nodes
    def __init__(self):
        self._RED = True
        self._BLACK = False

    RED = property(fget=lambda self: self._RED, doc="node's RED color")
    BLACK = property(fget=lambda self: self._BLACK, doc="node's BLACK color")
