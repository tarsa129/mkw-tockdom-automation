# The purpose of this file to is read mediawiki building blocks / text and return the raw mediawiki structure.
# More or less a wrapper for wikitextparser, with some functions having extra searching criteria added.

import wikitextparser as wtparser
from wikitextparser import Table, WikiLink, WikiText, Template, Parameter, Section, WikiList, ExternalLink

def read_text(text) -> WikiText:
    return wtparser.parse(text)

def clean_text(text) -> str:
    return wtparser.parse(text).plain_text()

def get_table(text, caption=None):
    if not isinstance(text, WikiText):
        text = wtparser.parse(text)
    tables_list = text.tables
    if len(tables_list) == 0:
        raise RuntimeError("Page has no tables")
    if caption is None:
        return tables_list[0]

    for table in tables_list:
        if table.caption.strip() == caption:
            return table
    return None

def get_first_section_from_page(page_text):
    if not isinstance(page_text, WikiText):
        page_text = read_text(page_text)
    return page_text.sections[0]

def get_section_info_from_page(page_text, section_name, loose=False):
    if not isinstance(page_text, WikiText):
        page_text = read_text(page_text)

    def check_section_title(section: Section):
        return section.title and section.title.strip() == section_name

    def check_section_title_loose(section: Section):
        return section.title and section_name.strip().lower() in section.title.lower()

    checking_function = check_section_title_loose if loose else check_section_title

    section_index, section_object = -1, None

    for i, curr_section in enumerate(page_text.sections):
        if not checking_function(curr_section):
            continue
        if section_index == -1:
            section_index, section_object = i, curr_section
        else:
            raise RuntimeError(f"Page has an invalid number of sections with name {section_name}.")

    if section_index != -1:
        return section_index, section_object

    raise RuntimeError(f"Page has an no sections with name {section_name}.")


def get_sectionid_from_page(page_text, section_name, loose=False):
    section_id, _ = get_section_info_from_page(page_text, section_name, loose)
    return section_id

def get_section_from_page(page_text, section_name, loose=False):
    _, section = get_section_info_from_page(page_text, section_name, loose)
    return section

def get_template_with_name(page_text, template_name):
    if not isinstance(page_text, WikiText):
        page_text = read_text(page_text)
    templates: list[Template] = page_text.templates

    for template in templates:
        if template.name.strip() == template_name:
            return template

    return None