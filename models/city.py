i#!/usr/bin/python3
""" City Module for HBNB project """
import uuid
from models.base_model import BaseModel, Base
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from models import storage_type

class City(BaseModel, Base):
    """City class

    Attributes:
        __tablename__ (str): The table name.
        name (sqlalchemy String): The city name.
        state_id (sqlalchemy String): The state id.
    """
    __tablename__ = 'cities'
    name = Column(String(128),
                  nullable=False)
    state_id = Column(String(60),
                      ForeignKey('states.id'),
                      nullable=False)
