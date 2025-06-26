import requests
from constants import *

from .tockdomread import get_page_text_by_pageids

def do_tockdom_query(base_params):
    headers = {
        'User-Agent': TOCKDOM_API_KEY,
    }

    response = requests.get(TOCKDOM_API, headers=headers, params=base_params)
    return response.json()

def get_pageids_of_category(category_name):
    base_params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle" : f"Category:{category_name}",
        "format": "json",
        "cmlimit": CATEGORYLIST_BULKCOUNT,
    }
    response = do_tockdom_query(base_params)

    last_continue = {}
    while True:
        params = base_params.copy()
        params.update(last_continue)

        response = do_tockdom_query(params)

        for result in response['query']['categorymembers']:
            yield result

        if 'continue' not in response:
            break

        last_continue = response['continue']

def get_pageid_batch(category_name, skip_until):
    page_ids = []

    i = 0
    for page_id in get_pageids_of_category(category_name):
        if skip_until and page_id['title'] < skip_until:
            continue
        page_ids.append(page_id)
        i += 1
        if i >= TRACKPAGE_BULKCOUNT:
            page_ids_copy = page_ids.copy()
            page_ids = []
            i = 0
            yield page_ids_copy
    yield page_ids

def get_page_entries_of_category(category_name, skip_until = None):
    for page_batch in get_pageid_batch(category_name, skip_until):
        page_ids = [entry['pageid'] for entry in page_batch]
        for page_entry in get_page_text_by_pageids(page_ids):
            yield page_entry
