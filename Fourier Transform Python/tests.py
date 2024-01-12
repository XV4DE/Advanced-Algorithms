import unittest
import math
import random
from classes import *
from two_body_massless import *
from logic import *
from graphs import *

class Testing(unittest.TestCase):
    def test_fourier_transform_all_zeros(self):
        zeros = []
        for i in range(10):
            zeros.append(Complex(0, 0))
        vz = Vector(zeros)
        self.assertEquals(vz, vz.fourier_transform())

    def test_fourier_transform_all_ones(self):
        ones = []
        for i in range(10):
            ones.append(Complex(1, 0))
        vo = Vector(ones)
        oc = [Complex(1, 0)]
        for i in range(9):
            oc.append(Complex(0, 0))
        voc = Vector(oc)
        for i in range(voc.size()):
            self.assertAlmostEquals(voc[i], vo.fourier_transform()[i])

    def test_fourier_transform(self):
        signal = [Complex(3, 0),
                  Complex(1, 0),
                  Complex(4, 0),
                  Complex(1, 0)]
        v = Vector(signal)
        correct = [Complex(2.25, 0),
                   Complex(-0.25, 0),
                   Complex(1.25, 0),
                   Complex(-0.25, 0)]
        c = Vector(correct)

        for i in range(len(signal)):
            self.assertAlmostEquals(v.fourier_transform()[i], c[i])

        signal = [Complex(0, 0),
                  Complex(1, 0),
                  Complex(0, 0),
                  Complex(0, 0)]
        v = Vector(signal)
        correct = [Complex(0.25, 0),
                   Complex(0, 0.25),
                   Complex(-0.25, 0),
                   Complex(0, -0.25)]
        c = Vector(correct)

        for i in range(len(signal)):
            self.assertAlmostEquals(v.fourier_transform()[i], c[i])

    def test_fft(self):
        for i in range(10):
            a = []
            for j in range(100):
                a.append(Complex(random.randint(-100, 100), random.randint(-100, 100)))
            ft = Vector(a).fourier_transform()
            fft = Vector(a).fast_fourier_transform()
            for k in range(len(a)):
                self.assertAlmostEquals(ft[k], fft[k])

    def test_inverse_fft(self):
        for i in range(10):
            a = []
            for j in range(128):
                a.append(Complex(random.randint(-100, 100), random.randint(-100, 100)))
            fft = Vector(a).fast_fourier_transform()
            ifft = fft.ifft_frfr()
            for k in range(len(a)):
                self.assertAlmostEquals(a[k], ifft[k])

    def test_polynomial_mult(self):
        self.assertEquals(Polynomial([1, 1]) * Polynomial([1, 1]), Polynomial([1, 2, 1]))

    def test_polynomial_fast_mult(self):
        for i in range(10):
            a, b = [], []
            n = random.randint(1, 10)
            for j in range(n):
                a.append(Complex(random.randint(-100, 100), random.randint(-100, 100)))
            for j in range(n):
                b.append(Complex(random.randint(-100, 100), random.randint(-100, 100)))
            a = Polynomial(a)
            b = Polynomial(b)
            for k in range((a*b).size()):
                self.assertAlmostEquals((a*b)[k], a.fast_mul(b)[k])

    def test_logic_is_legal(self):
        self.assertTrue(is_legal("a"))
        self.assertTrue(is_legal("b"))
        self.assertTrue(is_legal("~a"))
        self.assertTrue(is_legal("a<->a"))
        self.assertTrue(is_legal("~a<->b"))
        self.assertTrue(is_legal("~~a<->~b"))
        self.assertTrue(is_legal("a->b"))
        self.assertTrue(is_legal("a|b"))
        self.assertFalse(is_legal("^"))

    def test_logic_eval(self):
        tt = {
            't': True,
            'f': False,
            'p': True,
            'q': False
        }
        t = BasicLogicalSentence('t')
        f = BasicLogicalSentence('f')
        p = BasicLogicalSentence('p')
        q = BasicLogicalSentence('q')

        self.assertTrue(t.evaluate(tt))
        self.assertFalse(f.evaluate(tt))
        self.assertTrue((t or f).evaluate(tt))
        tt['t'] = False
        self.assertFalse((t or f).evaluate(tt))
        tt['t'] = True
        self.assertFalse((t and (-t)).evaluate(tt))

        self.assertTrue(Or(t, f).is_equivalent(Negate(And(Negate(t), Negate(f)))))

    def test_logic_str_to_sentence(self):
        self.assertEquals(str_to_sentence("~a"), Negate(BasicLogicalSentence('a')))
        self.assertEquals(str_to_sentence("~(~a&~b)"), Negate(And(Negate(BasicLogicalSentence('a')), Negate(BasicLogicalSentence('b')))))

    def generate_random_logical_sentence(self, pcs, count=0):
        if count > 2:
            return BasicLogicalSentence(random.choice(pcs))
        choice = random.randint(1, 6)
        if choice == 1:
            return BasicLogicalSentence(random.choice(pcs))
        if choice == 2:
            return Negate(self.generate_random_logical_sentence(pcs, count + 1))
        if choice == 3:
            return And(self.generate_random_logical_sentence(pcs, count + 1), self.generate_random_logical_sentence(pcs, count + 1))
        if choice == 4:
            return Or(self.generate_random_logical_sentence(pcs, count + 1), self.generate_random_logical_sentence(pcs, count + 1))
        if choice == 5:
            return MutuallyImplies(self.generate_random_logical_sentence(pcs, count + 1), self.generate_random_logical_sentence(pcs, count + 1))
        if choice == 6:
            return Implies(self.generate_random_logical_sentence(pcs, count + 1), self.generate_random_logical_sentence(pcs, count + 1))

    def test_indo(self):
        # rando = MutuallyImplies(BasicLogicalSentence('a'), Implies(BasicLogicalSentence('b'), BasicLogicalSentence('c')))
        # indo_rando = indo(rando)
        # self.assertTrue(rando.is_equivalent(indo_rando))
        # print(rando)
        # print(indo_rando)
        # self.assertTrue(is_indo(indo_rando))
        for i in range(2):
            # print(i)
            rando = self.generate_random_logical_sentence(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
            indo_rando = indo(rando)
            # self.assertTrue(rando.is_equivalent(indo_rando))
            # print(rando)
            # print(indo_rando)
            self.assertTrue(is_indo(indo_rando))

    def test_any_path(self):
        a = Node('a')
        b = Node('b')
        nodes = [a, b]
        edges = [Edge(a, b, 1)]
        g = Graph(nodes, edges)
        self.assertEquals(g.any_path(a, b), [a, b])


