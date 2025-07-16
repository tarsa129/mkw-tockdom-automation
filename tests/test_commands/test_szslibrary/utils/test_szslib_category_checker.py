import unittest

from commands.szslibrary.utils import szslib_category_checker as scc
from commands.szslibrary.utils.audit_entry import AuditSzsLibraryEntry
from constants import SZSLIB_NINTENDO, SZSLIB_WBZID, SZSLIB_EDIT, SZSLIB_TEXTURE


class TestSzsLibCategoryChecker(unittest.TestCase):
    def setUp(self):
        self.page_name = "Dummy Page Name"

    def test_has_wbz_id_valid(self):
        arguments = {"wbz-id": "12929"}
        audit_entry = scc.check_has_wbz_id(arguments, self.page_name)
        self.assertIsNone(audit_entry)

    def test_has_wbz_id_invalid(self):
        arguments = {}
        audit_entry = scc.check_has_wbz_id(arguments, self.page_name)
        self.assertIsInstance(audit_entry, AuditSzsLibraryEntry)
        self.assertEqual(audit_entry.faulty_column, "wbz-id")

    def test_check_custom_status_custom_valid(self):
        track_status = "Custom"
        track_info = {SZSLIB_WBZID: "1291239", SZSLIB_NINTENDO: "0"}
        audit_entry = scc.check_custom_status(track_status, track_info, self.page_name)
        self.assertIsNone(audit_entry)

    def test_check_custom_status_custom_invalid(self):
        track_status = "Custom"
        track_info = {SZSLIB_WBZID: "1291239", SZSLIB_NINTENDO: "1"}
        audit_entry = scc.check_custom_status(track_status, track_info, self.page_name)
        self.assertIsInstance(audit_entry, AuditSzsLibraryEntry)
        self.assertEqual(audit_entry.faulty_column, SZSLIB_NINTENDO)

    def test_check_custom_status_nintendo_valid(self):
        track_status = ""
        track_info = {SZSLIB_WBZID: "1291239", SZSLIB_NINTENDO: "1"}
        audit_entry = scc.check_custom_status(track_status, track_info, self.page_name)
        self.assertIsNone(audit_entry)

    def test_check_custom_status_nintendo_invalid(self):
        track_status = ""
        track_info = {SZSLIB_WBZID: "1291239", SZSLIB_NINTENDO: "0"}
        audit_entry = scc.check_custom_status(track_status, track_info, self.page_name)
        self.assertIsInstance(audit_entry, AuditSzsLibraryEntry)
        self.assertEqual(audit_entry.faulty_column, SZSLIB_NINTENDO)

    def test_check_track_modification_none_valid(self):
        track_modification = ""
        track_info = {SZSLIB_WBZID: "1291239", SZSLIB_EDIT: "0", SZSLIB_TEXTURE: "0"}
        audit_entry = scc.check_track_modification(track_modification, track_info, self.page_name)
        self.assertIsNone(audit_entry)

    def test_check_track_modification_none_invalid_edit(self):
        track_modification = ""
        track_info = {SZSLIB_WBZID: "1291239", SZSLIB_EDIT: "1", SZSLIB_TEXTURE: "0"}
        audit_entry = scc.check_track_modification(track_modification, track_info, self.page_name)
        self.assertIsInstance(audit_entry, AuditSzsLibraryEntry)
        self.assertEqual(audit_entry.faulty_column, SZSLIB_EDIT)

    def test_check_track_modification_none_invalid_texture(self):
        track_modification = ""
        track_info = {SZSLIB_WBZID: "1291239", SZSLIB_EDIT: "0", SZSLIB_TEXTURE: "1"}
        audit_entry = scc.check_track_modification(track_modification, track_info, self.page_name)
        self.assertIsInstance(audit_entry, AuditSzsLibraryEntry)
        self.assertEqual(audit_entry.faulty_column, SZSLIB_TEXTURE)
        self.assertFalse(audit_entry.suggested_value)

    def test_check_track_modification_edit_valid_edit(self):
        track_modification = "Edit"
        track_info = {SZSLIB_WBZID: "1291239", SZSLIB_EDIT: "1", SZSLIB_TEXTURE: "0"}
        audit_entry = scc.check_track_modification(track_modification, track_info, self.page_name)
        self.assertIsNone(audit_entry)

    def test_check_track_modification_edit_invalid_none(self):
        track_modification = "Edit"
        track_info = {SZSLIB_WBZID: "1291239", SZSLIB_EDIT: "0", SZSLIB_TEXTURE: "0"}
        audit_entry = scc.check_track_modification(track_modification, track_info, self.page_name)
        self.assertIsInstance(audit_entry, AuditSzsLibraryEntry)
        self.assertEqual(audit_entry.faulty_column, SZSLIB_EDIT)
        self.assertTrue(audit_entry.suggested_value)

    def test_check_track_modification_texture_valid(self):
        track_modification = "Texture"
        track_info = {SZSLIB_WBZID: "1291239", SZSLIB_EDIT: 0, SZSLIB_TEXTURE: 1}
        audit_entry = scc.check_track_modification(track_modification, track_info, self.page_name)
        self.assertIsNone(audit_entry)

    def test_check_track_modification_texture_invalid_none(self):
        track_modification = "Texture"
        track_info = {SZSLIB_WBZID: "1291239", SZSLIB_EDIT: "0", SZSLIB_TEXTURE: "0"}
        audit_entry = scc.check_track_modification(track_modification, track_info, self.page_name)
        self.assertIsInstance(audit_entry, AuditSzsLibraryEntry)
        self.assertEqual(audit_entry.faulty_column, SZSLIB_TEXTURE)
        self.assertTrue(audit_entry.suggested_value)

    def test_check_track_modification_texture_invalid_edit(self):
        track_modification = "Texture"
        track_info = {SZSLIB_WBZID: "1291239", SZSLIB_EDIT: 1, SZSLIB_TEXTURE: 1}
        audit_entry = scc.check_track_modification(track_modification, track_info, self.page_name)
        self.assertIsInstance(audit_entry, AuditSzsLibraryEntry)
        self.assertEqual(audit_entry.faulty_column, SZSLIB_EDIT)
        self.assertFalse(audit_entry.suggested_value)



if __name__ == '__main__':
    unittest.main()
