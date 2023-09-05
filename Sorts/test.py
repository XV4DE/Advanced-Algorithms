import random, time

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
