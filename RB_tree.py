import Color


class RBNode(object):             # red-black tree's node

    def __init__(self, key):      # constructor
        c = Color.Color()
        """setters"""
        self._key = key           # Node's key
        self._color = c.BLACK       # Node color: False = BLACK, True = RED
        self._left = None         # Left child
        self._right = None        # Right child
        self._p = None            # Parent

    """getters"""
    key = property(fget=lambda self: self._key, doc="The node's key")
    color = property(fget=lambda self: self._color, doc="The node color")
    left = property(fget=lambda self: self._left, doc="The node's left child")
    right = property(fget=lambda self: self._right, doc="The node's right child")
    p = property(fget=lambda self: self._p, doc="The node's parent")

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.key)


class RBTree(object):

    def __init__(self, create_node=RBNode):    # tree constructor

        self._nil = create_node(key=None)      # Leaves are nil and always black
        self._root = self.nil                  # The root of the tree in the beginning is nil
        self._create_node = create_node        # callable that creates a node

    root = property(fget=lambda self: self._root, doc="The tree's root node")
    nil = property(fget=lambda self: self._nil, doc="The tree's nil node")

    def _sibling(self, x):        # returns node's left or right brother
        assert x.p != self.nil
        if x == x.p.left:
            return x.p.right
        else:
            return x.p.left

    def min_key(self, x=None):       # The minimum value in the subtree rooted at x
        if x is None:
            x = self.root
        while x.left != self.nil:
            x = x.left
        return x.key

    def max_key(self, x=None):       # The maximum value in the subtree rooted at x
        if x is None:
            x = self.root
        while x.right != self.nil:
            x = x.right
        return x

    def _replace_node(self, old, new):  # replacing node if some node is deleted
        if old.p == self.nil:
            self._root = new
        else:
            if old == old.p.left:
                old.p._left = new
            else:
                old.p._right = new
        if new != self.nil:
            new._p = old.p

    def delete_key(self, key):  # operation that finds needed node and calls delete node func
        node = self.search(key)
        if node == self.nil:
            return False
        self.delete_node(node)
        return True

    def delete_node(self, z):
        c = Color.Color()
        if not z or z == self.nil:
            return
        if z.left == self.nil or z.right == self.nil:
            y = z
        else:
            y = z.right
            while y.left != self.nil:
                y = y.left
        if y.left != self.nil:
            x = y.left
        else:
            x = y.right
        x._p = y.p
        if y.p:
            if y == y.p.left:
                y.p._left = x
            else:
                y.p._right = x
        else:
            self._root = x
        if y != z:
            z._key = y.key
        if y.color == c.BLACK:
            self._delete_fix(x)

    def _delete_fix(self, x):
        c = Color.Color()
        while x == c.BLACK and x != self.root:
            if x == x.p.left:
                w = x.p.right
                if w.color == c.RED:
                    w._color = c.BLACK
                    x.p._color = c.RED
                    self._left_rotate(x.p)
                    w = x.p.right
                if w.left.color == c.BLACK and w.right.color == c.BLACK:
                    w._color = c.RED
                    x = x.p
                else:
                    if w.right.color == c.BLACK:
                        w.left._color = c.BLACK
                        w._color = c.RED
                        self._right_rotate(w)
                        w = x.p.right
                    w._color = x.p.color
                    x.p._color = c.BLACK
                    w.right._color = c.BLACK
                    self._left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.color == c.RED:
                    w._color = c.BLACK
                    x.p._color = c.RED
                    self._right_rotate(x.p)
                    w = x.p.left
                if w.right.color == c.BLACK and w.left.color == c.BLACK:
                    w._color = c.RED
                    x = x.p
                else:
                    if w.left.color == c.BLACK:
                        w.right._color = c.BLACK
                        w._color = c.RED
                        self._left_rotate(w)
                        w = x.p.left
                    w._color = x.p.color
                    x.p._color = c.BLACK
                    w.left._color = c.BLACK
                    self._right_rotate(x.p)
                    x = self.root
        x._color = c.BLACK

    def search(self, key, x=None):  # Search the subtree rooted at x
        if x is None:
            x = self.root
        while x != self.nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def insert_key(self, key):     # Insert the key into the tree
        self.insert_node(self._create_node(key=key))

    def insert_node(self, z):      # Insert node z into the tree
        c = Color.Color()
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z._p = y
        if y == self.nil:
            self._root = z
        elif z.key < y.key:
            y._left = z
        else:
            y._right = z
        z._left = self.nil
        z._right = self.nil
        z._color = c.RED
        self._insert_fix(z)

    def _insert_fix(self, z):  # Restore red-black properties after insert
        c = Color.Color()
        while z.p.color:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.color:
                    z.p._color = c.BLACK
                    y._color = c.BLACK
                    z.p.p._color = c.RED
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self._left_rotate(z)
                    z.p._color = c.BLACK
                    z.p.p._color = c.RED
                    self._right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.color:
                    z.p._color = c.BLACK
                    y._color = c.BLACK
                    z.p.p._color = c.RED
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self._right_rotate(z)
                    z.p._color = c.BLACK
                    z.p.p._color = c.RED
                    self._left_rotate(z.p.p)
        self.root._color = c.BLACK

    def tree_black_height(self):
        x = self.root
        count = 0
        while x is not None:
            if not x.color or x == self.nil:
                count += 1
            x = x.left
        return count

    def tree_height(self, x=None, l_height=0, r_height=0):
        if x is None:
            x = self.root
        if x.left is None and x.right is None:
            return 1
        else:
            if x.left is not None:
                l_height = self.tree_height(x.left, l_height, r_height)
            if x.right is not None:
                r_height = self.tree_height(x.right, l_height, r_height)
            if l_height > r_height:
                return l_height + 1
            else:
                return r_height + 1

    def _left_rotate(self, x):  # rotate node x to left
        y = x.right
        x._right = y.left
        if y.left != self.nil:
            y.left._p = x
        y._p = x.p
        if x.p == self.nil:
            self._root = y
        elif x == x.p.left:
            x.p._left = y
        else:
            x.p._right = y
        y._left = x
        x._p = y

    def _right_rotate(self, x):  # rotate node x to right
        y = x.left
        x._left = y.right
        if y.right != self.nil:
            y.right._p = x
        y._p = x.p
        if x.p == self.nil:
            self._root = y
        elif x == x.p.right:
            x.p._right = y
        else:
            x.p._left = y
        y._right = x
        x._p = y

    def check_prop(self):               # returns True if RBTree is ok

        def is_red_black_node(node):    # @return: num_black
            # check has _left and _right or neither
            if (node.left and not node.right) or (node.right and not node.left):
                return 0, False

            # check leaves are black
            if not node.left and not node.right and node.color:
                return 0, False

            # if node is red, check children are black
            if node.color and node.left and node.right:
                if node.left.color or node.right.color:
                    return 0, False

            # descend tree and check black counts are balanced
            if node.left and node.right:

                # check children's parents are correct
                if self.nil != node.left and node != node.left.p:
                    return 0, False
                if self.nil != node.right and node != node.right.p:
                    return 0, False

                # check children are ok
                left_counts, left_ok = is_red_black_node(node.left)
                if not left_ok:
                    return 0, False
                right_counts, right_ok = is_red_black_node(node.right)
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
        f.write("  %s [key=\"%s\", color=\"%s\"];\n" % (node_id(node), node, node_color(node)))
        if node.left:
            if node.left != t.nil:
                visit_node(node.left)
                f.write("  %s -> %s ; \n" % (node_id(node), node_id(node.left)))
        if node.right:
            if node.right != t.nil:
                visit_node(node.right)
                f.write("  %s -> %s ; \n" % (node_id(node), node_id(node.right)))

    f.write("Red black tree" + '\n')
    visit_node(t.root)


