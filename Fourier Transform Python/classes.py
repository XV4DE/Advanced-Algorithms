import math


def n_roots(n: int):
    ret = []
    for i in range(n):
        row = []
        for j in range(n):
            real_comp = math.cos(2 * math.pi * i * j / n)
            imag_comp = math.sin(2 * math.pi * i * j / n)
            row.append(Complex(real_comp, imag_comp))
        ret.append(row)
    return Matrix(ret)


def w(x, of):
    return Complex(math.cos(x/of*2*math.pi), math.sin(x/of*2*math.pi))


def hyperceil(n):
    return int(math.pow(2, math.ceil(math.log(n, 2))))


class Complex:
    def __init__(self, _real, _imaginary):
        self.real = _real
        self.imaginary = _imaginary

    def __add__(self, other):
        if type(other) == int:
            return Complex(self.real + other, self.imaginary)
        elif type(other) == Complex:
            return Complex(self.real + other.real, self.imaginary + other.imaginary)

    def __sub__(self, other):
        if type(other) == int:
            return Complex(self.real - other, self.imaginary)
        elif type(other) == Complex:
            return Complex(self.real - other.real, self.imaginary - other.imaginary)

    def __eq__(self, other):
        return self.real == other.real and self.imaginary == other.imaginary

    def __gt__(self, other):
        return self.__abs__() > other.__abs__()

    def __ge__(self, other):
        return self.__abs__() >= other.__abs__()

    def __lt__(self, other):
        return self.__abs__() < other.__abs__()

    def __le__(self, other):
        return self.__abs__() <= other.__abs__()

    def __str__(self):
        if self.imaginary == 0:
            return str(self.real)
        return str(self.real) + " + " + str(self.imaginary) + "i"

    def __mul__(self, other):
        if type(other) == int:
            return Complex(self.real * other, self.imaginary * other)
        elif type(other) == Complex:
            return Complex(self.real * other.real - self.imaginary * other.imaginary,
                           self.real * other.imaginary + self.imaginary * other.real)

    def __truediv__(self, other):
        if type(other) == int:
            return Complex(self.real/other, self.imaginary/other)

    def __abs__(self):
        return math.sqrt(math.pow(self.real, 2) + math.pow(self.imaginary, 2))

    def round(self):
        return Complex(int(self.real + 0.5), int(self.imaginary + 0.5))


class Vector:
    def __init__(self, _vals):
        self.vals = _vals.copy()

    def __getitem__(self, item):
        return self.vals[item]

    def __mul__(self, other):
        if type(other) == Vector:
            assert len(self.vals) == len(other.vals) and len(self.vals) != 0
            ret = []
            for i in self:
                total = 0
                for j in other:
                    total += i*j
                ret.append(total)
            return Vector(ret)
        if type(other) == int:
            return Vector([i * other for i in self])

    def __eq__(self, other):
        return self.vals == other.vals

    def __str__(self):
        out = ""
        for i in self.vals:
            out += str(i) + ", "
        return "<"+out[:-2]+">"

    def __copy__(self):
        return Vector(self.vals.copy())

    def get_evens(self):
        return Vector([self.vals[i] for i in range(len(self.vals)) if i % 2 == 0])

    def get_odds(self):
        return Vector([self.vals[i] for i in range(len(self.vals)) if i % 2 != 0])

    def as_polynomial(self):
        return Polynomial(self.vals)

    def inverse(self):
        return Vector([self[len(self.vals)-1-i] for i in range(len(self.vals))])

    def copy(self):
        return self.__copy__()

    def size(self):
        return len(self.vals)

    def pretty(self):
        out = ""
        for i in self.vals:
            out += str(i.round()) + ", "
        return "<"+out[:-2]+">"

    def simple_mul(self, other):
        out = []
        for i in range(self.size()):
            out.append(self[i] * other[i])
        return Vector(out)

    def fourier_transform(self):
        n = self.size()
        roots = n_roots(n)
        out = []
        for s in range(n):
            acc = Complex(0, 0)
            for k in range(n):
                acc += roots[s][k] * self[k]
            out.append(acc/n)
        return Vector(out)

    def fast_fourier_transform(self):
        n = self.size()
        if n % 2 != 0:
            return self.fourier_transform()
        evens = self.get_evens().fast_fourier_transform()
        odds = self.get_odds().fast_fourier_transform()
        out = []
        for k in range(n):
            out.append((evens[k % evens.size()] + odds[k % evens.size()] * w(k, n))/2)
        return Vector(out)

    def fft(self):
        return self.fast_fourier_transform()

    def fft_unnormalized(self):
        n = self.size()
        if n == 1:
            return self
        assert n % 2 == 0
        evens = self.get_evens().fast_fourier_transform()
        odds = self.get_odds().fast_fourier_transform()
        out = []
        for k in range(n):
            out.append((evens[k % evens.size()] + odds[k % evens.size()] * w(k, n)))
        return Vector(out)

    def inverse_fft(self):
        fft = self.fft() * self.size()
        out = fft.recursive_inverse()
        return out

    def ifft_frfr(self):
        n = self.size()
        if n % 2 != 0:
            return self.fourier_transform()
        evens = self.get_evens().ifft_frfr()
        odds = self.get_odds().ifft_frfr()
        out = []
        for k in range(n):
            out.append((evens[k % evens.size()] + odds[k % evens.size()] * w(-k, n)))
        return Vector(out)

    def recursive_inverse(self):
        if self.size() == 1:
            return self.copy()
        evens = self.get_evens().recursive_inverse()
        odds = self.get_odds().inverse()
        out = []
        for i in range(self.size()):
            if i % 2 == 0:
                out.append(evens[int(i / 2)])
            else:
                out.append(odds[int((i - 1) / 2)])
        return Vector(out)


