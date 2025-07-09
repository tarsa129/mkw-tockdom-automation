from common_utils.base_handler import *

from commands.szslibrary.action import audit_szslib_entries, audit_category_entries

handler = BaseHandler()
handler.add_action("audit", action_function = audit_szslib_entries.audit_entries,
                   args=("start_id", "end_id", "dump_file_path"))
handler.add_action("audit_category", action_function = audit_category_entries.audit_by_category,
                   args=("category", "dump_file_path"))
