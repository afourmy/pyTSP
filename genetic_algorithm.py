from base_algorithm import BaseAlgorithm
from random import randrange

class GeneticAlgorithm(BaseAlgorithm):
    
    def __init__(self):
        super().__init__()
    
    ## Mutation methods

    # random swap
    def random_swap(self, solution):
        i, j = randrange(self.size), randrange(self.size)
        solution[i], solution[j] = solution[j], solution[i]
    
    # 2-opt
    def two_opt(self, solution):
        stable = False
        while not stable:
            stable = True
            edges = zip(solution, solution[1:] + [solution[0]])
            for edgeA in edges:
                for edgeB in edges:
                    (a, b), (c, d) = edgeA, edgeB
                    ab, cd = self.distances[a][b], self.distances[c][d]
                    ac, bd = self.distances[a][c], self.distances[b][d]
                    if ab + cd > ac + bd:
                        for index, city in enumerate(solution):
                            if city in (b, c):
                                solution[index] = c if city == b else b
                            stable = False
        return solution
    
    ## Solution generator
    
    def cycle(self):
        cities = list(self.distances)
        candidate = self.generate_solution()
        mutant = self.two_opt(candidate)
        fitness_value = self.fitness(mutant)
        solution = [(city.latitude, city.longitude) for city in mutant]
        full_solution = solution + [solution[0]] 
        return fitness_value, full_solution