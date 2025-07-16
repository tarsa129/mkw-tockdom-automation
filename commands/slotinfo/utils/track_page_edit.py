from wikitextparser import Section, Template

from mediawiki.mediawiki_create import *
from mediawiki.mediawiki_read import get_template_with_name

def create_slotinfo_template(arguments):
    return create_template_from_args(arguments, "Slot-Info")

def replace_slot_section(section: Section, template_text):
    section.contents = template_text + "\n"
    return section.plain_text()

def replace_slotinfo_template(section, template_text):
    template: Template = get_template_with_name(section, "Slot-Info")

    if len(section.contents) == len(template) + 2:
        section.contents = template_text + "\n"
    else:
        template.string = template_text

    return section.plain_text()