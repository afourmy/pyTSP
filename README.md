# Introduction

The travelling salesman problem (TSP) asks the following question: "Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city and returns to the origin city ?

pyTSP uses various approaches to solve the TSP (linear programming, construction heuristics, optimization heuristics, genetic algorithm).
It provides a geographical step-by-step visualization of each of these algorithms.

![eNMS](readme/pyTSP.gif)

**You can find a demo of pyTSP on a small graph made of all U.S cities with a population larger than 800 000 inhabitants. _[here](http://afourmy.pythonanywhere.com/)_ !**
- Find the city which insertion in the tour causes the smallest increase in length, i.e the city k which minimize d(i, k)  + d(k, j) - d(i, j) with (i, j) an edge in the (partial) tour.
- Insert k between i and j.
- Repeat until every city has been visited.
```

# Getting started

The following modules are used in pyTSP:
```
flask (web framework)
flask_sqlalchemy (database)
```

In order to use pyTSP, you need to:
    
- (optional) set up a virtual environment.
[Python official doc on virtual environments](https://docs.python.org/3/library/venv.html) 
    
- clone pyTSP (or download as a zip archive from github)
```
git clone https://github.com/afourmy/pyTSP.git
```
    
- install the requirements
```
cd pyTSP
pip install -r requirements.txt
```

- run **/flask_app.py**.
```
python flask_app.py
```

- go the http://127.0.0.1:5000/.

- create an account and log in.

# Contact

You can contact me at my personal email address:
```
''.join(map(chr, (97, 110, 116, 111, 105, 110, 101, 46, 102, 111, 
117, 114, 109, 121, 64, 103, 109, 97, 105, 108, 46, 99, 111, 109)))
```

or on the [Network to Code slack](http://networktocode.herokuapp.com "Network to Code slack"). (@minto, channel #enms)

# Credits

[Bootstrap](https://getbootstrap.com/ "Bootstrap"): Front-end HTML/CSS framework.

[Flask](http://flask.pocoo.org/ "Flask"): A microframework based on the Werkzeug toolkit and Jinja2 template engine.

[Flask SQLAlchemy](http://flask-sqlalchemy.pocoo.org/ "Flask SQLAlchemy"): Adds support for SQLAlchemy to Flask.

[Jquery](https://jquery.com/ "Jquery"): JavaScript library designed to simplify the client-side scripting of HTML.

[Leaflet](http://leafletjs.com/ "Leaflet"): JavaScript library for mobile-friendly interactive maps.