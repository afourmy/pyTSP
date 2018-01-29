from collections import defaultdict
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
from json import load
from math import asin, cos, radians, sin, sqrt
import random
from os import environ
from os.path import abspath, dirname, join, pardir
import sys

# prevent python from writing *.pyc files / __pycache__ folders
sys.dont_write_bytecode = True

path_app = dirname(abspath(__file__))
if path_app not in sys.path:
    sys.path.append(path_app)

from database import db, create_database
from models import City

def configure_database(app):
    create_database()
    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def import_cities(path):
    with open(join(path, 'data', 'cities.json')) as data:    
        for city_dict in load(data):
            if int(city_dict['population']) < 500000:
                continue
            city = City(**city_dict)
            db.session.add(city)
        db.session.commit()


## distances between cities

def haversine_distance(s, d):
    coord = (s.longitude, s.latitude, d.longitude, d.latitude)
    # decimal degrees to radians conversion
    lon_s, lat_s, lon_d, lat_d = map(radians, coord)
    delta_lon = lon_d - lon_s 
    delta_lat = lat_d - lat_s 
    a = sin(delta_lat/2)**2 + cos(lat_s)*cos(lat_d)*sin(delta_lon/2)**2
    c = 2*asin(sqrt(a)) 
    # radius of earth: 6371 km
    return c*6371
    
def distances_matrix():
    cities = City.query.all()
    size = range(len(cities))
    dist = defaultdict(dict)
    for s in cities:
        for d in cities:
            dist[s][d] = dist[d][s] = haversine_distance(s, d)
    return dist

def fitness(dist, solution):
    total_length = 0
    for i in range(len(solution)):
        total_length += dist[solution[i]][solution[(i+1)%len(solution)]]
    return total_length
    
## Mutation methods

def random_swap(solution):
    i, j = random.randrange(len(solution)), random.randrange(len(solution))
    solution[i], solution[j] = solution[j], solution[i]
    
def two_opt(dist, solution):
    stable = False
    while not stable:
        stable = True
        edges = zip(solution, solution[1:] + [solution[0]])
        for edgeA in edges:
            for edgeB in edges:
                (a, b), (c, d) = edgeA, edgeB
                ab, cd = dist[a][b], dist[c][d]
                ac, bd = dist[a][c], dist[b][d]
                if ab + cd > ac + bd:
                    for index, city in enumerate(solution):
                        if city in (b, c):
                            solution[index] = c if city == b else b
                        stable = False
    return solution

def create_app(config='config'):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    
    configure_database(app)
    import_cities(path_app)
    distances = distances_matrix()
        
    async_mode = None
    socketio = SocketIO(app, async_mode=async_mode)
    thread = None
    thread_lock = Lock()
    
    return app, socketio, distances

app, socketio, distances = create_app()

@app.route('/')
def index():
    session['best'] = float('inf')
    return render_template(
        'index.html',
        minimum_population = 500000,
        cities = {
            city.id: {
                property: getattr(city, property)
                for property in City.properties
                }
            for city in City.query.all()
            },
        async_mode = socketio.async_mode
        )

@socketio.on('send_random')
def emit_random():
    cities = list(distances)
    sample = random.sample(cities, len(cities))
    solution = two_opt(distances, sample)
    fitness_value = fitness(distances, solution)
    solution = [(city.latitude, city.longitude) for city in solution]
    print(solution)
    if fitness_value < session['best']:
        print(str(fitness_value)*100)
        session['best'] = fitness_value
        emit('best_solution', solution + [solution[0]])
    else:
        emit('current_solution', solution + [solution[0]])

# @socketio.on('send_random')
# def emit_random():
#     emit('my_random_number', random.randint(1, 10))

if __name__ == '__main__':
    socketio.run(
        app, 
        port = int(environ.get('PORT', 5100)),
        debug = False
        )
