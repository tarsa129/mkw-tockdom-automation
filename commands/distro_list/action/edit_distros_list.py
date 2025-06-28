from commands.distro_list.utils import track_page_distros as track_page
from commands.distro_list.utils.distros_list_create import validate_distros, combine_distros
from tockdomio import tockdomwrite, tockdomread

def read_and_update_page(tockdom_response, new_distros, action):
    if not (validate_distros):
        raise RuntimeError("List of distro_list to add has repeats")
    if not "pageid" in tockdom_response:
        raise RuntimeError("Page with name {} does not exist".format(tockdom_response["title"]))
    page_id = tockdom_response["pageid"]
    page_text:str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
    curr_distros = track_page.get_distros_from_page(page_text)
    if not validate_distros(curr_distros):
        raise RuntimeWarning("Existing distro list has repeats")

    distros = combine_distros(curr_distros, new_distros, action)

    if not validate_distros(distros):
        raise RuntimeError("Existing distro_list in combined list.")

    distros_section_id = track_page.get_distros_sectionid(page_text)
    distros_section_text = track_page.create_distros_section(page_text, distros)
    edit_summary = "Edit distributions on page (via API)"
    response = tockdomwrite.edit_section(page_id, distros_section_id, distros_section_text, edit_summary)
    print(response.json())
    return response.json()["edit"]["result"]


def edit_distros_to_pagename(pagename, distros: dict, action):
    tockdom_response = tockdomread.get_page_text_by_name(pagename)
    read_and_update_page(tockdom_response, distros, action)


def edit_distros_to_pageid(pageid, distros: dict, action):
    tockdom_response = tockdomread.get_page_text_by_id(pageid)
    read_and_update_page(tockdom_response, distros, action)


def edit_distros_to_pagenames(distros_to_add: dict, action):
    for pagename, distros in distros_to_add.items():
        edit_distros_to_pagename(pagename, distros, action)
