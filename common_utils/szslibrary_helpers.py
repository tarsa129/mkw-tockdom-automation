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


def get_track_info(wbz_id):
    szslibrary_response = szslibrary_read.get_by_wbz_id(wbz_id)
    if not szslibrary_response or not szslibrary_response["track_info"]:
        return None

    track_info = szslibrary_response["track_info"]
    if not track_info:
        return None

    return track_info[0]