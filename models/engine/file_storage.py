#!/usr/bin/python3
"""This is the file storage class for AirBnB"""
import json
import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    __file_path = "file.json"
    __objects = {}

    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        if cls:
            return {key: obj for key, obj in self.__objects.items()
                    if isinstance(obj, cls)}
        else:
            return self.__objects

    def new(self, obj):
        """sets __object to given obj
        Args:
            obj: given object
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """serialize the file path to JSON file path
        """
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """deserialize the file path to JSON file path
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                json_dict = json.load(f)
                for key, value in json_dict.items():
                    class_name = value["__class__"]
                    if class_name in self.__classes:
                        self.__objects[key] = self.__classes[class_name](**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ delete an existing element
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]

    def close(self):
        """ calls reload()
        """
        self.reload()

