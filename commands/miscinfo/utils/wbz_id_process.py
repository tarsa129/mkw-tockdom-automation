import warnings

from common_utils.szslibrary_helpers import *

class WBZInfo:
    def __init__(self, page_id, track_name, track_version, wbz_id, image_id, image_hash):
        self.page_id = page_id
        self.track_name = track_name
        self.track_version = track_version
        self.wbz_id = wbz_id
        self.image_id = image_id
        self.image_hash = image_hash

    def __repr__(self):
        return f"{self.page_id}, {self.track_name}, {self.wbz_id}, {self.image_id}"

def get_wbz_info(wbz_id):
    track_info = get_track_info(wbz_id)
    if not track_info:
        return None

    page_id = track_info["track_wiki"]
    track_name = get_full_trackname(track_info)
    track_version = get_full_versionname(track_info)
    orig_wbz_id = track_info["track_family"]
    image_hash = get_imagehash_by_id(wbz_id)

    if image_hash is None and orig_wbz_id != wbz_id:
        warnings.warn(f"wbz id {wbz_id} does NOT have an image, and it is an update. Skipping writing")
        return None
    elif image_hash is None:
        warnings.warn(f"wbz id {wbz_id} does NOT have an image, and is a new track. Writing 0 for image-id")
        wbz_id = 0

    return WBZInfo(page_id, track_name, track_version, orig_wbz_id, wbz_id, image_hash)