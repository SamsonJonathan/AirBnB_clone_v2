#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", back_populates="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            """returns list of cities where state_id ==current State.id"""
            from models import storage
            from models.city import City

            all_cities = storage.all(City)
            cities = []

            for city in all_cities.values():
                if city.state_id == self.id:
                    cities.append(city)
            return cities
