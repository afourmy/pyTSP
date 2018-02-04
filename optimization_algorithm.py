from base_algorithm import *

class OptimizationAlgorithm(BaseAlgorithm):
    
    def __init__(self):
        super().__init__()

    # 2-opt
    def two_opt(self):
        solution = self.generate_solution()
        stable = False
        while not stable:
            stable = True
            edges = zip(solution, solution[1:] + [solution[0]])
            for edgeA in edges:
                for edgeB in edges:
                    (a, b), (c, d) = edgeA, edgeB
                    ab, cd = distances[a][b], distances[c][d]
                    ac, bd = distances[a][c], distances[b][d]
                    if ab + cd > ac + bd:
                        for index, city in enumerate(solution):
                            if city in (b, c):
                                solution[index] = c if city == b else b
                            stable = False
        return self.format_solution(solution)

