from commands.miscinfo.utils import track_page_miscinfo as track_page
from commands.miscinfo.utils import track_page_edit as track_edit
from common_utils.file_reader import read_csv_file
from tockdomio import tockdomread, tockdomwrite

def add_ids_to_page(page_id, page_text, new_arguments: dict, update_wbz=False):
    print(new_arguments)
    arguments = track_page.get_miscinfo_template(page_text)
    track_edit.patch_ids_to_miscinfo_template(arguments, new_arguments, update_wbz)
    template_text = track_edit.create_miscinfo_template(arguments)

    section_text = str(track_edit.replace_miscinfo_template(page_text, template_text))
    print(section_text)

    response = tockdomwrite.edit_section(page_id, 0, section_text, "Add wbz/image ids to template (via API)")
    print(response.json())
    was_successful = response.json()["edit"]["result"] == "Success"
    return was_successful

def add_ids_by_pageid(page_id, new_arguments: dict, update_existing=False):
    tockdom_response = tockdomread.get_page_text_by_id(page_id)
    page_text: str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
    return add_ids_to_page(page_id, page_text, new_arguments, update_wbz=False)

def add_ids_by_pagename(pagename, new_arguments: dict, update_existing=False):
    tockdom_response = tockdomread.get_page_text_by_name(pagename)
    page_id = tockdom_response["pageid"]
    page_text:str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
    return add_ids_to_page(page_id, page_text, new_arguments, update_existing)

def add_ids_from_file(filepath):
    wbzs_to_add: list[dict] = read_csv_file(filepath)
    for wbz_entry in wbzs_to_add:
        arguments = {"wbz-id": wbz_entry["wbz_id"], "image-id": wbz_entry["image_id"]}

        page_id = wbz_entry["page_id"]
        if page_id:
            add_ids_by_pageid(page_id, arguments, False)
        elif wbz_entry["track_name"]:
            add_ids_by_pagename(wbz_entry["track_name"], arguments, False)