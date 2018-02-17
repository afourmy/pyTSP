from database import Base
from sqlalchemy import Column, Integer, String, Float


class City(Base):

    __tablename__ = 'City'
    properties = ('id', 'name', 'longitude', 'latitude', 'population')

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    longitude = Column(Float)
    latitude = Column(Float)
    population = Column(Integer)

    def __init__(self, **data):
        self.name = data['city']
        self.longitude = data['longitude']
        self.latitude = data['latitude']
        self.population = data['population']

    def __repr__(self):
        return self.name
