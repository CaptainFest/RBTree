import Color


class RBNode(object):

    def __init__(self, data):          # инициализация узла
        c = Color.Color()
        """setters"""
        self._data = data              # Некие данные, хранимые в узле. В данной реализации - целые числа
        self._color = c.BLACK          # Цвет узла: False = BLACK, True = RED
        self._leftChild = None
        self._rightChild = None
        self._parent = None            # Родитель узла

    """getters"""
    @property
    def data(self):
        return self._data

    @property
    def color(self):
        return self._color

    @property
    def leftChild(self):
        return self._leftChild

    @property
    def rightChild(self):
        return self._rightChild

    @property
    def parent(self):
        return self._parent

    def __repr__(self):
        return str(self.data)