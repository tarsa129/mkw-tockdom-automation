import warnings

from common_utils.file_writer import write_csv_file
from common_utils.szslibrary_helpers import *
from common_utils.track_page_utils.template_utils import misc_info_utils
from common_utils.track_page_utils.version_utils.version_disambiguation import get_wbz_id_from_miscinfo
from common_utils.track_page_utils.wiiki_name_utils.track_disambiguation import get_page_from_name_authors
from tockdomio import tockdomread

def get_latest_version(page_id):
    tockdom_response = tockdomread.get_page_text_by_id(page_id)
    page_text: str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
    return misc_info_utils.get_miscinfo_template(page_text)

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
    arguments = get_latest_version(page_id)
    return page_id, arguments

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
    if family_id not in current_entries or not current_entries[family_id].track_info:
        return True
    #Check that you are not overriding the actual current version.
    currently_written_version = current_entries[family_id].track_info.get_full_versionname()
    return miscinfo_version != currently_written_version

class FamilyIDInformation:
    def __init__(self, page_id, miscinfo_information, track_info = None):
        self.page_id = page_id
        self.track_info: SZSLibraryTrackInfo = track_info
        self.miscinfo_information = miscinfo_information
        self.official_version = False

    def get_current_version(self):
        return self.miscinfo_information["version"]

    def is_trackinfo_written(self):
        effective_image_id = self.miscinfo_information["image-id"]
        if effective_image_id == "0":
            return True

        if not effective_image_id:
            effective_image_id= f'{self.miscinfo_information["wbz-id"]:{"0"}>{2}}'

        incoming_image_id =  f'{str(self.track_info.id_first):{"0"}>{2}}'
        return incoming_image_id == effective_image_id

def get_wbz_ids(start_id, end_id, file_path):
    if not validate_start_end_wbz_ids(start_id, end_id):
        return False

    family_ids = {}

    for i in range(int(start_id), int(end_id) + 1):
        track_info: SZSLibraryTrackInfo = get_track_info(i)
        if not track_info:
            warnings.warn(f"wbz_id {i} failed at getting track info. Skipping.")
            continue

        family_id = track_info.track_family
        if family_id not in family_ids:
            track_info.track_wiki, misc_info_arguments = get_familyid_information(track_info)
            if misc_info_arguments is None:
                continue
            family_ids[family_id] = FamilyIDInformation(track_info.track_wiki, misc_info_arguments)

        family_info = family_ids[family_id]
        miscinfo_version = family_info.get_current_version()
        if family_info.official_version or (family_info.track_info and family_info.is_trackinfo_written()):
            continue

        exact_match_track_info = get_wbz_id_from_miscinfo(family_id, family_info.miscinfo_information)
        if exact_match_track_info and get_imagehash_by_id(exact_match_track_info.id_first) is not None:
            exact_match_track_info.track_wiki = family_info.page_id
            family_info.track_info = exact_match_track_info
            family_info.official_version = True
            continue

        has_image = get_imagehash_by_id(track_info.id_first) is not None
        if not has_image:
            warnings.warn(f"wbz_id {i} does not have an image.")

        if valid_image_id(track_info, miscinfo_version, has_image, family_ids):
            track_info.track_wiki = family_info.page_id
            family_info.track_info = track_info

    family_ids = list(filter(lambda x: not x.is_trackinfo_written(), family_ids.values()))
    update_entries = [family_id_info.track_info.get_writeable_entry() for family_id_info in family_ids if family_id_info.track_info]
    update_entries.sort(key = lambda x: x["image_id"])
    write_csv_file(file_path, update_entries)

    return update_entries