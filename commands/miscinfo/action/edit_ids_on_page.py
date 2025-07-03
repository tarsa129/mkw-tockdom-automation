from commands.miscinfo.utils import track_page_miscinfo as track_page
from common_utils.file_reader import read_csv_file
from tockdomio import tockdomread, tockdomwrite

import warnings

def add_ids_by_pageid(page_id, page_text, new_arguments: dict, update_existing=False):
    arguments = track_page.get_miscinfo_template(page_text)
    track_page.patch_miscinfo_template(arguments, new_arguments, update_existing)
    template_text = track_page.create_miscinfo_template(arguments)

    section_text = str(track_page.replace_miscinfo_template(page_text, template_text))
    print(section_text)

    response = tockdomwrite.edit_section(page_id, 0, section_text, "Add miscinfo template (via API)")
    print(response.json())
    was_successful = response.json()["edit"]["result"] == "Success"
    return was_successful

def add_ids_from_file(filepath):
    wbzs_to_add: list[dict] = read_csv_file(filepath)
    for wbz_entry in wbzs_to_add:
        page_id = wbz_entry["page_id"]
        arguments = {"wbz-id": wbz_entry["wbz_id"], "image-id": wbz_entry["image_id"]}
        tockdom_response = tockdomread.get_page_text_by_id(page_id)
        page_text: str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
        add_ids_by_pageid(page_id, page_text, arguments, update_existing=False)

def add_ids_by_pagename(pagename, new_arguments: dict, update_existing=False):
    tockdom_response = tockdomread.get_page_text_by_name(pagename)
    page_id = tockdom_response["pageid"]
    page_text:str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
    return add_ids_by_pageid(page_id, page_text, new_arguments, update_existing)