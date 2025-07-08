from common_utils.base_category_action import BaseCategoryAction
from constants import UPDATE_COUNT


def audit_track_info(page_id, page_name, page_text):
    print(page_id, page_name, page_text)
    return {"hello": "a"}

def audit_by_category(category, dump_file_path):
    action = BaseCategoryAction(audit_track_info)
    return action.action_from_category_dump(category_name=category, dump_file_path=dump_file_path)