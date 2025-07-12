from commands.slotinfo.utils.track_page_read import get_slotinfo_template
from common_utils.base_category_action import BaseCategoryAction
from commands.slotinfo.utils import track_page_read as page_read

def find_slot_reason(page_id, page_name, page_text, **kwargs):
    section_id, slot_section = page_read.get_slot_section_info(page_text)
    arguments = get_slotinfo_template(slot_section)

    if "reason" in arguments:
        print(arguments)
        return [{"page_name": page_name, "slot": arguments["slot"], "reason": arguments["reason"]}]
    return False

def find_reasons_by_category(category, dump_file_path):
    action = BaseCategoryAction(find_slot_reason)
    return action.action_from_category_dump(category_name=category, bulk_count=1000, dump_file_path=dump_file_path)
