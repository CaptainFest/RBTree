import Color
import node


class RBTree(object):

    RBNode = node.RBNode

    def __init__(self, new_node=RBNode):

        """setters"""
        self._nil = new_node(data=None)      # Листья нули и всегда черны
        self._root = self.nil                # В начале корень нулевой
        self._new_node = new_node            # вызов, создающий узел

    """getters"""
    @property
    def root(self):
        return self._root

    @property
    def nil(self):
        return self._nil

    def _grandfather(self, node):               # возвращает дедушку узла
        if node != self.nil and node.parent != self.nil:
            return node.parent.parent
        else:
            return self.nil   # mb None

    def _uncle(self, node):                     # возвращает дядю узла
        g = self._grandfather(node)
        if g == self.nil:
            return self.nil
        else:
            if node.parent == g.leftChild:
                return g.rightChild
            else:
                return g.leftChild

    def _brother(self, node):                      # возвращает правого или левого брата
        assert node.parent != self.nil
        if node == node.parent.leftChild:
            return node.parent.rightChild
        else:
            return node.parent.leftChild

    def min_data(self, node=None):                 # Находит минимум в поддереве узла х
        if node is None:
            node = self.root
        while node.leftChild != self.nil:
            node = node.leftChild
        return node.data

    def max_data(self, node=None):                 # Находит максимум в поддереве узла х
        if node is None:
            node = self.root
        while node.rightChild != self.nil:
            node = node.rightChild
        return node

    def delete_data(self, data):  # вызывает операцию удаления для узла с параметром data
        node = self.find(data)
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

    def _delete_fix(self, node):
        c = Color.Color()
        while node.color == c.BLACK and node != self.root:
            b = self._brother(node)
            if b.color == c.RED:
                b._color = c.BLACK
                node.parent._color = c.RED
                self._turn_left(node.parent) if node == node.parent.leftChild else self._turn_right(node.parent)
                b = self._brother(node)
            if b.leftChild.color == c.BLACK and b.rightChild.color == c.BLACK:
                b._color = c.RED
                node = node.parent
            else:
                if node == node.parent.leftChild:
                    if b.rightChild.color == c.BLACK:
                        b.leftChild._color = c.BLACK
                        b._color = c.RED
                        self._turn_right(b)
                        b = self._brother(node)
                else:
                    if b.leftChild.color == c.BLACK:
                        b.rightChild._color = c.BLACK
                        b._color = c.RED
                        self._turn_left(b)
                        b = self._brother(node)
            b._color = node.parent.color
            node.parent._color = c.BLACK
            if node == node.parent.leftChild:
                b.rightChild._color = c.BLACK
                self._turn_left(node.parent)
            else:
                b.leftChild._color = c.BLACK
                self._turn_right(node.parent)
            node = self.root
        node._color = c.BLACK

    def find(self, data, node=None):      # находит узел с параметром data, если такой есть
        if node is None:
            node = self.root
        while node != self.nil and data != node.data:
            if data < node.data:
                node = node.leftChild
            else:
                node = node.rightChild
        return node

    def add_data(self, data):
        self.add_node(self._new_node(data=data))

    def add_node(self, node):           # добавление узла node в дерево
        c = Color.Color()
        par = self.nil
        ch = self.root
        while ch != self.nil:
            par = ch
            if node.data < ch.data:
                ch = ch.leftChild
            else:
                ch = ch.rightChild
        node._parent = par
        if par == self.nil:
            self._root = node
        elif node.data < par.data:
            par._leftChild = node
        else:
            par._rightChild = node
        node._leftChild = self.nil
        node._rightChild = self.nil
        node._color = c.RED
        self._add_fix(node)

    def _add_fix(self, node):           # восстановление свойств красно-черного дерева
        c = Color.Color()
        while node.parent.color:
            u = self._uncle(node)
            if u.color:
                node.parent._color = c.BLACK
                u._color = c.BLACK
                self._grandfather(node)._color = c.RED
                node = self._grandfather(node)
            else:
                if node.parent == node.parent.parent.leftChild:
                    if node == node.parent.rightChild:
                        node = node.parent
                        self._turn_left(node)
                    node.parent._color = c.BLACK
                    self._grandfather(node)._color = c.RED
                    self._turn_right(self._grandfather(node))
                else:
                    if node == node.parent.leftChild:
                        node = node.parent
                        self._turn_right(node)
                    node.parent._color = c.BLACK
                    self._grandfather(node)._color = c.RED
                    self._turn_left(self._grandfather(node))
        self.root._color = c.BLACK

    def tree_black_height(self):
        node = self.root
        count = 0
        while node is not None:
            if not node.color or node == self.nil:
                count += 1
            node = node.leftChild
        return count

    def tree_height(self, node=None, l_height=0, r_height=0):
        if node is None:
            node = self.root
        if node.leftChild is None and node.rightChild is None:
            return 1
        else:
            if node.leftChild is not None:
                l_height = self.tree_height(node.leftChild, l_height, r_height)
            if node.rightChild is not None:
                r_height = self.tree_height(node.rightChild, l_height, r_height)
            if l_height > r_height:
                return l_height + 1
            else:
                return r_height + 1

    def _turn_left(self, node):                     # выполнить левый поворот узла
        ch = node.rightChild
        node._rightChild = ch.leftChild
        if ch.leftChild != self.nil:
            ch.leftChild._parent = node
        ch._parent = node.parent
        if node.parent == self.nil:
            self._root = ch
        elif node == node.parent.leftChild:
            node.parent._leftChild = ch
        else:
            node.parent._rightChild = ch
        ch._leftChild = node
        node._parent = ch

    def _turn_right(self, node):                    # выполнить правый поворот узла
        ch = node.leftChild
        node._leftChild = ch.rightChild
        if ch.rightChild != self.nil:
            ch.rightChild._parent = node
        ch._parent = node.parent
        if node.parent == self.nil:
            self._root = ch
        elif node == node.parent.rightChild:
            node.parent._rightChild = ch
        else:
            node.parent._leftChild = ch
        ch._rightChild = node
        node._parent = ch

    def check_prop(self):               # returns True if RBTree is ok

        def check(x):
            if (x.leftChild and not x.rightChild) or (x.rightChild and not x.leftChild):
                return 0, False
            if not x.leftChild and not x.rightChild and x.color:
                return 0, False
            if x.color and x.leftChild and x.rightChild:
                if x.leftChild.color or x.rightChild.color:
                    return 0, False
            if x.leftChild and x.rightChild:
                if x.leftChild != self.nil and x != x.leftChild.parent:
                    return 0, False
                if x.rightChild != self.nil and x != x.rightChild.parent:
                    return 0, False
                l_count, l_ok = check(x.leftChild)
                if not l_ok:
                    return 0, False
                r_count, r_ok = check(x.rightChild)
                if not r_ok:
                    return 0, False
                if l_count != r_count:
                    return 0, False
                return l_count, True
            else:
                    return 0, True
        num_black, is_ok = check(self.root)
        return is_ok and not self.root.color


