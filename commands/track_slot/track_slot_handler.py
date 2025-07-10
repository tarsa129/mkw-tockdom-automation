from commands.track_slot.action import convert_to_slot_template as convert_action

def handle_command(args):
    action = args["action"]
    if action == "convert":
        category_name = args["category_name"]
        skip_until = args["skip_until"] if "skip_until" in args else None
        convert_action.get_action().action_from_category(category_name, skip_until=skip_until)