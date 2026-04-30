from .local_optimization import LocalOptmizationHeuristics
from random import randint, random, randrange, sample


class GeneticAlgorithm(LocalOptmizationHeuristics):

    crossovers = {
        'Crossover method': 'order_crossover',
        'OC': 'order_crossover',
        'MPC': 'maximal_preservative_crossover',
        'PMC': 'partially_mapped_crossover'
    }

    mutations = {
        'Mutation method': 'swap_mutation',
        'Swap': 'swap_mutation',
        'Insertion': 'insertion_mutation',
        'Displacement': 'displacement_mutation'
    }

    def __init__(self):
        super().__init__()
        self.crossover = 'order_crossover'
        self.mutation = 'random_mutation'

    ## Mutation methods

    def swap_mutation(self, solution):
        solution = solution[:]
        i, j = randrange(self.size), randrange(self.size)
        solution[i], solution[j] = solution[j], solution[i]
        return solution

    def insertion_mutation(self, solution):
        solution = solution[:]
        random_city, random_position = randrange(self.size), randrange(self.size)
        city = solution.pop(random_city)
        solution.insert(random_position, city)
        return solution

    def displacement_mutation(self, solution):
        a, b = self.crossover_cut()
        random_position = randint(0, self.size)
        substring = solution[a:b]
        solution = solution[:a] + solution[b:]
        return solution[:random_position] + substring + solution[random_position:]

    ## Crossover methods

    def crossover_cut(self):
        first_cut = randint(1, self.size - 2)
        return first_cut, randint(first_cut + 1, self.size)

    def order_crossover(self, i1, i2):
        a, b = self.crossover_cut()
        ni1, ni2, i1, i2 = i1[a:b], i2[a:b], i1[b:] + i1[:b], i2[b:] + i2[:b]
        for x in i1:
            if x in ni2:
                continue
            ni2.append(x)
        for x in i2:
            if x in ni1:
                continue
            ni1.append(x)
        return ni1, ni2

    def maximal_preservative_crossover(self, i1, i2):
        c = len(i1) // 2
        r = randrange(self.size + 1)
        s1, s2 = (i1 * 2)[r:r + c], (i2 * 2)[r:r + c]
        for x in s1:
            i2.remove(x)
        for x in s2:
            i1.remove(x)
        ni1, ni2 = s2 + i1, s1 + i2
        return ni1, ni2

    def partial_mapping(self, i1, i2, ni1, ni2, a, b):
        for x in i2[a:b]:
            if x in i1[a:b]:
                continue
            curr = x
            while True:
                index_curr = i2.index(curr)
                j = i1[index_curr]
                if not ni1[i2.index(j)]:
                    ni1[i2.index(j)] = x
                    break
                else:
                    curr = ni2[i2.index(j)]

    def partially_mapped_crossover(self, i1, i2):
        a, b = self.crossover_cut()
        ni1, ni2 = [0] * self.size, [0] * self.size
        ni1[a:b], ni2[a:b] = i1[a:b], i2[a:b]
        self.partial_mapping(i1, i2, ni1, ni2, a, b)
        self.partial_mapping(i2, i1, ni2, ni1, a, b)
        ni1 = [x if x else i2[i] for i, x in enumerate(ni1)]
        ni2 = [x if x else i1[i] for i, x in enumerate(ni2)]
        return ni1, ni2

    ## Core algorithm

    def select(self, population):
        return min(sample(population, 5), key=self.compute_length)[:]

    def cycle(self, generation, **data):
        cr, crossover = data['cr'], self.crossovers[data['crossover']]
        mr, mutation = data['mr'], self.mutations[data['mutation']]
        if not generation:
            generation = [self.generate_solution() for _ in range(100)]
        generation = sorted(generation, key=self.compute_length)
        # elitism: keep best, fill rest via selection + crossover + mutation
        ng = [generation[0][:]]
        while len(ng) < len(generation):
            p1, p2 = self.select(generation), self.select(generation)
            children = getattr(self, crossover)(p1, p2) if random() < cr else (p1, p2)
            ng.extend(getattr(self, mutation)(c) if random() < mr else c for c in children)
        ng = sorted(ng[:len(generation)], key=self.compute_length)
        return ng, self.format_solution(ng[0]), self.compute_length(ng[0])
