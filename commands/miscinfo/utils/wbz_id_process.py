from common_utils.szslibrary_helpers import get_track_info, get_full_versionname, get_full_trackname
from common_utils.track_disambiguation import get_page_from_name_authors

class WBZInfo:
    def __init__(self, page_id, track_name, track_version, wbz_id, image_id):
        self.page_id = page_id
        self.track_name = track_name
        self.track_version = track_version
        self.wbz_id = wbz_id
        self.image_id = image_id

    def __repr__(self):
        return f"{self.page_id}, {self.track_name}, {self.wbz_id}, {self.image_id}"

def get_wbz_info(wbz_id):
    track_info = get_track_info(wbz_id)
    if not track_info:
        return None

    print(track_info)

    page_id = track_info["track_wiki"]
    track_name = get_full_trackname(track_info)
    track_version = get_full_versionname(track_info)
    track_authors = set(track_info["track_author"].split(","))

    if not page_id:
        track_name = get_page_from_name_authors(track_name, track_authors)
        print(track_name)

    orig_wbz_id = track_info["track_family"]

    return WBZInfo(page_id, track_name, track_version, orig_wbz_id, wbz_id)