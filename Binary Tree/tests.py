from classes import *
import random
import tqdm

funcs = [Node.__init__, Node.__gt__, Node.insert, Node.tree_walk, Tree.__init__, Tree.insert, Tree.walk, tree_sort,
         Node.search, Tree.search, Node.successor, Node.remove]


def test_all():
    attempts = len(funcs)
    successes = 0
    fails = []
    for func in funcs:
        if test(func):
            successes += 1
        else:
            fails.append(func)
    if len(fails) == 0:
        print("Success! All tests passed.")
    else:
        fail_statement = "Failure! Some tests ("
        for i in range(len(fails) - 1):
            fail_statement += fails[i].__qualname__ + ", "
        fail_statement += fails[len(fails) - 1].__qualname__ + ") failed."
        print(fail_statement)
    return fails


def test(func) -> bool:
    if func.__qualname__ == "Node.__init__":
        return test_node_init()
    if func.__qualname__ == "Node.__gt__":
        return test_node_gt()
    if func.__qualname__ == "Node.insert":
        return test_node_insert()
    if func.__qualname__ == "Node.tree_walk":
        return test_node_tree_walk()
    if func.__qualname__ == "Tree.__init__":
        return test_tree_init()
    if func.__qualname__ == "Tree.insert":
        return test_tree_insert()
    if func.__qualname__ == "Tree.walk":
        return test_tree_walk()
    if func.__qualname__ == "tree_sort":
        return test_tree_sort()
    if func.__qualname__ == "Node.search":
        return test_node_search()
    if func.__qualname__ == "Tree.search":
        return test_tree_search()
    if func.__qualname__ == "Node.successor":
        return test_node_successor()
    if func.__qualname__ == "Node.remove":
        return test_node_remove()

    return False


def test_node_init() -> bool:
    try:
        n = Node(2)
        assert n.key == 2
        assert n.parent is None
        n2 = Node(4, n)
        assert n2.key == 4
        assert n2.parent == n
        return True
    except:
        return False


def test_node_gt() -> bool:
    try:
        n = Node(2)
        n2 = Node(4)
        assert n2 > n
        return True
    except:
        return False


def test_node_insert() -> bool:
    try:
        n = Node(2)
        n2 = Node(4)
        n3 = Node(8)
        n.insert(n2)
        n.insert(n3)
        assert n.rchild == n2
        assert n2.parent == n
        assert n2.rchild == n3
        assert n3.parent == n2
        return True
    except:
        return False


def test_node_tree_walk() -> bool:
    try:
        n = Node(2)
        assert n.tree_walk() == [2]
        n2 = Node(1)
        n3 = Node(4)
        n.insert(n2)
        n.insert(n3)
        assert n2.tree_walk() == [1]
        assert n3.tree_walk() == [4]
        assert n.tree_walk() == [1, 2, 4]

        for i in range(100):
            l = [j for j in range(-i, i)]
            c = l.copy()
            random.shuffle(c)
            t = Tree()
            for num in c:
                t.insert(Node(num))
            assert t.walk() == l
        return True
    except:
        return False


def test_tree_init() -> bool:
    try:
        t = Tree()
        assert t.root is None
        return True
    except:
        return False


def test_tree_insert() -> bool:
    try:
        t = Tree()
        n = Node(0)
        t.insert(n)
        assert t.root == n
        n1 = Node(1)
        t.insert(n1)
        assert n.rchild == n1
        return True
    except:
        return False


def test_tree_walk() -> bool:
    try:
        t = Tree()
        assert t.walk() == []
        n3 = Node(3)
        n1 = Node(1)
        n2 = Node(2)
        n4 = Node(4)
        t.insert(n3)
        assert t.walk() == [3]
        t.insert(n1)
        t.insert(n2)
        t.insert(n4)
        assert t.walk() == [1, 2, 3, 4]
        return True
    except:
        return False


def test_tree_sort() -> bool:
    try:
        assert tree_sort([]) == []
        assert tree_sort([1]) == [1]
        assert tree_sort([1, 2]) == [2, 1]
        assert tree_sort([1, 2, 3]) == [2, 3, 1]
        assert tree_sort([1, 2, 3, 4]) == [3, 4, 2, 1]
        assert tree_sort([1, 2, 3, 4, 5]) == [3, 5, 4, 2, 1]
        return True
    except:
        return False


def test_node_search() -> bool:
    try:
        n = Node(1)
        assert n.search(3) is None
        assert n.search(1) == n
        for k in range(-100, 100):
            n = Node(k)
            assert n.search(k) == n
        n = Node(-1)
        for k in range(10):
            n.insert(Node(k))
        n2 = Node(10)
        n.insert(n2)
        assert n.search(10) == n2
        n.insert(Node(10))
        assert n.search(10) == n2
        return True
    except:
        return False


def test_node_successor() -> bool:
    try:
        n = Node(0)
        assert n.successor() is None
        n2 = Node(2)
        n.insert(n2)
        assert n.successor() == n2
        assert n2.successor() is None
        n1 = Node(1)
        n.insert(n1)
        assert n.successor() == n1
        assert n1.successor() == n2

        t = Tree()
        l = [i for i in range(1000)]
        random.shuffle(l)
        for num in l:
            t.insert(Node(num))
        tw = t.walk()
        succ = [t.root.leftmost().key]
        # Made a mistake here at first, I didn't initialize succ with the first key
        focus = t.root.leftmost()
        while focus.successor() is not None:
            succ.append(focus.successor().key)
            focus = focus.successor()
        assert tw == succ
        return True
    except:
        return False


def test_node_remove() -> bool:
    # try:
        n = Node(0)
        n1 = Node(1)
        n.insert(n1)
        n.remove()
        assert n1.parent is None

        n = Node(0)
        n1 = Node(1)
        n2 = Node(2)
        n.insert(n2)
        n.insert(n1)
        n1.remove()
        assert n.rchild == n2
        assert n2.parent == n

        for i in tqdm.tqdm(range(100)):
            for size in range(1, 100):
                l = [num for num in range(size)]
                ls = l.copy()
                random.shuffle(ls)
                t = Tree()
                for num in l:
                    t.insert(Node(num))
                remove = random.randint(0, size-1)
                l.pop(remove)
                t.remove(t.search(remove))
                # Didn't think of this contingency at first.
                if t.root is not None:
                    tl = [t.root.leftmost().key]
                    focus = t.root.leftmost()
                else:
                    tl = []
                    focus = None
                # I also missed the possibility focus could/should be None
                while focus is not None and focus.successor() is not None:
                    tl.append(focus.successor().key)
                    focus = focus.successor()
                print(tl)
                print(l)
                print(remove)
                assert tl == l
        return True
    # except:
    #     return False


def test_tree_search() -> bool:
    try:
        t = Tree()
        assert t.search(1) is None
        n = Node(1)
        t.insert(n)
        assert t.search(1) == n
        return True
    except:
        return False
