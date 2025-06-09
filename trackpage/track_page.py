from trackpage.mediawikiparse import *

def get_distros_from_section(section_text: WikiText):
    assert(len(section_text.get_lists()) == 1)
    raw_distro_list =  section_text.get_lists()[0]
    parsed_distro_list = {}

    for item in raw_distro_list.items:
        if str(item).strip() == "(none)":
            return parsed_distro_list
        distro_name = item
        item_parsed: WikiText = read_text(item)
        if len(item_parsed.wikilinks) > 0:
            distro_wikilink = item_parsed.wikilinks[0]
            _, distro_name = read_wiikilink(distro_wikilink)
        elif len(item_parsed.templates) > 0:
            distro_template = item_parsed.templates[0]
            assert(distro_template.name == "Distrib-ref")
            assert(len(distro_template.arguments) == 3)
            distro_name = distro_template.arguments[0].value
        parsed_distro_list[distro_name] = item
    return parsed_distro_list

def get_distros_from_page(page_text):
    if not isinstance(page_text, WikiText):
        page_text = read_text(page_text)

    distro_section = [section for section in page_text.sections if section.title and "Custom Track Distributions" in section.title][0]
    return get_distros_from_section(distro_section)