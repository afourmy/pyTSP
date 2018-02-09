from base_algorithm import *
from cvxopt import matrix, glpk, solvers
from itertools import chain, combinations
from numpy import concatenate, eye, float, full, ones, vstack, zeros

class LinearProgramming(BaseAlgorithm):
    
    def edges_to_tour(self, edges):
        tour, current = [], None
        while edges:
            if not current:
                x, y = edges.pop()
                tour.extend([x, y])
                current = y
            else:
                for edge in edges:
                    if current not in edge:
                        continue
                    current = edge[0] if current == edge[1] else edge[1]
                    tour.append(current)
                    edges.remove(edge)
        return tour[:-1]
    
    def ILP_solver(self):
        n = len(distances)
        sx = n*(n - 1)//2
        c = [float(distances[i+1][j+1]) for i in range(n) for j in range(i + 1, n)]
        
        G, h = [], []
        for st in list(chain.from_iterable(combinations(range(n), r) for r in range(2, n))):
            row = [float(i in st and j in st) for i in range(n) for j in range(i + 1, n)]
            h.append(-float(1 - len(st)))
            G.append(row)
        
        A = [[float(k in (i, j)) for i in range(n) for j in range(i + 1, n)] for k in range(n)]
        b = full(n, 2, dtype=float)
        
        A, G, b, c, h = map(matrix, (A, G, b, c, h))
        solsta, x = glpk.ilp(c, G.T, h, A.T, b, B=set(range(sx)))
        print(c)
        reverse_mapping = [(i+1, j+1) for i in range(n) for j in range(i + 1, n)]
        print(x)
        edges = [reverse_mapping[k] for k in range(sx) if x[k]]
        tour = self.edges_to_tour(edges)
        return self.format_solution(tour), self.compute_length(tour)