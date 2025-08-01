from common_utils.track_page_utils.template_utils.misc_info_utils import get_miscinfo_template
from common_utils.track_page_utils.wiiki_name_utils.match_page_to_track import parse_page_name
from mediawiki.mediawiki_read import clean_text
from tockdomio import tockdomread
from tockdomio.tockdom_search import search_by_page_name

# Without checking what the track is a modification of (e.g. "Rainbow Road Edit" vs "Luigi Circuit Edit")
# This will fail for same-named, same-typed, same-authored tracks of different origins.
# Such a case is hopefully rare.
def full_page_check(page_name, mod_type, authors):
    tockdom_response = tockdomread.get_page_text_by_name(page_name) #guaranteed to exist, minus some edge case where page is deleted

    # Check for misc-info (for confirmation of this being an actual track page, not a disambiguation)
    misc_info = get_miscinfo_template(tockdom_response["revisions"][0]["slots"]["main"]["content"])
    if misc_info is None:
        return False

    # Strict check for equality of authors
    misc_info_authors = misc_info["author"] if "author" in misc_info and misc_info["author"] else misc_info["creator"]
    if misc_info_authors is None and authors:
        return False

    page_authors = set(clean_text(misc_info_authors).split(", "))
    if page_authors != authors:
        return False

    # Check type of track (for mod type)
    for category in tockdom_response["categories"]:
        if category["title"].endswith("/Edit") and mod_type != "Edit":
            return False
        if category["title"].endswith("/Texture") and mod_type != "Texture":
            return False

    return True

def get_page_from_name_authors(base_page_name, mod_type, authors: set[str], check_strict=True):
    all_pages_with_title = search_by_page_name(base_page_name)

    # Currently does not filter out custom characters/vehicles.
    # This would probably fail for some niche Factory Island edge case.
    valid_names = [page["title"] for page in all_pages_with_title if page["title"].startswith(base_page_name)]

    for page in valid_names:
        track_page_parse = parse_page_name(page, base_page_name)
        if not track_page_parse:
            continue

        # The loose check will only check for obvious errors, like the mod type or author list being completely wrong
        # The strict check will check for equality of both, and will only pass in rare cases
        loose_check, strict_check = track_page_parse.check_modtype_authors(mod_type, authors)
        #print(track_page_parse, mod_type, authors, loose_check, strict_check)
        if not loose_check:
            continue

        if not check_strict or strict_check or full_page_check(page, mod_type, authors):
            return page

    return base_page_name