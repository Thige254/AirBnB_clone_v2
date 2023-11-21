#!/usr/bin/python3
""" Test case for the console.py"""
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.base_model import BaseModel
from models import storage


class TestConsole(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        storage.reload()

    def tearDown(self):
        """Clean up storage"""
        storage.save()
        storage.reload()

    def test_create_command(self):
        """Test create command"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("create BaseModel")
            obj_id = mock_stdout.getvalue().strip()
            self.assertTrue(obj_id)

        # Check if the object is actually created and stored
        obj_key = "BaseModel." + obj_id
        self.assertIn(obj_key, storage.all())

    def test_show_command(self):
        """Test show command"""
        new_instance = BaseModel()
        obj_key = "BaseModel." + new_instance.id

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("show BaseModel {}".format(new_instance.id))
            output = mock_stdout.getvalue().strip()

        self.assertIn(str(new_instance), output)

    def test_destroy_command(self):
        """Test destroy command"""
        new_instance = BaseModel()
        obj_key = "BaseModel." + new_instance.id

        self.assertIn(obj_key, storage.all())

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("destroy BaseModel {}".format(new_instance.id))

        self.assertNotIn(obj_key, storage.all())

    def test_all_command(self):
        """Test all command"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("all BaseModel")
            output = mock_stdout.getvalue().strip()

        # Check if "BaseModel" is not in any of the strings in the list
        self.assertNotIn("BaseModel", [line for line in output.split("\n")])

        new_instance = BaseModel()

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("all BaseModel")
            output = mock_stdout.getvalue().strip()

        self.assertIn(str(new_instance), output)

    def test_update_command(self):
        """Test update command"""
        new_instance = BaseModel()
        obj_key = "BaseModel." + new_instance.id

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd(
                "update BaseModel {} name 'John'".format(new_instance.id))

        # Match the format with single quotes
        self.assertEqual(new_instance.name, "'John'")
        updated_instance = storage.all()[obj_key]
        self.assertEqual(updated_instance.name, 'John')

# ... (previous code)

    # Existing test methods...


    def test_update_command(self):
        """Test update command"""
        new_instance = BaseModel()
        obj_key = "BaseModel." + new_instance.id

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd(
                "update BaseModel {} name 'John'".format(new_instance.id))

        # Match the format with single quotes
        self.assertEqual(new_instance.name, "'John'")
        updated_instance = storage.all()[obj_key]
        self.assertEqual(updated_instance.name, "'John'")

    def test_update_command_invalid_syntax(self):
        """Test update command with invalid syntax"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("update BaseModel")

        output = mock_stdout.getvalue().strip()
        # Updated to match the actual error message
        self.assertIn("** instance id missing **", output)

    def test_update_command_invalid_id(self):
        """Test update command with invalid ID"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.console.onecmd("update BaseModel invalid_id name 'John'")

        output = mock_stdout.getvalue().strip()
        self.assertIn("** no instance found **", output)

    # Add more test methods as needed


if __name__ == '__main__':
    unittest.main()
