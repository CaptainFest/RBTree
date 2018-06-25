import Color
import node


class RBTree(object):

    RBNode = node.RBNode

    def __init__(self, create_node=RBNode):

        self._nil = create_node(data=None)     # Листья нули и всегда черны
        self._root = self.nil                  # В начале корень нулевой
        self._create_node = create_node        # вызов, создающий узел

    @property
    def root(self):
        return self._root

    @property
    def nil(self):
        return self._nil

    """def _brother(self, x):        # returns node's left or right brother
        assert x.parent != self.nil
        if x == x.parent.leftChild:
            return x.parent.rightChild
        else:
            return x.parent.leftChild"""

    def min_data(self, x=None):         # Находит минимум в поддереве узла х
        if x is None:
            x = self.root
        while x.leftChild != self.nil:
            x = x.leftChild
        return x.data

    def max_data(self, x=None):         # Находит максимум в поддереве узла х
        if x is None:
            x = self.root
        while x.rightChild != self.nil:
            x = x.rightChild
        return x

    def _replace_node(self, old, new):  # замена узла при удалении
        if old.parent == self.nil:
            self._root = new
        else:
            if old == old.parent.leftChild:
                old.parent._leftChild = new
            else:
                old.parent._rightChild = new
        if new != self.nil:
            new._parent = old.parent

    def delete_data(self, data):  # вызывает операцию удаления для узла с параметром data
        node = self.search(data)
        if node == self.nil:
            return False
        self.delete_node(node)
        return True

    def delete_node(self, node):
        c = Color.Color()
        if not node or node == self.nil:
            return
        if node.leftChild == self.nil or node.rightChild == self.nil:
            y_node = node
        else:
            y_node = node.rightChild
            while y_node.leftChild != self.nil:
                y_node = y_node.leftChild
        if y_node.leftChild != self.nil:
            x = y_node.leftChild
        else:
            x = y_node.rightChild
        x._parent = y_node.parent
        if y_node.parent:
            if y_node == y_node.parent.leftChild:
                y_node.parent._leftChild = x
            else:
                y_node.parent._rightChild = x
        else:
            self._root = x
        if y_node != node:
            node._data = y_node.data
        if y_node.color == c.BLACK:
            self._delete_fix(x)

    def _delete_fix(self, x):
        c = Color.Color()
        while x.color == c.BLACK and x != self.root:
            if x == x.parent.leftChild:
                w = x.parent.rightChild
                if w.color == c.RED:
                    w._color = c.BLACK
                    x.parent._color = c.RED
                    self._left_rotate(x.parent) ####
                    w = x.parent.rightChild
                if w.leftChild.color == c.BLACK and w.rightChild.color == c.BLACK:
                    w._color = c.RED
                    x = x.parent
                else:
                    if w.rightChild.color == c.BLACK:
                        w.leftChild._color = c.BLACK
                        w._color = c.RED
                        self._right_rotate(w)
                        w = x.parent.rightChild
                    w._color = x.parent.color
                    x.parent._color = c.BLACK
                    w.rightChild._color = c.BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.leftChild
                if w.color == c.RED:
                    w._color = c.BLACK
                    x.parent._color = c.RED
                    self._right_rotate(x.parent)
                    w = x.parent.leftChild
                if w.rightChild.color == c.BLACK and w.leftChild.color == c.BLACK:
                    w._color = c.RED
                    x = x.parent
                else:
                    if w.leftChild.color == c.BLACK:
                        w.rightChild._color = c.BLACK
                        w._color = c.RED
                        self._left_rotate(w)
                        w = x.parent.leftChild
                    w._color = x.parent.color
                    x.parent._color = c.BLACK
                    w.leftChild._color = c.BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        x._color = c.BLACK

    def search(self, data, x=None):  # Search the subtree rooted at x
        if x is None:
            x = self.root
        while x != self.nil and data != x.data:
            if data < x.data:
                x = x.leftChild
            else:
                x = x.rightChild
        return x

    def insert_data(self, data):     # Insert the data into the tree
        self.insert_node(self._create_node(data=data))

    def insert_node(self, z):      # Insert node z into the tree
        c = Color.Color()
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.data < x.data:
                x = x.leftChild
            else:
                x = x.rightChild
        z._parent = y
        if y == self.nil:
            self._root = z
        elif z.data < y.data:
            y._leftChild = z
        else:
            y._rightChild = z
        z._leftChild = self.nil
        z._rightChild = self.nil
        z._color = c.RED
        self._insert_fix(z)

    def _insert_fix(self, z):  # Restore red-black properties after insert
        c = Color.Color()
        while z.parent.color:
            if z.parent == z.parent.parent.leftChild:
                y = z.parent.parent.rightChild
                if y.color:
                    z.parent._color = c.BLACK
                    y._color = c.BLACK
                    z.parent.parent._color = c.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.rightChild:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent._color = c.BLACK
                    z.parent.parent._color = c.RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.leftChild
                if y.color:
                    z.parent._color = c.BLACK
                    y._color = c.BLACK
                    z.parent.parent._color = c.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.leftChild:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent._color = c.BLACK
                    z.parent.parent._color = c.RED
                    self._left_rotate(z.parent.parent)
        self.root._color = c.BLACK

    def tree_black_height(self):
        x = self.root
        count = 0
        while x is not None:
            if not x.color or x == self.nil:
                count += 1
            x = x.leftChild
        return count

    def tree_height(self, x=None, l_height=0, r_height=0):
        if x is None:
            x = self.root
        if x.leftChild is None and x.rightChild is None:
            return 1
        else:
            if x.leftChild is not None:
                l_height = self.tree_height(x.leftChild, l_height, r_height)
            if x.rightChild is not None:
                r_height = self.tree_height(x.rightChild, l_height, r_height)
            if l_height > r_height:
                return l_height + 1
            else:
                return r_height + 1

    def _left_rotate(self, x):  # rotate node x to left
        y = x.rightChild
        x._rightChild = y.leftChild
        if y.leftChild != self.nil:
            y.leftChild._parent = x
        y._parent = x.parent
        if x.parent == self.nil:
            self._root = y
        elif x == x.parent.leftChild:
            x.parent._leftChild = y
        else:
            x.parent._rightChild = y
        y._leftChild = x
        x._parent = y

    def _right_rotate(self, x):  # rotate node x to right
        y = x.leftChild
        x._leftChild = y.rightChild
        if y.rightChild != self.nil:
            y.rightChild._parent = x
        y._parent = x.parent
        if x.parent == self.nil:
            self._root = y
        elif x == x.parent.rightChild:
            x.parent._rightChild = y
        else:
            x.parent._leftChild = y
        y._rightChild = x
        x._parent = y

    def check_prop(self):               # returns True if RBTree is ok

        def is_red_black_node(node):    # @return: num_black
            # check has _left and _right or neither
            if (node.leftChild and not node.rightChild) or (node.rightChild and not node.leftChild):
                return 0, False

            # check leaves are black
            if not node.leftChild and not node.rightChild and node.color:
                return 0, False

            # if node is red, check children are black
            if node.color and node.leftChild and node.rightChild:
                if node.leftChild.color or node.rightChild.color:
                    return 0, False

            # descend tree and check black counts are balanced
            if node.leftChild and node.rightChild:

                # check children's parents are correct
                if self.nil != node.leftChild and node != node.leftChild.parent:
                    return 0, False
                if self.nil != node.rightChild and node != node.rightChild.parent:
                    return 0, False

                # check children are ok
                left_counts, left_ok = is_red_black_node(node.leftChild)
                if not left_ok:
                    return 0, False
                right_counts, right_ok = is_red_black_node(node.rightChild)
                if not right_ok:
                    return 0, False

                # check children's counts are ok
                if left_counts != right_counts:
                    return 0, False
                return left_counts, True
            else:
                    return 0, True

        num_black, is_ok = is_red_black_node(self.root)
        return is_ok and not self.root.color


