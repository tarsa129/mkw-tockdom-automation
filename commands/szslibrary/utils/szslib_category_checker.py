from commands.szslibrary.utils.audit_entry import AuditSzsLibraryEntry
from constants import CATEGORY_CUSTOM, SZSLIB_NINTENDO, SZSLIB_EDIT, SZSLIB_TEXTURE, SZSLIB_BATTLE, SZSLIB_TRACK, \
    CATEGORY_EDIT, CATEGORY_TEXTURE, SZSLIB_WBZID


def check_track_type(track_type, track_info, page_name):
    audit_entry = AuditSzsLibraryEntry(track_info["wbz_id"], page_name)
    is_track = track_info[SZSLIB_TRACK] == "1"
    is_arena = track_info[SZSLIB_BATTLE] == "1"
    if track_type == "Track" and not is_track:
        audit_entry.set_should_be_true(SZSLIB_TRACK)
    elif track_type == "Track" and is_arena:
        audit_entry.set_should_be_false(SZSLIB_BATTLE)
    elif track_type == "Battle" and not is_arena:
        audit_entry.set_should_be_true(SZSLIB_BATTLE)
    elif track_type == "Battle" and is_track:
        audit_entry.set_should_be_false(SZSLIB_TRACK)
    return audit_entry.get_if_has_audit_info()

def check_has_wbz_id(arguments, page_name):
    if "wbz-id" in arguments and arguments["wbz-id"]:
        return None
    audit_entry = AuditSzsLibraryEntry("", page_name)
    audit_entry.add_audit_info("wbz-id", "Empty", "Not Empty")
    return audit_entry

def check_custom_status(track_status, track_info, page_name):
    audit_entry = AuditSzsLibraryEntry(track_info[SZSLIB_WBZID], page_name)
    is_nintendo = str(track_info[SZSLIB_NINTENDO]) == "1"
    if track_status == CATEGORY_CUSTOM and is_nintendo:
        audit_entry.set_should_be_false(SZSLIB_NINTENDO)
    elif track_status != CATEGORY_CUSTOM and not is_nintendo:
        audit_entry.set_should_be_true(SZSLIB_NINTENDO)
    return audit_entry.get_if_has_audit_info()

def check_track_modification(track_modification, track_info, page_name):
    audit_entry = AuditSzsLibraryEntry(track_info[SZSLIB_WBZID], page_name)
    is_edit = str(track_info[SZSLIB_EDIT]) == "1"
    is_texture = str(track_info[SZSLIB_TEXTURE]) == "1"
    if not track_modification and is_edit:
        audit_entry.set_should_be_false(SZSLIB_EDIT)
    elif not track_modification and is_texture:
        audit_entry.set_should_be_false(SZSLIB_TEXTURE)
    elif track_modification == CATEGORY_EDIT and not is_edit:
        audit_entry.set_should_be_true(SZSLIB_EDIT)
    elif track_modification == CATEGORY_EDIT and is_texture:
        audit_entry.set_should_be_false(SZSLIB_TEXTURE)
    elif track_modification == CATEGORY_TEXTURE and not is_texture:
        audit_entry.set_should_be_true(SZSLIB_TEXTURE)
    elif track_modification == CATEGORY_TEXTURE and is_edit:
        audit_entry.set_should_be_false(SZSLIB_EDIT)
    return audit_entry.get_if_has_audit_info()

