from tockdomio import tockdomread, tockdomwrite
from trackpage import track_page
import warnings

def combine_distros(curr_distros, new_distros, update_existing):
    for new_distro, new_distro_text in new_distros.items():
        if new_distro in curr_distros:
            if update_existing:
                curr_distros[new_distro] = new_distro_text
            else:
                warnings.warn("{} already on the page!".format(new_distro))
        else:
            curr_distros[new_distro] = new_distro_text
    curr_distros = dict(sorted(curr_distros.items(), key=lambda x: x[0].lower()))


def read_and_update_page(tockdom_response, new_distros, update_existing):
    page_id = tockdom_response["pageid"]
    page_text:str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
    curr_distros = track_page.get_distros_from_page(page_text)

    combine_distros(curr_distros, new_distros, update_existing)

    distros_section_id = track_page.get_distros_sectionid(page_text)
    distros_section_text = track_page.create_distros_section(curr_distros)
    response = tockdomwrite.edit_section(page_id, distros_section_id, distros_section_text)
    print(response.json())


def add_distros_to_pagename(pagename, new_distros: dict, update_existing=False):
    tockdom_response = tockdomread.get_page_text_by_name(pagename)
    read_and_update_page(tockdom_response, new_distros, update_existing)


def add_distros_to_pageid(pageid, new_distros: dict, update_existing=False):
    tockdom_response = tockdomread.get_page_text_by_id(pageid)
    read_and_update_page(tockdom_response, new_distros, update_existing)


def handle_command(action, file):

    added_distros = {}
    added_distros["Aurora"] = "[[Aurora]] (v2.1)"
    added_distros["tarsa's epic track pack"] = "[[tarsa's epic track pack]] (v2.0)"
    added_distros["Tarsa's epic track pack 2"] = "{{Distrib-ref|Tarsa's epic track pack 2|129129|tarsa-pack}}"
    add_distros_to_pagename("User:tarsa129/Test", added_distros, update_existing=True)

