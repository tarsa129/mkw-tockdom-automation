import warnings

from common_utils.szslibrary_helpers import *
from common_utils.szslibrary_helpers import get_track_info
from common_utils.track_page_utils.wiiki_name_utils.track_disambiguation import get_page_from_name_authors

class WBZInfo:
    def __init__(self, wbz_id, image_id, page_id, track_name, track_version, version_extra, find_manually, image_hash,
                 authors, editors):
        self.wbz_id = wbz_id
        self.image_id = image_id
        self.page_id = page_id
        self.track_name = track_name
        self.track_version = track_version
        self.track_version_extra = version_extra
        self.find_manually = find_manually
        self.authors = authors
        self.editors = editors
        self.image_hash = image_hash

    def __repr__(self):
        base_text = f"{self.wbz_id}/{self.image_id}: {self.track_name} {self.track_version}"
        if self.track_version_extra:
            base_text = f"{base_text}--{self.track_version_extra}"
        return base_text

def get_wbz_info(wbz_id):
    track_info = get_track_info(wbz_id)
    if not track_info:
        return None

    track_name = track_info.get_full_trackname()
    find_manually = False
    if not track_info.track_wiki:
        disambig_page_id, disambig_track_name = get_page_from_name_authors(
            track_info.get_full_trackname(), track_info.get_mod_type(), track_info.track_author)
        if disambig_track_name:
            track_name = disambig_track_name
            track_info.track_wiki = disambig_page_id
        else:
            find_manually = True
        print(track_name)

    image_hash = get_imagehash_by_id(wbz_id)
    if image_hash is None and track_info.track_family != wbz_id:
        warnings.warn(f"wbz id {wbz_id} does NOT have an image, and it is an update. Skipping writing")
        return None
    elif image_hash is None:
        warnings.warn(f"wbz id {wbz_id} does NOT have an image, and is a new track. Writing 0 for image-id")
        wbz_id = 0

    return WBZInfo(track_info.track_family, wbz_id,
                   track_info.track_wiki, track_name,
                   track_info.get_full_versionname(), track_info.track_version_extra, find_manually,
                   image_hash,
                   track_info.track_author, track_info.track_updaters)