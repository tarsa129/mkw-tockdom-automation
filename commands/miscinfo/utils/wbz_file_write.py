from common_utils.file_writer import write_csv_file

def write_wbz_file(file, track_info):
    dict_info = [vars(track) for track in track_info]
    write_csv_file(file, dict_info)