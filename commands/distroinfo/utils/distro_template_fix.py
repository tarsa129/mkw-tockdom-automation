import re

def remove_ctgp_from_type(value):
    #going to be annoying without the ability to read nodes.
    if "CTGP Revolution" not in value:
        return value
    if "My Stuff" in value:
        value = str(re.sub("\[\[CTGP Revolution\]\](, )?", "", value))
        value = value.strip(", ")
    else:
        value = str(re.sub("CTGP Revolution", "My Stuff", value))
    return value

def get_pagename(value, page_name):
    if value == "{{PAGENAME}}" or value == page_name:
        return "{{PAGENAME}}"
    else:
        return value

def fix_template_arguments(arguments, page_name):
    changed_template = False
    for name, value in arguments.items():
        if name == "name":
            new_name = get_pagename(value, page_name)
            if new_name != value:
                arguments[name] = new_name
                changed_template = True
        elif name == "type":
            new_type = remove_ctgp_from_type(value)
            if new_type != value:
                arguments[name] = new_type
                changed_template = True

    return changed_template