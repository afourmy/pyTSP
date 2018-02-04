from base_algorithm import BaseAlgorithm, coordinates, distances
from random import randrange

class GeneticAlgorithm(BaseAlgorithm):
    
    def __init__(self):
        super().__init__()
    
    ## Mutation methods

    # random swap
    def random_swap(self, solution):
        i, j = randrange(self.size), randrange(self.size)
        solution[i], solution[j] = solution[j], solution[i]

    ## Crossover methods
    
    ## Solution generator
    
    def cycle(self):
        candidate = self.generate_solution()
        mutant = self.two_opt(candidate)
        fitness_value = self.compute_length(mutant)
        solution = [coordinates[city] for city in mutant]
        full_solution = solution + [solution[0]] 
        return fitness_value, full_solution