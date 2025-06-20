from trackpage.mediawiki_create import *
from trackpage.wiiki_page_parse import get_first_section_from_page, read_table_sidecaption, read_text, get_table
from trackpage.mediawikiparse import read_text, WikiList, WikiText, ExternalLink

import re

caption_to_argument = {"battle": "arenas",
                       "online service": "online", "online services": "online", "online region": "region", "online regions": "region",
                       "wiimmfi region": "region", "wiimmfi regions": "region",
                       "date of latest version": "date of release"}

def get_distroinfo_table(page_text):
    first_section = get_first_section_from_page(page_text)
    return read_table_sidecaption(first_section)

def extract_download_link(download_extlink_text):
    download_extlinks = read_text(download_extlink_text).external_links
    if len(download_extlinks) == 0:
        return download_extlink_text

    download_extlink: ExternalLink = download_extlinks[0]
    download_url = download_extlink.url

    download_desc = ""
    comment_search = re.search("\((.*)\)", download_extlink.text)
    if comment_search and comment_search.group(1):
        download_desc = f"({comment_search.group(1)})"

    return f"{download_url} {download_desc}"

def create_downloads_dict(downloads_text):
    parsed_value = read_text(downloads_text)

    downloads_list: list[WikiList] = parsed_value.get_lists()
    if len(downloads_list) == 0:
        downloads_value = extract_download_link(downloads_text)
        return {"download" : downloads_value}

    downloads_map = {}
    for i, download_extlink in enumerate(downloads_list[0].items):
        download_number = f"download {i + 1}"
        downloads_map[download_number] = extract_download_link(download_extlink)
    return downloads_map

def extract_sourcecode(sourcecode_text):
    parsed_value = read_text(sourcecode_text)
    if len(parsed_value.external_links) == 1:
        return parsed_value.external_links[0].url
    return sourcecode_text

def get_ordered_distroinfo_arguments():
    arguments = {}

    distro_arguments = ["name", "cover", "logo", "author", "type", "wii id",
            "tracks", "arenas", "characters", "songs",
            "language", "online", "region", "version", "date of release", "download"]
    for i in range(1, 11):
        distro_arguments.append(f"download {i}")
        distro_arguments.append(f"download {i} note")
    distro_arguments.extend(["discord server", "website", "source code"])

    for expected_param in distro_arguments:
        arguments[expected_param] = None

    required_arguments = ["author", "type", "version", "date of release"]
    for required_arg in required_arguments:
        arguments[required_arg] = ""
    return arguments

def get_distroinfo_arguments(distrotable_info: dict):
    arguments = get_ordered_distroinfo_arguments()

    for name, value in distrotable_info.items():
        template_parameters_name = get_template_paramname(arguments, name)

        value = "".join(value).strip()
        if value is None or len(value) == 0 or value in ("&mdash;", "&ndash;"):
            continue

        arguments = assign_value_to_template(arguments, template_parameters_name, value)

    return arguments


def assign_value_to_template(arguments, template_parameters_name, value):
    if "download" in template_parameters_name:
        arguments = arguments | create_downloads_dict(value)
    elif "source code" == template_parameters_name:
        # Assume that the source code is from a link that is handled by another template
        value = extract_sourcecode(value)
        arguments[template_parameters_name] = value
    elif template_parameters_name in ("cover", "logo"):
        # We can reasonably expect that no non-cover or logo fields will have an image
        value = get_file_name_if_exists(value)
        arguments[template_parameters_name] = value
    else:
        arguments[template_parameters_name] = value
    return arguments


def get_template_paramname(arguments, name):
    name = name.lower()  # We know that all the template items are lower case
    name = re.sub(":", "", name)
    if name in arguments:
        template_parameters_name = name
    elif name in caption_to_argument:
        template_parameters_name = caption_to_argument[name]
    else:
        raise RuntimeError(f"{name} is not a valid miscinfo argument")
    return template_parameters_name


def get_file_name_if_exists(value):
    parsed_value = read_text(value)
    if len(parsed_value.wikilinks) == 1:
        wikilink_title = parsed_value.wikilinks[0].title
        if wikilink_title.startswith("File:"):
            value = wikilink_title[5:]
    return value

def create_distroinfo_template(arguments):
    return create_template_from_args(arguments, "Distribution-Info")

def edit_distroinfo_section(page_text, template_text):
    section_text = get_first_section_from_page(page_text)
    table = get_table(section_text)
    table.string = template_text
    return section_text