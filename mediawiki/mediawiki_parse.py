# The purpose of this file is to convert mediawiki building blocks into python objects (dicts, lists, etc.)
# Some of these are wrappers for other functions in the read file, for convenience.

from .mediawiki_read import *

def read_wikilink(wikilink: WikiLink):
    if wikilink.text:
        return str(wikilink.title), str(wikilink.text)
    else:
        return str(wikilink.title), str(wikilink.title)


def read_template(text: str):
    if not isinstance(text, WikiText):
        text = read_text(text)
    templates = text.templates
    if not templates:
        raise RuntimeError("No templates found in text.")

    template: Template = templates[0]
    template_info = {}
    for param in template.arguments:
        template_info[str(param.name)] = str(param.value).strip()
    return template_info

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

    data = {"name": table.caption}

    for row in all_table_rows:
        caption = row[0].strip()
        if len(row) > 1:
            data[caption] = row[1:]
        else:
            data[caption] = None
    return data