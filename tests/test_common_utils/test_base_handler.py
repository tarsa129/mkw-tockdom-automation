import unittest

from common_utils.base_handler import *

class BaseHandlerTest(unittest.TestCase):
    def test_create_argument_dict(self):
        argument = BaseHandlerActionArgument.create_new_arg(
            {"name": "argument name", "description": "argument desc"})
        self.assertEqual(argument.name, "argument name")
        self.assertIsNone(argument.value)
        self.assertEqual(argument.description, "argument desc")

    def test_create_argument_str(self):
        argument = BaseHandlerActionArgument.create_new_arg("arg name")
        self.assertEqual(argument.name, "arg name")
        self.assertIsNone(argument.value)
        self.assertIsNone(argument.description)

    def test_create_argument_value(self):
        argument = BaseHandlerActionArgument.create_new_arg(1)
        self.assertIsNone(argument.name)
        self.assertIsNone(argument.value, 1)
        self.assertIsNone(argument.description)

if __name__ == '__main__':
    unittest.main()
