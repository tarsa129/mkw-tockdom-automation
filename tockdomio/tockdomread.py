#The purpose of this file is to communicate with the tockdom wiki.

import requests
from constants import *

def do_tockdom_query(base_params, getcontinue=False):
    headers = {
        'User-Agent': TOCKDOM_API_KEY,
    }

    response = requests.get(TOCKDOM_API, headers=headers, params=base_params)
    print(response.url)
    if getcontinue:
        return response.json()
    action = base_params["action"]
    return response.json()[action]

def get_pageids_of_category(szs_type, track_type):
    base_params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle" : "Category:" + szs_type + "/" + track_type,
        "format": "json",
        "cmlimit": CATEGORYLIST_BULKCOUNT,
    }
    response = do_tockdom_query(base_params)

    last_continue = {}
    while True:
        params = base_params.copy()
        params.update(last_continue)

        response = do_tockdom_query(params, getcontinue=True)

        for result in response['query']['categorymembers']:
            yield result

        if 'continue' not in response:
            break

        last_continue = response['continue']

def get_page_text_by_pageids(pageids):
    if len(pageids) == 0:
        return []

    base_params = {
        "action": "query",
        "format": "json",
        "pageids": "{0}".format("|".join(str(pageid) for pageid in pageids)),
        "prop": "revisions|info|redirects|categories",
        "rvprop": "content",
        "rvslots": "*",
        "formatversion": 2,
        "inprop": "displaytitle",
        "rdprop": "title|pageid",
    }

    return do_tockdom_query(base_params)['pages']

def get_page_text_by_id(pageid):
    return get_page_text_by_pageids((pageid, ))[0]