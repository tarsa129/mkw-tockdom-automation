from commands.track_slot.action import convert_to_slot_template as convert_action

def handle_command(args):
    action = args["action"]
    if action == "convert":
        convert_action.get_action().action_from_pagename("The Great Apple War")
