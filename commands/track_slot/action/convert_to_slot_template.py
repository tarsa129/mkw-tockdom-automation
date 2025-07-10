from common_utils.base_category_action import BaseCategoryAction
from commands.track_slot.utils import track_page_read as page_read
from commands.track_slot.utils import track_page_edit as page_edit
from commands.track_slot.utils import section_text_parse as section_text_parse
from tockdomio import tockdomwrite


def convert_to_slot_template(page_id, page_name, page_text, **kwargs):
    section_id, slot_section = page_read.get_slot_section_info(page_text)
    has_slot_template = page_read.has_slot_template(slot_section)
    if has_slot_template:
        return False

    print(page_name)
    try:
        template_info = section_text_parse.read_slot_text(slot_section.contents)

        template_text = page_edit.create_slotinfo_template(template_info)
        page_edit.replace_slot_section(slot_section, template_text)
        section_text = str(slot_section)

        print(section_text)

        response = tockdomwrite.edit_section(page_id, section_id, section_text, "Convert to slot template (via API)")
        print(response.json())
        was_successful = response.json()["edit"]["result"] == "Success"
        return was_successful
    except Exception as e:
        print(e)
        return False

def get_action():
    return BaseCategoryAction(convert_to_slot_template)