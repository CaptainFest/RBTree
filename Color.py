class Color(object):    # subclass color of nodes
    def __init__(self):
        self._RED = True
        self._BLACK = False

    @property
    def RED(self):
        return self._RED

    @property
    def BLACK(self):
        return self._BLACK
