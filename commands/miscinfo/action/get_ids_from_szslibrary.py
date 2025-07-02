from tockdomio import szslibrary_read

def get_wbz_ids(start_id, end_id, file_path):
    szslibrary_response = szslibrary_read.get_by_wbz_id(start_id)
    print(szslibrary_response)