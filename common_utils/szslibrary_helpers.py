from common_utils.track_page_utils.wiiki_name_utils.track_disambiguation import get_page_from_name_authors
from constants import SZSLIB_EDIT, SZSLIB_TEXTURE
import hashlib

from tockdomio import szslibrary_read
from tockdomio.szslibrary_read import get_image_from_id


def validate_wbz_id(id_text):
    if not id_text.isnumeric():
        return False

    id_num = int(id_text)
    if id_num == 0:
        return False

    return True

def validate_start_end_wbz_ids(start_id, end_id):
    if not validate_wbz_id(start_id):
        raise RuntimeError(f"Start id {start_id} must be a positive integer")
    if not validate_wbz_id(end_id):
        raise RuntimeError(f"End id {end_id} must be a positive integer")

    start_id_num = int(start_id)
    end_id_num = int(end_id)

    if end_id_num < start_id_num:
        raise RuntimeError(f"Start id {start_id_num} cannot be greater than end id {end_id}")

    return True

def get_track_info(wbz_id):
    szslibrary_response = szslibrary_read.get_by_wbz_id(wbz_id)
    if not szslibrary_response or not szslibrary_response["track_info"]:
        return None

    track_info = szslibrary_response["track_info"]
    if not track_info:
        return None

    return track_info

def get_mod_type(track_info):
    if track_info[SZSLIB_EDIT] == 1:
        return "Edit"
    if track_info[SZSLIB_TEXTURE] == 1:
        return "Texture"
    return None

def get_full_trackname(track_info):
    track_name = f"{track_info['trackname']}".strip()
    prefix = track_info['prefix']
    if prefix:
        track_name = f"{prefix} {track_name}"
    return track_name

def get_full_versionname(track_info):
    version_name = f"{track_info['track_version']}".strip()
    version_extra = track_info['track_version_extra']
    if version_extra:
        version_name = f"{version_name}-{version_extra}"
    return version_name

def get_full_trackname_version(track_info):
    track_name = get_full_trackname(track_info)
    version_name = get_full_versionname(track_info)
    return f"{track_name} {version_name}"

def get_full_disambiguation(track_info):
    track_name = get_full_trackname(track_info)

    track_authors = set(track_info["track_author"].split(","))
    track_disambig = get_page_from_name_authors(track_name, track_authors)

    return track_disambig

def get_imagehash_by_id(image_id):
    image_content = get_image_from_id(image_id)
    if image_content is None:
        return None

    return hashlib.sha256(str(image_content).encode()).hexdigest()