from base_algorithm import *
from random import randrange

class GeneticAlgorithm(BaseAlgorithm):
    
    def __init__(self):
        super().__init__()
    
    ## Mutation methods

    def random_swap(self, solution):
        i, j = randrange(self.size), randrange(self.size)
        solution[i], solution[j] = solution[j], solution[i]
        return solution

    ## Crossover methods

    def cycle(self):
        candidate = self.generate_solution()
        mutant = self.random_swap(candidate)
        fitness_value = self.compute_length(mutant)
        solution = [coordinates[city] for city in mutant]
        full_solution = solution + [solution[0]] 
        return fitness_value, full_solution