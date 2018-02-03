from random import randrange

class GeneticAlgorithm():
    
    def __init__(self, distances):
        self.distances = distances

    ## Fitness function

    # computes the total geographical distance with the haversine formula
    def fitness(self, solution):
        total_length = 0
        for i in range(len(solution)):
            total_length += self.distances[solution[i]][solution[(i+1)%len(solution)]]
        return total_length
    
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
    
    def generate_solution(self):
        cities = list(self.distances)
        candidate = sample(cities, self.size)
        mutant = self.two_opt(candidate)
        fitness_value = self.fitness(mutant)
        solution = [(city.latitude, city.longitude) for city in mutant]
        full_solution = solution + [solution[0]] 
        return fitness_value, full_solution