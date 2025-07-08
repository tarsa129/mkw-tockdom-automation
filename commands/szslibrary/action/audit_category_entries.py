from common_utils.base_category_action import BaseCategoryAction
from common_utils.szslibrary_helpers import get_track_info
from common_utils.track_page_utils.template_utils import misc_info_utils
from commands.szslibrary.utils.szslib_category_checker import *
from constants import CATEGORY_CUSTOM, CATEGORY_EDIT, CATEGORY_TEXTURE


def audit_track_info(page_id, page_name, page_text, **kwargs):
    arguments = misc_info_utils.get_miscinfo_template(page_text)

    has_wbz_audit = check_has_wbz_id(arguments, page_name)
    if has_wbz_audit:
        return [has_wbz_audit]

    track_info = get_track_info(arguments["wbz-id"])
    audits = []

    szs_categories = kwargs["category"].split("/")
    track_custom = CATEGORY_CUSTOM if len(szs_categories) == 3 and szs_categories[1] == CATEGORY_CUSTOM else ""
    custom_status_audit = check_custom_status(track_custom, track_info, page_name)
    if custom_status_audit:
        audits.append(custom_status_audit)

    track_modification = szs_categories[-1] if szs_categories[-1] in (CATEGORY_EDIT, CATEGORY_TEXTURE) else ""
    track_modification_audit = check_track_modification(track_modification, track_info, page_name)
    if track_modification_audit:
        audits.append(track_modification_audit)

    return audits

def audit_by_category(category, dump_file_path):
    action = BaseCategoryAction(audit_track_info)
    kwargs = {"category": category}
    return action.action_from_category_dump(category_name=category, bulk_count=1000, dump_file_path=dump_file_path, **kwargs)