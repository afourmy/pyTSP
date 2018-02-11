from .base_algorithm import *

class LocalOptmizationHeuristics(BaseAlgorithm):
    
    ## Pairwise exchange (2-opt)
    
    # swap two edges
    def swap(self, solution, x, y):
        return solution[:x] + solution[x:y+1][::-1] + solution[y+1:]

    def pairwise_exchange(self):
        solution = self.generate_solution()
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
        return [self.format_solution(step) for step in tours], lengths

    ## Node insertion

    def node_insertion(self):
        solution = self.generate_solution()
        stable, best = False, self.compute_length(solution)
        lengths, tours = [best], [solution]
        while not stable:
            stable = True
            for i in range(1, self.size - 1):
                for j in range(1, self.size - 1):
                    substring = solution[i:i+1]
                    candidate = solution[:i] + solution[i+1:]
                    candidate = candidate[:j] + substring + candidate[j:]
                    print(len(solution), len(candidate))
                    tour_length = self.compute_length(candidate)
                    if best > tour_length:
                        stable, solution, best = False, candidate, tour_length
                        tours.append(solution)
                        lengths.append(best)
        print(tours, lengths)
        return [self.format_solution(step) for step in tours], lengths