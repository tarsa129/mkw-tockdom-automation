from mediawiki.mediawiki_read import *
from mediawiki.mediawiki_parse import get_template_with_name, read_template


def get_slot_section_info(page_text):
    return get_section_info_from_page(page_text, "Slot", loose=True)

def has_slot_template(section_text):
    template_info = get_template_with_name(section_text, "Slot-Info")
    return template_info is not None

def get_slotinfo_template(section_text):
    template_info = get_template_with_name(section_text, "Slot-Info")
    if template_info is None:
        return None
    return read_template(str(template_info))