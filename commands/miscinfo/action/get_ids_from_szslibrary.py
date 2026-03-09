from commands.miscinfo.utils.wbz_id_process import *
from commands.miscinfo.utils.wbz_file_write import write_wbz_file





def get_wbz_ids(start_id, end_id, file_path):
    if not validate_start_end_wbz_ids(start_id, end_id):
        return False

    for i in range(int(start_id), int(end_id) + 1):
        track_info: SZSLibraryTrackInfo = get_track_info(i)
        if track_info is None:
            warnings.warn(f"wbz_id {i} failed at getting track info. Skipping.")
            continue

    write_wbz_file(file_path, wbz_info_entries)


    return wbz_info_entries