from trackpage.mediawikiparse import *
import warnings

def get_ordered_miscinfo_arguments():
    arguments = {}
    expected_params = ["name", "image", "image-id", "creator", "author", "designer", "version", "date of release",
                       "editors used", "video", "scale", "wbz-id", "download", "download 1", "download 2"]
    for expected_param in expected_params:
        arguments[expected_param] = ""
    return arguments

def get_miscinfo_template(page_text):
    if not isinstance(page_text, WikiText):
        page_text = read_text(page_text)
    templates: list[Template] = page_text.templates
    miscinfo_template: Template = None
    for template in templates:
        if template.name.strip() == "Misc-Info":
            miscinfo_template = template
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
    template_text = "{{Misc-Info\n"
    for argument, value in arguments.items():
        if not value:
            continue
        template_text += "|{}= {}\n".format(argument, value)
    template_text += "}}"
    return template_text