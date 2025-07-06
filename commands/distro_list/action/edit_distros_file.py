import re
import warnings

from common_utils.file_reader import read_csv_file
from common_utils.file_writer import write_csv_file

def fix_version(version_text):
    return re.sub("^([0-9])", "v\g<1>", version_text)

def edit_distros_list(file, distro_name, flags):
    raw_file_info = read_csv_file(file)
    flags = flags.split(",")

    for i, entry in enumerate(raw_file_info):
        page_name = entry["page_name"]
        if not page_name:
            warnings.warn(f"Line {i + 1} needs a page name.")
            continue

        if distro_name and not entry["distro_text"]:
            entry["distro_text"] = distro_name

        if "version-fix" in flags:
            entry["version"] = fix_version(entry["version"])

    write_csv_file(file,raw_file_info)
