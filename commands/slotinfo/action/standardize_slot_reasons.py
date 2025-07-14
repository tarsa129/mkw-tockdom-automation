from commands.slotinfo.utils.reason_text_parse import parse_reasons
from commands.slotinfo.utils.track_page_read import get_slotinfo_template
from common_utils.base_category_action import BaseCategoryAction
from commands.slotinfo.utils import track_page_read as page_read
from commands.slotinfo.utils import track_page_edit as page_edit
from common_utils.track_page_utils.template_utils.slot_info_utils import SlotInfoTemplate
from tockdomio import tockdomwrite

def edit_slot_reason(page_id, page_name, page_text, **kwargs):
    section_id, slot_section = page_read.get_slot_section_info(page_text)
    arguments = get_slotinfo_template(slot_section)
    if not arguments or "reason" not in arguments:
        return False
    template = SlotInfoTemplate.from_template_dict(arguments)
    print(f"{page_name}:{arguments['reason']}")
    reason_args = parse_reasons(arguments["reason"])

    if reason_args is None or (len(reason_args) == 1 and arguments["reason"] == reason_args["reason"]):
        print("NO ACTION")
        return False

    template.merge_with_dict(reason_args)
    page_edit.replace_slotinfo_template(slot_section, template.to_text())
    section_text = str(slot_section)

    print(section_text)
    response = tockdomwrite.edit_section(page_id, section_id, section_text, "Standardize reason text")
    print(response.json())
    was_successful = response.json()["edit"]["result"] == "Success"
    return was_successful
    #return True

def edit_slot_reason_by_category(category, skip_until):
    action = BaseCategoryAction(edit_slot_reason)
    return action.action_from_category(category_name=category, skip_until=skip_until)