from .base_algorithm import *
from operator import itemgetter


class TourConstructionHeuristics(BaseAlgorithm):

    # find the closest neighbor (or the farthest) to a given node in the tour
    # or not yet visited (default)
    # returns the neighbor as well as the distance between the two
    def closest_neighbor(self, tour, node, in_tour=False, farthest=False):
        neighbors = distances[node]
        current_dist = [(c, d) for c, d in neighbors.items()
                        if (c in tour if in_tour else c not in tour)]
        return sorted(current_dist, key=itemgetter(1))[-farthest]

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
        best_tour, best_length, best_lengths = None, float('inf'), []
        for city in cities:
            current, tour, tour_length, tour_lengths = city, [city], 0, []
            while len(tour) != len(cities):
                arg_min, edge_length = self.closest_neighbor(tour, current)
                tour_length += edge_length
                tour_lengths.append(tour_length)
                tour.append(arg_min)
                current = arg_min
            # we close the tour by adding the last edge length
            tour_length += distances[current][city]
            tour_lengths.append(tour_length)
            if tour_length < best_length:
                best_length, best_lengths, best_tour = tour_length, tour_lengths, tour
        intermediate_steps = [[]]
        for point in self.format_solution(best_tour):
            intermediate_steps.append(intermediate_steps[-1] + [point])
        return intermediate_steps[2:], best_lengths

    def nearest_insertion(self, farthest=False):
        best_length, best_tours = float('inf'), []
        for city in cities:
            # we start the tour with one node I
            tour, tours, tour_lengths = [city], [], []
            # we find the closest node R to the first node
            neighbor, length = self.closest_neighbor(tour, city, False, farthest)
            tour.append(neighbor)
            tour_length = length
            tour_lengths.append(tour_length)
            while len(tour) != len(cities):
                best, min_distance = None, 0 if farthest else float('inf')
                # (selection step) given a sub-tour,we find node r not in the
                # sub-tour closest to any node j in the sub-tour,
                # i.e. with minimal c_rj
                for candidate in cities:
                    if candidate in tour:
                        continue
                    # we consider only the distances to nodes already in the tour
                    _, length = self.closest_neighbor(tour, candidate, True, farthest)
                    if (length > min_distance if farthest else length < min_distance):
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
                tour_lengths.append(tour_length)
                tours.append(tour)
                tour.insert(min_index + 1, best)
                tour = tour[:-1]
            tour_length += distances[tour[0]][tour[-1]]
            tour_lengths.append(tour_length)
            if tour_length < best_length:
                best_length, best_tours = tour_length, tours
                best_lengths = tour_lengths
        best_lengths = best_lengths[2:]
        return [self.format_solution(step) for step in best_tours], best_lengths

    def farthest_insertion(self):
        return self.nearest_insertion(farthest=True)

    def cheapest_insertion(self):
        best_tour, best_length = None, float('inf')
        # store intermediate tours for visualization purposes
        best_tours, best_lengths = [], []
        for city in cities:
            # we start the tour with one node I
            tour, tours, tour_lengths = [city], [], []
            # we find the closest node R to the first node
            neighbor, length = self.closest_neighbor(tour, city)
            tour_length = length
            tour_lengths.append(length)
            tour.append(neighbor)
            while len(tour) != len(cities):
                length, tour = self.add_closest_to_tour(tour)
                tour_length += length
                tours.append(tour)
                tour_lengths.append(tour_length)
            tour_length += distances[tour[-1]][tour[0]]
            tour_lengths.append(tour_length)
            if tour_length < best_length:
                best_lengths, best_tour, best_tours = tour_lengths, tour, tours
        best_lengths = [sum(best_lengths[:3])] + best_lengths[3:]
        return [self.format_solution(step) for step in best_tours], best_lengths
