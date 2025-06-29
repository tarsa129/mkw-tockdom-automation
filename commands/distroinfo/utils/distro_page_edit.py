from mediawiki.mediawiki_create import *
from mediawiki.mediawiki_parse import get_first_section_from_page, get_table, get_template_with_name

def create_distroinfo_template(arguments):
    return create_template_from_args(arguments, "Distribution-Info")

def replace_table(page_text, template_text):
    section_text = get_first_section_from_page(page_text)
    table = get_table(section_text)
    table.string = template_text
    return section_text

def replace_template(page_text, template_text):
    section_text = get_first_section_from_page(page_text)
    template = get_template_with_name(section_text, "Distribution-Info")
    template.string = template_text
    return section_text