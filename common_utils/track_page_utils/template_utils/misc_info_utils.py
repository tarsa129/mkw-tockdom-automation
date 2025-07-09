import warnings

from mediawiki.mediawiki_read import get_template_with_name


def get_ordered_miscinfo_arguments():
    arguments = {}
    expected_params = ["name", "image", "image-id", "creator", "author", "designer", "version", "date of release",
                       "editors used", "video", "scale", "wbz-id", "download", "download 1", "download 2", "download 3"]
    for expected_param in expected_params:
        arguments[expected_param] = None

    return arguments

def get_miscinfo_template(page_text):
    miscinfo_template = get_template_with_name(page_text, "Misc-Info")
    if miscinfo_template is None:
        return None

    arguments = get_ordered_miscinfo_arguments()
    for argument in miscinfo_template.arguments:
        converted_arg_name = argument.name.strip()
        if converted_arg_name not in arguments:
            warnings.warn(f"{converted_arg_name} is not a valid miscinfo argument")
            continue

        if argument.name not in arguments:
            warnings.warn(f"{argument.name} has leading whitespace, which will be fixed")
        arguments[converted_arg_name] = argument.value.strip()

    return arguments