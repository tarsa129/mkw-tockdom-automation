from common_utils.szslibrary_helpers import get_track_info

class WBZInfo:
    def __init__(self, page_id, track_name, wbz_id, image_id):
        self.page_id = page_id
        self.track_name = track_name
        self.wbz_id = wbz_id
        self.image_id = image_id

    def __repr__(self):
        return f"{self.page_id}, {self.track_name}, {self.wbz_id}, {self.image_id}"

def get_wbz_info(wbz_id):
    track_info = get_track_info(wbz_id)
    if not track_info:
        return None

    page_id = track_info["track_wiki"]
    track_name = f"{track_info['prefix']} {track_info['trackname']} {track_info['track_version']}".strip()
    orig_wbz_id = track_info["track_family"]

    return WBZInfo(page_id, track_name, orig_wbz_id, wbz_id)