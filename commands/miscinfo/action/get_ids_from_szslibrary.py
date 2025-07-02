from tockdomio import szslibrary_read
from commands.miscinfo.utils.wbz_id_process import *


def get_wbz_ids(start_id, end_id, file_path):
    szslibrary_response = szslibrary_read.get_by_wbz_id(start_id)
    print(szslibrary_response)
    if not validate_start_end_wbz_ids(start_id, end_id):
        return False
