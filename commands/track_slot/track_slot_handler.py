from commands.track_slot.action import convert_to_slot_template as convert_action

def handle_command(args):
    action = args["action"]
    if action == "convert":
        category_name = args["category_name"]
        convert_action.get_action().action_from_category(category_name)