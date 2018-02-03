from collections import defaultdict
from math import asin, cos, radians, sin, sqrt
from models import City
from random import sample

def haversine_distance(cityA, cityB):
    coords = (cityA.longitude, cityA.latitude, cityB.longitude, cityB.latitude)
    # we convert from decimal degree to radians
    lon_cityA, lat_cityA, lon_cityB, lat_cityB = map(radians, coords)
    delta_lon = lon_cityB - lon_cityA 
    delta_lat = lat_cityB - lat_cityA
    hav = lambda t: sin(t/2)**2
    a = hav(delta_lat) + cos(lat_cityA) * cos(lat_cityB) * hav(delta_lat)
    c = 2 * asin(sqrt(a)) 
    # radius of earth: 6371 km
    return c*6371

def compute_distances():
    cities = City.query.all()
    size = len(cities)
    distances = defaultdict(dict)
    for cityA in cities:
        for cityB in cities:
            if cityB not in distances[cityA]:
                distances[cityA][cityB] = haversine_distance(cityA, cityB)
                distances[cityB][cityA] = distances[cityA][cityB]

def generate_solution():
    cities = City.query.all()
    return sample(cities, len(cities))