import Color


class RBNode(object):             # color-black tree's node

    def __init__(self, key):      # constructor
        """setters"""
        c = Color.Color()
        self._key = key           # Node's key
        self._color = c.BLACK       # Node color: False = BLACK, True = color
        self._left = None         # Left child
        self._right = None        # Right child
        self._p = None            # Parent

    """getters"""
    key = property(fget=lambda self: self._key, doc="The node's key")
    color = property(fget=lambda self: self._color, doc="The node color")
    left = property(fget=lambda self: self._left, doc="The node's left child")
    right = property(fget=lambda self: self._right, doc="The node's right child")
    p = property(fget=lambda self: self._p, doc="The node's parent")

    def __repr__(self):           # node's string representation
        return str(self.key)


class RBTree(object):
    c = Color.Color()

    def __init__(self, create_node=RBNode):    # tree constructor

        self._nil = create_node(key=None)      # Leaves are nil and always black
        self._root = self.nil                  # The root of the tree in the beginning is nil
        self._create_node = create_node        # callable that creates a node

    root = property(fget=lambda self: self._root, doc="The tree's root node")
    nil = property(fget=lambda self: self._nil, doc="The tree's nil node")

    def delete_key(self, key):   # operation that finds needed node and calls delete node func
        node = self.search(key)
        if node == self.nil:
            return False
        self.delete_node(node)
        return True

    def delete_node(self, x):    # directly node deletion
        if x.left != self.nil and x.right != self.nil:
            pred = self.max_key(x.left)
            x._key = pred.key
            x = pred
        assert x.left == self.nil or x.right == self.nil
        if x.right == self.nil:
            child = x.left
        else:
            child = x.right
        if not x.color:
            x._color = child.color
            self._delete_case1(x)
        self._replace_node(x, child)
        if self.root.color:
            self.root._color = False

    def _replace_node(self, oldn, newn):  # replacing node if some node is deleted
        if oldn.p == self.nil:
            self._root = newn
        else:
            if oldn == oldn.p.left:
                oldn.p._left = newn
            else:
                oldn.p._right = newn
        if newn != self.nil:
            newn._p = oldn.p

    def _delete_case1(self, n):
            """ In this case, N has become the root node. The deletion
                removed one black node from every path, so no properties
                are violated.
            """
            if n.p == self.nil:
                return
            else:
                self._delete_case2(n)

    def _delete_case2(self, n):
        """ N has a red sibling. In this case we exchange the colors
            of the parent and sibling, then rotate about the parent
            so that the sibling becomes the parent of its former
            parent. This does not restore the tree properties, but
            reduces the problem to one of the remaining cases. """

        if self._sibling(n).color:
            n.p.color = True
            self._sibling(n)._color = False
        if n == n.p.left:
            self._left_rotate(n.p)
        else:
            self._right_rotate(n.p)
        self._delete_case3(n)

    def _delete_case3(self, n):
        """ In this case N's parent, sibling, and sibling's children
            are black. In this case we paint the sibling red. Now
            all paths passing through N's parent have one less black
            node than before the deletion, so we must recursively run
            this procedure from case 1 on N's parent.
        """
        tmp = self._sibling(n)
        if not n.p.color and not tmp.color and not tmp.left and not tmp.right:
            tmp._color = True
            self._delete_case1(n.p)
        else:
            self._delete_case4(n)

    def _delete_case4(self, n):
        """ N's sibling and sibling's children are black, but its
        parent is red. We exchange the colors of the sibling and
        parent; this restores the tree properties.
        """
        tmp = self._sibling(n)
        if n.p.color and not tmp.color and not tmp.left.color and not tmp.right.color:
            tmp._color = True
            n.p._color = False
        else:
            self._delete_case5(n)

    def _delete_case5(self, n):
        """ There are two cases handled here which are mirror images
        of one another:
            N's sibling S is black, S's left child is red, S's
            right child is black, and N is the left child of its
            parent. We exchange the colors of S and its left
            sibling and rotate right at S.
            N's sibling S is black, S's right child is red,
            S's left child is black, and N is the right child of
            its parent. We exchange the colors of S and its right
            sibling and rotate left at S.
            Both of these function to reduce us to the situation
            described in case 6. """
        tmp = self._sibling(n)
        if n == n.p.left and not tmp.color and tmp.left and not tmp.right:
            tmp._color = True
            tmp.left._color = False
            self._right_rotate(tmp)
        elif n == n.p.right and not tmp.color and tmp.right and not tmp.left:
            tmp._color = True
            tmp.right._color = False
            self._left_rotate(tmp)
            self._delete_case6(n)

    def _delete_case6(self, n):
        """ There are two cases handled here which are mirror images
        of one another:
        N's sibling S is black, S's right child is red, and N is
        the left child of its parent. We exchange the colors of
        N's parent and sibling, make S's right child black, then
        rotate left at N's parent.
        N's sibling S is black, S's left child is red, and N is
        the right child of its parent. We exchange the colors of
        N's parent and sibling, make S's left child black, then
        rotate right at N's parent.
        """
        tmp = self._sibling(n)
        tmp._color = n.p.color
        n.p._color = False
        if n == n.p.left:
            assert tmp.right.color
            tmp.right._color = False
            self._left_rotate(n.p)
        else:
            assert tmp.left.color
            tmp.left._color = False
            self._right_rotate(n.p)

    def _sibling(self, x):        # returns node's n left or right brother
        assert x.p != self.nil
        if x == x.p.left:
            return x.p.right
        else:
            return x.p.left

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

    def insert_key(self, key):  # Insert the key into the tree
        self.insert_node(self._create_node(key=key))

    def insert_node(self, z):  # Insert node z into the tree
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


def write_tree_as_dot(t, f, show_nil=False):  # writing file in a file f.dot

    def node_id(node):
        return 'N%d' % id(node)

    def node_color(node):
        if node.color:
            return "red"
        else:
            return "black"

    def visit_node(node):                      # BFA pre-order search
        f.write("  %s [key=\"%s\", color=\"%s\"];\n" % (node_id(node), node, node_color(node)))
        if node.left:
            if node.left != t.nil or show_nil:
                visit_node(node.left)
                f.write("  %s -> %s ; \n" % (node_id(node), node_id(node.left)))
        if node.right:
            if node.right != t.nil or show_nil:
                visit_node(node.right)
                f.write("  %s -> %s ; \n" % (node_id(node), node_id(node.right)))

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
        os.system('dot %s.dot -T svg -o %s.svg' % (filename, filename))


    # test the RBTree
    r.seed(2)
    size = 50
    # keys = list(r.randint(-50, 50) for x in range(size)
    keys = [5, 3, 6, 7, 2, 4, 21, 8, 99, 32, 23]
    t = RBTree()

    test_tree(t, keys)
    write_tree(t, 'tree')
