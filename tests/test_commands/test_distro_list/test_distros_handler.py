import unittest
import warnings

import commands.distro_list.action.edit_distros_list
import commands.distro_list.distro_list_handler as dh
from commands.distro_list.utils.distro_list_enums import Action
import commands.distro_list.utils.distros_list_create


class TestDistroHandler(unittest.TestCase):
    def setUp(self):
        self.curr_distros = {
            "A Distro": "[[A Distro]]",
            "x Distro": "{{Distrib-ref|X Distro|129129|x-pack}}",
            "Y Distro": "[[Y Distro]] (v1.1)"
        }
        self.new_distros = {
            "C Distro":  "{{Distrib-ref|C Distro|129129|c-pack}}",
        }

        self.expected_distros = {
            "A Distro": "[[A Distro]]",
            "C Distro": "{{Distrib-ref|C Distro|129129|c-pack}}",
            "x Distro": "{{Distrib-ref|X Distro|129129|x-pack}}",
            "Y Distro": "[[Y Distro]] (v1.1)"
        }

    def test_validate_distros_normal(self):
        validation = commands.distro_list.utils.distros_list_create.validate_distros(self.curr_distros)
        self.assertTrue(validation)

    def test_validate_distros_repeat_distroname(self):
        self.curr_distros["X Distro"] = "[[X Distro]]"
        self.curr_distros["y Distro"] = "[[y Distro]]"
        with warnings.catch_warnings(record=True) as w:
            validation = commands.distro_list.utils.distros_list_create.validate_distros(self.curr_distros)
            self.assertEqual(len(w), 2)
            self.assertTrue(not validation)

    def test_combine_distros_add_noduplicate(self):
        action = Action.ADD
        actual_distros = commands.distro_list.utils.distros_list_create.combine_distros(self.curr_distros, self.new_distros, action)

        self.assertDictEqual(actual_distros, self.expected_distros)

    def test_combine_distros_add_duplicate(self):
        action = Action.ADD
        self.new_distros["x Distro"] = "[[X Distro]]"

        with warnings.catch_warnings(record=True) as w:
            actual_distros = commands.distro_list.utils.distros_list_create.combine_distros(self.curr_distros, self.new_distros, action)
            self.assertEqual(len(w), 1)
            self.assertDictEqual(actual_distros, self.expected_distros)

    def test_combine_distros_update_noduplicate(self):
        action = Action.UPDATE
        actual_distros = commands.distro_list.utils.distros_list_create.combine_distros(self.curr_distros, self.new_distros, action)
        self.assertDictEqual(actual_distros, self.expected_distros)


    def test_combine_distros_update_duplicate(self):
        action = Action.UPDATE
        self.new_distros["x Distro"] = "[[X Distro]]"
        self.expected_distros["x Distro"] = "[[X Distro]]"

        actual_distros = commands.distro_list.utils.distros_list_create.combine_distros(self.curr_distros, self.new_distros, action)

        self.assertDictEqual(actual_distros, self.expected_distros)

    def test_combine_distros_delete_noduplicate(self):
        action = Action.DELETE
        self.expected_distros.pop("C Distro")

        with warnings.catch_warnings(record=True) as w:
            actual_distros = commands.distro_list.utils.distros_list_create.combine_distros(self.curr_distros, self.new_distros, action)
            self.assertEqual(len(w), 1)
            self.assertDictEqual(actual_distros, self.expected_distros)

    def test_combine_distros_delete_duplicate(self):
        action = Action.DELETE
        self.curr_distros["C Distro"] = "{{Distrib-ref|C Distro|129129|c-pack}}"
        self.expected_distros.pop("C Distro")

        actual_distros = commands.distro_list.utils.distros_list_create.combine_distros(self.curr_distros, self.new_distros, action)

        self.assertDictEqual(actual_distros, self.expected_distros)

if __name__ == '__main__':
    unittest.main()