#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.__init__ import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.
        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        # Scan for general formatting - i.e '.', '(', ')'
        if '.' not in line or '(' not in line or ')' not in line:
            return line

        try:
            # Parse line left to right
            class_cmd, _, args = line.partition('.')
            cls, _, cmd_args = args.partition('(')
            cls = cls.strip()
            cmd_args = cmd_args.strip('()')
            if ',' in cmd_args:
                args_list = cmd_args.split(',')
                args_list = [a.strip() for a in args_list]
                cmd_args = ', '.join(args_list)
            line = f'{cls} {cmd_args}'
        except Exception:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        arg_list = args.split()
        class_name = arg_list[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        kwargs = {}
        for arg in arg_list[1:]:
            if '=' not in arg:
                print("** invalid argument format **")
                return
            key, value = arg.split('=')
            kwargs[key] = value.strip('"')
        new_instance = self.classes[class_name](**kwargs)
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        if not args:
            print("** class name missing **")
            return
        arg_list = args.split()
        if arg_list[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        obj_id = arg_list[1]
        obj_key = f"{arg_list[0]}.{obj_id}"
        if obj_key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[obj_key])

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        if not args:
            print("** class name missing **")
            return
        arg_list = args.split()
        if arg_list[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        obj_id = arg_list[1]
        obj_key = f"{arg_list[0]}.{obj_id}"
        if obj_key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[obj_key]
        storage.save()

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []
        if args:
            class_name = args.split()[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
                return
            for key, obj in storage.all(self.classes[class_name]).items():
                print_list.append(str(obj))
        else:
            for key, obj in storage.all().items():
                print_list.append(str(obj))
        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        if not args:
            print("** class name missing **")
            return
        class_name = args.strip()
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        count = sum(1 for k in storage.all() if k.startswith(class_name + "."))
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        if not args:
            print("** class name missing **")
            return
        arg_list = args.split()
        if arg_list[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        obj_id = arg_list[1]
        obj_key = f"{arg_list[0]}.{obj_id}"
        if obj_key not in storage.all():
            print("** no instance found **")
            return
        if len(arg_list) < 3:
            print("** attribute name missing **")
            return
        if len(arg_list) < 4:
            print("** value missing **")
            return
        attr_name = arg_list[2]
        attr_value = arg_list[3].strip('"')
        setattr(storage.all()[obj_key], attr_name, attr_value)
        storage.all()[obj_key].save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
