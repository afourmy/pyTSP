from collections import defaultdict
from database import db
from json import load
from math import asin, cos, radians, sin, sqrt
from models import City
from os.path import join
from random import randrange, sample
from sqlalchemy import exc

class TravelingSalesmanProblem():
    
    def __init__(self, path):
        self.import_cities(path)
        self.compute_distances()
    
    ## Initialization
    
    # import data
    def import_cities(self, path):
        with open(join(path, 'data', 'cities.json')) as data:    
            for city_dict in load(data):
                if int(city_dict['population']) < 500000:
                    continue
                city = City(**city_dict)
                db.session.add(city)
            try:
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
    
    def compute_distances(self):
        cities = City.query.all()
        self.size = len(cities)
        self.distances = defaultdict(dict)
        for s in cities:
            for d in cities:
                self.distances[s][d] = self.haversine_distance(s, d)
                self.distances[d][s] = self.distances[s][d]

    # distances between cities
    def haversine_distance(self, s, d):
        coord = (s.longitude, s.latitude, d.longitude, d.latitude)
        # decimal degrees to radians conversion
        lon_s, lat_s, lon_d, lat_d = map(radians, coord)
        delta_lon = lon_d - lon_s 
        delta_lat = lat_d - lat_s 
        a = sin(delta_lat/2)**2 + cos(lat_s)*cos(lat_d)*sin(delta_lon/2)**2
        c = 2*asin(sqrt(a)) 
        # radius of earth: 6371 km
        return c*6371
    
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