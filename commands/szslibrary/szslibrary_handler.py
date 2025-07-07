from common_utils.base_handler import *

from commands.szslibrary.action import audit_szslib_entries

handler = BaseHandler()
handler.add_action("audit", action_function = audit_szslib_entries.audit_entries, args=("start_id", "end_id", "dump_file_path"))
