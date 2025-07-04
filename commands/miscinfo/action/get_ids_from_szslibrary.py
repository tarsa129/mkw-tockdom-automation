from common_utils.szslibrary_helpers import validate_start_end_wbz_ids
from commands.miscinfo.utils.wbz_id_process import *
from commands.miscinfo.utils.wbz_file_write import write_wbz_file

def get_wbz_ids(start_id, end_id, file_path):
    if not validate_start_end_wbz_ids(start_id, end_id):
        return False

    wbz_info_entries = []
    for i in range(int(start_id), int(end_id) + 1):
        wbz_info_entry = get_wbz_info(i)
        if wbz_info_entry:
            wbz_info_entries.append(wbz_info_entry)

    write_wbz_file(file_path, wbz_info_entries)

    return wbz_info_entries