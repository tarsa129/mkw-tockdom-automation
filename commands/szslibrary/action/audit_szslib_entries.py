from commands.miscinfo.utils.wbz_file_write import write_wbz_file
from commands.szslibrary.utils.szslib_entry_checker import check_szslib_entry
from common_utils.szslibrary_helpers import validate_start_end_wbz_ids

def audit_entries(start_id, end_id, file_path):
    if not validate_start_end_wbz_ids(start_id, end_id):
        return False

    szslib_audit_entries = []
    for i in range(int(start_id), int(end_id) + 1):
        szslib_audit_entries.extend(check_szslib_entry(i))

    if szslib_audit_entries:
        write_wbz_file(file_path, szslib_audit_entries)

    return szslib_audit_entries