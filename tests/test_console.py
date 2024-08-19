#!/usr/bin/env python3
"""Unit tests for console.py"""

import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel


class TestHBNBCommand(unittest.TestCase):
    """Test cases for HBNBCommand class"""

    def setUp(self):
        """Set up test environment"""
        self.cli = HBNBCommand()
        # Clear storage before each test
        storage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up after each test"""
        storage._FileStorage__objects = {}

    def test_quit(self):
        """Test quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.cli.onecmd("quit"))

    def test_EOF(self):
        """Test EOF command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.cli.onecmd("EOF"))

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("\n")
            self.assertEqual(f.getvalue(), "")

    def test_create(self):
        """Test create command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create BaseModel")
            self.assertRegex(f.getvalue(), r'^[0-9a-f-]{36}\n$')

    def test_create_missing_class(self):
        """Test create command with missing class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create")
            self.assertEqual(f.getvalue(), "** class name missing **\n")

    def test_create_invalid_class(self):
        """Test create command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create MyModel")
            self.assertEqual(f.getvalue(), "** class doesn't exist **\n")

    def test_show(self):
        """Test show command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create BaseModel")
            model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd(f"show BaseModel {model_id}")
            self.assertIn(model_id, f.getvalue())

    def test_show_missing_class(self):
        """Test show command with missing class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show")
            self.assertEqual(f.getvalue(), "** class name missing **\n")

    def test_show_invalid_class(self):
        """Test show command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show MyModel")
            self.assertEqual(f.getvalue(), "** class doesn't exist **\n")

    def test_show_missing_id(self):
        """Test show command with missing id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show BaseModel")
            self.assertEqual(f.getvalue(), "** instance id missing **\n")

    def test_show_invalid_id(self):
        """Test show command with invalid id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show BaseModel 121212")
            self.assertEqual(f.getvalue(), "** no instance found **\n")

    def test_destroy(self):
        """Test destroy command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create BaseModel")
            model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd(f"destroy BaseModel {model_id}")
            self.assertEqual(f.getvalue(), "")
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd(f"show BaseModel {model_id}")
            self.assertEqual(f.getvalue(), "** no instance found **\n")

    def test_all(self):
        """Test all command"""
        self.cli.onecmd("create BaseModel")
        self.cli.onecmd("create BaseModel")
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("all")
            self.assertIn("BaseModel", f.getvalue())

    def test_all_invalid_class(self):
        """Test all command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("all MyModel")
            self.assertEqual(f.getvalue(), "** class doesn't exist **\n")

    def test_update(self):
        """Test update command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create BaseModel")
            model_id = f.getvalue().strip()
        self.cli.onecmd(f'update BaseModel {model_id} name "test"')
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd(f"show BaseModel {model_id}")
            self.assertIn("test", f.getvalue())

    def test_update_missing_class(self):
        """Test update command with missing class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("update")
            self.assertEqual(f.getvalue(), "** class name missing **\n")

    def test_update_invalid_class(self):
        """Test update command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("update MyModel")
            self.assertEqual(f.getvalue(), "** class doesn't exist **\n")

    def test_update_missing_id(self):
        """Test update command with missing id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("update BaseModel")
            self.assertEqual(f.getvalue(), "** instance id missing **\n")

    def test_update_invalid_id(self):
        """Test update command with invalid id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("update BaseModel 121212")
            self.assertEqual(f.getvalue(), "** no instance found **\n")

    def test_update_missing_attribute(self):
        """Test update command with missing attribute name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create BaseModel")
            model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd(f"update BaseModel {model_id}")
            self.assertEqual(f.getvalue(), "** attribute name missing **\n")

    def test_update_missing_value(self):
        """Test update command with missing value"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create BaseModel")
            model_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd(f"update BaseModel {model_id} name")
            self.assertEqual(f.getvalue(), "** value missing **\n")


if __name__ == "__main__":
    unittest.main()
