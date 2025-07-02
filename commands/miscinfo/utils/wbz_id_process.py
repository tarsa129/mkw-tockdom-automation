from tockdomio import szslibrary_read

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

class WBZInfo:
    def __init__(self, page_id, track_name, wbz_id, image_id):
        self.page_id = page_id
        self.track_name = track_name
        self.wbz_id = wbz_id
        self.image_id = image_id

    def __repr__(self):
        return f"{self.page_id}, {self.track_name}, {self.wbz_id}, {self.image_id}"

def get_wbz_info(wbz_id):
    szslibrary_response = szslibrary_read.get_by_wbz_id(wbz_id)
    if not szslibrary_response or not szslibrary_response["track_info"]:
        return None

    track_info = szslibrary_response["track_info"][0]
    if not track_info["track_wiki"]:
        return None

    page_id = track_info["track_wiki"]
    track_name = f"{track_info['prefix']} {track_info['trackname']} {track_info['track_version']}"
    orig_wbz_id = track_info["track_family"]

    return WBZInfo(page_id, track_name, orig_wbz_id, wbz_id)