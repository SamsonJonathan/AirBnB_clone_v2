#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from models import storage, storage_mode

place_amenity = Table('place_amenity',
                      Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False),
                      extend_existing=True)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer(), default=0, nullable=False)
    number_bathrooms = Column(Integer(), default=0, nullable=False)
    max_guest = Column(Integer(), default=0, nullable=False)
    price_by_night = Column(Integer(), default=0, nullable=False)
    latitude = Column(Float())
    longitude = Column(Float())
    amenity_ids = []

    if storage_mode():
        reviews = relationship('Review', backref='place',
                               cascade="all, delete")
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False, backref="place_amenities")
    else:
        def reviews(self):
            """Return all reviews for this place object"""
            revs = []
            [revs.append(item) for item in storage.all('Review')
                if item.place_id == self.id]
            return revs

        @property
        def amenities(self):
            """Return the list of amenities linked to this place"""
            am_list = []
            [am_list.append(item) for item in self.amenity_ids
                if item == self.id]
            return am_list

        @amenities.setter
        def amenities(self, obj):
            """Add the amenity object to the list of amenity ids"""
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
