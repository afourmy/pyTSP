from base_algorithm import *

class OptimizationAlgorithm(BaseAlgorithm):
    
    def __init__(self):
        super().__init__()

    def swap(self, solution, x, y):
        candidate = solution[:x] + solution[x:y+1][::-1] + solution[y+1:]
        print(solution, x, y, candidate)
        return candidate

    # 2-opt
    def two_opt(self):
        print('test')
        solution = self.generate_solution()
        stable, best = False, self.compute_length(solution)
        while not stable:
            stable = True
            for i in range(1, len(solution) - 1):
                for j in range(i + 1, len(solution)):
                    candidate = self.swap(solution, i, j)
                    length_candidate = self.compute_length(candidate)
                    if best > length_candidate:
                        solution, best = candidate, length_candidate
                        stable = False
        return best, self.format_solution(solution)

