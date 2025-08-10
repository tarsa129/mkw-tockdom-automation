from commands.miscinfo import miscinfo_handler
from commands.distro_list import distro_list_handler
from commands.distroinfo import distroinfo_handler
from commands.szslibrary import szslibrary_handler
from commands.slotinfo import track_slot_handler
from common_utils.execution_arguments import combine_arguments

from common_utils.file_reader import read_csv_file

def call_command_action(command_args):
    command_group = command_args["commandgroup"]
    if command_group.lower() == "distro_list":
        distro_list_handler.handler.handle_action(command_args)
    elif command_group.lower() == "miscinfo":
        miscinfo_handler.handler.handle_action(command_args)
    elif command_group.lower() == "distroinfo":
        distroinfo_handler.handler.handle_action(command_args)
    elif command_group.lower() == "slotinfo":
        track_slot_handler.handler.handle_action(command_args)
    elif command_group.lower() == "szslibrary":
        szslibrary_handler.handler.handle_action(command_args)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--commandgroup", default=None, help="name of the group of actions")
    parser.add_argument("--action", default=None, help="Action to perform")
    parser.add_argument("--file", default=None, help="File load")
    args = parser.parse_args()
    print(args)

    combined_arguments = vars(args)
    if args.file:
        additional_args = read_csv_file(args.file)
        combined_arguments = combine_arguments(vars(args), additional_args)

        for arg_list in combined_arguments:
            call_command_action(arg_list)
    else:
        call_command_action(combined_arguments)