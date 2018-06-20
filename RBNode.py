import Color


class RBNode(object):             # red-black tree's node

    def __init__(self, key):      # constructor
        """setters"""
        c = Color.Color()
        self._key = key           # Node's key
        self._red = c.BLACK       # Node color: False = BLACK, True = RED
        self._left = None         # Left child
        self._right = None        # Right child
        self._p = None            # Parent

    """getters"""
    key = property(fget=lambda self: self._key, doc="The node's key")
    red = property(fget=lambda self: self._red, doc="The node color")
    left = property(fget=lambda self: self._left, doc="The node's left child")
    right = property(fget=lambda self: self._right, doc="The node's right child")
    p = property(fget=lambda self: self._p, doc="The node's parent")

    def __repr__(self):           # node's string representation
        return str(self.key)
