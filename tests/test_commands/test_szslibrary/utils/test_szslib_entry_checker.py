import unittest

from commands.szslibrary.utils import szslib_entry_checker as sec

class TestSzslibEntryChecker(unittest.TestCase):
    def test_check_version_extra_valid(self):
        wbz_id = 129
        track_name = "Test Track"
        track_info = {"track_version": "v1.1", "track_version_extra": ""}
        audit_entry = sec.check_version_extra(wbz_id, track_name, track_info)
        self.assertIsNone(audit_entry)

    def test_check_version_extra_simpleversion(self):
        wbz_id = 129
        track_name = "Test Track"
        track_info = {"track_version": "v1.1a", "track_version_extra": ""}
        audit_entry = sec.check_version_extra(wbz_id, track_name, track_info)
        self.assertIsNone(audit_entry)


    def test_check_version_extra_invalid(self):
        wbz_id = 129
        track_name = "Test Track"
        track_info = {"track_version": "v1.1.ikw", "track_version_extra": ""}
        audit_entry = sec.check_version_extra(wbz_id, track_name, track_info)
        self.assertIsNotNone(audit_entry)
        self.assertEqual(audit_entry.suggested_value, ".ikw")


if __name__ == '__main__':
    unittest.main()
