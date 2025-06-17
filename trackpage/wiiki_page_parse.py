from .mediawikiparse import *

def get_first_section_from_page(page_text):
    if not isinstance(page_text, WikiText):
        page_text = read_text(page_text)
    return page_text.sections[0]

def get_section_from_page(page_text, section_name):
    if not isinstance(page_text, WikiText):
        page_text = read_text(page_text)

    def check_section_title(section: Section):
        return section.title and section.title.strip() == section_name

    valid_sections = list(filter(lambda x: check_section_title(x), page_text.sections))
    if len(valid_sections) != 1:
        raise RuntimeError(f"Page has an invalid number of sections with name {section_name}.")

    return valid_sections[0]

def get_template_with_name(page_text, template_name):
    if not isinstance(page_text, WikiText):
        page_text = read_text(page_text)
    templates: list[Template] = page_text.templates

    for template in templates:
        if template.name.strip() == template_name:
            return template

    return None

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

def read_table_topcaption(text, caption=None):
    table = get_table(text, caption)
    if table is None:
        return None

    all_table_rows = table.data()
    columns = all_table_rows[0]
    data = []
    for row in all_table_rows[1:]:
        row_dict = dict()
        for i, column in enumerate(row):
            row_dict[columns[i]] = column
        data.append(row_dict)
    return data

def read_table_sidecaption(text, caption=None):
    table = get_table(text, caption)
    if table is None:
        return None

    all_table_rows = table.data()

    data = {}
    data["name"] = table.caption

    for row in all_table_rows:
        caption = row[0].strip()
        if len(row) > 1:
            data[caption] = row[1:]
        else:
            data[caption] = None
    return data