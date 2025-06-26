from tockdomio import tockdomread, tockdomwrite, tockdomread_category
from commands.distroinfo.utils import distro_page_distroinfo as distro_page
from commands.distroinfo.utils import distro_page_edit as page_edit
from commands.distroinfo.utils import distro_page_read as page_read

def convert_to_template(page_id, page_name, page_text):
    distro_info = page_read.get_distroinfo_table(page_text)
    distro_info_arguments = distro_page.get_distroinfo_arguments(distro_info, page_name)
    template_text = page_edit.create_distroinfo_template(distro_info_arguments)
    section_text = str(page_edit.edit_distroinfo_section(page_text, template_text))
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