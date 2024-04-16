import unittest
from unittest.mock import patch
from io import StringIO

class TestHBNBCommand(unittest.TestCase):
    def setUp(self):
        self.console = HBNBCommand()

    def test_create_with_string_param(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("create BaseModel name=\"My_little_house\"")
            created_id = fake_out.getvalue().strip()
            self.assertIsNotNone(created_id)

    def test_create_with_float_param(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("create BaseModel score=4.5")
            created_id = fake_out.getvalue().strip()
            self.assertIsNotNone(created_id)

    def test_create_with_int_param(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("create BaseModel quantity=10")
            created_id = fake_out.getvalue().strip()
            self.assertIsNotNone(created_id)

    def test_create_invalid_param(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("create BaseModel invalid_param")
            output = fake_out.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

if __name__ == '__main__':
    unittest.main()