def test_insert(t):   # Insert keys one by one checking prop
    keys = [5, 3, 6, 7, 2, 4, 21, 8, 99, 9, 32, 23]
    for i, key in enumerate(keys):
        t.insert_key(key)
    assert t.check_prop()
    # print("Черная высота дерева = ", t.tree_black_height())
    # print("Высота дерева = ", t.tree_height())


def test_min_max(t):
    keys = [5, 3, 6, 7, 2, 4, 21, 8, 99, 9, 32, 23]
    m_keys = [5, 3, 21, 10, 32]
    for i, key in enumerate(keys):
        t.insert_key(key)
    for i, m_key in enumerate(m_keys):
        if t.search(m_key).key is not None:
            print("максимум в поддереве узла", m_key, " = ", t.max_key(t.search(m_key)))
            print("минимум в поддереве узла", m_key, " = ", t.min_key(t.search(m_key)))
            print("")
        else:
            print("нет узла", m_key, "в дереве")
            print("")


def test_search(t):
    keys = [5, 3, 6, 7, 2, 4, 21, 8, 99, 9, 32, 23]
    s_keys = [6, 3, 24, 23, 99, 101]
    for i, key in enumerate(keys):
        t.insert_key(key)
    for i, s_key in enumerate(s_keys):
        if t.search(s_key).key is not None:
            print("key", s_key, "exists")
        else:
            print("key", s_key, "is not exist")


def test_random_insert(t, s):
    max_key = 2000
    r.seed(2)
    rand_keys = list(r.SystemRandom().sample(range(max_key), s))
    for i, key in enumerate(rand_keys):
        t.insert_key(key)
    assert t.check_prop()


def test_delete(t):
    keys = [5, 3, 6, 7, 2, 4, 21, 8, 99, 9, 32, 23]
    dkeys = [3, 21, 7, 32]
    for i, key in enumerate(keys):
        t.insert_key(key)
    for i, dkey in enumerate(dkeys):
        t.delete_key(dkey)
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
        for size in range(1, 101, 1):
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
