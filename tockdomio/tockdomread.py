#The purpose of this file is to communicate with the tockdom wiki.

import requests
from constants import *

def do_tockdom_query(base_params, getcontinue=False):
    headers = {
        'User-Agent': TOCKDOM_API_KEY,
    }

    response = requests.get(TOCKDOM_API, headers=headers, params=base_params)
    if getcontinue:
        return response.json()
    action = base_params["action"]
    return response.json()[action]

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

def get_page_text_by_names(pagnenames):
    if len(pagnenames) == 0:
        return []

    base_params = {
        "action": "query",
        "format": "json",
        "titles": "{0}".format("|".join(str(pagename) for pagename in pagnenames)),
        "prop": "revisions|info|redirects|categories",
        "rvprop": "content",
        "rvslots": "*",
        "formatversion": 2,
        "inprop": "displaytitle",
        "rdprop": "title|pageid",
    }

    return do_tockdom_query(base_params)['pages']

def get_page_text_by_name(pagnename):
    return get_page_text_by_names((pagnename, ))[0]