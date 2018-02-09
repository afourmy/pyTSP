from cvxopt import matrix, glpk, solvers
from itertools import chain, combinations
import numpy as np


tour = [1, 2, 3, 4]
distances = [[0, 4, 5, 9], [4, 0, 6, 15], [5, 6, 0, 60], [9, 15, 60, 0]]

n = len(tour)
sx = n*(n - 1)//2
rn = range(n)
c = [float(distances[i][j]) for i in range(n) for j in range(i + 1, n)]

# for the condition 0 < x_ij < 1 and sum(x_ij) < n - 1

id = np.eye(sx, sx)
G1 = np.concatenate((id, -1*id), axis=0).tolist()
print(G1)


G2, h1 = [], []
for st in list(chain.from_iterable(combinations(range(n), r) for r in range(3, n))):
    row = [-float(i in st and j in st) for i in range(n) for j in range(i + 1, n)]
    print(st, row, float(1 - len(st)))
    h1.append(float(1 - len(st)))
    G2.append(row)
print(matrix(G2), matrix(h1))

h = np.concatenate([np.ones(sx), np.zeros(sx), h1])
G = np.vstack((G1, G2))

A = [[float(k in (i, j)) for i in range(n) for j in range(i + 1, n)] for k in range(n)]

b = np.full(n, 2, dtype=np.float)

A, G, b, c, h = map(matrix, (A, G, b, c, h))
# print(G, h)
# print(A.T, b)
# print(c)
solsta, x = glpk.ilp(c, G, h, A.T, b)
# 
print(x)