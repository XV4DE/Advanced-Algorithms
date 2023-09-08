import math


# One node of a binary tree. Each node has a key that it is responsible for storing. Each node (save the root) has a
# parent. Each node may have a right child with a key greater than or equal to its own key. Each node may have a left
# child with a key less than or equal to its own.
class Node:
    def __init__(self, key, parent=None) -> None:
        self.key = key
        self.parent = parent
        self.rchild = None
        self.lchild = None

    def __gt__(self, other):
        return self.key > other.key

    def __ge__(self, other):
        return self.key >= other.key

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key

    # add an element to the tree where this node is the root, preserving the tree property (lower or equal values are
    # descendants to the left, greater to the right)
    def insert(self, other):
        if other > self:
            if self.rchild is None:
                self.rchild = other
                other.parent = self
                # At first I made a mistake here, I did not set other.parent to self. I also did not have testing for this.

            else:
                self.rchild.insert(other)
        else:
            if self.lchild is None:
                self.lchild = other
                other.parent = self
            else:
                self.lchild.insert(other)

    # Use the tree property to recursively develop a sorted list of the keys
    def tree_walk(self):
        r = []
        if self.lchild is not None:
            r.extend(self.lchild.tree_walk())
        r.append(self.key)
        if self.rchild is not None:
            r.extend(self.rchild.tree_walk())
        return r

    # Return a node with key k that is the node or one of its descendants or None if no such node exists
    def search(self, k: int):
        if self.key == k:
            return self
        if k > self.key and self.rchild is not None:
            return self.rchild.search(k)
        if k < self.key and self.lchild is not None:
            return self.lchild.search(k)
        return None

    # Remove this node without disrupting the tree property or loosing any nodes
    def remove(self):
        r = None
        if self.parent is None:
            r = self.successor()
        if self.lchild is None and self.rchild is None:
            if self.parent is not None:
                if self.parent.lchild == self:
                    self.parent.lchild = None
                else:
                    self.parent.rchild = None
                self.parent = None
        else:
            succ = self.successor()
            r = succ.remove() if r is None else r
            if self.lchild is not None:
                self.lchild.parent = succ
            succ.lchild = self.lchild
            if self.rchild is not None:
                self.rchild.parent = succ
            succ.rchild = self.rchild
            if self.parent is not None:
                if self.parent.rchild == self:
                    self.parent.rchild = succ
                else:
                    self.parent.lchild = succ
            succ.parent = self.parent
            self.parent = None
            self.lchild = None
            self.rchild = None
        return r

    # Get the smallest node in the tree where this node is the root
    def leftmost(self):
        if self.lchild is not None:
            return self.lchild.leftmost()
        return self

    # The successor of a node is the next node whose key would be printed in a treewalk
    def successor(self):
        if self.rchild is not None:
            return self.rchild.leftmost()
        if self.parent is not None and self.parent.lchild == self:
            return self.parent
        focus = self
        while focus.parent is not None and focus.parent.rchild == focus:
            focus = focus.parent
        if focus.parent is not None and focus.parent.lchild == focus:
            return focus.parent
        return None


# The binary tree itself. Most of the fun stuff happens in the nodes, the structure of the tree is mostly there to serve
# as a package for the root and its descendants.
class Tree:
    def __init__(self) -> None:
        self.root = None

    # Add a new node to the tree
    def insert(self, n: Node):
        if self.root is None:
            self.root = n
        else:
            self.root.insert(n)

    # Return a sorted list of the keys in the tree
    def walk(self):
        if self.root is None:
            # I made a mistake here. At first I returned None but I realized that that didn't make sense when I implemented random testing
            return []
        else:
            return self.root.tree_walk()

    # Return a node in the tree with the key k or None if there is no such node.
    def search(self, k: int):
        # Originally didn't consider that root could be None here, wrote a test and found the problem
        if self.root is None:
            return None
        return self.root.search(k)

    # Remove a node in the tree from the tree while maintaining the tree property
    def remove(self, n: Node):
        new_root = n.remove()
        # Had to fix this up to account for the possibility that there are now no nodes in the tree.
        if self.root.lchild is None and self.root.rchild is None:
            self.root = new_root


# Takes a sorted list (lowest to highest) and arranges it for the creation of an optimal binary tree (original list is not modified)
def tree_sort(input_list):
    if len(input_list) <= 1:
        return input_list.copy()
    l = []
    midpoint = math.ceil((len(input_list)-1)/2)
    l.append(input_list[midpoint])
    # I had some difficulties here with infinite recursion because I didn't understand how slice worked well enough, the
    # result being the +1 on the end of the midpoint below.
    l.extend(tree_sort(input_list[midpoint+1:]))
    l.extend(tree_sort(input_list[:midpoint]))
    return l





