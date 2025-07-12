import unittest

from commands.miscinfo.action import get_ids_from_szslibrary as gifs
from commands.miscinfo.utils.wbz_id_process import WBZInfo


class TestGetIdsFromSzslibrary(unittest.TestCase):
    def setUp(self):
        self.wbz_entries = []
        self.wbz_entries.append(WBZInfo(1, 1, 1, "Track 1", "v1.0", None, "hash1"))
        self.wbz_entries.append(WBZInfo(2, 4, 2, "Track 2", "v1.0", None,"hash2"))
        self.wbz_entries.append(WBZInfo(3, 3, 3, "Track 3", "v1.0", None, None))

    def test_remove_unnecessary_entries_all_keep(self):
        actual_entries = gifs.remove_unnecessary_entries(self.wbz_entries)
        self.assertListEqual(actual_entries, self.wbz_entries)

    def test_remove_unnecessary_entries_remove_duplicate_update(self):
        self.wbz_entries.append(WBZInfo(1, 4, 1, "Track 1", "v1.1", None, "hash1"))
        actual_entries = gifs.remove_unnecessary_entries(self.wbz_entries)
        self.assertEqual(len(actual_entries), 3)
        wbz_id_1_entries = [e for e in actual_entries if e.wbz_id == 1]
        self.assertEqual(len(wbz_id_1_entries), 1)
        self.assertEqual(wbz_id_1_entries[0].image_id, 1)

    def test_remove_unnecessary_entries_keep_image_update(self):
        self.wbz_entries.append(WBZInfo(1, 4, 1, "Track 1", "v1.1", None, "hash4"))
        actual_entries = gifs.remove_unnecessary_entries(self.wbz_entries)
        self.assertEqual(len(actual_entries), 3)
        wbz_id_1_entries = [e for e in actual_entries if e.wbz_id == 1]
        self.assertEqual(len(wbz_id_1_entries), 1)
        self.assertEqual(wbz_id_1_entries[0].image_id, 4)

    def test_remove_unnecessary_entries_keep_latest_image(self):
        self.wbz_entries.append(WBZInfo(1, 4, 1, "Track 1", "v1.1-alt", None, "hash1"))
        self.wbz_entries.append(WBZInfo(1, 5, 1, "Track 1", "v1.2", None,"hash1"))
        self.wbz_entries.append(WBZInfo(1, 6, 1, "Track 1", "v1.3", None,"hash1"))
        self.wbz_entries.append(WBZInfo(1, 7, 1, "Track 1", "v1.4", None,"hash1"))
        actual_entries = gifs.remove_unnecessary_entries(self.wbz_entries)
        self.assertEqual(len(actual_entries), 3)
        wbz_id_1_entries = [e for e in actual_entries if e.wbz_id == 1]
        self.assertEqual(len(wbz_id_1_entries), 1)
        self.assertEqual(wbz_id_1_entries[0].image_id, 1)

    def test_remove_update_no_image(self):
        self.wbz_entries.append(WBZInfo(1, 4, 1, "Track 1", "v1.1", None,None))
        actual_entries = gifs.remove_unnecessary_entries(self.wbz_entries)
        self.assertEqual(len(actual_entries), 3)
        wbz_id_1_entries = [e for e in actual_entries if e.wbz_id == 1]
        self.assertEqual(len(wbz_id_1_entries), 1)
        self.assertEqual(wbz_id_1_entries[0].image_id, 1)


if __name__ == '__main__':
    unittest.main()
