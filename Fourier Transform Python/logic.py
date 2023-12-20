propositional_constants = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                           'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def is_legal(_sentence: str):
    sentence = _sentence
    sentence.replace('(', '')
    sentence.replace(')', '')
    if len(sentence) == 0:
        return False

    if sentence in propositional_constants:
        return True

    if "<->" in sentence:
        return sentence[:sentence.find("<->")] and sentence[sentence.find("<->")+2:]

    if "->" in sentence:
        return sentence[:sentence.find("->")] and sentence[sentence.find("->")+1:]

    if "&" in sentence:
        return sentence[:sentence.find("&")] and sentence[sentence.find("&"):]

    if "|" in sentence:
        return sentence[:sentence.find("|")] and sentence[sentence.find("|"):]

    if sentence[0] == '~':
        return is_legal(sentence[1:])


def are_parens_balanced(phrase: str):
    return phrase.count('(') == phrase.count(')')


# takes a phrase with balanced parens and returns weather or not a given index is inside any parens
def is_in_parens(idx: int, phrase: str):
    return not are_parens_balanced(phrase[idx:])


def index_of_first_thing_to_deal_with(in_str: str):
    if len(in_str) == 0:
        return -1

    for i in range(len(in_str)):
        if not is_in_parens(i, in_str) and in_str[i] != '~' and in_str[i] not in propositional_constants:
            return i

    for i in range(len(in_str)):
        if not is_in_parens(i, in_str) and in_str[i] not in propositional_constants:
            return i

    for i in range(len(in_str)):
        if not is_in_parens(i, in_str):
            return i

    return -1


def remove_outermost_parens(in_str: str):
    if in_str[0] == '(' and in_str[-1] == ')':
        return in_str[1:-1]
    return in_str


def str_to_sentence(_in_str: str):
    in_str = remove_outermost_parens(_in_str)
    if in_str in propositional_constants:
        return BasicLogicalSentence(in_str)
    idx = index_of_first_thing_to_deal_with(in_str)
    symbol = in_str[idx]
    # print(symbol)
    if symbol == '~':
        return Negate(str_to_sentence(in_str[idx+1:]))
    if symbol == '&':
        return And(str_to_sentence(in_str[:idx]), str_to_sentence(in_str[idx+1:]))
    if symbol == '|':
        return Or(str_to_sentence(in_str[:idx]), str_to_sentence(in_str[idx+1:]))
    if symbol == '=':
        return MutuallyImplies(str_to_sentence(in_str[:idx]), str_to_sentence(in_str[idx+1:]))
    if symbol == '>':
        return Implies(str_to_sentence(in_str[:idx]), str_to_sentence(in_str[idx+1:]))


def is_indo(sentence):
    op = type(sentence)
    if op == Implies or op == MutuallyImplies:
        return False
    if op == Negate:
        return type(sentence.right) == BasicLogicalSentence
    if op == And:
        return is_indo(sentence.left) and is_indo(sentence.right)
    if op == Or:
        if type(sentence.left) == And or type(sentence.right == And):
            return False
        return is_indo(sentence.left) and is_indo(sentence.right)


def find_op(arg: str):
    count = 0
    for i in range(len(arg)):
        if arg[i] == '(':
            count += 1
        elif arg[i] == ')':
            count -= 1
        if count == 0 and arg[i] != ')' and arg[i] != '(':
            char = i
            op = ''
            while arg[char] != '(' and arg[char] != ')':
                op += arg[char]
                char += 1
            return i, op


def transform_one(_arg: str):
    arg = _arg[1:-1]
    op_pos, op = find_op(arg)
    left = arg[:op_pos]
    right = arg[op_pos + len(op):]
    if op == "<->":
        return '(' + left + '->' + right + ')&(' + right + '->' + left + ')'
    if op == "->":
        return '((~' + left + ')|' + right + ')'
    if op == "&":
        return _arg
    if op == "|":
        return '(~(~' + left + ')&(~' + right + ')'


def ind_transform(initial: str):
    start = initial
    one_deeper = transform_one(start)
    while start != one_deeper:
        start = one_deeper
        one_deeper = transform_one(start)
    return start


