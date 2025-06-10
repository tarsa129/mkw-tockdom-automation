from commands import distros

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--commandgroup", default=None, help="name of the group of actions")
    parser.add_argument("--action", default=None, help="Action to perform")
    parser.add_argument("--file", default=None, help="File load")
    args = parser.parse_args()
    print(args)

    commandgroup = args.commandgroup
    print(commandgroup)
    if commandgroup.lower() == "distros":
        distros.handle_command(args.action, args.file)