from collections import defaultdict
from math import asin, cos, radians, sin, sqrt
from models import City
from random import sample


class BaseAlgorithm():

    def __init__(self):
        self.update_data()

    def update_data(self):
        self.cities = [c.id for c in City.query.all()]
        self.size = len(self.cities)
        self.coords = {c.id: (c.latitude, c.longitude) for c in City.query.all()}
        self.distances = self.compute_distances()

    def hav(self, angle):
        return sin(angle / 2)**2

    def haversine_distance(self, cityA, cityB):
        coords = (*self.coords[cityA], *self.coords[cityB])
        # we convert from decimal degree to radians
        lat_cityA, lon_cityA, lat_cityB, lon_cityB = map(radians, coords)
        delta_lon = lon_cityB - lon_cityA
        delta_lat = lat_cityB - lat_cityA
        a = self.hav(delta_lat) + cos(lat_cityA) * cos(lat_cityB) * self.hav(delta_lon)
        c = 2 * asin(sqrt(a))
        # approximate radius of the Earth: 6371 km
        return c * 6371

    def compute_distances(self):
        self.distances = defaultdict(dict)
        for cityA in self.cities:
            for cityB in self.cities:
                if cityB not in self.distances[cityA]:
                    distance = self.haversine_distance(cityA, cityB)
                    self.distances[cityA][cityB] = distance
                    self.distances[cityB][cityA] = distance
        return self.distances

    # add node k between node i and node j
    def add(self, i, j, k):
        return self.distances[i][k] + self.distances[k][j] - self.distances[i][j]

    def generate_solution(self):
        return sample(self.cities, len(self.cities))

    # computes the total geographical length of a solution
    def compute_length(self, solution):
        total_length = 0
        for i in range(len(solution)):
            length = self.distances[solution[i]][solution[(i + 1) % len(solution)]]
            total_length += length
        return total_length

    def format_solution(self, solution):
        solution = solution + [solution[0]]
        return [self.coords[city] for city in solution]
