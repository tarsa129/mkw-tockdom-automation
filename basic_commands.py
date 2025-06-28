from commands.miscinfo import miscinfo_handler
from commands.distros import distros_handler
from commands.distroinfo import distroinfo_handler

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--commandgroup", default=None, help="name of the group of actions")
    parser.add_argument("--action", default=None, help="Action to perform")
    parser.add_argument("--file", default=None, help="File load")
    parser.add_argument("--wiikipage", help="Wiiki page for supported operations")
    args = parser.parse_args()
    print(args)

    commandgroup = args.commandgroup
    print(commandgroup)
    if commandgroup.lower() == "distros":
        distros_handler.handle_command(args)
    elif commandgroup.lower() == "miscinfo":
        miscinfo_handler.handle_command(args.action, args.file)
    elif commandgroup.lower() =="distroinfo":
        distroinfo_handler.handle_command(args)
    if args.file:
        additional_args = read_csv_file(args.file)