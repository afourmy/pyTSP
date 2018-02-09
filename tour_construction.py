from base_algorithm import *
from operator import itemgetter

class TourConstruction(BaseAlgorithm):
    
    def add(self, i, j, k):
        return distances[i][k] + distances[k][j] - distances[i][j]
    
    # find the closest neighbo in the tour or not yet visited (default) 
    # to a given node
    # returns the neighbor as well as the distance between the two
    def closest_neighbor(self, tour, node, in_tour=False):
        neighbors = distances[node]
        current_dist = [(c, d) for c, d in neighbors.items() 
                        if (c in tour if in_tour else c not in tour)]
        return sorted(current_dist, key=itemgetter(1))[0]

    # find the neighbor k closest to the tour, i.e such that
    # cik + ckj - cij is minimized with (i, j) an edge of the tour
    # add k between the edge (i, j), resulting in a tour with subtour (i, k, j)
    # used for the cheapest insertion algorithm
    def add_closest_to_tour(self, tour):
        best_dist, new_tour = float('inf'), None
        for city in cities:
            if city in tour:
                continue
            for index in range(len(tour) - 1):
                dist = self.add(tour[index], tour[index + 1], city)
                if dist < best_dist:
                    best_dist = dist
                    new_tour = tour[:index + 1] + [city] + tour[index + 1:]
        return best_dist, new_tour
    
    def nearest_neighbor(self):
        best_tour, best_length = None, float('inf')
        for city in cities:
            current, tour, length = city, [city], 0
            while len(tour) != len(cities):
                arg_min, edge_length = self.closest_neighbor(tour, current)
                length += edge_length
                tour.append(arg_min)
                current = arg_min
            # we close the tour by adding the last edge length
            length += distances[current][city]
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
                min_index, min_distance = None, float('inf')
                tour = tour + [tour[0]]
                for i in range(len(tour) - 1):
                    added_distance = self.add(tour[i], tour[i+1], best)
                    if added_distance < min_distance:
                        min_index, min_distance = i, added_distance
                tour_length += self.add(tour[min_index], tour[min_index + 1], best)
                tours.append(tour)
                tour.insert(min_index + 1, best)
                tour = tour[:-1]
            tour_length += distances[tour[0]][tour[-1]]
            if tour_length < best_length:
                best_length, best_tour, best_tours = tour_length, tour, tours
        return [self.format_solution(step) for step in best_tours], best_length       
            
    def cheapest_insertion(self):
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
                length, tour = self.add_closest_to_tour(tour)
                tour_length += length
                tours.append(tour)
            if tour_length < best_length:
                best_length, best_tour, best_tours = tour_length, tour, tours
        return [self.format_solution(step) for step in best_tours], best_length        
    
    ## Local search: pairwise exchange (2-opt)
    
    # swap two edges
    def swap(self, solution, x, y):
        return solution[:x] + solution[x:y+1][::-1] + solution[y+1:]

    # main 2-opt algorithm
    def two_opt(self):
        solution = self.generate_solution()
        stable, best = False, self.compute_length(solution)
        while not stable:
            stable = True
            for i in range(1, len(solution) - 1):
                for j in range(i + 1, len(solution)):
                    candidate = self.swap(solution, i, j)
                    length_candidate = self.compute_length(candidate)
                    if best > length_candidate:
                        solution, best = candidate, length_candidate
                        stable = False
        return best, self.format_solution(solution)

                