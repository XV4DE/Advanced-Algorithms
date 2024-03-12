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
    if op == BasicLogicalSentence:
        return True
    if op == Implies or op == MutuallyImplies:
        return False
    if op == Negate:
        return type(sentence.right) == BasicLogicalSentence
    if op == And:
        return is_indo(sentence.left) and is_indo(sentence.right)
    if op == Or:
        if type(sentence.left) == And or type(sentence.right) == And:
            return False
        return is_indo(sentence.left) and is_indo(sentence.right)


def indo(sentence):
    t = type(sentence)
    if t == BasicLogicalSentence:
        return sentence
    elif t == MutuallyImplies:
        return indo_mutuallyimplies(sentence)
    elif t == Implies:
        return indo_implies(sentence)
    elif t == And:
        return indo_and(sentence)
    elif t == Or:
        return indo_or(sentence)
    elif t == Negate:
        return indo_negate(sentence)


def indo_negate(_sentence):
    if type(_sentence.right) == BasicLogicalSentence:
        return _sentence
    if type(_sentence.right) == Negate:
        return indo(_sentence.right.right)
    sentence = indo(_sentence.right)
    return indo(recursive_invert(sentence))


def recursive_invert(sentence):
    t = type(sentence)
    if t == BasicLogicalSentence:
        return Negate(sentence)
    if t == Negate:
        return sentence.right
    if t == And:
        return Or(recursive_invert(sentence.left), recursive_invert(sentence.right))
    if t == Or:
        return And(recursive_invert(sentence.left), recursive_invert(sentence.right))


def indo_and(_sentence):
    return And(indo(_sentence.left), indo(_sentence.right))


def indo_or(_sentence):
    sentence = Or(indo(_sentence.left), indo(_sentence.right))
    if type(sentence.left) == And:
        return indo(And(Or(sentence.left.left, sentence.right), Or(sentence.left.right, sentence.right)))
    if type(sentence.right) == And:
        return indo(And(Or(sentence.right.left, sentence.left), Or(sentence.right.right, sentence.left)))
    return sentence


def indo_mutuallyimplies(_sentence):
    l = indo(_sentence.left)
    r = indo(_sentence.right)
    return And(indo(Or(l, indo(Negate(r)))), indo(Or(indo(Negate(l)), r)))


def indo_implies(_sentence):
    l = indo(_sentence.left)
    r = indo(_sentence.right)
    return indo(Or(indo(Negate(l)), r))


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
    # print(f"n = {n}, pcs = {pcs}")
    out = {}
    for i in range(len(pcs)):
        idx = len(pcs) - 1 - i
        out[pcs[idx]] = bool(bits(n)[len(bits(n)) - 1 - i]) if i < len(bits(n)) else False
    return out


# Returns a list of all logical sentences contained within the input that are not basic logical sentences. If a
# subsentence (subformula)'s left child is also a subsentence it will appear immediately after it in the list, the right
# child will follow immediately after that assuming it meets the same requirements.
def all_subformulas(ls):
    if type(ls) == BasicLogicalSentence:
        return []
    out = [ls]
    if type(ls) is not Negate and type(ls.left) is not BasicLogicalSentence:
        out.append(all_subformulas(ls.left)[0])
    if type(ls.right) is not BasicLogicalSentence:
        out.append(all_subformulas(ls.right)[0])
    if type(ls) is not Negate:
        out.extend(all_subformulas(ls.left)[1:])
    out.extend(all_subformulas(ls.right)[1:])
    return out


