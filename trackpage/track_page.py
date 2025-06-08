from trackpage.mediawikiparse import *

def find_distrocount(section_text) -> int:
    parsed_list = read_list(str(section_text))
    for item in parsed_list.items:
        if str(item).strip() == "(none)":
            return 0
    return len(parsed_list.items)

def read_trackpage(page_text):
    distro_section = [section for section in page_text.sections if section.title and "Custom Track Distributions" in section.title][0]
    distro_count = find_distrocount(distro_section.contents)
    print(distro_count)


def read_trackpage_from_text(page_text):
    page_wikitext = read_text(page_text)
    return read_trackpage(page_wikitext)