def bits(n):
    return [bool(int(digit)) for digit in bin(n)[2:]]


def int_to_truth_permutation(n: int, pcs):
    out = {}
    for i in range(len(pcs)):
        out[pcs[i]] = bool(bits(n)[i]) if i < len(bits(n)) else False
    return out


class TruthTable:
    def __init__(self, _keys=None, _values=None):
        if _values is None:
            _values = []
        if _keys is None:
            _keys = []
        self.keys = _keys
        self.values = _values

    def __getitem__(self, item):
        return self.values[self.keys.find(item)]

    def __setitem__(self, key, value):
        self.keys.append(key)
        self.values.append(value)

    def print(self):
        first_row = ""
        print(self.keys[0].keys())
        for key in self.keys[0].keys():
            first_row += key + " "
        first_row = first_row[:-1]
        print(first_row)
        for i in range(len(self.keys)):
            row = ""
            for j in range(len(self.keys[i])):
                row += ('T' if list(self.keys[i].values())[j] else 'F') + "|"
            row += 'T' if self.values[i] else 'F'
            print(row)


class LogicalSentence:
    def __init__(self):
        pass

    def evaluate(self, conditions) -> bool:
        pass

    def pcs_used(self):
        return set()

    def truth_table(self):
        out = TruthTable()
        pcs = self.pcs_used()
        for i in range(2 ** len(pcs)):
            perm = int_to_truth_permutation(i, list(pcs))
            out[perm] = self.evaluate(perm)
        return out

    def is_valid(self):
        return False not in self.truth_table().values

    def is_equivalent(self, other):
        return (self == other).is_valid()

    def is_contingent(self, other):
        return (self and other).is_valid()

    def entails(self, other):
        return (self > other).is_valid()

    def __neg__(self):
        return Negate(self)

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __eq__(self, other):
        return MutuallyImplies(self, other)

    def __gt__(self, other):
        return Implies(self, other)


class BasicLogicalSentence (LogicalSentence):
    def __init__(self, _pc: str):
        self.pc = _pc
        super().__init__()

    def pcs_used(self):
        return {self.pc}

    def evaluate(self, conditions):
        return conditions[self.pc]


class Negate(LogicalSentence):
    def __init__(self, _right: LogicalSentence):
        self.right = _right
        super().__init__()

    def pcs_used(self):
        return self.right.pcs_used()

    def evaluate(self, conditions):
        return not self.right.evaluate(conditions)


class And(LogicalSentence):
    def __init__(self, _left: LogicalSentence, _right: LogicalSentence):
        self.left = _left
        self.right = _right
        super().__init__()

    def pcs_used(self):
        return self.left.pcs_used().union(self.right.pcs_used())

    def evaluate(self, conditions):
        return self.left.evaluate(conditions) and self.right.evaluate(conditions)


class Or(LogicalSentence):
    def __init__(self, _left: LogicalSentence, _right: LogicalSentence):
        self.left = _left
        self.right = _right
        super().__init__()

    def pcs_used(self):
        return self.left.pcs_used().union(self.right.pcs_used())

    def evaluate(self, conditions):
        return self.left.evaluate(conditions) or self.right.evaluate(conditions)


class MutuallyImplies(LogicalSentence):
    def __init__(self, _left: LogicalSentence, _right: LogicalSentence):
        self.left = _left
        self.right = _right
        super().__init__()

    def pcs_used(self):
        return self.left.pcs_used().union(self.right.pcs_used())

    def evaluate(self, conditions):
        return self.left.evaluate(conditions) == self.right.evaluate(conditions)


class Implies(LogicalSentence):
    def __init__(self, _left: LogicalSentence, _right: LogicalSentence):
        self.left = _left
        self.right = _right
        super().__init__()

    def pcs_used(self):
        return self.left.pcs_used().union(self.right.pcs_used())

    def evaluate(self, conditions):
        l_eval = self.left.evaluate(conditions)
        r_eval = self.right.evaluate(conditions)
        return (not l_eval) or (l_eval and r_eval)

