from database import Base
from sqlalchemy import Column, Integer, String, Float


class City(Base):

    __tablename__ = 'City'
    properties = ('name', 'population', 'longitude', 'latitude')

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    longitude = Column(Float)
    latitude = Column(Float)
    population = Column(Integer)

    def __init__(self, **data):
        self.name = data['city']
        self.longitude = data['longitude']
        self.latitude = data['latitude']
        self.population = data.get('population', 0)

    def __repr__(self):
        return self.name
