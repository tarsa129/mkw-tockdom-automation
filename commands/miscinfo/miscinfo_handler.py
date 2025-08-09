from commands.miscinfo.action import get_ids_from_szslibrary
from commands.miscinfo.action import edit_ids_on_page
from common_utils.base_handler import BaseHandler

handler = BaseHandler()
handler.add_action("get_ids", action_function = get_ids_from_szslibrary.get_wbz_ids,
                   args=("start_id", "end_id", "dump_file_path"))
handler.add_action("write_ids", action_function = edit_ids_on_page.add_ids_from_file,
                   args=("dump_file_path", ))