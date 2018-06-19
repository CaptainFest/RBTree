
class RBNode(object):

    def __init__(self, key):  # структура
        self._key = key
        self._red = False
        self._left = None
        self._right = None
        self._p = None

    key = property(fget=lambda self: self._key, doc="The node's key")
    red = property(fget=lambda self: self._red, doc="Is the node red?")
    left = property(fget=lambda self: self._left, doc="The node's left child")
    right = property(fget=lambda self: self._right, doc="The node's right child")
    p = property(fget=lambda self: self._p, doc="The node's parent")

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.key)


class RBTree(object):

    def __init__(self, create_node=RBNode):        # tree construct

        self._nil = create_node(key=None)
        "Our nil node, used for all leaves."

        self._root = self.nil
        "The root of the tree."

        self._create_node = create_node
        "A callable that creates a node."

    root = property(fget=lambda self: self._root, doc="The tree's root node")
    nil = property(fget=lambda self: self._nil, doc="The tree's nil node")

    def search(self, key, x=None):
        """
        Search the subtree rooted at x (or the root if not given) iteratively for the key.
        
        @return: self.nil if it cannot find it.
        """
        if x is None:
            x = self.root
        while x != self.nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def minimum(self, x=None):
        """
        @return: The minimum value in the subtree rooted at x.
        """
        if x is None:
            x = self.root
        while x.left != self.nil:
            x = x.left
        return x

    def maximum(self, x=None):
        """
        @return: The maximum value in the subtree rooted at x.
        """
        if x is None:
            x = self.root
        while x.right != self.nil:
            x = x.right
        return x

    def insert_key(self, key):  # Insert the key into the tree
        self.insert_node(self._create_node(key=key))

    def insert_node(self, z):  # Insert node z into the tree
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
        z._red = True
        self._insert_fix(z)

    def _insert_fix(self, z):  # Restore red-black properties after insert
        while z.p.red:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self._left_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self._right_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._left_rotate(z.p.p)
        self.root._red = False

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
            if not node.left and not node.right and node.red:
                return 0, False

            # if node is red, check children are black
            if node.red and node.left and node.right:
                if node.left.red or node.right.red:
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
        return is_ok and not self.root.red


def write_tree_as_dot(t, f, show_nil=False):  # writing file in a file f.dot

    def node_id(node):
        return 'N%d' % id(node)

    def node_color(node):
        if node.red:
            return "red"
        else:
            return "black"

    def visit_node(node):
        f.write("  %s [key=\"%s\", color=\"%s\"];" % (node_id(node), node, node_color(node)))
        if node.left:
            if node.left != t.nil or show_nil:
                visit_node(node.left)
                f.write("  %s -> %s ;" % (node_id(node), node_id(node.left)))
        if node.right:
            if node.right != t.nil or show_nil:
                visit_node(node.right)
                f.write("  %s -> %s ;" % (node_id(node), node_id(node.right)))

    f.write("Red black tree" + '\n')
    visit_node(t.root)


def test_tree(t, keys):   # Insert keys one by one checking prop
    assert t.check_prop()
    for i, key in enumerate(keys):
        for key2 in keys[:i]:
            assert t.nil != t.search(key2)
        for key2 in keys[i:]:
            assert (t.nil == t.search(key2)) ^ (key2 in keys[:i])
        t.insert_key(key)
        assert t.check_prop()


if '__main__' == __name__:
    import os
    import random as r


    def write_tree(t, filename):  # Write the tree as an SVG file
        f = open('%s.dot' % filename, 'w')
        write_tree_as_dot(t, f)
        f.close()
        os.system('dot %s.dot -Tsvg -o %s.svg' % (filename, filename))


    # test the RBTree
    r.seed(2)
    size = 50
    # keys = list(r.randint(-50, 50) for x in range(size)
    keys = [5, 3, 6]          # 7, 2, 4, 21, 8, 99, 32, 23]
    t = RBTree()

    test_tree(t, keys)
    write_tree(t, 'tree')
