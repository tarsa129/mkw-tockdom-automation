import re

from common_utils.szslibrary_helpers import get_track_info, get_full_trackname_version


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

def get_track_name(track_info):
    track_name = f"{track_info['trackname']} {track_info['track_version']}".strip()
    prefix = track_info['prefix']
    if prefix:
        track_name = f"{prefix} {track_name}"
    version_extra = track_info['track_version_extra']
    if version_extra:
        track_name = f"{track_name}{version_extra}"
    return track_name

def check_track_wiki(wbz_id, track_name, track_info):
    page_id = track_info["track_wiki"]
    if not page_id:
        return AuditSzsLibraryEntry.create_no_pageid(wbz_id, track_name)
    return None

def check_version_extra(wbz_id, track_name, track_info):
    track_version_extra = track_info['track_version_extra']
    if track_version_extra:
        return None

    track_version = track_info['track_version']
    extra_regex = re.search("[0-9]([-.][a-zA-Z]{2,})$", track_version)
    if not extra_regex or not extra_regex.group(1):
        return None

    return AuditSzsLibraryEntry.create_wrong_extended(wbz_id, track_name, extra_regex.group(1))

checker_functions = (check_track_wiki, check_version_extra)

def check_szslib_entry(wbz_id):
    track_info = get_track_info(wbz_id)
    if not track_info:
        return []

    print(track_info)

    audits = []
    track_name = get_full_trackname_version(track_info)

    for checker_function in checker_functions:
        audit = checker_function(wbz_id, track_name, track_info)
        if audit:
            audits.append(audit)

    return audits