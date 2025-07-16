from constants import *
from tockdomio.tockdomread import do_tockdom_query

def search_by_page_name(page_name):
    base_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch":  "{0}".format(page_name),
        "srnamespace": MAIN_NAMESPACE,
        "srlimit": CATEGORYLIST_BULKCOUNT,
        "srwhat": "title"
    }

    return do_tockdom_query(base_params)['search']