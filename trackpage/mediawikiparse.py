#The purpos of this file to is read mediawiki text.
#In practice, it relies on a library, but that just makes life easier for me.

#Uses wikitextparser for Tables
#And mwparserfromhell for any sort of mixed text (table entries).

import wikitextparser as wtparser
from wikitextparser import Table, WikiLink, WikiText, Template, Parameter

def read_text(text):
    return wtparser.parse(text)

def read_wiikilink(text):
    parsed_text: WikiText = wtparser.parse(text)
    WikiLinks = parsed_text.filter(forcetype=WikiLink)
    if not WikiLinks:
        return str(text), str(text)
    wiikilink: WikiLink = WikiLinks[0]
    if wiikilink.text:
        return str(wiikilink.title), str(wiikilink.text)
    else:
        return str(wiikilink.title), str(wiikilink.title)

def read_template(text: str):
    template: Template = [node for node in wtparser.parse(text).nodes if isinstance(node, Template)][0]
    template_info = {}
    for param in template.parameters:
        template_info[str(param.name)] = str(param.plain_text).strip()
    return template_info

def read_list(text: str):
    parsed_test = wtparser.parse(text)
    return parsed_test.get_lists()[0]