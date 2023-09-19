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
        if self.num_children() == 0:
            if self.parent is not None:
                self.scrub_parent()
        elif self.num_children() == 1:
            return self.splice_out()
        else:
            return self.rotate_out()

    # return the number of children this node has, an int between 0 and 2
    def num_children(self) -> int:
        return int(self.lchild is not None) + int(self.rchild is not None)

    # removes this node from its parent node and the parent node from this node, tcdr: destroys teh connection between this node and its parent
    def scrub_parent(self):
        if self.is_lchild():
            self.parent.lchild = None
        elif self.is_rchild():
            self.parent.rchild = None
        self.parent = None

    # removes this node from the tree, assuming that it has one child, returns the new root of the tree if the root changed
    def splice_out(self):
        if self.lchild is not None:
            child = self.lchild
        else:
            child = self.rchild

        if self.is_lchild():
            self.parent.lchild = child
            child.parent = self.parent
        elif self.is_rchild():
            self.parent.rchild = child
            child.parent = self.parent
        else:
            child.scrub_parent()
            return child

    # removes this node from the tree, assuming this node has two children, returns the new root of the tree if it changed
    def rotate_out(self):
        succ = self.successor()
        root = succ.remove()
        if self.parent is not None:
            succ.parent = self.parent
            if self.is_rchild():
                self.parent.rchild = succ
            else:
                self.parent.lchild = succ
        succ.lchild = self.lchild
        if self.lchild is not None:
            self.lchild.parent = succ
        succ.rchild = self.rchild
        if self.rchild is not None:
            self.rchild.parent = succ
        if self.parent is None:
            return succ
        return root

    # return True if this node is a left child, False otherwise
    def is_lchild(self):
        return self.parent and self.parent.lchild == self

    # return True if this node is a right child, False otherwise
    def is_rchild(self):
        return self.parent and self.parent.rchild == self

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

    # Return the depth of the tree for which this node is the root (how many connections it takes to get to the node
    # that it takes the most connections to get to)
    def depth(self):
        if self.lchild is not None:
            ldepth = self.lchild.depth()
        else:
            ldepth = 0
        if self.rchild is not None:
            rdepth = self.rchild.depth()
        else:
            rdepth = 0
        return max(ldepth, rdepth) + 1


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
        if self.root.lchild is None and self.root.rchild is None and n == self.root:
            self.root = None
            return
        new_root = n.remove()
        if new_root is not None:
            self.root = new_root

    # Get the depth of the tree
    def depth(self) -> int:
        if self.root is None:
            return 0
        else:
            return self.root.depth()


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





