from tockdomio import tockdomread, tockdomwrite
from commands.distros import track_page_distros as track_page
import warnings
from enum import Enum
from collections import Counter

class Action(Enum):
    ADD = 1
    UPDATE = 2
    DELETE = 3

# While duplicate distribution names are technically allowed, we still assume that all names are unique.
# At time of writing, only 4 such distributions exist, and only 1 is actually for tracks
# This one distribution does not have any overlapping tracks.
# Thus, is it more likely that duplicate distro names are a result of human error.
# In the future, if needed, we can revisit this by implementing this all as a dict of lists.
def validate_distros(distros: dict):
    distroname_counter = Counter(map(str.lower, distros.keys()))

    is_valid = True

    for distroname, distrocount in distroname_counter.most_common(len(distroname_counter)):
        if distrocount == 1:
            break
        is_valid = False
        warnings.warn("Distro with lowercase name {} appears more than once.".format(distroname))

    return is_valid

def combine_distros(curr_distros: dict, new_distros: dict, action):
    for new_distro, new_distro_text in new_distros.items():
        if new_distro in curr_distros:
            if action == Action.DELETE:
                curr_distros.pop(new_distro)
            elif action == Action.UPDATE:
                curr_distros[new_distro] = new_distro_text
            else:
                warnings.warn("{} already on the page!".format(new_distro))
        else:
            if action == Action.DELETE:
                warnings.warn("{} not on the page!".format(new_distro))
            else:
                curr_distros[new_distro] = new_distro_text
    return dict(sorted(curr_distros.items(), key=lambda x: x[0].lower()))


def read_and_update_page(tockdom_response, new_distros, action):
    if not (validate_distros):
        raise RuntimeError("List of distros to add has repeats")
    page_id = tockdom_response["pageid"]
    page_text:str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
    curr_distros = track_page.get_distros_from_page(page_text)
    if not validate_distros(curr_distros):
        raise RuntimeWarning("Existing distro list has repeats")

    distros = combine_distros(curr_distros, new_distros, action)

    if not validate_distros(distros):
        raise RuntimeError("Existing distros in combined list.")

    distros_section_id = track_page.get_distros_sectionid(page_text)
    distros_section_text = track_page.create_distros_section(distros)
    response = tockdomwrite.edit_section(page_id, distros_section_id, distros_section_text)

    return response.json()["edit"]["result"]

def edit_distros_to_pagename(pagename, new_distros: dict, action):
    tockdom_response = tockdomread.get_page_text_by_name(pagename)
    read_and_update_page(tockdom_response, new_distros, action)

def edit_distros_to_pageid(pageid, new_distros: dict, action):
    tockdom_response = tockdomread.get_page_text_by_id(pageid)
    read_and_update_page(tockdom_response, new_distros, action)

def handle_command(action, file):
    added_distros = {}
    added_distros["Aurora"] = "[[Aurora]] (v2.1)"
    added_distros["tarsa's epic track pack"] = "[[tarsa's epic track pack]] (v2.0)"
    added_distros["Tarsa's epic track pack 2"] = "{{Distrib-ref|Tarsa's epic track pack 2|129129|tarsa-pack}}"
    if action == "add":
        edit_distros_to_pagename("User:tarsa129/Test", added_distros, action = Action.ADD)
    elif action == "update":
        edit_distros_to_pagename("User:tarsa129/Test", added_distros, action = Action.UPDATE)
    elif action == "delete":
        edit_distros_to_pagename("User:tarsa129/Test", added_distros, action = Action.DELETE)

