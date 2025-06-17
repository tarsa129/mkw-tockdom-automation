from trackpage.mediawikiparse import *
from trackpage.wiiki_page_parse import get_section_from_page, read_table_topcaption

import warnings

def get_tracklist_from_page(page_text):
    track_section = get_section_from_page(page_text, "Tracks")
    track_listing_track: list[dict] = read_table_topcaption(track_section, caption="Track Listing")
    if track_listing_track is None:
        raise RuntimeWarning("Not able to read distribution page for Track Listing table.")

    file_contents = []
    for track in track_listing_track:
        pass

    return file_contents