class Polynomial:
    def __init__(self, _coefficients):
        self.coefficients = _coefficients

    def __getitem__(self, item):
        return self.coefficients[item]

    def __eq__(self, other):
        return self.coefficients == other.coefficients

    def __mul__(self, other):
        if type(other) == Polynomial:
            assert self.size() == other.size()
            out = [0 for i in range(self.size() * 2 - 1)]
            for m in range(self.size()):
                for l in range(self.size()):
                    out[l+m] = self[m] * other[l] + out[m+l]
            return Polynomial(out)
        if type(other) == int:
            return Polynomial([i*other for i in self.coefficients])

    def __str__(self):
        out = ""
        for i in range(self.size()):
            out += "(" + str(self.coefficients[i]) + ")" + "x^" + str(i) + " + "
        return "P"+out[:-3]+"P"

    def pretty(self):
        out = ""
        for i in range(self.size()):
            out += "(" + self.coefficients[i].pretty() + ")" + "x^" + str(i) + " + "
        return "P" + out[:-3] + "P"

    def size(self):
        return len(self.coefficients)

    def eval(self, x):
        acc = Complex(0, 0)
        for i in range(self.size()):
            acc += x^i * self[i]

    def as_vector(self):
        return Vector(self.coefficients.copy())

    def pad_for_fast_mul(self):
        c = self.coefficients.copy()
        n = hyperceil(self.size() * 2) - self.size()
        for i in range(n):
            c.append(0)
        return Polynomial(c)

    def fast_mul(self, other):
        return self.pad_for_fast_mul().as_vector().fft().simple_mul(other.pad_for_fast_mul().as_vector().fft()).inverse_fft().as_polynomial()*hyperceil(self.size()*2)


class Matrix:
    def __init__(self, _vals):
        self.vals = _vals.copy()

    def __getitem__(self, item):
        return self.vals[item]

    def __mul__(self, other):
        if type(other) == Matrix:
            return self._dot_prod_matrix(other)
        elif type(other) == Vector:
            return self._dot_prod_vector(other)

    def size(self):
        return len(self.vals)

    def _dot_prod_matrix(self, other):
        assert self.size() == other.size()
        size = self.size()
        ret = []
        for i in range(size):
            row = []
            for j in range(size):
                acc = Complex(0, 0)
                for k in range(size):
                    acc += self[i][k] * other[k][j]
                row.append(acc)
            ret.append(row)
        return Matrix(ret)

    def _dot_prod_vector(self, other):
        assert self.size() == other.size()
        size = self.size()
        ret = []
        for i in range(size):
            acc = Complex(0, 0)
            for j in range(size):
                acc += self[i][j] * other[j]
            ret.append(acc)
        return Vector(ret)

