import unittest

from common_utils.track_page_utils.wiiki_name_utils import identify_from_existing_page as td

class TestTrackDisambiguation(unittest.TestCase):
    def test_read_authors_one(self):
        page_name = "Ew Retro Track (notTarsa129)"
        expected_set = {"notTarsa129"}
        actual_set = td.read_authors(page_name)
        self.assertSetEqual(expected_set, actual_set)

    def test_read_authors_two(self):
        page_name = "Ew Retro Track (notTarsa129 & randouser)"
        expected_set = {"notTarsa129", "randouser"}
        actual_set = td.read_authors(page_name)
        self.assertSetEqual(expected_set, actual_set)

    def test_read_authors_three(self):
        page_name = "Ew Retro Track (notTarsa129, nottarsa & randouser)"
        expected_set = {"notTarsa129", "nottarsa", "randouser"}
        actual_set = td.read_authors(page_name)
        self.assertSetEqual(expected_set, actual_set)

    def test_read_authors_four(self):
        page_name = "Ew Retro Track (notTarsa129, nottarsa, stillnottarsa & randouser)"
        expected_set = {"notTarsa129", "nottarsa", "stillnottarsa", "randouser"}
        actual_set = td.read_authors(page_name)
        self.assertSetEqual(expected_set, actual_set)

if __name__ == '__main__':
    unittest.main()
