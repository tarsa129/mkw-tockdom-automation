class AuditSzsLibraryEntry:
    def __init__(self, wbz_id, track_name_version):
        self.wbz_id = wbz_id
        self.faulty_column = ""
        self.curr_value = ""
        self.suggested_value = ""
        self.track_name_version = track_name_version

    def add_audit_info(self, faulty_column, curr_value, suggested_value):
        self.faulty_column = faulty_column
        self.curr_value = curr_value
        self.suggested_value = suggested_value

    def set_should_be_false(self, faulty_column):
        self.faulty_column = faulty_column
        self.curr_value = True
        self.suggested_value = False

    def set_should_be_true(self, faulty_column):
        self.faulty_column = faulty_column
        self.curr_value = False
        self.suggested_value = True

    def get_if_has_audit_info(self):
        if self.faulty_column:
            return self
        return None

    @classmethod
    def create_no_pageid(cls, wbz_id, track_name_version):
        audit_entry = cls(wbz_id, track_name_version)
        audit_entry.faulty_column = "track_wiki"
        audit_entry.curr_value = "Empty"
        audit_entry.suggested_value = "Not Empty"
        return audit_entry

    @classmethod
    def create_wrong_extended(cls, wbz_id, track_name_version, new_version):
        audit_entry = cls(wbz_id, track_name_version)
        audit_entry.faulty_column = "track_version_extra"
        audit_entry.curr_value = "Empty"
        audit_entry.suggested_value = new_version
        return audit_entry