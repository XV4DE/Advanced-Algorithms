import time
import random


def time_it(operations: int) -> float:
    sets = [DisjointSet() for i in range(operations)]
    nums = [random.randint(0, operations - 1) for i in range(operations * 2 + 2)]
    cnt = 0
    start = time.time()
    while cnt < operations:
        DisjointSet.union(sets[nums.pop() % len(sets)], sets[nums.pop() % len(sets)])
        cnt += 1
    return time.time() - start


class DisjointSet:
    def __init__(self, _val=None):
        self.parent = self
        self.rank = 0
        if _val is not None:
            self.val = _val

    # This method is really cool. I like the recursive version for its elegance but the wiki is right that this is just
    # plain more memory efficient. The one thing that I don't like about this algorithm is that it doesn't behave
    # super predictably. I would imagine one would run it when they want to know the representative member of the set (
    # given that's what the method returns) but they also get their data structure reformatted without asking for it. I
    # can see a practical application for a version of this structure with a find() and a reformat(), though it would be
    # rare that you would want to find without first reformatting.
    def find(self):
        root = self
        while root.parent != root:
            root = root.parent
        focus = self
        while focus.parent != root:
            focus.parent, focus = root, focus.parent
        return root

    @staticmethod
    def union(x, y):
        x = x.find()
        y = y.find()

        if x is y:
            return

        # x has the larger (or equal) size of [x, y] after this if
        if x.rank < y.rank:
            x, y = y, x

        # I was surprised, the wiki uses the slightly less efficient "y.parent = x", guaranteeing some lost time on the
        # next run of find().
        y.parent = x

        if x.rank > y.rank:
            x.rank += 1

        # This line was not on the wiki but should improve the memory efficiency a little bit, though I suspect I'm just
        # reclaiming some of the inefficiency I brought on myself when I decided to use Python, since this line would
        # not be legal in Java. That being said, we take what we can get.
        del y.rank



