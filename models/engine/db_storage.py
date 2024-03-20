#!/usr/bin/python3
""" DB storage module """

import models
from models.base_model import Base
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session



classes = {"State": State, "City": City, "User": User,
           "Place": Place, "Review": Review, "Amenity": Amenity}


class DBStorage:
    """ DBStorage class """
    __engine = None
    __session = None

    def __init__(self):
        """initialization"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        test_env = getenv("HBNB_ENV", "none")

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
                                     user, pwd, host, db), pool_pre_ping=True)

        if test_env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current sessionobjects depending on class name"""
        """obj_dict = {}

        if cls:
            objs = self.__session.query(models.classes[cls]).all()
            for obj in objs:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                obj_dict[key] = obj
        else:
            for key, value in models.classes.items():
                if not isinstance(value, type(BaseModel)):
                    objs = self.__session.query(value).all()
                    for obj in objs:
                        key = "{}.{}".format(obj.__class__.__name__, obj.id)
                        obj_dict[key] = obj
        return obj_dict"""
        dbobjects = {}
        if cls:
            if type(cls) is str and cls in classes:
                for obj in self.__session.query(classes[cls]).all():
                    key = str(obj.__class__.__name__) + "." + str(obj.id)
                    val = obj
                    dbobjects[key] = val
            elif cls.__name__ in classes:
                for obj in self.__session.query(cls).all():
                    key = str(obj.__class__.__name__) + "." + str(obj.id)
                    val = obj
                    dbobjects[key] = val
        else:
            for k, v in classes.items():
                for obj in self.__session.query(v).all():
                    key = str(v.__name__) + "." + str(obj.id)
                    val = obj
                    dbobjects[key] = val
        return dbobjects

    def new(self, obj):
        """Add the obj to the current db session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current db session of obj is not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """creates all tables in the db"""
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        """ Close and reload session """
        self.__session.close()
