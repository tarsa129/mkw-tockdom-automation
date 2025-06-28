import os.path
import csv
import warnings
from collections import defaultdict

from commands.distro_list.utils import track_page_distros


def parse_row(i, row):
    if len(row) == 0:
        warnings.warn("Line #{} is empty".format(i))
        return None, None
    elif len(row[0]) == 0:
        warnings.warn("Line #{} contains an empty page name".format(i))
        return None, None
    elif len(row) == 1:
        warnings.warn("Line #{} for pagename {} does not contain distro_list".format(i, row[0]))
        return None, None

    pagename = row[0]
    distros = {}

    for distro_text in row[1:]:
        distro_name = track_page_distros.read_distro_name(distro_text)
        if distro_name is not None:
            distros[distro_name] = distro_text
    return pagename, distros

def read_distro_file(file):
    if file is None or not os.path.exists(file):
        raise RuntimeError("File {} does not exist.".format(file))

    pages = defaultdict(lambda: dict())

    with open(file, newline='', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar="\"")
        for i, row in enumerate(reader):
            pagename, distros = parse_row(i, row)
            if pagename is None:
                continue
            pages[pagename] |= distros
    return pages