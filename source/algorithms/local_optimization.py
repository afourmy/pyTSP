from .base_algorithm import BaseAlgorithm
from functools import partialmethod


class LocalOptmizationHeuristics(BaseAlgorithm):

    ## Pairwise exchange (2-opt)

    # swap two edges
    def swap(self, solution, x, y):
        return solution[:x] + solution[x:y + 1][::-1] + solution[y + 1:]

    def pairwise_exchange(self, ga_solution=None):
        solution = ga_solution or self.generate_solution()
        stable, best = False, self.compute_length(solution)
        lengths, tours = [best], [solution]
        while not stable:
            stable = True
            for i in range(1, self.size - 1):
                for j in range(i + 1, self.size):
                    candidate = self.swap(solution, i, j)
                    length_candidate = self.compute_length(candidate)
                    if best > length_candidate:
                        solution, best = candidate, length_candidate
                        tours.append(solution)
                        lengths.append(best)
                        stable = False
        if ga_solution:
            return tours[-1]
        return [self.format_solution(step) for step in tours], lengths

    ## Node and edge insertion

    def substring_insertion(self, k):
        solution = self.generate_solution()
        stable, best = False, self.compute_length(solution)
        lengths, tours = [best], [solution]
        while not stable:
            stable = True
            for i in range(self.size - k):
                for j in range(self.size):
                    substring = solution[i:(i + k)]
                    candidate = solution[:i] + solution[(i + k):]
                    candidate = candidate[:j] + substring + candidate[j:]
                    tour_length = self.compute_length(candidate)
                    if best > tour_length:
                        stable, solution, best = False, candidate, tour_length
                        tours.append(solution)
                        lengths.append(best)
        return [self.format_solution(step) for step in tours], lengths

    node_insertion = partialmethod(substring_insertion, 1)
    edge_insertion = partialmethod(substring_insertion, 2)
