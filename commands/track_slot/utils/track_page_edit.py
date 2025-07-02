from wikitextparser import Section

from mediawiki.mediawiki_create import *

def create_slotinfo_template(arguments):
    return create_template_from_args(arguments, "Slot-Info")

def replace_slot_section(section: Section, template_text):
    section.contents = template_text + "\n"
    return section.plain_text()