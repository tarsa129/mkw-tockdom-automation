from commands.slotinfo.utils.reason_text_parse import is_defined_reason
from commands.slotinfo.utils.track_page_read import get_slotinfo_template
from common_utils.base_category_action import BaseCategoryAction
from commands.slotinfo.utils import track_page_read as page_read
from common_utils.track_page_utils.template_utils.slot_info_utils import SlotInfoTemplate

def find_slot_reason(page_id, page_name, page_text, **kwargs):
    section_id, slot_section = page_read.get_slot_section_info(page_text)
    arguments = get_slotinfo_template(slot_section)
    template = SlotInfoTemplate.from_template_dict(arguments)
    filter_defined = "filter_defined" in kwargs and kwargs["filter_defined"]

    reasons = []
    for reason_text in template.get_reasons():
        if filter_defined and is_defined_reason(reason_text):
            continue
        reasons.append({"page_name": page_name, "slot": template.slot, "reason": reason_text})
    return reasons

def find_reasons_by_category(category, dump_file_path, filter_defined):
    action = BaseCategoryAction(find_slot_reason)
    kwargs = {"filter_defined": filter_defined}
    return action.action_from_category_dump(category_name=category, bulk_count=1000, dump_file_path=dump_file_path, **kwargs)
