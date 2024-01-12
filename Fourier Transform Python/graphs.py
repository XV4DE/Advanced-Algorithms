from classes import *
import numpy as np
from numpy.linalg import matrix_power
import copy


class Node:
    def __init__(self, _name=None):
        self.name = _name

    def __eq__(self, other):
        return self is other

    def __str__(self):
        return '「' + self.name + '」'


class Edge:
    def __init__(self, _start, _end, _value = 1):
        self.start = _start
        self.end = _end
        self.value = _value

    def __eq__(self, other):
        return (type(other) is Graph and ((self.start == other.start and self.end == other.end) or
                                          (self.start == other.end and self.end == other.start)))


class Graph:
    def __init__(self, _nodes, _edges):
        self.nodes = _nodes
        self.edges = _edges

    def add_node(self, a: Node):
        self.nodes.append(a)

    def are_connected(self, a, b):
        for edge in self.edges:
            if (edge.start == a and edge.end == b) or edge.start == b and edge.end == a:
                return True
        return False

    def connect(self, a: Node, b: Node, value: int):
        self.edges.append(Edge(a, b, value))

    def neighbors(self, a: Node):
        connections = []
        for edge in self.edges:
            if edge.start == a and edge.end not in connections:
                connections.append(edge.end)
            if edge.end == a and edge.start not in connections:
                connections.append(edge.start)
        return connections

    def any_path(self, start: Node, end: Node):
        if end in self.neighbors(start):
            return [start, end]
        for neighbor in self.neighbors(start):
            if end in self.any_path(neighbor, end):
                return self.any_path(neighbor, end).insert(start, 0)

    def adjacency_matrix(self):
        out = []
        for a in self.nodes:
            v = []
            for b in self.nodes:
                if self.are_connected(a, b):
                    v.append(1)
                else:
                    v.append(0)
            out.append(v)
        return np.array(out)

    def inverted_adjacency_matrix(self):
        out = []
        for a in self.nodes:
            v = []
            for b in self.nodes:
                if self.are_connected(a, b):
                    v.append(0)
                else:
                    v.append(1)
            out.append(v)
        return np.array(out)

    def experimental_indep_finder(self, k):
        adj_mat = self.adjacency_matrix()
        b = copy.deepcopy(adj_mat)
        for i in range(2, k * 2 + 2):
            b += matrix_power(adj_mat, i)
        return b

    def special_max(self, arr, exclude):
        current_max = -1
        for i in range(len(arr)):
            if arr[i] > current_max and self.nodes[i] not in exclude:
                current_max = arr[i]

        if current_max == -1:
            return None
        else:
            return current_max

    def biggest_fully_connected_set(self, k):
        out = []
        indep_matrix = self.experimental_indep_finder(k)
        diag = np.diag(indep_matrix)
        big = diag.max()

        start = np.where(diag == big)[0][0]
        current = start

        moving_horizontal = True
        for i in range(k):
            if moving_horizontal:
                row = indep_matrix[current]
                big = self.special_max(row, out)
                for num in range(len(row)):
                    if row[num] == big and self.nodes[num] not in out:
                        out.append(self.nodes[num])
                        current = num
                        break
            else:
                col = np.array([i[current] for i in indep_matrix])
                big = self.special_max(col, out)
                for num in range(len(col)):
                    if col[num] == big and self.nodes[num] not in out:
                        out.append(self.nodes[num])
                        current = num
                        break

            moving_horizontal = not moving_horizontal

        return Vector(out)











