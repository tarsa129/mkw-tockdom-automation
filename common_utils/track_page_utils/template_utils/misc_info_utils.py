import warnings

from mediawiki.mediawiki_read import get_template_with_name


def get_ordered_miscinfo_arguments():
    arguments = {}
    expected_params = ["name",
                       "image","image-id", "image2", "image-id2", "image3", "image-id3", "image4", "image-id4", "image5", "image-id5",
                       "item-tab", "item-tab2", "item-tab3", "item-tab4", "item-tab5",
                       "creator", "author", "designer", "version", "date of release",
                       "editors used", "video", "scale", "wbz-id",
                       "download", "download2", "download3", "download4", "download5", "download6",
                       "download7", "download8", "download9", "download10"]
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

def get_download_links(misc_info_args):
    download_links = [misc_info_args["download"],
                      misc_info_args["download2"], misc_info_args["download3"], misc_info_args["download4"],
                      misc_info_args["download5"], misc_info_args["download6"], misc_info_args["download7"],
                      misc_info_args["download8"], misc_info_args["download9"], misc_info_args["download10"]]
    return list(filter(lambda x: x is not None and x.strip(), download_links))