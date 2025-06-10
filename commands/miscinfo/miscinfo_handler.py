from tockdomio import tockdomread, tockdomwrite
from trackpage import track_page

def add_ids_by_pagename(pagename, ids_dict: dict):
    tockdom_response = tockdomread.get_page_text_by_name(pagename)


def handle_command(action, file):
    pass