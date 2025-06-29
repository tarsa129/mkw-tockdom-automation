# The purpose of this file is to create mediawiki elements from other data types.

def create_template_from_args(arguments: dict, template_name):
    template_text = "{{" + template_name+ "\n"
    for argument, value in arguments.items():
        if value is None:
            continue
        template_text += f"|{argument}= {value}\n"
    template_text += "}}"
    return template_text