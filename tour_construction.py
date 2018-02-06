from base_algorithm import *
from operator import itemgetter

class TourConstruction(BaseAlgorithm):
    
    # find the closest neighbor in the tour or not yet visited (default) 
    # returns the neighbor as well as the distance between the two
    def closest_neighbor(self, tour, node, in_tour=False):
        neighbors = distances[node]
        current_dist = [(c, d) for c, d in neighbors.items() 
                        if (c in tour if in_tour else c not in tour)]
        return sorted(current_dist, key=itemgetter(1))[0]
    
    def nearest_neighbor(self):
        best_tour, best_length = None, float('inf')
        for city in cities:
            current, tour, length = city, [city], 0
            while len(tour) != len(cities):
                arg_min, edge_length = self.closest_neighbor(tour, current)
                length += edge_length
                tour.append(arg_min)
                current = arg_min
            if length < best_length:
                best_length, best_tour = length, tour
        return self.format_solution(best_tour), best_length
            
    def nearest_insertion(self):
        best_tour, best_length = None, float('inf')
        # store intermediate tours for visualization purposes
        best_tours = []
        for city in cities:
            # we start the tour with one node I
            tour, tour_length, tours = [city], 0, []
            # we find the closest node R to the first node
            neighbor, _ = self.closest_neighbor(tour, city)
            tour.append(neighbor)
            while len(tour) != len(cities):
                best, min_distance = None, float('inf')
                # (selection step) given a sub-tour,we find node r not in the 
                # sub-tour closest to any node j in the sub-tour, 
                # i.e. with minimal c_rj
                for candidate in cities:
                    if candidate in tour:
                        continue
                    # we consider only the distances to nodes already in the tour
                    _, length = self.closest_neighbor(tour, candidate, True)
                    if length < min_distance:
                        best, min_distance = candidate, length
                # (insertion step) we find the arc (i, j) in the sub-tour which 
                # minimizes cir + crj - cij, and we insert r between i and j
                add = lambda i, j, r: distances[i][r] + distances[r][j] - distances[i][j]
                min_index, min_distance = None, float('inf')
                tour = tour + [tour[0]]
                for i in range(len(tour) - 1):
                    added_distance = add(tour[i], tour[i+1], best)
                    if added_distance < min_distance:
                        min_index, min_distance = i, added_distance
                tour_length += add(tour[min_index], tour[min_index + 1], best)
                tours.append(tour)
                tour.insert(min_index + 1, best)
                tour = tour[:-1]
            if tour_length < best_length:
                best_length, best_tour, best_tours = tour_length, tour, tours
            print(best_length)
        return [self.format_solution(step) for step in best_tours], best_length
                