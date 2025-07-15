from commands.slotinfo.action import convert_to_slot_template as convert_action
from commands.slotinfo.action import find_manual_slot_conversions as find_manual
from commands.slotinfo.action import pull_all_slot_reasons as get_reasons
from commands.slotinfo.action import standardize_slot_reasons as edit_reason
from common_utils.base_handler import BaseHandler

handler = BaseHandler()
handler.add_action("convert", action_function = convert_action.convert_by_category,
                   args=("category_name", "skip_until"))
handler.add_action("find_fixes", action_function = find_manual.find_unparseable_by_category,
                   args=("category_name", "dump_file_path"))
handler.add_action("get_reasons", action_function = get_reasons.find_reasons_by_category,
                   args=("category_name", "dump_file_path", "filter_defined"))
handler.add_action("edit_reason", action_function = edit_reason.edit_slot_reason_by_category,
                   args=("category_name", "skip_until", "edit_custom"))