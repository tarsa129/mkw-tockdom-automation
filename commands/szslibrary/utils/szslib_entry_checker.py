import re

from common_utils.szslibrary_helpers import get_track_info, get_full_trackname_version
from commands.szslibrary.utils.audit_entry import AuditSzsLibraryEntry

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