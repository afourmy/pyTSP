from base_algorithm import *
from random import randrange, shuffle

class GeneticAlgorithm(BaseAlgorithm):
    
    def __init__(self):
        super().__init__()
    
    ## Mutation methods

    def random_swap(self, solution):
        i, j = randrange(self.size), randrange(self.size)
        solution[i], solution[j] = solution[j], solution[i]
        return solution

    ## Crossover methods

    def crossover(self, i1, i2):
        return i1, i2

    ## Core algorithm
    
    def create_first_generation(self):
        return [self.generate_solution() for _ in range(10)]

    def cycle(self, generation):
        shuffle(generation)
        ng = []
        # first step: crossover with a Pc probability
        for i1, i2 in zip(generation[::2], generation[1::2]):
            ng.extend(self.crossover(i1, i2) if 1 else (i1, i2))
        # second step: mutation with a Pm probability
        ng = [self.random_swap(i) if True else i for i in ng]
        # order the generation according to the fitness value
        ng = sorted(ng, key=self.compute_length)
        return ng, self.format_solution(ng[0]), self.compute_length(ng[0])