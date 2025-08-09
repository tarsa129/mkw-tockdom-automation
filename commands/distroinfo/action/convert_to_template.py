from tockdomio import tockdomwrite
from commands.distroinfo.utils import distro_template_convert as distro_page
from commands.distroinfo.utils import distro_page_edit as page_edit
from commands.distroinfo.utils import distro_page_read as page_read
from common_utils.base_category_action import BaseCategoryAction

def convert_to_template(page_id, page_name, page_text, **kwargs):
    distro_info = page_read.get_distroinfo_table(page_text)
    distro_info_arguments = distro_page.get_distroinfo_arguments(distro_info, page_name)
    template_text = page_edit.create_distroinfo_template(distro_info_arguments)
    section_text = str(page_edit.replace_table(page_text, template_text))
    print(section_text)
    response = tockdomwrite.edit_section(page_id, 0, section_text, "Convert to Distro-Info template (via API)")
    print(response.json())
    was_successful = response.json()["edit"]["result"] == "Success"
    return was_successful

def convert_by_category(category, skip_until):
    action = BaseCategoryAction(convert_to_template)
    return action.action_from_category(category_name=category, skip_until=skip_until)