#!/usr/bin/env python3
"""
This module contains the entry point of the command interpreter.
"""

import cmd
import json
from models import storage
from models.base_model import BaseModel

class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class for the command interpreter.
    """

    prompt = "(hbnb) "
    valid_classes = ["BaseModel"]  # Add other classes as needed

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it and prints the id"""
        if not arg:
            print("** class name missing **")
            return
        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        objs = storage.all()
        if not arg:
            print([str(objs[obj]) for obj in objs])
            return
        if arg not in self.valid_classes:
            print("** class doesn't exist **")
            return
        print([str(objs[obj]) for obj in objs if obj.startswith(arg)])

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        obj = storage.all()[key]
        attr_name = args[2]
        attr_value = args[3].strip('"')
        setattr(obj, attr_name, attr_value)
        obj.save()

    def help_create(self):
        """Help message for create command"""
        print("Creates a new instance of BaseModel, saves it and prints the id")
        print("Usage: create <class name>")

    def help_show(self):
        """Help message for show command"""
        print("Prints the string representation of an instance")
        print("Usage: show <class name> <id>")

    def help_destroy(self):
        """Help message for destroy command"""
        print("Deletes an instance based on the class name and id")
        print("Usage: destroy <class name> <id>")

    def help_all(self):
        """Help message for all command"""
        print("Prints all string representation of all instances")
        print("Usage: all [<class name>]")

    def help_update(self):
        """Help message for update command"""
        print("Updates an instance based on the class name and id")
        print("Usage: update <class name> <id> <attribute name> \"<attribute value>\"")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
