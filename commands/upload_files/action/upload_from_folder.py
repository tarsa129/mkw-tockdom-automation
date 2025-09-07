import os
from tockdomio import tockdomwrite

def upload_file(file_path, file_name):
    print(f"Uploading {file_name}")
    with open(file_path, 'rb') as file_data:
        response = tockdomwrite.upload_file(file_name, file_data)
        print(response.json())

def upload_files_from_folder(folder_name):
    print(f"Uploading all .jpg images from {folder_name}")
    files = [f for f in os.listdir(folder_name) if os.path.isfile(f"{folder_name}/{f}") and f.lower().endswith(".jpg")]
    for f in files:
        full_file_name = f"{folder_name}/{f}"
        upload_file(full_file_name, f)
