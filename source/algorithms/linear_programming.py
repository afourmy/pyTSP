from .base_algorithm import BaseAlgorithm
from itertools import chain, combinations
try:
    from cvxopt import matrix, glpk
    from numpy import float, full
except ImportError:
    import warnings
    warnings.warn('cvxopt/numpy import failed: linear programming will not work')


class LinearProgramming(BaseAlgorithm):

    def edges_to_tour(self, edges):
        tour, current = [], None
        while edges:
            if current:
                for edge in edges:
                    if current not in edge:
                        continue
                    current = edge[0] if current == edge[1] else edge[1]
                    tour.append(current)
                    edges.remove(edge)
            else:
                x, y = edges.pop()
                tour.extend([x, y])
                current = y
        return tour[:-1]

    def ILP_solver(self):
        n, sx = len(self.distances), len(self.distances) * (len(self.distances) - 1) // 2
        c = [float(self.distances[i + 1][j + 1]) for i in range(n) for j in range(i + 1, n)]
        G, h, A, b = [], [], [], full(n, 2, dtype=float)
        for st in chain.from_iterable(combinations(range(n), r) for r in range(2, n)):
            G += [[float(i in st and j in st) for i in range(n) for j in range(i + 1, n)]]
            h.append(-float(1 - len(st)))
        for k in range(n):
            A.append([float(k in (i, j)) for i in range(n) for j in range(i + 1, n)])
        A, G, b, c, h = map(matrix, (A, G, b, c, h))
        _, x = glpk.ilp(c, G.T, h, A.T, b, B=set(range(sx)))
        reverse_mapping = [(i + 1, j + 1) for i in range(n) for j in range(i + 1, n)]
        tour = self.edges_to_tour([reverse_mapping[k] for k in range(sx) if x[k]])
        intermediate_steps = [[]]
        for point in self.format_solution(tour):
            intermediate_steps.append(intermediate_steps[-1] + [point])
        return intermediate_steps[2:], [self.compute_length(tour)] * n
