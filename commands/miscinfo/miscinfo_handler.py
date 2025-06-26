from tockdomio import tockdomread, tockdomwrite, tockdomread_category
from commands.miscinfo import track_page_miscinfo as track_page
from . import distro_page_distroinfo as distro_page
import warnings

def add_ids_by_pagename(pagename, new_arguments: dict, update_existing=False):
    tockdom_response = tockdomread.get_page_text_by_name(pagename)
    page_id = tockdom_response["pageid"]
    page_text:str = tockdom_response["revisions"][0]["slots"]["main"]["content"]
    arguments = track_page.get_miscinfo_template(page_text)

    for argument, value in new_arguments.items():
        if not update_existing and argument in arguments and arguments[argument]:
            warnings.warn("{} already exists and update flag is false".format(argument))
            continue
        elif argument not in arguments:
            warnings.warn("{} not a valid argument!".format(argument))
            continue
        arguments[argument] = value

    template_text = track_page.create_miscinfo_template(arguments)
    response = tockdomwrite.edit_section(page_id, 0, template_text)
    print(response)

def convert_to_template(page_id, page_name, page_text):
    distro_info = distro_page.get_distroinfo_table(page_text)
    distro_info_arguments = distro_page.get_distroinfo_arguments(distro_info, page_name)
    template_text = distro_page.create_distroinfo_template(distro_info_arguments)
    section_text = str(distro_page.edit_distroinfo_section(page_text, template_text))
    print(section_text)
    response = tockdomwrite.edit_section(page_id, 0, section_text, "Convert to Distro-Info template (via API)")
    print(response.json())

def convert_to_template_from_entry(page_entry):
    page_id = page_entry["pageid"]
    page_name = page_entry["title"]
    page_text:str = page_entry["revisions"][0]["slots"]["main"]["content"]
    convert_to_template(page_id, page_name, page_text)

def convert_to_template_from_pagename(page_name):
    tockdom_response = tockdomread.get_page_text_by_name(page_name)
    convert_to_template_from_entry(tockdom_response)

def convert_to_template_bulk(category_name):
    success_count = 0
    for page_entry in tockdomread_category.get_page_entries_of_category(category_name):
        try:
            convert_to_template_from_entry(page_entry)
            success_count += 1
        except Exception as e:
            continue
        if success_count >= 20:
            break

def handle_command(action, file):
    #convert_to_template_from_pagename("Falco's Texture Pack")
    convert_to_template_bulk("Distribution")
    #add_ids_by_pagename("User:Tarsa129/Test", {"wbz-id": "129129", "image-id":"129130", "download 1": "invalid"})