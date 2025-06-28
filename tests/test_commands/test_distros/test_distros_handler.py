import unittest
import warnings

import commands.distros.distros_handler as dh


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
        validation = dh.validate_distros(self.curr_distros)
        self.assertTrue(validation)

    def test_validate_distros_repeat_distroname(self):
        self.curr_distros["X Distro"] = "[[X Distro]]"
        self.curr_distros["y Distro"] = "[[y Distro]]"
        with warnings.catch_warnings(record=True) as w:
            validation = dh.validate_distros(self.curr_distros)
            self.assertEqual(len(w), 2)
            self.assertTrue(not validation)

    def test_combine_distros_add_noduplicate(self):
        action = dh.Action.ADD

        actual_distros = dh.combine_distros(self.curr_distros, self.new_distros, action)

        self.assertDictEqual(actual_distros, self.expected_distros)

    def test_combine_distros_add_duplicate(self):
        action = dh.Action.ADD
        self.new_distros["x Distro"] = "[[X Distro]]"

        with warnings.catch_warnings(record=True) as w:
            actual_distros = dh.combine_distros(self.curr_distros, self.new_distros, action)
            self.assertEqual(len(w), 1)
            self.assertDictEqual(actual_distros, self.expected_distros)

    def test_combine_distros_update_noduplicate(self):
        action = dh.Action.UPDATE
        actual_distros = dh.combine_distros(self.curr_distros, self.new_distros, action)
        self.assertDictEqual(actual_distros, self.expected_distros)


    def test_combine_distros_update_duplicate(self):
        action = dh.Action.UPDATE
        self.new_distros["x Distro"] = "[[X Distro]]"
        self.expected_distros["x Distro"] = "[[X Distro]]"

        actual_distros = dh.combine_distros(self.curr_distros, self.new_distros, action)

        self.assertDictEqual(actual_distros, self.expected_distros)

    def test_combine_distros_delete_noduplicate(self):
        action = dh.Action.DELETE
        self.expected_distros.pop("C Distro")

        with warnings.catch_warnings(record=True) as w:
            actual_distros = dh.combine_distros(self.curr_distros, self.new_distros, action)
            self.assertEqual(len(w), 1)
            self.assertDictEqual(actual_distros, self.expected_distros)

    def test_combine_distros_delete_duplicate(self):
        action = dh.Action.DELETE
        self.curr_distros["C Distro"] = "{{Distrib-ref|C Distro|129129|c-pack}}"
        self.expected_distros.pop("C Distro")

        actual_distros = dh.combine_distros(self.curr_distros, self.new_distros, action)

        self.assertDictEqual(actual_distros, self.expected_distros)

if __name__ == '__main__':
    unittest.main()