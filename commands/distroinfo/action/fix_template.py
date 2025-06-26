from common_utils.basic_action import BasicAction
from commands.distroinfo.utils import distro_page_edit as page_edit
from trackpage.mediawikiparse import read_template

def fix_template(page_id, page_name, page_text):
    print(page_id, page_name, page_text)

    template_text = str(page_read.get_distroinfo_template(page_text))
    distro_info = read_template(template_text)
    print(distro_info)
def get_action():
    return BasicAction(fix_template)