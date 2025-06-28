import unittest
import warnings

import commands.distro_list.utils.distros_list_create as dlc
from commands.distro_list.utils.distro_list_enums import Action


class TestDistroListCreate(unittest.TestCase):
    def test_validate_distros(self):
        mock_distros = {"Distro 1":"Value 1", "Distro 2": "Value 2"}
        is_valid = dlc.validate_distros(mock_distros)
        self.assertEqual(is_valid, True)

    def test_validate_distros_empty(self):
        mock_distros = {}
        is_valid = dlc.validate_distros(mock_distros)
        self.assertEqual(is_valid, True)

    def test_validate_distros_invalid(self):
        mock_distros = {"Distro 1":"Value 1", "distro 1": "Value 2"}
        with warnings.catch_warnings(record=True) as w:
            is_valid = dlc.validate_distros(mock_distros)
            self.assertEqual(is_valid, False)
            self.assertEqual(len(w), 1)

    def test_combine_distros_add(self):
        curr_distros = {"Distro 1a": "Value 1a", "Distro 2a": "Value 2a"}
        new_distros = {"Distro 1b": "Value 1b", "Distro 2b": "Value 2b"}
        expected_combined = {"Distro 1a": "Value 1a", "Distro 1b": "Value 1b",
                             "Distro 2a": "Value 2a", "Distro 2b": "Value 2b"}
        actual_combined = dlc.combine_distros(curr_distros, new_distros, Action.ADD)
        self.assertDictEqual(expected_combined, actual_combined)

    def test_combine_distros_add_duplicate(self):
        curr_distros = {"Distro 1a": "Value 1a", "Distro 2a": "Value 2a"}
        new_distros = {"Distro 1a": "Value 1a", "Distro 2b": "Value 2b"}
        expected_combined = {"Distro 1a": "Value 1a",
                             "Distro 2a": "Value 2a", "Distro 2b": "Value 2b"}
        with warnings.catch_warnings(record=True) as w:
            actual_combined = dlc.combine_distros(curr_distros, new_distros, Action.ADD)
            self.assertDictEqual(expected_combined, actual_combined)
            self.assertEqual(len(w), 1)

    def test_combine_distros_update(self):
        curr_distros = {"Distro 1a": "Value 1a", "Distro 2a": "Value 2a"}
        new_distros = {"Distro 1b": "Value 1b", "Distro 2b": "Value 2b"}
        expected_combined = {"Distro 1a": "Value 1a", "Distro 1b": "Value 1b",
                             "Distro 2a": "Value 2a", "Distro 2b": "Value 2b"}
        actual_combined = dlc.combine_distros(curr_distros, new_distros, Action.UPDATE)
        self.assertDictEqual(expected_combined, actual_combined)

    def test_combine_distros_update_duplicate(self):
        curr_distros = {"Distro 1a": "Value 1a", "Distro 2a": "Value 2a"}
        new_distros = {"Distro 1a": "Value 1b", "Distro 2b": "Value 2b"}
        expected_combined = {"Distro 1a": "Value 1b",
                             "Distro 2a": "Value 2a", "Distro 2b": "Value 2b"}
        actual_combined = dlc.combine_distros(curr_distros, new_distros, Action.UPDATE)
        self.assertDictEqual(expected_combined, actual_combined)

    def test_combine_distros_delete(self):
        curr_distros = {"Distro 1a": "Value 1a", "Distro 2a": "Value 2a"}
        new_distros = {"Distro 1a": "Value 1b"}
        actual_combined = dlc.combine_distros(curr_distros, new_distros, Action.DELETE)
        self.assertDictEqual(curr_distros, actual_combined)

    def test_combine_distros_delete_noduplicate(self):
        curr_distros = {"Distro 1a": "Value 1a", "Distro 2a": "Value 2a"}
        new_distros = {"Distro 1b": "Value 1b"}
        with warnings.catch_warnings(record=True) as w:
            actual_combined = dlc.combine_distros(curr_distros, new_distros, Action.DELETE)
            self.assertDictEqual(curr_distros, actual_combined)


if __name__ == '__main__':
    unittest.main()
