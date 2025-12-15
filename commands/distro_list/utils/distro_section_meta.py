from mediawiki.mediawiki_read import get_section_info_from_page


def get_distrosectioninfo_from_page(page_text):
    return get_section_info_from_page(page_text, "Distribution", loose=True)

def get_distrosection_from_page(page_text):
    _, section_text = get_distrosectioninfo_from_page(page_text)
    return section_text


def get_distros_sectionid(page_text):
    section_id, _ = get_distrosectioninfo_from_page(page_text)
    return section_id
