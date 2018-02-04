from base_algorithm import *
from operator import itemgetter

class TourConstruction(BaseAlgorithm):
    
    def nearest_neighbor(self):
        best_tour, best_length = None, float('inf')
        for city in cities:
            current, tour, length = city, [city], 0
            while len(tour) != len(cities):
                current_dist = [(c, d) for c, d in distances[current].items() 
                                                            if c not in tour]
                arg_min, edge_length = sorted(current_dist, key=itemgetter(1))[0]
                length += edge_length
                tour.append(arg_min)
                current = arg_min
            if length < best_length:
                best_length, best_tour = length, tour
        return self.format_solution(best_tour)
            
            