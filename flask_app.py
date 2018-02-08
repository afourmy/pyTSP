from threading import Lock
from flask import Flask, render_template, request, session
from flask_socketio import emit, SocketIO
from json import load
from os import environ
from os.path import abspath, dirname, join
from sqlalchemy import exc as sql_exception
from sys import dont_write_bytecode, path

# prevent python from writing *.pyc files / __pycache__ folders
dont_write_bytecode = True

path_app = dirname(abspath(__file__))
if path_app not in path:
    path.append(path_app)

from database import db, create_database
from models import City

def configure_database(app):
    create_database()
    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()
    db.init_app(app)

def configure_socket(app):
    async_mode, thread = None, None
    socketio = SocketIO(app, async_mode=async_mode)
    thread_lock = Lock()
    return socketio
    
# import data
def import_cities():
    with open(join(path_app, 'data', 'cities.json')) as data:    
        for city_dict in load(data):
            if int(city_dict['population']) < 500000:
                continue
            city = City(**city_dict)
            db.session.add(city)
        try:
            db.session.commit()
        except sql_exception.IntegrityError:
            db.session.rollback()

def create_app(config='config'):
    app = Flask(__name__)
    app.config.from_object('config')
    configure_database(app)
    socketio = configure_socket(app)
    import_cities()
    return app, socketio

app, socketio = create_app()

from genetic_algorithm import GeneticAlgorithm
from tour_construction import TourConstruction
from optimization_algorithm import OptimizationAlgorithm

ga = GeneticAlgorithm()
tc = TourConstruction()
oa = OptimizationAlgorithm()

## Views

@app.route('/', methods = ['GET', 'POST'])
def algorithm():
    session['best'] = float('inf')
    view = request.form['view'] if 'view' in request.form else '2D'
    print(request.form)
    return render_template(
        'index.html',
        minimum_population = 500000,
        view = view,
        cities = {
            city.id: {
                property: getattr(city, property)
                for property in City.properties
                }
            for city in City.query.all()
            },
        async_mode = socketio.async_mode
        )

@socketio.on('nearest_neighbor')
def nearest_neighbor():
    emit('build_tour', tc.nearest_neighbor())

@socketio.on('nearest_insertion')
def nearest_insertion():
    emit('build_tours', tc.nearest_insertion())

def optimization(function):
    length, solution = getattr(oa, function)()
    if length < session['best']:
        session['best'] = length
        emit('best_solution', (solution, length))
    else:
        emit('current_solution', (solution, length))
    
@socketio.on('2opt')
def two_opt():
    optimization('two_opt')

@socketio.on('3opt')
def three_opt():
    optimization('three_opt')

@socketio.on('genetic_algorithm')
def genetic_algorithm():
    fitness_value, solution = genetic_algorithm.cycle()
    if fitness_value < session['best']:
        session['best'] = fitness_value
        emit('best_solution', solution)
    else:
        emit('current_solution', solution)

if __name__ == '__main__':
    socketio.run(
        app, 
        port = int(environ.get('PORT', 5100))
        )
