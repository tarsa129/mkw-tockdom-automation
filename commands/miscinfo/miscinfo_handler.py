from tockdomio import tockdomread, tockdomwrite
from commands.miscinfo import track_page_miscinfo as track_page

def add_ids_by_pagename(pagename, ids_dict: dict):
    tockdom_response = tockdomread.get_page_text_by_name(pagename)
    page_text:str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
    arguments = track_page.get_miscinfo_template(page_text)
    print(arguments)


def handle_command(action, file):
    add_ids_by_pagename("User:Tarsa129/Test", {})