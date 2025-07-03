from mediawiki.mediawiki_create import *
from mediawiki.mediawiki_parse import *
import warnings

def get_ordered_miscinfo_arguments():
    arguments = {}
    expected_params = ["name", "image", "image-id", "creator", "author", "designer", "version", "date of release",
                       "editors used", "video", "scale", "wbz-id", "download", "download 1", "download 2"]
    for expected_param in expected_params:
        arguments[expected_param] = None

    return arguments

def get_miscinfo_template(page_text):
    miscinfo_template = get_template_with_name(page_text, "Misc-Info")
    if miscinfo_template is None:
        return None

    arguments = get_ordered_miscinfo_arguments()
    for argument in miscinfo_template.arguments:
        if argument.name not in arguments:
            warnings.warn("{} is not a valid miscinfo argument".format(argument.name))
            continue
        arguments[argument.name] = argument.value.strip()

    return arguments

def patch_miscinfo_template(arguments, new_arguments, update_existing):
    for new_arg, new_val in new_arguments.items():
        if new_arg not in arguments:
            warnings.warn("{} not a valid argument!".format(new_arg))
            continue

        would_replace_existing = (new_arg in arguments) and arguments[new_arg] and arguments[new_arg] != new_val
        if update_existing and would_replace_existing:
            warnings.warn("{} already exists and update flag is false".format(new_arg))
            continue

        if new_val:
            arguments[new_arg] = new_val

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