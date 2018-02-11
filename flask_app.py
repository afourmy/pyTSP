from threading import Lock
from flask import Flask, render_template, request, session
from flask_socketio import emit, SocketIO
from json import dumps, load
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
            if int(city_dict['population']) < 800000:
                continue
            city = City(**city_dict)
            db.session.add(city)
        try:
            db.session.commit()
        except sql_exception.IntegrityError:
            print('commit ok'*10)
            db.session.rollback()

def create_app(config='config'):
    app = Flask(__name__)
    app.config.from_object('config')
    configure_database(app)
    socketio = configure_socket(app)
    import_cities()
    return app, socketio

app, socketio = create_app()

from algorithms.genetic_algorithm import GeneticAlgorithm
from algorithms.linear_programming import LinearProgramming
from algorithms.local_optimization import LocalOptmizationHeuristics
from algorithms.tour_construction import TourConstructionHeuristics

ga = GeneticAlgorithm()
lp = LinearProgramming()
loh = LocalOptmizationHeuristics()
tch = TourConstructionHeuristics()

## Views

@app.route('/', methods = ['GET', 'POST'])
def algorithm():
    print(session)
    session['best'] = float('inf')
    view = request.form['view'] if 'view' in request.form else '2D'
    print(City.query.all())
    return render_template(
        'index.html',
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
    emit('build_tour', tch.nearest_neighbor())

@socketio.on('nearest_insertion')
def nearest_insertion():
    emit('build_tours', tch.nearest_insertion())

@socketio.on('cheapest_insertion')
def cheapest_insertion():
    emit('build_tours', tch.cheapest_insertion())

@socketio.on('pairwise_exchange')
def pairwise_exchange():
    emit('build_tours', loh.pairwise_exchange())

@socketio.on('lp')
def ilp_solver():
    emit('build_tour', lp.ILP_solver())

## Genetic algorithm

@socketio.on('genetic_algorithm')
def genetic_algorithm():
    if 'generation' not in session:
        session['generation'] = ga.create_first_generation()
    new_generation, best_individual, length = ga.cycle(session['generation'])
    session['generation'] = new_generation
    if length < session['best']:
        session['best'] = length
        emit('best_solution', (best_individual, length))
    else:
        emit('current_solution', (best_individual, length))

@app.route('/<method>', methods = ['POST'])
def selection(method):
    session[method] = request.form['value']
    return dumps({'success': True}), 200, {'ContentType': 'application/json'}

if __name__ == '__main__':
    socketio.run(
        app, 
        port = int(environ.get('PORT', 5100))
        )
