from tockdomio import tockdomread, tockdomwrite
from commands.miscinfo import track_page_miscinfo as track_page
import warnings

def add_ids_by_pagename(pagename, new_arguments: dict, update_existing=False):
    tockdom_response = tockdomread.get_page_text_by_name(pagename)
    page_text:str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
    arguments = track_page.get_miscinfo_template(page_text)

    for argument, value in new_arguments.items():
        if not update_existing and argument in arguments and arguments[argument]:
            warnings.warn("{} already exists and update flag is false".format(argument))
        elif argument not in arguments:
            warnings.warn("{} not a valid argument!".format(argument))
        arguments[argument] = value
    print(arguments)

def handle_command(action, file):
    add_ids_by_pagename("User:Tarsa129/Test", {"wbz-id": "129129", "image-id":"129130", "invalid": "invalid"})