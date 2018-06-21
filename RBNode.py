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
"""
    def delete_key(self, key):    # operation that finds needed node and calls delete node func
        node = self.search(key)
        if node == self.nil:
            return False
        self.delete_node(node)
        return True

    def delete_node(self, x):     # directly node deletion
        c = Color.Color()
        if x.left != self.nil and x.right != self.nil:
            max_left = self.max_key(x.left)
            x._key = max_left.key
            x = max_left
        assert x.left == self.nil or x.right == self.nil
        if x.right == self.nil:
            print('l')
            child = x.left
        else:
            print('r')
            child = x.right
        if not x.color:
            x._color = child.color
            self._delete_case1(x)
        self._replace_node(x, child)
        if self.root.color:
            self.root._color = c.BLACK

    ef _delete_case1(self, n):         # node will become the root node or next case
        print(1)
        if n.p == self.nil:
            return
        else:
            self._delete_case2(n)

    def _delete_case2(self, n):         # case if node has a red sibling
        c = Color.Color()
        print(2)
        if self._sibling(n).color:
            n.p.color = c.RED
            self._sibling(n)._color = c.BLACK
        if n == n.p.left:
            self._left_rotate(n.p)
        else:
            self._right_rotate(n.p)
        self._delete_case3(n)

    def _delete_case3(self, n):         # case if node's parent, sibling, and sibling's children are black
        c = Color.Color()
        print(3)
        tmp = self._sibling(n)
        if not n.p.color and not tmp.color and not tmp.left and not tmp.right:
            tmp._color = c.RED
            self._delete_case1(n.p)
        else:
            self._delete_case4(n)

    def _delete_case4(self, n):         # case if sibling, and sibling's children are black, but parent red
        c = Color.Color()
        print(4)
        tmp = self._sibling(n)
        if n.p.color and not tmp.color and not tmp.left.color and not tmp.right.color:
            tmp._color = c.RED
            n.p._color = c.BLACK
        else:
            self._delete_case5(n)

    def _delete_case5(self, n):         #
        print(5)
        c = Color.Color()     
        tmp = self._sibling(n)
        if n == n.p.left and not tmp.color and tmp.left and not tmp.right:
            tmp._color = c.RED
            tmp.left._color = c.BLACK
            self._right_rotate(tmp)
        elif n == n.p.right and not tmp.color and tmp.right and not tmp.left:
            tmp._color = c.RED
            tmp.right._color = c.BLACK
            self._left_rotate(tmp)
            self._delete_case6(n)

    def _delete_case6(self, n):
        c = Color.Color()
        print(6)
        tmp = self._sibling(n)
        tmp._color = n.p.color
        n.p._color = c.BLACK
        if n == n.p.left:
            assert tmp.right.color
            tmp.right._color = c.BLACK
            self._left_rotate(n.p)
        else:
            assert tmp.left.color
            tmp.left._color = c.BLACK
            self._right_rotate(n.p)"""


def delete_node(self, x):
    c = Color.Color()
    y = x
    y_orig_color = y.color
    q = self.nil
    if x.right == self.nil and x.left == self.nil:
        if x == self.root:
            x._root = self.nil
        else:
            if x == x.p._left:
                x.p._left = self.nil
            else:
                x.p._right = self.nil
        return
    elif x.right == self.nil or x.left == self.nil:
        if x.p.left == x:
            x.p._left = child
        else:
            x.p._right = child
    else:
        y = self.max_key(x.left)
        if y.right != self.nil:
            t.right._p = y.p
        elif y == self.root:
            self._root = t.right
        else:
            y._right = y.left
    if y != x
        x._color = y.color
        x._key = y.key
    if y.color = c.BLACK
    self._delete_fix(q)


    def delete_node(self, x):
        c = Color.Color()
        y = x
        y_orig_color = y.color
        if x.left == self.nil:
            q = x.right
            self._replace_node(x, x.right)
        elif x.right == self.nil:
            q = x.left
            self._replace_node(x, x.left)
        else:
            y = self.min_key(x.right)
            y_orig_color = y.color
            x = y.right
            if y.p == x:
                q._p = y
            else:
                self._replace_node(y, y.right)
                y._right = x.right
                y.right._p = y
            self._replace_node(x, y)
            y._left = x.left
            y.left._p = y
            y._color = x.color
        if y_orig_color == c.BLACK:
            self._delete_fix(q)

    def _delete_fix(self, q):
        c = Color.Color()
        while q == c.BLACK and q != self.root:
            if q == q.p.left:
                w = q.p.right
                if w == c.RED:
                    w._color = c.BLACK
                    w.p._color = c.RED
                    self._left_rotate(w.p)
                    w = q.p.right
                elif w.left.color == c.BLACK and w.right.color == c.BLACK:
                    w._color = c.RED
                    q = q.p
                else:
                    if w.right.color == c.BLACK:
                        w.left._color = c.BLACK
                        w._color = c.RED
                        self._right_rotate(w)
                        w = q.p.right
                    w._color = q.p.color
                    q.p._color = c.BLACK
                    w.right._color = c.BLACK
                    self._left_rotate(q.p)
                    q = q.root
            else:
                w._color = c.BLACK
                q.p._color = c.RED
                _right_rotate(q.p)
                w = q.p.left

        q._color = c.BLACK