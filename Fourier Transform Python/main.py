import unittest
import tests
from classes import *
from two_body_massless import *
from logic import *
from fibonacci import *
from graphs import *
import numpy as np
from numpy.linalg import matrix_power

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)

    g = graph_from_file("graph1.txt")
    print(g.biggest_fully_connected_set(3))
    print(g.experimental_indep_finder(3))
