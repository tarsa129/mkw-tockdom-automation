import warnings

from common_utils.file_writer import write_csv_file
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

def valid_image_id(track_info: SZSLibraryTrackInfo, miscinfo_version, has_image, current_entries):
    # Initial wbz-ids should always be added.
    if track_info.track_family == track_info.id_first:
        return True
    # If there is no image, it is not a valid image-id.
    if not has_image:
        return False
    #The version on the template is a valid write.
    if miscinfo_version == track_info.get_full_versionname():
        return True
    #If the latest version does not have an image (or has not been processed) use the latest official version as a backup
    #Check if the current version is official
    if not track_info.is_official_version():
        return False
    #Check that nothing is currently staged for the track.
    family_id = track_info.track_family
    if family_id not in current_entries:
        return True
    #Check that you are not overriding the actual current version.
    currently_written_version = current_entries[family_id].get_full_versionname()
    return miscinfo_version != currently_written_version

def get_wbz_ids(start_id, end_id, file_path):
    if not validate_start_end_wbz_ids(start_id, end_id):
        return False

    miscinfo_versions = {} # family_id: miscinfo_version
    family_id_to_track_info = {} #family_id: track_info

    for i in range(int(start_id), int(end_id) + 1):
        track_info: SZSLibraryTrackInfo = get_track_info(i)
        if track_info is None:
            warnings.warn(f"wbz_id {i} failed at getting track info. Skipping.")
            continue

        family_id = track_info.track_family
        if family_id not in miscinfo_versions:
            track_info.track_wiki, latest_version_on_page = get_familyid_information(track_info)
            miscinfo_versions[family_id] = latest_version_on_page

        has_image = get_imagehash_by_id(track_info.id_first) is not None
        if not has_image:
            warnings.warn(f"wbz_id {i} does not have an image.")

        miscinfo_version = miscinfo_versions[family_id]
        if valid_image_id(track_info, miscinfo_version, has_image, family_id_to_track_info):
            family_id_to_track_info[family_id] = track_info

    update_entries = [track_info.get_writeable_entry() for track_info in family_id_to_track_info.values()]
    update_entries.sort(key = lambda x: x["image_id"])
    write_csv_file(file_path, update_entries)

    return update_entries