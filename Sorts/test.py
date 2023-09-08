import random, time, tqdm

from sorts import *


def test_xor_swap():
    for i in range(2, 2049):
        bits = []
        for _j in range(i):
            bits.append(random.randint(0, 1))
        a = random.randint(0, i - 1)
        b = random.randint(0, i - 1)
        ai = bits[a]
        bi = bits[b]
        og_bits = bits.copy()
        xor_swap(bits, a, b)
        if ai != bits[b] or bi != bits[a]:
            print(og_bits)
            print(bits)
            print(a)
            print(b)
            return False
    return True


def test_traditional_swap():
    for i in range(2, 2049):
        bits = []
        for _j in range(i):
            bits.append(random.randint(0, 1))
        a = random.randint(0, i - 1)
        b = random.randint(0, i - 1)
        ai = bits[a]
        bi = bits[b]
        og_bits = bits.copy()
        traditional_swap(bits, a, b)
        if ai != bits[b] or bi != bits[a]:
            print(og_bits)
            print(bits)
            print(a)
            print(b)
            return False
    return True


def test_additive_swap():
    for i in range(2, 2049):
        bits = []
        for _j in range(i):
            bits.append(random.randint(0, 1))
        a = random.randint(0, i - 1)
        b = random.randint(0, i - 1)
        ai = bits[a]
        bi = bits[b]
        og_bits = bits.copy()
        additive_swap(bits, a, b)
        if ai != bits[b] or bi != bits[a]:
            print(og_bits)
            print(bits)
            print(a)
            print(b)
            return False
    return True


def test_xor_swap_time(num):
    nums = [0, num]
    start = time.time()
    for i in range(10000):
        xor_swap(nums, 0, 1)
    return time.time() - start


def test_traditional_swap_time(num):
    nums = [0, num]
    start = time.time()
    for i in range(10000):
        traditional_swap(nums, 0, 1)
    return time.time() - start


def test_sort(sort) -> bool:
    try:
        ml = []
        sort(ml)
        assert ml == []
        ml.append(1)
        sort(ml)
        assert ml == [1]
        ml.append(0)
        sort(ml)
        assert ml == [1, 0]
        ml.append(2)
        sort(ml)
        assert ml == [2, 1, 0]
        return True
    except:
        return False


def test_transpose(transp) -> bool:
  try:
    ml = []
    ml = transp(ml, 0)
    assert ml == []
    ml.append(1)
    ml = transp(ml, 1)
    assert ml == [1]
    ml.append(2)
    ml.append(3)
    ml.append(4)
    ml = transp(ml, 2)
    assert ml == [1, 3,
                  2, 4]
    ml = transp(ml, 2)
    assert ml == [1, 2,
                  3, 4]
    return True
  except:
    return False


def test_greatest(greatest_func) -> bool:
  try:
    assert greatest_func([0, 0]) == 0
    assert greatest_func([0, 1]) == 1
    return True
  except:
    return False


def test_column(cs) -> bool:
  try:
    ml = [1, 4, 3, 2]
    ml = cs(ml, 2)
    assert ml == [4, 2,
                  3, 1]
    return True
  except:
    return False


def sorting_time_efficiency(sort):
    times = []
    for i in tqdm.tqdm(range(100)):
        l = [j for j in range(i * 100)]
        random.shuffle(l)
        start = time.time()
        l = sort(l)
        speed = time.time() - start
        times.append(speed)
    return times

