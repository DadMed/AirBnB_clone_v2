#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """State class

    Attributes:
        __tablename__ (str): The table name.
        name (sqlalchemy String): The state name.
        cities (relationship): Relationship with City class.
    """
    __tablename__ = 'states'
    name = Column(String(128),
                  nullable=False)
    cities = relationship('City',
                          cascade='all, delete',
                          backref='state')
