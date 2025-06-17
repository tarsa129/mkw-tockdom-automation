from trackpage.mediawikiparse import *
from trackpage.mediawiki_create import *
from trackpage.wiiki_page_parse import *
import warnings

def get_ordered_miscinfo_arguments():
    arguments = {}
    expected_params = ["name", "image", "image-id", "creator", "author", "designer", "version", "date of release",
                       "editors used", "video", "scale", "wbz-id", "download", "download 1", "download 2"]
    for expected_param in expected_params:
        arguments[expected_param] = ""
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

def create_miscinfo_template(arguments: dict):
    return create_template_from_args(arguments, "Misc-Info")