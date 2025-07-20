import unittest

from common_utils.track_page_utils.wiiki_name_utils import match_page_to_track as mpt
from common_utils.track_page_utils.wiiki_name_utils.match_page_to_track import TrackPageName


class MyTestCase(unittest.TestCase):
    def test_get_parenthesis_groups(self):
        self.assertEqual(["(Temple Edit)"], mpt.get_parenthesis_groups("(Temple Edit)"))
        self.assertEqual(["(Temple Edit)", "(LucioWins)"], mpt.get_parenthesis_groups("(Temple Edit) (LucioWins)"), )
        self.assertEqual(["(Temple Edit)", "(tarsa129 (&) LucioWins)"], mpt.get_parenthesis_groups("(Temple Edit) (tarsa129 (&) LucioWins)"), )

    def test_read_parenthetical_groups(self):
        mod_type, authors = mpt.read_parenthetical_groups("(Temple Edit)")
        self.assertEqual(("Edit", None), (mod_type, authors))
        mod_type, authors = mpt.read_parenthetical_groups("(Temple Edit) (LucioWins)")
        self.assertEqual(("Edit", {"LucioWins"}), (mod_type, authors))
        mod_type, authors = mpt.read_parenthetical_groups("(LucioWins)")
        self.assertEqual((None, {"LucioWins"}), (mod_type, authors))

    def test_parse_page_name(self):
        expected_track = TrackPageName("Track (Track Edit)", "Track", "Edit", None)
        actual_track = mpt.parse_page_name("Track (Track Edit)", "Track")
        self.assertEqual(expected_track, actual_track)

        expected_track = TrackPageName("Track (tarsa129 & Lucio)", "Track", None, {"tarsa129", "Lucio"})
        actual_track = mpt.parse_page_name("Track (tarsa129 & Lucio)", "Track")
        self.assertEqual(expected_track, actual_track)

        expected_track = TrackPageName("SNES Ghost Valley 2 HD (SNES Ghost Valley 2 Texture) (MRAP12)",
                                       "SNES Ghost Valley 2 HD", "Texture", {"MRAP12"})
        actual_track = mpt.parse_page_name("SNES Ghost Valley 2 HD (SNES Ghost Valley 2 Texture) (MRAP12)",
                                       "SNES Ghost Valley 2 HD")
        self.assertEqual(expected_track, actual_track)

        expected_track = TrackPageName("Track (Track Edit) (tarsa129)", "Track", "Edit", {"tarsa129"})
        actual_track = mpt.parse_page_name("Track (Track Edit) (tarsa129)", "Track")
        self.assertEqual(expected_track, actual_track)

    def test_parse_page_name_missing(self):
        actual_track = mpt.parse_page_name("Epic Track (Track Edit) (tarsa129)", "Track")
        self.assertIsNone(actual_track)

if __name__ == '__main__':
    unittest.main()
