from common_utils.base_category_action import BaseCategoryAction
from tockdomio import tockdomwrite
from commands.distroinfo.utils import distro_template_fix as template_fix
from commands.distroinfo.utils import distro_page_edit as page_edit
from commands.distroinfo.utils import distro_page_read as page_read
from mediawiki.mediawiki_parse import read_template

def fix_template(page_id, page_name, page_text, **kwargs):
    template_text = str(page_read.get_distroinfo_template(page_text))
    distro_info = read_template(template_text)
    fixes_needed = template_fix.fix_template_arguments(distro_info, page_name)
    if not fixes_needed:
        return False
    template_text = page_edit.create_distroinfo_template(distro_info)
    section_text = str(page_edit.replace_template(page_text, template_text))
    print(section_text)
    response = tockdomwrite.edit_section(page_id, 0, section_text, "Fix template (via API)")
    print(response.json())
    was_successful = response.json()["edit"]["result"] == "Success"
    return was_successful

def fix_by_category(category, skip_until):
    action = BaseCategoryAction(fix_template)
    return action.action_from_category(category_name=category, skip_until=skip_until)