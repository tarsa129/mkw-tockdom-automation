from commands.miscinfo.utils.wbz_id_process import *
from commands.miscinfo.utils.wbz_file_write import write_wbz_file


def remove_unnecessary_entries(wbz_entries: list[WBZInfo]) -> list[WBZInfo]:
    existing_image_ids = {}
    for entry in wbz_entries:
        #new tracks should ALWAYS be added to the file
        is_new_track = entry.wbz_id == entry.image_id
        if is_new_track:
            existing_image_ids[entry.wbz_id] = entry
            continue

        #having no image OR being an alt version are grounds for NOT updating an image id
        is_no_image = entry.image_hash is None
        is_alt_version = entry.track_version_extra is not None
        if is_no_image or is_alt_version:
            warnings.warn(
                f"{entry} is an update with no image ({is_no_image}) or is an alt version ({is_alt_version}), so skipping. Replace with {entry.image_hash} if needed.")
            continue

        if entry.wbz_id not in existing_image_ids:
            existing_image_ids[entry.wbz_id] = entry
            continue

        existing_entry = existing_image_ids[entry.wbz_id]
        if existing_entry.image_hash is None:
            warnings.warn(f"{entry} is replacing entry with no image {existing_entry}.")
            existing_image_ids[entry.wbz_id] = entry
        elif existing_entry.image_hash == entry.image_hash:
            warnings.warn(f"{entry} already has the image hash as {existing_entry}, so skipping.")
        else:
            warnings.warn(f"{entry} is replacing entry with image {existing_entry}. Replace with {existing_entry.image_hash} if needed.")
            existing_image_ids[entry.wbz_id] = entry

    return list(existing_image_ids.values())

def get_wbz_ids(start_id, end_id, file_path):
    if not validate_start_end_wbz_ids(start_id, end_id):
        return False

    wbz_info_entries = []
    for i in range(int(start_id), int(end_id) + 1):
        wbz_info_entry = get_wbz_info(i)
        if wbz_info_entry is None:
            continue
        wbz_info_entries.append(wbz_info_entry)

    write_wbz_file(file_path, wbz_info_entries)

    wbz_info_entries = remove_unnecessary_entries(wbz_info_entries)
    write_wbz_file(file_path + "_trimmed.csv", wbz_info_entries)

    return wbz_info_entries