def save(t, f,):  # writing file in a file f.dot

    def node_c(x):
        if x.color:
            return "RED"
        else:
            return "BLACK"

    def writing(x):                      # BFA pre-order search
        f.write("  data=\"%s\", color=\"%s\" \t[" % (x, node_c(x)))
        if x.leftChild != t.nil:
            f.write("leftChild = \"%s\" " % (x.leftChild))
        if x.rightChild != t.nil:
            f.write("rightChild = \"%s\"" % (x.rightChild))
        f.write("]")
        f.write("\n")
        if x.leftChild:
            if x.leftChild != t.nil:
                writing(x.leftChild)
        if x.rightChild:
            if x.rightChild != t.nil:
                writing(x.rightChild)
    f.write("Red black tree" + '\n')
    writing(t.root)


def test_add(t):   # Insert datas one by one checking prop
    datas = [5, 3, 6, 7, 2, 4, 21, 8, 99, 9, 32, 23]
    for i, data in enumerate(datas):
        t.add_data(data)
    assert t.check_prop()


def test_min_max(t):
    datas = [5, 3, 6, 7, 2, 4, 21, 8, 99, 9, 32, 23]
    m_datas = [5, 3, 21, 10, 32]
    for i, data in enumerate(datas):
        t.add_data(data)
    for i, m_data in enumerate(m_datas):
        if t.find(m_data).data is not None:
            print("максимум в поддереве узла", m_data, " = ", t.max_data(t.find(m_data)))
            print("минимум в поддереве узла", m_data, " = ", t.min_data(t.find(m_data)))
            print("")
        else:
            print("нет узла", m_data, "в дереве")
            print("")


def test_find(t):
    datas = [5, 3, 6, 7, 2, 4, 21, 8, 99, 9, 32, 23]
    s_datas = [6, 3, 24, 23, 99, 101]
    for i, data in enumerate(datas):
        t.add_data(data)
    for i, s_data in enumerate(s_datas):
        if t.find(s_data).data is not None:
            print("data", s_data, "exists")
        else:
            print("data", s_data, "is not exist")


def test_random_insert(t, s):
    max_data = 2000
    r.seed(2)
    rand_datas = list(r.SystemRandom().sample(range(max_data), s))
    for i, data in enumerate(rand_datas):
        t.add_data(data)
    assert t.check_prop()


def test_delete(t):
    datas = [5, 3, 6, 7, 2, 4, 21, 8, 99, 9, 32, 23]
    ddatas = [3, 21, 7, 32]
    for i, data in enumerate(datas):
        t.add_data(data)
    for i, ddata in enumerate(ddatas):
        t.delete_data(ddata)
        for k, data in enumerate(datas):
            if t.find(data).data is not None:
                print("%d" % data, end=' ')
        print("")
    assert t.check_prop()


if '__main__' == __name__:
    import os
    import random as r

    def save_tree(tree, filename):
        f = open('%s.txt' % filename, 'w')
        save(tree, f)
        f.close()
        os.system('txt %s.txt -T' % filename)

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
        test_add(t)
    elif a == 3:
        test_delete(t)
    elif a == 4:
        test_min_max(t)
    elif a == 5:
        test_find(t)
    save_tree(t, 'tree')
