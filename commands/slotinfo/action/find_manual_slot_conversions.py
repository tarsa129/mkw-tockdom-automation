from common_utils.base_category_action import BaseCategoryAction
from commands.slotinfo.utils import track_page_read as page_read
from commands.slotinfo.utils import track_page_edit as page_edit
from commands.slotinfo.utils import section_text_parse as section_text_parse

def find_unparseable_slot_text(page_id, page_name, page_text, **kwargs):
    section_id, slot_section = page_read.get_slot_section_info(page_text)
    has_slot_template = page_read.has_slot_template(slot_section)
    if has_slot_template:
        return False

    try:
        template_info = section_text_parse.read_slot_text(slot_section.contents)
        page_edit.create_slotinfo_template(template_info)
        return False
    except Exception as e:
        return [{"page_name": page_name, "parse_fail_message":str(e)}]

def find_unparseable_by_category(category, dump_file_path):
    action = BaseCategoryAction(find_unparseable_slot_text)
    return action.action_from_category_dump(category_name=category, bulk_count=1000, dump_file_path=dump_file_path)
