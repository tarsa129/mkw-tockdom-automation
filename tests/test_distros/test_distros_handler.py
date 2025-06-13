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

    def test_combine_distros_add_noduplicate(self):
        action = dh.Action.ADD

        actual_distros = dh.combine_distros(self.curr_distros, self.new_distros, action)

        expected_distros = {
            "A Distro": "[[A Distro]]",
            "C Distro": "{{Distrib-ref|C Distro|129129|c-pack}}",
            "x Distro": "{{Distrib-ref|X Distro|129129|x-pack}}",
            "Y Distro": "[[Y Distro]] (v1.1)"
        }

        self.assertDictEqual(actual_distros, expected_distros)

    def test_combine_distros_add_duplicate(self):
        action = dh.Action.ADD
        self.new_distros["x Distro"] = "[[X Distro]]"

        with warnings.catch_warnings(record=True) as w:
            actual_distros = dh.combine_distros(self.curr_distros, self.new_distros, action)
            self.assertEqual(len(w), 1)

            expected_distros = {
                "A Distro": "[[A Distro]]",
                "C Distro":  "{{Distrib-ref|C Distro|129129|c-pack}}",
                "x Distro": "{{Distrib-ref|X Distro|129129|x-pack}}",
                "Y Distro": "[[Y Distro]] (v1.1)"
            }

            self.assertDictEqual(actual_distros, expected_distros)


if __name__ == '__main__':
    unittest.main()