class AuditSzsLibraryEntry:
    def __init__(self, wbz_id, track_name_version):
        self.wbz_id = wbz_id
        self.faulty_column = ""
        self.curr_value = ""
        self.suggested_value = ""
        self.track_name_version = track_name_version

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