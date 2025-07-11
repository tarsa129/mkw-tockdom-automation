from commands.track_slot.action import convert_to_slot_template as convert_action
from commands.track_slot.action import find_manual_slot_conversions as find_manual
from common_utils.base_handler import BaseHandler

handler = BaseHandler()
handler.add_action("convert", action_function = convert_action.convert_by_category,
                   args=("category_name", "skip_until"))
handler.add_action("find_fixes", action_function = find_manual.find_unparseable_by_category,
                   args=("category_name", "dump_file_path"))
