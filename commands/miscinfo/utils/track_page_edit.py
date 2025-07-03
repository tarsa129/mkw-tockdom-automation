from mediawiki.mediawiki_create import create_template_from_args
from mediawiki.mediawiki_read import get_template_with_name, get_first_section_from_page
from wikitextparser import Template
import warnings

def patch_ids_to_miscinfo_template(arguments, new_arguments, update_wbz):
    curr_wbz_id = arguments["wbz-id"]
    new_wbz_id = new_arguments["wbz-id"]

    if not update_wbz and (curr_wbz_id and curr_wbz_id != new_wbz_id):
        warnings.warn(f"{curr_wbz_id} is the current wbz-id and will not be replaced with {new_wbz_id}.")
    else:
        arguments["wbz-id"] = new_wbz_id

    new_image_id = new_arguments["image-id"]
    if new_image_id != new_wbz_id:
        arguments["image-id"] = new_image_id
    else:
        arguments["image-id"] = None

def create_miscinfo_template(arguments: dict):
    return create_template_from_args(arguments, "Misc-Info")

def replace_miscinfo_template(page_text, template_text):
    section = get_first_section_from_page(page_text)
    template: Template = get_template_with_name(section, "Misc-Info")

    if len(section.contents) == len(template) + 2:
        section.contents = template_text + "\n"
    else:
        template.string = template_text

    return str(section)