# Returns an equivalent logical sentence in non-indo cnf3 as described in
# https://en.wikipedia.org/wiki/Tseytin_transformation
def cnf3(ls):
    subformulas = all_subformulas(ls)
    out = BasicLogicalSentence('0')
    next_free_idx = 1
    for i in range(len(subformulas)):
        if next_free_idx < i + 1:
            next_free_idx = i + 1
        # This block of ifs is entirely dedicated to forcing the output to make use of the newly created pcs when
        # defining a subsentence.
        if type(subformulas[i]) is Negate:
            if type(subformulas[i].right) is BasicLogicalSentence:
                subformula = subformulas[i]
            else:
                subformula = Negate(BasicLogicalSentence(str(next_free_idx)))
                next_free_idx += 1
        else:
            if type(subformulas[i].left) is BasicLogicalSentence:
                left = subformulas[i].left
            else:
                left = BasicLogicalSentence(str(next_free_idx))
                next_free_idx += 1

            if type(subformulas[i].right) is BasicLogicalSentence:
                right = subformulas[i].right
            else:
                right = BasicLogicalSentence(str(next_free_idx))
                next_free_idx += 1
            subformula = type(subformulas[i])(left, right)

        out = And(out, MutuallyImplies(BasicLogicalSentence(str(i)), subformula))
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
            fixed_pcs = list(pcs)
            fixed_pcs.sort(key=ord)
            perm = int_to_truth_permutation(i, fixed_pcs)
            out[perm] = self.evaluate(perm)
        return out

    def is_valid(self):
        return False not in self.truth_table().values

    def is_satisfiable(self):
        return True in self.truth_table().values

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

    def __str__(self):
        return self.pc


class Negate(LogicalSentence):
    def __init__(self, _right: LogicalSentence):
        self.right = _right
        super().__init__()

    def pcs_used(self):
        return self.right.pcs_used()

    def evaluate(self, conditions):
        return not self.right.evaluate(conditions)

    def __str__(self):
        if type(self.right) != BasicLogicalSentence:
            return '~(' + str(self.right) + ')'
        else:
            return '~' + str(self.right)


class And(LogicalSentence):
    def __init__(self, _left: LogicalSentence, _right: LogicalSentence):
        self.left = _left
        self.right = _right
        super().__init__()

    def pcs_used(self):
        return self.left.pcs_used().union(self.right.pcs_used())

    def evaluate(self, conditions):
        return self.left.evaluate(conditions) and self.right.evaluate(conditions)

    def __str__(self):
        l = '(' + str(self.left) + ')' if type(self.left) != BasicLogicalSentence else str(self.left)
        r = '(' + str(self.right) + ')' if type(self.right) != BasicLogicalSentence else str(self.right)
        return l + '&' + r


class Or(LogicalSentence):
    def __init__(self, _left: LogicalSentence, _right: LogicalSentence):
        self.left = _left
        self.right = _right
        super().__init__()

    def pcs_used(self):
        return self.left.pcs_used().union(self.right.pcs_used())

    def evaluate(self, conditions):
        return self.left.evaluate(conditions) or self.right.evaluate(conditions)

    def __str__(self):
        l = '(' + str(self.left) + ')' if type(self.left) != BasicLogicalSentence else str(self.left)
        r = '(' + str(self.right) + ')' if type(self.right) != BasicLogicalSentence else str(self.right)
        return l + '|' + r


class MutuallyImplies(LogicalSentence):
    def __init__(self, _left: LogicalSentence, _right: LogicalSentence):
        self.left = _left
        self.right = _right
        super().__init__()

    def pcs_used(self):
        return self.left.pcs_used().union(self.right.pcs_used())

    def evaluate(self, conditions):
        return self.left.evaluate(conditions) == self.right.evaluate(conditions)

    def __str__(self):
        l = '(' + str(self.left) + ')' if type(self.left) != BasicLogicalSentence else str(self.left)
        r = '(' + str(self.right) + ')' if type(self.right) != BasicLogicalSentence else str(self.right)
        return l + '<->' + r


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

    def __str__(self):
        l = '(' + str(self.left) + ')' if type(self.left) != BasicLogicalSentence else str(self.left)
        r = '(' + str(self.right) + ')' if type(self.right) != BasicLogicalSentence else str(self.right)
        return l + '->' + r