def save_as_dot(t, f,):  # writing file in a file f.dot

    def node_id(node):
        return 'N%d' % id(node)

    def node_color(node):
        if node.color:
            return "RED"
        else:
            return "BLACK"

    def visit_node(node):                      # BFA pre-order search
        f.write("  %s [data=\"%s\", color=\"%s\"];\n" % (node_id(node), node, node_color(node)))
        if node.leftChild:
            if node.leftChild != t.nil:
                visit_node(node.leftChild)
                f.write("  %s -> %s ; \n" % (node_id(node), node_id(node.leftChild)))
        if node.rightChild:
            if node.rightChild != t.nil:
                visit_node(node.rightChild)
                f.write("  %s -> %s ; \n" % (node_id(node), node_id(node.rightChild)))

    f.write("Red black tree" + '\n')
    visit_node(t.root)


def test_insert(t):   # Insert datas one by one checking prop
    datas = [5, 3, 6, 7, 2, 4, 21, 8, 99, 9, 32, 23]
    for i, data in enumerate(datas):
        t.insert_data(data)
    assert t.check_prop()
    # print("Черная высота дерева = ", t.tree_black_height())
    # print("Высота дерева = ", t.tree_height())


def test_min_max(t):
    datas = [5, 3, 6, 7, 2, 4, 21, 8, 99, 9, 32, 23]
    m_datas = [5, 3, 21, 10, 32]
    for i, data in enumerate(datas):
        t.insert_data(data)
    for i, m_data in enumerate(m_datas):
        if t.search(m_data).data is not None:
            print("максимум в поддереве узла", m_data, " = ", t.max_data(t.search(m_data)))
            print("минимум в поддереве узла", m_data, " = ", t.min_data(t.search(m_data)))
            print("")
        else:
            print("нет узла", m_data, "в дереве")
            print("")


