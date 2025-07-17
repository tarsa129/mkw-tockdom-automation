from common_utils.track_page_utils.wiiki_name_utils.identify_from_existing_page import get_from_existing_page, \
    read_authors
from common_utils.track_page_utils.wiiki_name_utils.match_page_to_track import parse_page_name
from tockdomio import tockdomread
from tockdomio.tockdom_search import search_by_page_name

def get_from_full_search(base_page_name, authors: set[str]):
    all_pages_with_title = search_by_page_name(base_page_name)
    for page in all_pages_with_title:
        page_title = page["title"]
        track_page_parse = parse_page_name(page_title, base_page_name)
        if track_page_parse.check_authors(authors):
            return page_title
    return None

def get_page_from_name_authors(base_page_name, authors: set[str]):
    tockdom_response = tockdomread.get_page_text_by_name(base_page_name)
    page_exists = "pageid" in tockdom_response
    if page_exists:
        return get_from_existing_page(tockdom_response, base_page_name, authors)
    return get_from_full_search(base_page_name, authors)