import os.path
import csv
import warnings
from collections import defaultdict

from trackpage import mediawikiparse as mwp

def parse_row(i, row):
    if len(row) == 0:
        warnings.warn("Line #{} is empty".format(i))
        return None, None
    elif len(row[0]) == 0:
        warnings.warn("Line #{} contains an empty page name".format(i))
        return None, None
    elif len(row) == 1:
        warnings.warn("Line #{} for pagename {} does not contain distros".format(i, row[0]))
        return None, None

    pagename = row[0]
    distros = {}

    for distro_text in row[1:]:
        parsed_text: mwp.WikiText = mwp.read_text(distro_text)
        if len(parsed_text.templates) > 0:
            assert(len(parsed_text.templates) == 1)
            distro_template = parsed_text.templates[0]
            if distro_template.name != "Distrib-ref":
                warnings.warn('{} is a template but is not named "Distrib-ref"'.format(distro_text))
            distro_name = distro_template.arguments[0].value
            distros[distro_name] = str(distro_template)
        elif len(parsed_text.wikilinks) > 0:
            assert(len(parsed_text.wikilinks) == 1)
            _, distro_name = mwp.read_wiikilink(parsed_text.wikilinks[0])
            distros[distro_name] = str(distro_text)
        else:
            warnings.warn("{} is not a valid distribution Wiiki text".format(distro_text))

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