from common_utils.basic_action import BasicAction
from commands.distroinfo.utils import distro_template_fix as template_fix
from commands.distroinfo.utils import distro_page_edit as page_edit
from commands.distroinfo.utils import distro_page_read as page_read
from trackpage.mediawikiparse import read_template

def fix_template(page_id, page_name, page_text):
    template_text = str(page_read.get_distroinfo_template(page_text))
    distro_info = read_template(template_text)
    print(distro_info)
    fixes_needed = template_fix.fix_template_arguments(distro_info, page_name)
    if not fixes_needed:
        return False
    template_text = page_edit.create_distroinfo_template(distro_info)
    section_text = str(page_edit.replace_template(page_text, template_text))
    print(section_text)
    #return was_successful
    return True
def get_action():
    return BasicAction(fix_template)