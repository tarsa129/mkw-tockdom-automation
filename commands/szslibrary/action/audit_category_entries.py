from common_utils.base_category_action import BaseCategoryAction
from common_utils.track_page_utils.template_utils import misc_info_utils


def audit_track_info(page_id, page_name, page_text):
    arguments = misc_info_utils.get_miscinfo_template(page_text)
    return arguments

def audit_by_category(category, dump_file_path):
    action = BaseCategoryAction(audit_track_info)
    return action.action_from_category_dump(category_name=category, dump_file_path=dump_file_path)