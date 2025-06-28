import unittest

import commands.distro_list.action.edit_distros_list as edl
from commands.distro_list.utils.distro_list_enums import Action


class TestEditDistrosList(unittest.TestCase):
    def test_read_and_update_page_no_pageid(self):
        mock_tockdom_response = {"title": "Page Name"}
        mock_new_distros = {}
        self.assertRaises(RuntimeError, edl.read_and_update_page,
                          mock_tockdom_response, mock_new_distros, Action.ADD)

    def test_read_and_update_page_invalid_new_distros(self):
        mock_tockdom_response = {"pageid":"129"}
        mock_new_distros = {"Distro Name":"", "distro name":""}
        self.assertRaises(RuntimeError, edl.read_and_update_page,
                          mock_tockdom_response, mock_new_distros, Action.ADD)


if __name__ == '__main__':
    unittest.main()
