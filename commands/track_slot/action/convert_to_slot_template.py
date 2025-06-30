from common_utils.base_category_action import BaseCategoryAction
from commands.track_slot.utils import track_page_read as page_read
from tockdomio import tockdomwrite


def convert_to_slot_template(page_id, page_name, page_text):
    section_id, slot_section_text = page_read.get_slot_section_info(page_text)
    print(slot_section_text)
    has_slot_template = page_read.has_slot_template(slot_section_text)
    print(has_slot_template)
    if has_slot_template:
        return False

    return True

def get_action():
    return BaseCategoryAction(convert_to_slot_template)