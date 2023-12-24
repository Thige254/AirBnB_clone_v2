#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """This class manages storage of hbnb models using SQLAlchemy"""
    __engine = None
    __session = None

    def __init__(self):
        """Creates a new instance of DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries current database session based on class name"""
        query_dict = {}
        if cls is not None:
            result = self.__session.query(cls).all()
            for obj in result:
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                query_dict[key] = obj
        else:
            for cls in [State, City, User, Place, Amenity, Review]:
                result = self.__session.query(cls).all()
                for obj in result:
                    key = '{}.{}'.format(type(obj).__name__, obj.id)
                    query_dict[key] = obj
        return query_dict

    def new(self, obj):
        """Adds object to current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commits all changes of current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and initializes a session"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """Calls remove() method on the private session attribute"""
        self.__session.close()
