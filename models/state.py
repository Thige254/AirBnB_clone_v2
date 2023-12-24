#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.city import City
from models import storage


class State(BaseModel):
    """ State class """
    name = ""

    @property
    def cities(self):
        """ Getter attribute that returns the list of City instances """
        cities_list = []
        for city in storage.all(City).values():
            if city.state_id == self.id:
                cities_list.append(city)
        return cities_list
