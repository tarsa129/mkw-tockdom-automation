from trackpage.mediawiki_create import *
from trackpage.wiiki_page_parse import get_first_section_from_page, get_table

def create_distroinfo_template(arguments):
    return create_template_from_args(arguments, "Distribution-Info")

def edit_distroinfo_section(page_text, template_text):
    section_text = get_first_section_from_page(page_text)
    table = get_table(section_text)
    table.string = template_text
    return section_text