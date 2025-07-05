import re
import warnings
from collections import defaultdict

from commands.distro_list.utils import track_page_distros
from mediawiki.mediawiki_read import read_text
from common_utils.file_reader import read_csv_file

def does_distro_need_version(distro_text):
    parsed_text = read_text(distro_text)
    if len(parsed_text.wikilinks) > 0:
        return True
    elif len(parsed_text.templates) > 0:
        distro_template = parsed_text.templates[0]
        assert(distro_template.name == "Distrib-ref")
        return False
    return True

def validate_distro_entry(update_entry, line_num):
    page_name = update_entry["page_name"]
    distro_text = update_entry["distro_text"]
    version = update_entry["version"]

    if not page_name or not distro_text:
        warnings.warn(f"entry on line {line_num} does NOT have a valid pagename or distro name")
        return False
    if does_distro_need_version(distro_text) and not version:
        warnings.warn(f"entry on line {line_num} does NOT have a version")
        return False

    return True

def read_distro_file(file):
    raw_file_info = read_csv_file(file)

    pages = defaultdict(lambda: dict())
    for i, entry in enumerate(raw_file_info):
        if not validate_distro_entry(entry, i+1):
            continue

        distro_text = entry["distro_text"]
        distro_name = track_page_distros.read_distro_name(distro_text)
        version = entry["version"]
        if version:
            distro_text = f"{distro_text} ({version})"

        pages[entry["page_name"]] |= {distro_name: distro_text}
    return pages