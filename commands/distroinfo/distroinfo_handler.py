from commands.distroinfo.action import convert_to_template as convert_to_template
from commands.distroinfo.action import fix_template

def handle_command(args):
    action = args.action
    if action == "convert":
        convert_to_template.get_action().action_from_category("Distribution")
    elif action == "fix":
        fix_template.get_action().action_from_category("Distribution", 1)