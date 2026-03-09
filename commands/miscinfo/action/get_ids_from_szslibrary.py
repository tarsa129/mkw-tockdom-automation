import warnings

from common_utils.szslibrary_helpers import *
from common_utils.track_page_utils.template_utils import misc_info_utils
from common_utils.track_page_utils.wiiki_name_utils.track_disambiguation import get_page_from_name_authors
from tockdomio import tockdomread

def get_latest_version(page_id):
    tockdom_response = tockdomread.get_page_text_by_id(page_id)
    page_text: str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
    arguments = misc_info_utils.get_miscinfo_template(page_text)
    return arguments["version"].strip()

def get_familyid_information(track_info: SZSLibraryTrackInfo):
    page_id = track_info.track_wiki
    if not page_id:
        found_page_id, found_page_name = get_page_from_name_authors(track_info.get_full_trackname(),
                                                              track_info.get_mod_type(),
                                                              track_info.track_author)
        if not found_page_id:
            warnings.warn(f"wbz_id {track_info.id_first} - {track_info.get_full_trackname_version()} does not have an associated page.")
            return None, None
        page_id = found_page_id
    miscinfo_version = get_latest_version(page_id)
    return page_id, miscinfo_version


def get_wbz_ids(start_id, end_id, file_path):
    if not validate_start_end_wbz_ids(start_id, end_id):
        return False

    miscinfo_versions = {} # family_id: miscinfo_version

    for i in range(int(start_id), int(end_id) + 1):
        track_info: SZSLibraryTrackInfo = get_track_info(i)
        if track_info is None:
            warnings.warn(f"wbz_id {i} failed at getting track info. Skipping.")
            continue

    write_wbz_file(file_path, wbz_info_entries)
        family_id = track_info.track_family
        if family_id not in miscinfo_versions:
            track_info.track_wiki, latest_version_on_page = get_familyid_information(track_info)
            miscinfo_versions[family_id] = latest_version_on_page

        has_image = get_imagehash_by_id(track_info.id_first) is not None
        if not has_image:
            warnings.warn(f"wbz_id {i} does not have an image.")


    return wbz_info_entries