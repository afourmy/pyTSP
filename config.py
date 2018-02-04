from os.path import abspath, dirname, join

basedir = abspath(dirname(__file__))
DEBUG = True
SECRET_KEY = 'key'

# SQL Alchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(basedir, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False