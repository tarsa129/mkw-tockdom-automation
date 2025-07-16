import unittest

from common_utils.track_page_utils.wiiki_name_utils import track_disambiguation as td

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

    def get_page_from_name_authors(self):
        # Probably not good practice to not mock external API calls in unit tests.
        # This is why the name has been altered to NOT run as part of the test suite
        # You can reenable it by editing the method name to have "test_" in front.

        #test not a disambiguation
        toads_temple = td.get_page_from_name_authors("Toad's Temple", {"LucioWins"})
        self.assertEqual("Toad's Temple", toads_temple)

        #test simple retro
        snes_mc1_zpl = td.get_page_from_name_authors("SNES Mario Circuit 1", {"ZPL"})
        self.assertEqual("SNES Mario Circuit 1 (ZPL)", snes_mc1_zpl)

        #test version that does not exist, given the author
        wicked_woods_kh = td.get_page_from_name_authors("Wicked Woods", {"The Bad Kevin"})
        self.assertIsNone(wicked_woods_kh)

if __name__ == '__main__':
    unittest.main()
