import re
import warnings

from common_utils.track_page_utils.wiiki_name_utils.match_page_to_track import parse_page_name
from mediawiki.mediawiki_parse import read_wikilink
from mediawiki.mediawiki_read import read_text

def is_disambiguation_page(tockdom_response):
    if "pageid" not in tockdom_response:
        warnings.warn(f"No category or page ID for page {tockdom_response['title']} - likely not valid.")
        return False

    categories = tockdom_response["categories"]
    for category_entry in categories:
        category_name = category_entry["title"]
        if category_name.startswith("Category:Disambiguation"):
            return True

    return False

def get_authors_from_item_entry(item_text, base_page_name):
    wikilinks = read_text(item_text).wikilinks
    if len(wikilinks) == 0:
        warnings.warn(f"Track implementation {item_text} of {base_page_name} is invalid due to lack of links.")
        return None
    title, text = read_wikilink(wikilinks[0])
    return parse_page_name(title, base_page_name)

def get_from_existing_page(tockdom_response, base_page_name, authors: set[str]):
    if not is_disambiguation_page(tockdom_response):
        return base_page_name

    page_text:str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
    page_list = read_text(page_text).get_lists()[0]

    for track_variant in page_list.fullitems:
        track_info = get_authors_from_item_entry(track_variant, base_page_name)
        if track_info.check_authors(authors):
            return track_info.full_name

    return None
