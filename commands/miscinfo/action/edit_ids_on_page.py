from commands.miscinfo.utils import track_page_miscinfo as track_page
from common_utils.file_reader import read_csv_file
from tockdomio import tockdomread, tockdomwrite

import warnings

def add_ids_by_pageid(page_id, page_text, new_arguments: dict, update_existing=False):
    arguments = track_page.get_miscinfo_template(page_text)

    for argument, value in new_arguments.items():
        if not update_existing and argument in arguments and arguments[argument]:
            warnings.warn("{} already exists and update flag is false".format(argument))
            continue
        elif argument not in arguments:
            warnings.warn("{} not a valid argument!".format(argument))
            continue
        arguments[argument] = value

    template_text = track_page.create_miscinfo_template(arguments)
    response = tockdomwrite.edit_section(page_id, 0, template_text)
    print(response)

def add_ids_from_file(filepath):
    wbzs_to_add: list[dict] = read_csv_file(filepath)
    for wbz_entry in wbzs_to_add:
        page_id = wbz_entry["pageid"]
        arguments = {"wbz_id": wbz_entry["wbz_id"], "image_id": wbz_entry["image_id"]}
        tockdom_response = tockdomread.get_page_text_by_id(page_id)
        page_text: str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
        add_ids_by_pageid(page_id, page_text, arguments, update_existing=False)

def add_ids_by_pagename(pagename, new_arguments: dict, update_existing=False):
    tockdom_response = tockdomread.get_page_text_by_name(pagename)
    page_id = tockdom_response["pageid"]
    page_text:str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
    return add_ids_by_pageid(page_id, page_text, new_arguments, update_existing)