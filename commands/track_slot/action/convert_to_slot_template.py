from common_utils.base_category_action import BaseCategoryAction
from commands.track_slot.utils import track_page_read as page_read
from commands.track_slot.utils import section_text_parse as section_text
from tockdomio import tockdomwrite


def convert_to_slot_template(page_id, page_name, page_text):
    section_id, slot_section = page_read.get_slot_section_info(page_text)
    has_slot_template = page_read.has_slot_template(slot_section)
    if has_slot_template:
        return False

    template_info = section_text.read_slot_text(slot_section.contents)
    print(template_info)

    return True

def get_action():
    return BaseCategoryAction(convert_to_slot_template)