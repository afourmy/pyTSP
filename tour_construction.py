from base_algorithm import *
from operator import itemgetter

class TourConstruction(BaseAlgorithm):
    
    def nearest_neighbor(self):
        tours = {}
        for city in cities:
            current, tour = city, [city]
            while len(tour) != len(cities):
                current_dist = [(c, d) for c, d in distances[current].items() if c not in tour]
                arg_min, _ = sorted(current_dist, key=itemgetter(1))[0]
                tour.append(arg_min)
                current = arg_min
            tours[city] = [coordinates[city] for city in tour]
        return tours
            
            