from mediawiki.mediawiki_read import *
from mediawiki.mediawiki_parse import get_section_from_page, read_wikilink
import warnings

def fix_distro_custom_name(distro_name):
    if distro_name.startswith("The "):
        return distro_name[4:]

    if distro_name.islower() or distro_name[0].isdigit():
        return distro_name

    for i in range(len(distro_name)):
        if distro_name[i].isupper():
            return distro_name[i:]

    return distro_name

def read_distro_name(item):
    if str(item).strip() == "(none)":
        return None
    distro_name = item
    item_parsed: WikiText = read_text(item)
    if len(item_parsed.wikilinks) > 0:
        distro_wikilink = item_parsed.wikilinks[0]
        _, distro_name = read_wikilink(distro_wikilink)
    elif len(item_parsed.templates) > 0:
        distro_template = item_parsed.templates[0]
        assert(distro_template.name == "Distrib-ref")
        assert(len(distro_template.arguments) == 3)
        distro_name = distro_template.arguments[0].value
    return fix_distro_custom_name(distro_name)

def get_distros_from_section(section_text: WikiText):
    assert(len(section_text.get_lists()) == 1)
    raw_distro_list =  section_text.get_lists()[0]
    parsed_distro_list = {}
    for item in raw_distro_list.items:
        distro_name = read_distro_name(item)
        if distro_name is None:
            warnings.warn("(none) distribution after {} valid distro_list".format(len(parsed_distro_list)))
            return parsed_distro_list
        parsed_distro_list[distro_name] = item.strip()
    return parsed_distro_list

def get_distrosection_from_page(page_text):
    return get_section_from_page(page_text, "<span id=distrib-list>Custom Track Distributions</span>")

def get_distros_from_page(page_text):
    distro_section = get_distrosection_from_page(page_text)
    return get_distros_from_section(distro_section)

def create_distros_section(page_text, distros:dict):
    distro_section = get_distrosection_from_page(page_text)
    raw_distro_list =  distro_section.get_lists()[0]
    raw_distro_list.string = create_distros_list(distros)

    return distro_section.string

def create_distros_list(distros: dict):
    distro_list_text = ""

    if len(distros) == 0:
        distro_list_text += "* (none)\n"
        return distro_list_text

    for key, value in distros.items():
        distros[key] = "* " + value.strip()
    distro_list_text += "\n".join(distros.values())
    distro_list_text += "\n"
    return distro_list_text

def get_distros_sectionid(page_text):
    if not isinstance(page_text, WikiText):
        page_text = read_text(page_text)

    for i, section in enumerate(page_text.sections):
        if section.title and "Custom Track Distributions" in section.title:
            return i
    return -1