def test_search(t):
    datas = [5, 3, 6, 7, 2, 4, 21, 8, 99, 9, 32, 23]
    s_datas = [6, 3, 24, 23, 99, 101]
    for i, data in enumerate(datas):
        t.insert_data(data)
    for i, s_data in enumerate(s_datas):
        if t.search(s_data).data is not None:
            print("data", s_data, "exists")
        else:
            print("data", s_data, "is not exist")


def test_random_insert(t, s):
    max_data = 2000
    r.seed(2)
    rand_datas = list(r.SystemRandom().sample(range(max_data), s))
    for i, data in enumerate(rand_datas):
        t.insert_data(data)
    assert t.check_prop()


def test_delete(t):
    datas = [5, 3, 6, 7, 2, 4, 21, 8, 99, 9, 32, 23]
    ddatas = [3, 21, 7, 32]
    for i, data in enumerate(datas):
        t.insert_data(data)
    for i, ddata in enumerate(ddatas):
        t.delete_data(ddata)
    assert t.check_prop()


if '__main__' == __name__:
    import os
    import random as r

    def write_tree(tree, filename):  # Write the tree as an SVG file
        f = open('%s.dot' % filename, 'w')
        save_as_dot(tree, f)
        f.close()
        os.system('dot %s.dot -T svg -o %s.svg' % (filename, filename))

    r.seed(2)
    t = RBTree()
    print("Введите цифру 1, если хотите построить дерево со случайным набором ключей и определить его высоту")
    print("Введите цифру 2, если хотите построить дерево с заданным набором ключей, чтобы проверить вставку")
    print("Введите цифру 3, если хотите протестировать удаление узлов")
    print("Введите цифру 4, если хотите протестировать max и min")
    print("Введите цифру 5, если хотите протестировать поиск")
    a = int(input())
    if a == 1:
        for size in range(30, 101, 10):
            h_1, h_2, hh_1, hh_2, c_1, c_2, c_3, c_4 = 0, 0, 0, 0, 0, 0, 0, 0
            for i in range(1000):
                t = RBTree()
                test_random_insert(t, size)
                if i == 0:
                    h_1 = t.tree_height()
                    h_2 = t.tree_black_height()
                if t.tree_height() == h_1:
                    c_1 += 1
                else:
                    hh_1 = t.tree_height()
                    c_2 += 1
                if t.tree_black_height() == h_2:
                    c_3 += 1
                else:
                    hh_2 = t.tree_black_height()
                    c_4 += 1
            print("----------")
            print("Количество ключей = %d" % size)
            print("Средняя черн высота дерева = %f" % ((h_2 * c_3 + hh_2 * c_4) / 1000))
            print("Средняя высота дерева = %f" % ((h_1 * c_1 + hh_1 * c_2) / 1000))
    elif a == 2:
        test_insert(t)
    elif a == 3:
        test_delete(t)
    elif a == 4:
        test_min_max(t)
    elif a == 5:
        test_search(t)
    write_tree(t, 'tree')
